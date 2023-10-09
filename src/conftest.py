import pytest


@pytest.fixture
def fixture_window():
    """Fixture with Window example"""
    return {
        "window_id": "abc1234567890",
        "is_muting": False,
        "system_message": "Hello World",
        "agent_language": "en",
        "temperature": 20.0,
    }


@pytest.fixture
def fixture_window_with_muting():
    """Fixture with Window example"""
    return {
        "window_id": "abc1234567890",
        "is_muting": True,
        "system_message": "Hello World",
        "agent_language": "en",
        "temperature": 20.0,
    }


@pytest.fixture
def fixture_message():
    """Fixture with Message example"""
    return {
        "window_id": "1234567890",
        "message": {},
    }
