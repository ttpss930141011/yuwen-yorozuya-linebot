# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


from src.interactor.dtos.window_dtos \
    import WindowOutputDto
from src.domain.entities.window import Window
from .window_presenter import WindowPresenter


def test_create_window_presenter(fixture_window_developer):
    window = Window(
        window_id=fixture_window_developer["window_id"],
        is_muting=fixture_window_developer["is_muting"],
        system_message="Test system message",
        agent_language="en",
        temperature=0.9,
    )
    output_dto = WindowOutputDto(window)
    presenter = WindowPresenter()
    assert presenter.present(output_dto) == {
        "window_id": fixture_window_developer["window_id"],
        "is_muting": fixture_window_developer["is_muting"],
    }
