""" Module for WindowPostgresqlRepository
"""

from typing import Optional
from sqlalchemy.exc import IntegrityError

from src.domain.entities.window import Window
from src.infrastructure.db_models.db_base import Session
from src.interactor.interfaces.repositories.window_repository import WindowRepositoryInterface
from src.infrastructure.db_models.window_db_model import WindowsDBModel


class WindowPostgresqlRepository(WindowRepositoryInterface):
    """ Postgresql Repository for Window
    """

    def __init__(self) -> None:
        self.__db = Session

    def __db_to_entity(
            self, db_row: WindowsDBModel
    ) -> Optional[Window]:
        return Window(
            window_id=db_row.window_id,
            is_muting=db_row.is_muting,
            system_message=db_row.system_message,
            agent_language=db_row.agent_language,
            temperature=db_row.temperature
        )

    def create(
            self,
            window_id: str,
            is_muting: bool,
            agent_language: str,
            system_message: str,
            temperature: float
    ) -> Optional[Window]:
        window_db_model = WindowsDBModel(
            window_id=window_id,
            is_muting=is_muting,
            system_message=system_message,
            agent_language=agent_language,
            temperature=temperature
        )
        try:
            self.__db.add(window_db_model)
            self.__db.commit()
            self.__db.refresh(window_db_model)
        except IntegrityError:
            self.__db.rollback()
            raise ValueError("Window creation failed")
        finally:
            self.__db.close()

        if window_db_model is None:
            return None
        
        return self.__db_to_entity(window_db_model)

    def get(self, window_id: str) -> Optional[Window]:
        """ Get Window by id
        :param window_id: str
        :return: Optional[Window]
        """
        result = self.__db.query(WindowsDBModel).get(window_id)
        if result is None:
            return None
        return self.__db_to_entity(result)

    def update(self, window: Window) -> Optional[Window]:
        """ Update Window
        :param window: Window
        :return: Optional[Window]
        """
        window_db_model = WindowsDBModel(
            window_id=window.window_id,
            is_muting=window.is_muting,
            system_message=window.system_message,
            agent_language=window.agent_language,
            temperature=window.temperature
        )
        result = self.__db.query(WindowsDBModel).filter_by(window_id=window.window_id).update(
            {
                "is_muting": window_db_model.is_muting,
                "system_message": window_db_model.system_message,
                "agent_language": window_db_model.agent_language,
                "temperature": window_db_model.temperature
            }
        )
        if result == 0:
            return None
        self.__db.commit()
        return self.__db_to_entity(window_db_model)
