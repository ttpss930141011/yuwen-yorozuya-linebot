from unittest import mock

from linebot.v3.messaging.models import TextMessage

from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.message.cor.default_handler import DefaultHandler


def test_default_handler(mocker: mock, fixture_window: dict):
    repository_mock = mocker.patch(
        "src.interactor.use_cases.message.cor.default_handler.AgentExecutorRepositoryInterface"
    )
    agent_executor_mock = mocker.Mock(run=mocker.Mock(return_value="mock agent executor result"))
    get_agent_executor_mock = mocker.patch(
        "src.interactor.use_cases.message.cor.default_handler.DefaultHandler._get_agent_executor"
    )
    get_agent_executor_mock.return_value = agent_executor_mock

    response = []

    input_dto_mock = EventInputDto(
        window=fixture_window,
        user_input="mock user input",
    )

    default_handler = DefaultHandler()
    default_handler.handle(input_dto_mock, repository_mock, response)

    get_agent_executor_mock.assert_called_once_with(input_dto_mock, repository_mock)
    agent_executor_mock.run.assert_called_once_with(input=input_dto_mock.user_input)

    assert len(response) == 1
    assert response[0] == TextMessage(text="mock agent executor result")


def test_get_agent_executor_in_default_handler(mocker: mock, fixture_window: dict):
    repository_mock = mocker.patch(
        "src.interactor.use_cases.message.cor.default_handler.AgentExecutorRepositoryInterface"
    )
    repository_mock.get.return_value = None
    agent_executor_mock = mocker.Mock(run=mocker.Mock(return_value="mock agent executor result"))
    repository_mock.create.return_value = mocker.Mock(return_value=agent_executor_mock)

    input_dto_mock = EventInputDto(
        window=fixture_window,
        user_input="mock user input",
    )

    default_handler = DefaultHandler()
    default_handler._get_agent_executor(input_dto_mock, repository_mock)

    repository_mock.get.assert_called_once_with(window_id=fixture_window["window_id"])
    repository_mock.create.assert_called_once_with(window_id=fixture_window["window_id"])
