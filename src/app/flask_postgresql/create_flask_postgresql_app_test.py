# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


from unittest import mock
from flask import Flask
from flask.testing import FlaskClient
import pytest
from src.infrastructure.loggers.logger_default import LoggerDefault
from src.app.flask_postgresql.configs import Config


with mock.patch(
    "sqlalchemy.create_engine"
) as mock_create_engine, \
    mock.patch(
        "langchain.utilities.SerpAPIWrapper"
) as mock_sessionmaker:
    from .create_flask_postgresql_app import create_flask_postgresql_app


logger = LoggerDefault()


@pytest.fixture(name="flask_postgresql_app")
def fixture_flask_postgresql_app():
    """ Fixture for flask app with blueprint
    """
    app: Flask = create_flask_postgresql_app(Config,logger)
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture(name="client_flask_postgresql_app")
def fixture_client_flask_postgresql_app(flask_postgresql_app:Flask):
    """ Fixture to test app_flask_with_blueprint
    """
    return flask_postgresql_app.test_client()


def test_request_window(
        mocker,
        client_flask_postgresql_app: FlaskClient
):
    """ Test request example
    """
    headers_data = {
        "X-Line-Signature": "test"
    }
    input_data = {
        "destination":"test_destination",
        "events":[
            {
                "type":"message",
                "message":{
                    "type":"text",
                    "id":"test_id",
                    "text":""
                },
                "replyToken":"test_reply_token",
                "mode":"active"
            }
        ]
    }
    handler_mock = mocker.patch(
        "src.app.flask_postgresql.event_handlers.handler.handle"
    )
    response = client_flask_postgresql_app.post(
        "/callback",
        headers=headers_data,
        json=input_data
    )
    assert response.status_code == 200
    handler_mock.assert_called_once()


def test_request_window_wrong_url_error(
        mocker,
        client_flask_postgresql_app,
):
    """ Test request example
    """
    headers_data = {
        "X-Line-Signature": "test"
    }
    input_data = {
        "destination":"test_destination",
        "events":[
            {
                "type":"message",
                "message":{
                    "type":"text",
                    "id":"test_id",
                    "text":""
                },
                "replyToken":"test_reply_token",
                "mode":"active"
            }
        ]
    }
    handler_mock = mocker.patch(
        "src.app.flask_postgresql.event_handlers.handler.handle"
    )
    response = client_flask_postgresql_app.post(
        "/callbac",
        headers=headers_data,
        json=input_data
    )
    assert response.status_code == 404
    handler_mock.assert_not_called()
    assert b"The requested URL was not found on the server" in response.data
    
