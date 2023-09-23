# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


from src.interactor.dtos.window_dtos \
    import WindowOutputDto
from src.domain.entities.window import Window
from .window_presenter import WindowPresenter


def test_create_window_presenter(fixture_window):
    window = Window(
        window_id=fixture_window["window_id"],
        is_muting=fixture_window["is_muting"],
        system_message=fixture_window["system_message"],
        agent_language=fixture_window["agent_language"],
        temperature=fixture_window["temperature"],
    )
    output_dto = WindowOutputDto(window)
    presenter = WindowPresenter()
    assert presenter.present(output_dto) == {
        "window_id": fixture_window["window_id"],
        "is_muting": fixture_window["is_muting"],
        "system_message": fixture_window["system_message"],
        "agent_language": fixture_window["agent_language"],
        "temperature": fixture_window["temperature"]
    }
