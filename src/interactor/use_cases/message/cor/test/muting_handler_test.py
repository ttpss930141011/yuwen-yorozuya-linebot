from unittest import mock

from linebot.v3.messaging.models import TextMessage

from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.message.cor.muting_handler import MutingHandler


def test_muting_handler_with_fixture_window_with_muting(
        mocker: mock, fixture_window_with_muting: dict
):
    container_mock = mocker.MagicMock()

    input_dto_mock = EventInputDto(
        window=fixture_window_with_muting,
        user_input="mock user input",
        source_type="mock source type",
    )

    muting_handler = MutingHandler(container_mock)
    messages = muting_handler.handle(input_dto_mock)

    # self._successor.handle is not called
    assert len(messages) == 0
    assert muting_handler._successor is None
    assert messages == []


def test_muting_handler_with_no_successor(mocker: mock, fixture_window: dict):
    input_dto_mock = EventInputDto(
        window=fixture_window,
        user_input="mock user input",
        source_type="mock source type",
    )
    container_mock = mocker.MagicMock()
    muting_handler = MutingHandler(container_mock)
    messages = muting_handler.handle(input_dto_mock)

    # self._successor.handle is not called
    assert len(messages) == 1
    assert muting_handler._successor is None
    assert messages[0] == TextMessage(text="Something went wrong! >_<")


def test_muting_handler_with_successor(mocker: mock, fixture_window: dict):

    container_mock = mocker.MagicMock()

    input_dto_mock = EventInputDto(
        window=fixture_window,
        user_input="mock user input",
        source_type="mock source type",
    )

    muting_handler = MutingHandler(container_mock)
    muting_handler.set_successor(mocker.MagicMock())
    messages = muting_handler.handle(input_dto_mock)

    # self._successor.handle is called
    assert len(messages) == 0
    assert muting_handler._successor.handle.call_count == 1
