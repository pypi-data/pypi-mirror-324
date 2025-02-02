from importlib.metadata import version
import json
from unittest import mock
from uuid import uuid4

from workflow_server.server import create_app


def test_stream_workflow_route__happy_path():
    # GIVEN a flask app
    flask_app = create_app()

    # AND a valid request body
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "inputs": [],
        "workspace_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow

class Workflow(BaseWorkflow):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
        },
    }

    # WHEN we call the stream route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream", json=request_body)
        status_code = response.status_code
        events = [json.loads(line) for line in response.data.decode().split("\n") if line]

    # THEN we get a 200 response
    assert status_code == 200, events

    # THEN we get the expected events
    assert events[0] == {
        "id": mock.ANY,
        "trace_id": mock.ANY,
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "name": "vembda.execution.initiated",
        "body": {
            "sdk_version": version("vellum-ai"),
            "server_version": "local",
            "display_context": None,
        },
    }

    assert events[1]["name"] == "workflow.execution.initiated", events[1]
    assert events[2]["name"] == "workflow.execution.fulfilled", events[2]

    assert events[3] == {
        "id": mock.ANY,
        "trace_id": events[0]["trace_id"],
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "name": "vembda.execution.fulfilled",
        "body": mock.ANY,
    }
    assert events[3]["body"] == {
        "exit_code": 0,
        "log": "",
        "stderr": "",
        "timed_out": False,
        "container_overhead_latency": mock.ANY,
    }

    assert len(events) == 4


def test_stream_workflow_route__happy_path_with_inputs():
    # GIVEN a flask app
    flask_app = create_app()

    # AND a valid request body
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "inputs": [
            {"name": "foo", "type": "STRING", "value": "hello"},
        ],
        "workspace_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState
from .inputs import Inputs

class Workflow(BaseWorkflow[Inputs, BaseState]):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
            "inputs.py": """\
from vellum.workflows.inputs import BaseInputs

class Inputs(BaseInputs):
    foo: str
""",
        },
    }

    # WHEN we call the stream route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream", json=request_body)
        status_code = response.status_code

    # THEN we get a 200 response
    assert status_code == 200, response.json()
    events = [json.loads(line) for line in response.data.decode().split("\n") if line]

    # THEN we get the expected events
    assert events[0] == {
        "id": mock.ANY,
        "trace_id": mock.ANY,
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "name": "vembda.execution.initiated",
        "body": {
            "sdk_version": version("vellum-ai"),
            "server_version": "local",
            "display_context": None,
        },
    }

    assert events[1]["name"] == "workflow.execution.initiated", events[1]
    assert events[2]["name"] == "workflow.execution.fulfilled", events[2]

    assert events[3] == {
        "id": mock.ANY,
        "trace_id": events[0]["trace_id"],
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "name": "vembda.execution.fulfilled",
        "body": mock.ANY,
    }
    assert events[3]["body"] == {
        "exit_code": 0,
        "log": "",
        "stderr": "",
        "timed_out": False,
        "container_overhead_latency": mock.ANY,
    }

    assert len(events) == 4


def test_stream_workflow_route__bad_indent_in_inputs_file():
    # GIVEN a flask app
    flask_app = create_app()

    # AND a valid request body
    span_id = uuid4()
    request_body = {
        "timeout": 360,
        "execution_id": str(span_id),
        "inputs": [
            {"name": "foo", "type": "STRING", "value": "hello"},
        ],
        "workspace_api_key": "test",
        "module": "workflow",
        "files": {
            "__init__.py": "",
            "workflow.py": """\
from vellum.workflows import BaseWorkflow
from vellum.workflows.state import BaseState
from .inputs import Inputs

class Workflow(BaseWorkflow[Inputs, BaseState]):
    class Outputs(BaseWorkflow.Outputs):
        foo = "hello"
""",
            "inputs.py": """\
from vellum.workflows.inputs import BaseInputs

  class Inputs(BaseInputs):
     foo: str
""",
        },
    }

    # WHEN we call the stream route
    with flask_app.test_client() as test_client:
        response = test_client.post("/workflow/stream", json=request_body)
        status_code = response.status_code

    # THEN we get a 200 response
    assert status_code == 200, response.json()
    events = [json.loads(line) for line in response.data.decode().split("\n") if line]

    # THEN we get the expected events
    assert events[0] == {
        "id": mock.ANY,
        "trace_id": mock.ANY,
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "name": "vembda.execution.initiated",
        "body": {
            "sdk_version": version("vellum-ai"),
            "server_version": "local",
            "display_context": None,
        },
    }

    assert events[1] == {
        "id": mock.ANY,
        "trace_id": events[0]["trace_id"],
        "span_id": str(span_id),
        "timestamp": mock.ANY,
        "api_version": "2024-10-25",
        "parent": None,
        "name": "vembda.execution.fulfilled",
        "body": mock.ANY,
    }
    assert events[1]["body"] == {
        "exit_code": -1,
        "log": "",
        "stderr": "Failed to initialize workflow inputs: unexpected indent (<string>, line 3)",
        "timed_out": False,
        "container_overhead_latency": mock.ANY,
    }

    assert len(events) == 2
