from unittest import mock

from linebot.v3.messaging.models import TextMessage

from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.message.cor.muting_handler import MutingHandler


def test_muting_handler_with_fixture_window_with_muting(
    mocker: mock, fixture_window_with_muting: dict
):
    repository_mock = mocker.patch(
        "src.interactor.use_cases.message.cor.muting_handler.AgentExecutorRepositoryInterface"
    )
    response = []

    input_dto_mock = EventInputDto(
        window=fixture_window_with_muting,
        user_input="mock user input",
    )

    muting_handler = MutingHandler()
    muting_handler.handle(input_dto_mock, repository_mock, response)

    # self._successor.handle is not called
    assert len(response) == 0
    assert muting_handler._successor is None
    assert response == []


def test_muting_handler_with_no_successor(mocker: mock, fixture_window: dict):
    repository_mock = mocker.patch(
        "src.interactor.use_cases.message.cor.muting_handler.AgentExecutorRepositoryInterface"
    )
    response = []

    input_dto_mock = EventInputDto(
        window=fixture_window,
        user_input="mock user input",
    )

    muting_handler = MutingHandler()
    muting_handler.handle(input_dto_mock, repository_mock, response)

    # self._successor.handle is not called
    assert len(response) == 1
    assert muting_handler._successor is None
    assert response[0] == TextMessage(text="靜悄悄的，什麼都沒有發生。")


def test_muting_handler_with_successor(mocker: mock, fixture_window: dict):
    repository_mock = mocker.patch(
        "src.interactor.use_cases.message.cor.muting_handler.AgentExecutorRepositoryInterface"
    )
    response = []

    input_dto_mock = EventInputDto(
        window=fixture_window,
        user_input="mock user input",
    )

    muting_handler = MutingHandler(mocker.Mock())
    muting_handler.handle(input_dto_mock, repository_mock, response)

    # self._successor.handle is called
    assert len(response) == 0
    assert muting_handler._successor.handle.call_count == 1
