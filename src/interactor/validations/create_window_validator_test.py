import pytest

from src.interactor.validations.create_window_validator import CreateWindowInputDtoValidator


def test_create_window_validator_valid_data(mocker, fixture_window):
    mocker.patch("src.interactor.validations.base_input_validator.BaseInputValidator.verify")
    input_data = {
        "window_id": fixture_window["window_id"],
        "is_muting": fixture_window["is_muting"],
        "agent_language": fixture_window["agent_language"],
        "system_message": fixture_window["system_message"],
        "temperature": fixture_window["temperature"],
    }
    schema = {
        "window_id": {"type": "string", "required": True, "empty": False},
        "is_muting": {"type": "boolean", "required": True, "empty": False},
        "agent_language": {"type": "string", "required": True, "empty": False},
        "system_message": {"type": "string", "required": True, "empty": False},
        "temperature": {"type": "float", "required": True, "empty": False},
    }
    validator = CreateWindowInputDtoValidator(input_data)
    validator.validate()
    validator.verify.assert_called_once_with(schema)


def test_create_window_validator_none_input(fixture_window):
    # We are doing just a simple test as the complete test is done in
    # base_input_validator_test.py
    input_data = {
        "window_id": fixture_window["window_id"],
        "is_muting": None,
        "agent_language": fixture_window["agent_language"],
        "system_message": fixture_window["system_message"],
        "temperature": fixture_window["temperature"],
    }
    validator = CreateWindowInputDtoValidator(input_data)
    with pytest.raises(ValueError) as exception_info:
        validator.validate()
    assert str(exception_info.value) == "Is_muting: null value not allowed"


def test_create_window_custom_validation(fixture_window):
    input_data = {
        "window_id": "Window",
        "is_muting": fixture_window["is_muting"],
        "agent_language": fixture_window["agent_language"],
        "system_message": fixture_window["system_message"],
        "temperature": fixture_window["temperature"],
    }
    validator = CreateWindowInputDtoValidator(input_data)
    with pytest.raises(ValueError) as exception_info:
        validator.validate()
    assert str(exception_info.value) == "Window_id: Window is not permitted"
