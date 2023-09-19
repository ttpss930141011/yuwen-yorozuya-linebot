# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


import pytest
from src.interactor.validations.create_window_validator import CreateWindowInputDtoValidator


def test_create_window_validator_valid_data(
        mocker,
        fixture_window
):
    mocker.patch("src.interactor.validations.base_input_validator.BaseInputValidator.verify")
    input_data = {
            "window_id": fixture_window["window_id"],
            "is_muting": fixture_window["is_muting"]
    }
    schema = {
        "window_id": {
            "type": "string",
            "required": True,
            "empty": False
        },
        "is_muting": {
            "type": "boolean",
            "required": True,
            "empty": False
        }
    }
    validator = CreateWindowInputDtoValidator(input_data)
    validator.validate()
    validator.verify.assert_called_once_with(schema)  # pylint: disable=E1101


def test_create_window_validator_none_input(fixture_window):
    # We are doing just a simple test as the complete test is done in
    # base_input_validator_test.py
    input_data = {
            "window_id": fixture_window["window_id"],
            "is_muting": None,
        }
    validator = CreateWindowInputDtoValidator(input_data)
    with pytest.raises(ValueError) as exception_info:
        validator.validate()
    assert str(exception_info.value) == "Is_muting: null value not allowed"


def test_create_window_custom_validation(fixture_window):
    input_data = {
            "window_id": "Window",
            "is_muting": fixture_window["is_muting"],
        }
    validator = CreateWindowInputDtoValidator(input_data)
    with pytest.raises(ValueError) as exception_info:
        validator.validate()
    assert str(exception_info.value) == "Window_id: Window is not permitted"
