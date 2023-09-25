from unittest import mock

from src.interactor.dtos.event_dto import EventInputDto, EventOutputDto
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.interactor.interfaces.presenters.message_reply_presenter import EventPresenterInterface
from src.interactor.use_cases.create_text_message_reply import CreateTextMessageReplyUseCase


def test_new_user_create_text_message_reply(mocker: mock, fixture_window):
    presenter_mock = mocker.patch.object(EventPresenterInterface, "present")
    presenter_mock.present.return_value = "Test output"

    repository_mock = mocker.patch(
        "src.interactor.use_cases.create_text_message_reply.AgentExecutorRepositoryInterface"
    )
    repository_mock.get.return_value = None
    repository_mock.create.return_value = mocker.Mock(run=mocker.Mock(return_value="Test output"))

    input_dto_validator_mock = mocker.patch(
        "src.interactor.use_cases.create_text_message_reply.\
EventInputDtoValidator"
    )
    logger_mock = mocker.patch.object(LoggerInterface, "log_info")

    use_case = CreateTextMessageReplyUseCase(presenter_mock, repository_mock, logger_mock)
    input_dto = EventInputDto(window=fixture_window, user_input="Test input")
    result = use_case.execute(input_dto)

    input_dto_validator_mock.assert_called_once_with(input_dto.to_dict())
    input_dto_validator_instance = input_dto_validator_mock.return_value
    input_dto_validator_instance.validate.assert_called_once_with()

    repository_mock.get.assert_called_once_with(window_id=input_dto.window.get("window_id"))
    repository_mock.create.assert_called_once()
    logger_mock.log_info.assert_called_once_with("Create reply successfully")

    output_dto = EventOutputDto(
        window=fixture_window, user_input="Test input", response="Test output"
    )
    presenter_mock.present.assert_called_once_with(output_dto)
    assert result == "Test output"


def test_regular_create_text_message_reply(mocker: mock, fixture_window):
    presenter_mock = mocker.patch.object(EventPresenterInterface, "present")
    presenter_mock.present.return_value = "Test output"

    repository_mock = mocker.patch(
        "src.interactor.use_cases.create_text_message_reply.AgentExecutorRepositoryInterface"
    )
    repository_mock.get.return_value = mocker.Mock(run=mocker.Mock(return_value="Test output"))

    input_dto_validator_mock = mocker.patch(
        "src.interactor.use_cases.create_text_message_reply.\
EventInputDtoValidator"
    )
    logger_mock = mocker.patch.object(LoggerInterface, "log_info")

    use_case = CreateTextMessageReplyUseCase(presenter_mock, repository_mock, logger_mock)
    input_dto = EventInputDto(window=fixture_window, user_input="Test input")
    result = use_case.execute(input_dto)

    input_dto_validator_mock.assert_called_once_with(input_dto.to_dict())
    input_dto_validator_instance = input_dto_validator_mock.return_value
    input_dto_validator_instance.validate.assert_called_once_with()

    repository_mock.get.assert_called_once_with(window_id=input_dto.window.get("window_id"))
    repository_mock.create.assert_not_called()
    logger_mock.log_info.assert_called_once_with("Create reply successfully")

    output_dto = EventOutputDto(
        window=fixture_window, user_input="Test input", response="Test output"
    )
    presenter_mock.present.assert_called_once_with(output_dto)
    assert result == "Test output"


def test_create_text_message_reply_if_window_is_muting(mocker: mock, fixture_window):
    presenter_mock = mocker.patch.object(EventPresenterInterface, "present")
    presenter_mock.present.return_value = "Test output"

    repository_mock = mocker.patch(
        "src.interactor.use_cases.create_text_message_reply.AgentExecutorRepositoryInterface"
    )

    input_dto_validator_mock = mocker.patch(
        "src.interactor.use_cases.create_text_message_reply.\
EventInputDtoValidator"
    )
    logger_mock = mocker.patch.object(LoggerInterface, "log_info")

    use_case = CreateTextMessageReplyUseCase(presenter_mock, repository_mock, logger_mock)

    fixture_window["is_muting"] = True
    input_dto = EventInputDto(window=fixture_window, user_input="Test input")
    result = use_case.execute(input_dto)

    input_dto_validator_mock.assert_called_once_with(input_dto.to_dict())
    input_dto_validator_instance = input_dto_validator_mock.return_value
    input_dto_validator_instance.validate.assert_called_once_with()

    repository_mock.get.assert_not_called()
    repository_mock.create.assert_not_called()
    logger_mock.log_info.assert_called_once_with("Create reply successfully")

    output_dto = EventOutputDto(
        window=fixture_window, user_input="Test input", response="靜悄悄的，什麼都沒有發生。"
    )
    presenter_mock.present.assert_called_once_with(output_dto)
    assert result == "Test output"
