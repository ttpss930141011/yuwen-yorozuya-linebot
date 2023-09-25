from unittest import mock

import pytest
from sqlalchemy.exc import IntegrityError

from src.domain.entities.window import Window

with mock.patch("sqlalchemy.create_engine") as mock_create_engine:
    from src.infrastructure.db_models import WindowsDBModel
    from src.infrastructure.repositories.window import WindowPostgresqlRepository


def test_window_postgresql_repository(mocker, fixture_window):
    windows_db_model_mock = mocker.patch(
        "src.infrastructure.repositories.window.window_postgresql_repository.WindowsDBModel"
    )
    session_mock = mocker.patch(
        "src.infrastructure.repositories.window.window_postgresql_repository.Session"
    )
    windows_db_model = WindowsDBModel(
        window_id=fixture_window["window_id"],
        is_muting=fixture_window["is_muting"],
        system_message=fixture_window["system_message"],
        agent_language=fixture_window["agent_language"],
        temperature=fixture_window["temperature"],
    )
    windows_db_model_mock.return_value = windows_db_model
    repository = WindowPostgresqlRepository()
    result = repository.create(
        fixture_window["window_id"],
        fixture_window["is_muting"],
        fixture_window["system_message"],
        fixture_window["agent_language"],
        fixture_window["temperature"],
    )
    window = Window(
        window_id=windows_db_model_mock.return_value.window_id,
        is_muting=windows_db_model_mock.return_value.is_muting,
        system_message=windows_db_model_mock.return_value.system_message,
        agent_language=windows_db_model_mock.return_value.agent_language,
        temperature=windows_db_model_mock.return_value.temperature,
    )
    session_mock.add.assert_called_once_with(windows_db_model_mock())
    session_mock.add.assert_called_once()
    session_mock.commit.assert_called_once_with()
    session_mock.refresh.assert_called_once_with(windows_db_model_mock())
    assert result == window

    # Testing create return None
    windows_db_model_mock.return_value = None
    result = repository.create(
        fixture_window["window_id"],
        fixture_window["is_muting"],
        fixture_window["system_message"],
        fixture_window["agent_language"],
        fixture_window["temperature"],
    )
    assert result is None

    # Testing successful update
    windows_edited_db_model = WindowsDBModel(
        window_id=fixture_window["window_id"],
        is_muting=True,
        system_message="Edited System Message",
        agent_language="Edited Agent Language",
        temperature=25.0,
    )
    windows_db_model_mock.return_value = windows_edited_db_model
    edited_window = Window(
        window_id=windows_db_model_mock.return_value.window_id,
        is_muting=windows_db_model_mock.return_value.is_muting,
        system_message=windows_db_model_mock.return_value.system_message,
        agent_language=windows_db_model_mock.return_value.agent_language,
        temperature=windows_db_model_mock.return_value.temperature,
    )
    repository = WindowPostgresqlRepository()
    result = repository.update(edited_window)
    session_mock.query.assert_called_once_with(windows_db_model_mock)
    session_mock.query.return_value.filter_by.return_value.update.assert_called_once_with(
        {
            "is_muting": edited_window.is_muting,
            "system_message": edited_window.system_message,
            "agent_language": edited_window.agent_language,
            "temperature": edited_window.temperature,
        }
    )
    assert result == edited_window

    # Testing create with id that violate unique
    session_mock.add.side_effect = IntegrityError(
        None,
        None,
        'psycopg2.errors.UniqueViolation: duplicate key value violates unique \
constraint "windows_id_key"',
    )
    windows_db_model_mock.return_value = None
    with pytest.raises(ValueError) as exception_info:
        result = repository.create(
            fixture_window["window_id"],
            fixture_window["is_muting"],
            fixture_window["system_message"],
            fixture_window["agent_language"],
            fixture_window["temperature"],
        )
    assert str(exception_info.value) == "Window creation failed"


def test_window_postgresql_repository_get(mocker, fixture_window):
    windows_db_model_mock = mocker.patch("src.infrastructure.db_models.WindowsDBModel")
    session_mock = mocker.patch(
        "src.infrastructure.repositories.window.window_postgresql_repository.Session"
    )

    windows_db_model_mock.return_value = WindowsDBModel(
        window_id=fixture_window["window_id"],
        is_muting=fixture_window["is_muting"],
        system_message=fixture_window["system_message"],
        agent_language=fixture_window["agent_language"],
        temperature=fixture_window["temperature"],
    )

    session_mock.query.return_value.get.return_value = windows_db_model_mock.return_value

    repository = WindowPostgresqlRepository()
    result = repository.get(window_id=fixture_window["window_id"])
    window = Window(
        window_id=windows_db_model_mock.return_value.window_id,
        is_muting=windows_db_model_mock.return_value.is_muting,
        system_message=windows_db_model_mock.return_value.system_message,
        agent_language=windows_db_model_mock.return_value.agent_language,
        temperature=windows_db_model_mock.return_value.temperature,
    )

    assert result == window


def test_window_postgresql_repository_get_none(mocker, fixture_window):
    windows_db_model_mock = mocker.patch("src.infrastructure.db_models.WindowsDBModel")
    session_mock = mocker.patch(
        "src.infrastructure.repositories.window.window_postgresql_repository.Session"
    )
    session_mock.query.return_value.get.return_value = None

    windows_db_model_mock.return_value = None

    repository = WindowPostgresqlRepository()
    result = repository.get(window_id=fixture_window["window_id"])
    assert result is None
