import pytest

from src.domain.entities.window import Window
from src.interactor.dtos.window_dtos import CreateWindowInputDto, WindowOutputDto
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.interactor.interfaces.presenters.window_presenter import WindowPresenterInterface
from src.interactor.interfaces.repositories.window_repository import WindowRepositoryInterface
from src.interactor.use_cases import create_window


def test_create_window(mocker, fixture_window):
    window = Window(
        window_id=fixture_window["window_id"],
        is_muting=fixture_window["is_muting"],
        agent_language=fixture_window["agent_language"],
        system_message=fixture_window["system_message"],
        temperature=fixture_window["temperature"],
    )
    presenter_mock = mocker.patch.object(WindowPresenterInterface, "present")
    repository_mock = mocker.patch.object(WindowRepositoryInterface, "create")

    input_dto_validator_mock = mocker.patch(
        "src.interactor.use_cases.create_window.\
CreateWindowInputDtoValidator"
    )
    logger_mock = mocker.patch.object(LoggerInterface, "log_info")
    repository_mock.create.return_value = window
    presenter_mock.present.return_value = "Test output"
    use_case = create_window.CreateWindowUseCase(presenter_mock, repository_mock, logger_mock)
    input_dto = CreateWindowInputDto(
        window_id=fixture_window["window_id"],
        is_muting=fixture_window["is_muting"],
        agent_language=fixture_window["agent_language"],
        system_message=fixture_window["system_message"],
        temperature=fixture_window["temperature"],
    )
    result = use_case.execute(input_dto)
    repository_mock.create.assert_called_once()
    input_dto_validator_mock.assert_called_once_with(input_dto.to_dict())
    input_dto_validator_instance = input_dto_validator_mock.return_value
    input_dto_validator_instance.validate.assert_called_once_with()
    logger_mock.log_info.assert_called_once_with("Window created successfully")
    output_dto = WindowOutputDto(window)
    presenter_mock.present.assert_called_once_with(output_dto)
    assert result == "Test output"

    # Testing None return value from repository
    repository_mock.create.return_value = None
    with pytest.raises(ValueError) as exception_info:
        use_case.execute(input_dto)
    assert str(exception_info.value) == "Window creation failed"


def test_create_window_empty_field(mocker, fixture_window):
    presenter_mock = mocker.patch.object(WindowPresenterInterface, "present")
    repository_mock = mocker.patch.object(WindowRepositoryInterface, "create")
    logger_mock = mocker.patch.object(LoggerInterface, "log_info")
    use_case = create_window.CreateWindowUseCase(presenter_mock, repository_mock, logger_mock)
    input_dto = CreateWindowInputDto(
        window_id="",
        is_muting=fixture_window["is_muting"],
        agent_language=fixture_window["agent_language"],
        system_message=fixture_window["system_message"],
        temperature=fixture_window["temperature"],
    )

    with pytest.raises(ValueError) as exception_info:
        use_case.execute(input_dto)
    assert str(exception_info.value) == "Window_id: empty values not allowed"

    repository_mock.create.assert_not_called()
    presenter_mock.present.assert_not_called()
