from importlib.metadata import version
import json
import re
from typing import List, Literal, Optional

from vellum_ee.workflows.display.types import WorkflowEventDisplayContext

from vellum import (
    ChatMessageRequest,
    FunctionCallRequest,
    SearchResultRequest,
    VellumErrorRequest,
    VellumImageRequest,
    VellumValueRequest,
)
from vellum.client.core import UniversalBaseModel
from vellum.workflows import BaseWorkflow
from vellum.workflows.events.types import BaseEvent
from vellum.workflows.nodes import BaseNode
from workflow_server.config import is_development

VEMBDA_EXECUTION_INITIATED_EVENT_NAME = "vembda.execution.initiated"
VEMBDA_EXECUTION_FULFILLED_EVENT_NAME = "vembda.execution.fulfilled"


class VembdaExecutionFulfilledBody(UniversalBaseModel):
    exit_code: int = 0
    log: str = ""
    stderr: str = ""
    timed_out: bool = False
    container_overhead_latency: float = 0


class VembdaExecutionFulfilledEvent(BaseEvent):
    name: Literal["vembda.execution.fulfilled"] = VEMBDA_EXECUTION_FULFILLED_EVENT_NAME  # type: ignore
    body: VembdaExecutionFulfilledBody


class VembdaExecutionInitiatedBody(UniversalBaseModel):
    sdk_version: str
    server_version: str
    display_context: Optional[WorkflowEventDisplayContext] = None


class VembdaExecutionInitiatedEvent(BaseEvent):
    name: Literal["vembda.execution.initiated"] = VEMBDA_EXECUTION_INITIATED_EVENT_NAME  # type: ignore
    body: VembdaExecutionInitiatedBody


VembdaExecutionFulfilledEvent.model_rebuild(
    # Not sure why this is needed, but it is required for the VembdaExecutionFulfilledEvent to be
    # properly rebuilt with the recursive types.
    _types_namespace={
        "BaseWorkflow": BaseWorkflow,
        "BaseNode": BaseNode,
    },
)


def convert_json_inputs_to_vellum(inputs: List[dict]):
    vellum_inputs = {}

    for input in inputs:
        value = input["value"]
        name = to_python_safe_snake_case(input["name"])
        type = input["type"]

        if type == "CHAT_HISTORY":
            vellum_inputs[name] = [ChatMessageRequest.model_validate_json(json.dumps(item)) for item in value]
        elif type == "FUNCTION_CALL":
            vellum_inputs[name] = FunctionCallRequest.model_validate_json(json.dumps(value))
        elif type == "IMAGE":
            vellum_inputs[name] = VellumImageRequest.model_validate_json(json.dumps(value))
        elif type == "SEARCH_RESULTS":
            vellum_inputs[name] = SearchResultRequest.model_validate_json(json.dumps(value))
        elif type == "ERROR":
            vellum_inputs[name] = VellumErrorRequest.model_validate_json(json.dumps(value))
        elif type == "ARRAY":
            vellum_inputs[name] = [VellumValueRequest.model_validate_json(json.dumps(item)) for item in value]
        else:
            vellum_inputs[name] = value

    return vellum_inputs


def get_version():
    return {
        "sdk_version": version("vellum-ai"),
        "server_version": "local" if is_development() else version("vellum-workflow-server"),
    }


def to_python_safe_snake_case(string: str, safety_prefix: str = "_") -> str:
    # Strip special characters from start of string
    cleaned_str = re.sub(r"^[^a-zA-Z0-9_]+", "", string)

    # Check if cleaned string starts with a number
    starts_with_unsafe = bool(re.match(r"^\d", cleaned_str))

    # Convert to snake case
    snake_case = re.sub(r"([a-z])([A-Z])", r"\1_\2", cleaned_str)  # Insert underscore between lower and upper case
    snake_case = re.sub(r"[^a-zA-Z0-9]+", "_", snake_case)  # Replace any non-alphanumeric chars with underscore
    snake_case = re.sub(r"^_+|_+$", "", snake_case)  # Remove leading/trailing underscores
    snake_case = snake_case.lower()

    # Add safety prefix if needed
    cleaned_safety_prefix = (
        "_" if safety_prefix == "_" else f"{safety_prefix}{'_' if not safety_prefix.endswith('_') else ''}"
    )
    return f"{cleaned_safety_prefix}{snake_case}" if starts_with_unsafe else snake_case
