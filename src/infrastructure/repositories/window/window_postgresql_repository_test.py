# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring


from unittest import mock
import pytest
from sqlalchemy.exc import IntegrityError
from src.domain.entities.window import Window

with mock.patch(
    "sqlalchemy.create_engine"
) as mock_create_engine:
    from src.infrastructure.db_models.window_db_model import WindowsDBModel
    from .window_postgresql_repository \
        import WindowPostgresqlRepository


def test_window_postgresql_repository(
        mocker,
        fixture_window_developer
):

    mocker.patch(
        'uuid.uuid4',
        return_value=fixture_window_developer["window_id"]
    )

    windows_db_model_mock = mocker.patch(
        'src.infrastructure.repositories.window_postgresql_repository.\
WindowsDBModel')
    session_mock = mocker.patch(
        'src.infrastructure.repositories.window_postgresql_repository.Session')
    windows_db_model = WindowsDBModel(
        window_id=fixture_window_developer["window_id"],
        name=fixture_window_developer["name"],
        description=fixture_window_developer["description"]
    )
    windows_db_model_mock.return_value = windows_db_model
    repository = WindowPostgresqlRepository()
    result = repository.create(
        fixture_window_developer["name"],
        fixture_window_developer["description"]
    )
    window = Window(
        windows_db_model_mock.return_value.window_id,
        windows_db_model_mock.return_value.name,
        windows_db_model_mock.return_value.description
    )
    session_mock.add.assert_called_once_with(windows_db_model_mock())
    session_mock.commit.assert_called_once_with()
    session_mock.refresh.assert_called_once_with(windows_db_model_mock())
    assert result == window

    # Testing create return None
    windows_db_model_mock.return_value = None
    result = repository.create(
        fixture_window_developer["name"],
        fixture_window_developer["description"]
    )
    assert result is None

    # Testing successful update
    windows_edited_db_model = WindowsDBModel(
        window_id=fixture_window_developer["window_id"],
        name="Edited Window name",
        description="Edited Description"
    )
    windows_db_model_mock.return_value = windows_edited_db_model
    edited_window = Window(
        windows_db_model_mock.return_value.window_id,
        windows_db_model_mock.return_value.name,
        windows_db_model_mock.return_value.description
    )
    repository = WindowPostgresqlRepository()
    result = repository.update(
        edited_window
    )
    session_mock.query.assert_called_once_with(windows_db_model_mock)
    session_mock.query.return_value.filter_by.return_value.update.\
        assert_called_once_with(
            {
                "name": edited_window.name,
                "description": edited_window.description
            }
        )
    assert result == edited_window

    # Testing update with invalid window_id
    invalid_window = Window(
            window_id="Dont exist window_id",
            name="Edited Window name",
            description="Edited Description"
    )
    session_mock.query.return_value.filter_by.return_value.update.return_value\
        = 0
    repository = WindowPostgresqlRepository()
    result_invalid_id = repository.update(
        invalid_window
    )
    assert result_invalid_id is None

    # Testing create with name that violate unique
    session_mock.add.side_effect = IntegrityError(
        None, None,
        'psycopg2.errors.UniqueViolation: duplicate key value violates unique \
constraint "windows_name_key"')
    windows_db_model_mock.return_value = None
    with pytest.raises(ValueError) as exception_info:
        result = repository.create(
            fixture_window_developer["name"],
            fixture_window_developer["description"]
        )
    assert str(exception_info.value) == \
        "Window with the same name already exists"

    # Testing create raising another IntegrityError
    session_mock.add.side_effect = IntegrityError(None, None, "test error")
    with pytest.raises(IntegrityError) as exception_info:
        result = repository.create("", "")
    assert "test error" in str(exception_info.value)


def test_window_postgresql_repository_get(
        mocker,
        fixture_window_developer
):

    session_mock = mocker.patch(
        'src.infrastructure.repositories.window_postgresql_repository.Session'
    )
    windows_db_model_mock = mocker.patch(
        'src.infrastructure.db_models.window_db_model.WindowsDBModel'
    )
    session_mock.query.return_value.get.return_value = \
        windows_db_model_mock
    window_mock = Window(
            window_id=windows_db_model_mock.window_id,
            name=windows_db_model_mock.name,
            description=windows_db_model_mock.description
    )
    repository = WindowPostgresqlRepository()
    result = repository.get(
        windows_db_model_mock.window_id
    )
    assert result == window_mock

    # Testing the case that the query returns None
    session_mock.query.return_value.get.return_value = None
    repository = WindowPostgresqlRepository()
    result = repository.get(
        windows_db_model_mock.window_id
    )
    assert result is None
