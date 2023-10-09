from unittest import mock

from linebot.v3.messaging.models import TextMessage

from src.interactor.dtos.event_dto import EventInputDto, EventOutputDto
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.interactor.interfaces.presenters.message_reply_presenter import EventPresenterInterface
from src.interactor.use_cases.message.create_message_reply import CreateMessageReplyUseCase


def test_create_message_reply(mocker: mock, fixture_window):
    presenter_mock = mocker.patch.object(EventPresenterInterface, "present")
    presenter_mock.present.return_value = "Test output"

    reply_messages_cor_mock = mocker.patch(
        "src.interactor.use_cases.message.create_message_reply.ReplyMessagesCOR"
    )
    reply_messages_cor_instance = reply_messages_cor_mock.return_value
    reply_messages_cor_instance.handle.return_value = [TextMessage(text="Test output")]

    repository_mock = mocker.patch(
        "src.interactor.use_cases.message.create_message_reply.AgentExecutorRepositoryInterface"
    )

    input_dto_validator_mock = mocker.patch(
        "src.interactor.use_cases.message.create_message_reply.EventInputDtoValidator"
    )
    logger_mock = mocker.patch.object(LoggerInterface, "log_info")

    use_case = CreateMessageReplyUseCase(presenter_mock, repository_mock, logger_mock)
    input_dto = EventInputDto(window=fixture_window, user_input="Test input")
    result = use_case.execute(input_dto)

    input_dto_validator_mock.assert_called_once_with(input_dto.to_dict())
    input_dto_validator_instance = input_dto_validator_mock.return_value
    input_dto_validator_instance.validate.assert_called_once_with()

    logger_mock.log_info.assert_called_once_with("Create reply successfully")

    reply_messages_cor_instance.handle.assert_called_once_with(input_dto, repository_mock)

    output_dto = EventOutputDto(
        window=fixture_window, user_input="Test input", response=[TextMessage(text="Test output")]
    )
    presenter_mock.present.assert_called_once_with(output_dto)
    assert result == "Test output"
