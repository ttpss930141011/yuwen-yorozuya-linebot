# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


from .window import Window


def test_window_creation(fixture_window):
    window = Window(
        window_id=fixture_window["window_id"],
        is_muting=fixture_window["is_muting"],
    )
    assert window.is_muting == fixture_window["is_muting"]


def test_window_from_dict(fixture_window):
    window = Window.from_dict(fixture_window)
    assert window.is_muting == fixture_window["is_muting"]


def test_window_to_dict(fixture_window):
    window = Window.from_dict(fixture_window)
    assert window.to_dict() == fixture_window


def test_window_comparison(fixture_window):
    window_1 = Window.from_dict(fixture_window)
    window_2 = Window.from_dict(fixture_window)
    assert window_1 == window_2

def test_window_set_muting(fixture_window):
    window = Window.from_dict(fixture_window)
    window.set_muting(True)
    assert window.is_muting
