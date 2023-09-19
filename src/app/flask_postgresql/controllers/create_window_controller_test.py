# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


import pytest
from unittest import mock
from interactor.dtos.window_dtos import CreateWindowInputDto
from src.interactor.interfaces.logger.logger import LoggerInterface

with mock.patch(
    "sqlalchemy.create_engine"
) as mock_create_engine:
    from app.flask_postgresql.controllers.create_window_controller \
        import CreateWindowController


def test_create_window(monkeypatch, mocker, fixture_window_developer):
    name = fixture_window_developer["name"]
    description = fixture_window_developer["description"]
    fake_user_inputs = {
        "name": name,
        "description": description
    }
    monkeypatch.setattr('builtins.input', lambda _: next(fake_user_inputs))

    mock_repository = mocker.patch(
        'src.app.flask_postgresql.controllers.create_window_controller.\
WindowPostgresqlRepository')
    mock_presenter = mocker.patch(
        'src.app.flask_postgresql.controllers.create_window_controller.\
WindowPresenter')
    mock_use_case = mocker.patch(
        'src.app.flask_postgresql.controllers.create_window_controller.\
CreateWindowUseCase')
    mock_use_case_instance = mock_use_case.return_value
    logger_mock = mocker.patch.object(
        LoggerInterface,
        "log_info"
    )
    result_use_case = {
        "window_id": fixture_window_developer["window_id"],
        "name": fixture_window_developer["name"],
        "description": fixture_window_developer["description"]
    }
    mock_use_case_instance.execute.return_value = result_use_case

    controller = CreateWindowController(logger_mock)
    controller.get_window_info(fake_user_inputs)
    result = controller.execute()

    mock_repository.assert_called_once_with()
    mock_presenter.assert_called_once_with()
    mock_use_case.assert_called_once_with(
        mock_presenter.return_value,
        mock_repository.return_value,
        logger_mock
    )
    input_dto = CreateWindowInputDto(name, description)
    mock_use_case_instance.execute.assert_called_once_with(input_dto)
    assert result["name"] == name
    assert result["description"] == description

    # Test for missing inputs (name)
    fake_user_inputs = {
        "nam": name,
        "description": description
    }
    with pytest.raises(ValueError) as exception_info:
        controller.get_window_info(fake_user_inputs)
    assert str(exception_info.value) == "Missing Window Name"

    # Test for missing inputs (description)
    fake_user_inputs = {
        "name": name,
        "descriptio": description
    }
    with pytest.raises(ValueError) as exception_info:
        controller.get_window_info(fake_user_inputs)
    assert str(exception_info.value) == "Missing Window Description"
