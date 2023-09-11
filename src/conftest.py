# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


import uuid
import pytest


@pytest.fixture
def fixture_window():
    """ Fixture with Window example """
    return {
        "window_id": uuid.uuid4().hex,
        "is_muting": False,
    }

@pytest.fixture
def fixture_message():
    """ Fixture with Message example """
    return {
        "window_id": uuid.uuid4().hex,
        "message": {},
    }
