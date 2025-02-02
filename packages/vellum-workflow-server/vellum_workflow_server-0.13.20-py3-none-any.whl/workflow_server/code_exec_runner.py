from datetime import datetime
import json
import os
from uuid import uuid4

from workflow_server.api.workflow_view import get_workflow_request_context
from workflow_server.core.executor import stream_workflow
from workflow_server.utils.utils import (
    VembdaExecutionFulfilledBody,
    VembdaExecutionFulfilledEvent,
    VembdaExecutionInitiatedBody,
    VembdaExecutionInitiatedEvent,
    get_version,
)

_EVENT_LINE = "--event--"


def run():
    context = None

    try:
        input_raw = ""
        while "--vellum-input-stop--" not in input_raw:
            # os/read they come in chunks of idk length, not as lines
            input_raw += os.read(0, 100_000_000).decode("utf-8")

        split_input = input_raw.split("\n--vellum-input-stop--\n")
        input_json = split_input[0]

        input_data = json.loads(input_json)
        context = get_workflow_request_context(input_data)

        print("--vellum-output-start--")  # noqa: T201

        vembda_initiated_event = VembdaExecutionInitiatedEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            trace_id=context.trace_id,
            span_id=context.execution_id,
            body=VembdaExecutionInitiatedBody(
                sdk_version=get_version().get("sdk_version"),
                server_version=get_version().get("server_version"),
            ),
            parent=None,
        )
        vembda_initiated_event.model_dump(mode="json")

        print(f"{_EVENT_LINE}{json.dumps(vembda_initiated_event)}")  # noqa: T201

        for line in stream_workflow(context, output={}, disable_redirect=True):
            print(f"{_EVENT_LINE}{json.dumps(line)}")  # noqa: T201
    except Exception:
        vembda_fulfilled_event = VembdaExecutionFulfilledEvent(
            id=uuid4(),
            timestamp=datetime.now(),
            trace_id=context.trace_id if context else None,
            span_id=context.execution_id if context else None,
            body=VembdaExecutionFulfilledBody(
                exit_code=-1,
                stderr="Internal Server Error",
            ),
            parent=None,
        )
        event = json.dumps(vembda_fulfilled_event.model_dump(mode="json"))
        print(f"{_EVENT_LINE}{event}")  # noqa: T201
