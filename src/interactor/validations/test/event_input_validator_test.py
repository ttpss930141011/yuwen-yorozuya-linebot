import pytest

from src.interactor.validations.event_input_validator import EventInputDtoValidator


def test_event_input_validator_valid_data(mocker, fixture_window):
    mocker.patch("src.interactor.validations.base_input_validator.BaseInputValidator.verify")
    input_data = {"window": fixture_window, "user_input": "test"}
    schema = {
        "window": {
            "type": "dict",
            "required": True,
            "schema": {
                "window_id": {"type": "string", "required": True},
                "is_muting": {"type": "boolean", "required": True},
                "system_message": {"type": "string", "required": True},
                "agent_language": {"type": "string", "required": True},
                "temperature": {"type": "float", "required": True},
            },
        },
        "user_input": {"type": "string", "required": True},
        "source_type": {"type": "string", "required": True},
    }
    validator = EventInputDtoValidator(input_data)
    validator.validate()
    validator.verify.assert_called_once_with(schema)


def test_event_input_validator_without_user_input(fixture_window):
    # We are doing just a simple test as the complete test is done in
    # base_input_validator_test.py
    input_data = {"window": fixture_window, "source_type": "test"}
    validator = EventInputDtoValidator(input_data)
    with pytest.raises(ValueError) as exception_info:
        validator.validate()
    assert str(exception_info.value) == "User_input: required field"
