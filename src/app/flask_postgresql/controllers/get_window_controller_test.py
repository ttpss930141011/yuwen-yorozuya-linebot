# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


import pytest
from unittest import mock
from src.interactor.interfaces.logger.logger import LoggerInterface

with mock.patch(
    "sqlalchemy.create_engine"
) as mock_create_engine:
    from src.app.flask_postgresql.controllers.get_window_controller \
        import GetWindowController
    


def test_get_window(monkeypatch, mocker, fixture_window):
    window_id = fixture_window["window_id"]

    fake_user_inputs = {
        "window_id": window_id
    }
    monkeypatch.setattr('builtins.input', lambda _: next(fake_user_inputs))

    mock_repository = mocker.patch(
        'src.app.flask_postgresql.controllers.get_window_controller.\
WindowPostgresqlRepository')
    mock_presenter = mocker.patch(
        'src.app.flask_postgresql.controllers.get_window_controller.\
WindowPresenter')
    mock_use_case = mocker.patch(
        'src.app.flask_postgresql.controllers.get_window_controller.\
GetWindowUseCase')
    mock_use_case_instance = mock_use_case.return_value
    logger_mock = mocker.patch.object(
        LoggerInterface,
        "log_info"
    )
    result_use_case = {
        "window_id": fixture_window["window_id"],
        "is_muting": fixture_window["is_muting"],
        "system_message": fixture_window["system_message"],
        "agent_language": fixture_window["agent_language"],
        "temperature": fixture_window["temperature"]
    }
    mock_use_case_instance.execute.return_value = result_use_case

    controller = GetWindowController(logger_mock)
    controller.get_window_info(fake_user_inputs)
    result = controller.execute()

    mock_repository.assert_called_once_with()
    mock_presenter.assert_called_once_with()
    mock_use_case.assert_called_once_with(
        mock_presenter.return_value,
        mock_repository.return_value,
        logger_mock
    )
    assert result["window_id"] == fixture_window["window_id"]
    assert result["is_muting"] == fixture_window["is_muting"]
    assert result["system_message"] == fixture_window["system_message"]
    assert result["agent_language"] == fixture_window["agent_language"]
    assert result["temperature"] == fixture_window["temperature"]

    # Test for missing inputs (window_id)
    fake_user_inputs = {
        "window_i": window_id
    }
    with pytest.raises(ValueError) as exception_info:
        controller.get_window_info(fake_user_inputs)
    assert str(exception_info.value) == "Missing Window Id"
