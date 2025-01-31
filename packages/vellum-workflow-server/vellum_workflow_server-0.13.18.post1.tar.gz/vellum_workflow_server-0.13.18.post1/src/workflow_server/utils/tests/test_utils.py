from vellum import ChatMessageRequest
from workflow_server.utils.utils import convert_json_inputs_to_vellum


def test_map_error_message__no_remap():
    inputs = [
        {"type": "STRING", "name": "test", "value": "<example-string-value>"},
        {"type": "NUMBER", "name": "test2", "value": 5},
        {"type": "JSON", "name": "test3", "value": {"example-key": "example-value"}},
        {"type": "CHAT_HISTORY", "name": "chat_history", "value": [{"role": "USER", "text": "<example-user-text>"}]},
    ]

    expected = {
        "chat_history": [
            ChatMessageRequest(
                text="<example-user-text>",
                role="USER",
                content=None,
                source=None,
            )
        ],
        "test": "<example-string-value>",
        "test2": 5,
        "test3": {"example-key": "example-value"},
    }

    actual = convert_json_inputs_to_vellum(inputs)

    assert expected == actual


def test_input_variables_with_uppercase_gets_sanitized():
    inputs = [
        {"type": "STRING", "name": "Foo", "value": "<example-string-value>"},
        {"type": "STRING", "name": "Foo-Var", "value": "<another-example-string-value>"},
    ]

    expected = {
        "foo": "<example-string-value>",
        "foo_var": "<another-example-string-value>",
    }

    actual = convert_json_inputs_to_vellum(inputs)

    assert expected == actual
