# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


from .message import Message

def test_message_creation(fixture_message):
    message = Message(
        window_id=fixture_message["window_id"],
        message=fixture_message["message"],
    )
    assert message.message == fixture_message["message"]


def test_message_from_dict(fixture_message):
    message = Message.from_dict(fixture_message)
    assert message.message == fixture_message["message"]


def test_message_to_dict(fixture_message):
    message = Message.from_dict(fixture_message)
    assert message.to_dict() == fixture_message


def test_message_comparison(fixture_message):
    message_1 = Message.from_dict(fixture_message)
    message_2 = Message.from_dict(fixture_message)
    assert message_1 == message_2
