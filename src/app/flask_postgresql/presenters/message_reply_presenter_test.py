# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


from src.interactor.dtos.event_dto \
    import EventOutputDto
from src.domain.entities.window import Window
from .message_reply_presenter import EventPresenter


def test_create_window_presenter(fixture_window):
    window = {
        "window_id": fixture_window["window_id"],
        "is_muting": fixture_window["is_muting"],
        "system_message": fixture_window["system_message"],
        "agent_language": fixture_window["agent_language"],
        "temperature": fixture_window["temperature"],
    }
    user_input = "test user_input"
    response = "test response"

    output_dto = EventOutputDto(
        window=window,
        user_input=user_input,
        response=response
    )
    presenter = EventPresenter()
    assert presenter.present(output_dto) == response
