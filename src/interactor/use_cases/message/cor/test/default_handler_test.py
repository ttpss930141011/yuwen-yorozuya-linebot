from unittest import mock

from linebot.v3.messaging.models import TextMessage

from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.message.cor.default_handler import DefaultHandler


def test_default_handler(mocker: mock, fixture_window: dict):
    container_mock = mocker.MagicMock()
    agent_executor_mock = mocker.MagicMock()
    agent_executor_mock.run.return_value = "mock agent executor result"
    get_agent_executor_mock = mocker.patch(
        "src.interactor.use_cases.message.cor.default_handler.DefaultHandler._get_agent_executor"
    )
    get_agent_executor_mock.return_value = agent_executor_mock

    input_dto_mock = EventInputDto(
        window=fixture_window,
        user_input="mock user input",
        source_type="mock source type",
    )

    default_handler = DefaultHandler(container_mock)
    messages = default_handler.handle(input_dto_mock)

    get_agent_executor_mock.assert_called_once_with(input_dto_mock)
    agent_executor_mock.run.assert_called_once_with(input=input_dto_mock.user_input)

    assert len(messages) == 1
    assert messages[0] == TextMessage(text="mock agent executor result")


def test_get_agent_executor_in_default_handler(mocker: mock, fixture_window: dict):
    container_mock = mocker.MagicMock()
    agent_executor_repository_mock = mocker.MagicMock()
    container_mock.resolve.return_value = agent_executor_repository_mock
    agent_executor_mock = mocker.MagicMock()
    agent_executor_mock.run.return_value = "mock agent executor result"

    agent_executor_repository_mock.get.return_value = None
    agent_executor_repository_mock.create.return_value = mocker.MagicMock()
    agent_executor_repository_mock.create.return_value.run.return_value = "mock agent executor result"

    input_dto_mock = EventInputDto(
        window=fixture_window,
        user_input="mock user input",
        source_type="mock source type",
    )

    default_handler = DefaultHandler(container_mock)
    default_handler._get_agent_executor(input_dto_mock)

    agent_executor_repository_mock.get.assert_called_once_with(window_id=fixture_window["window_id"])
    agent_executor_repository_mock.create.assert_called_once_with(window_id=fixture_window["window_id"])
