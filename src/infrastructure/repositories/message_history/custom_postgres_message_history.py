from typing import List

from langchain.schema import BaseChatMessageHistory
from langchain.schema.messages import BaseMessage
from langchain.schema.messages import BaseMessage, _message_to_dict, messages_from_dict
from sqlalchemy.exc import IntegrityError


from src.infrastructure.db_models.db_base import Session
from src.infrastructure.db_models import MessagesDBModel

class CustomPostgresMessageHistory(BaseChatMessageHistory):
    """In Postgre implementation of chat message history.

    Stores messages in a Postgre database.
    """

    def __init__(self, window_id: str) -> None:
        self.__db = Session
        self.window_id = window_id
        if not self.window_id:
            raise ValueError("Window id is required")
        
    def __db_model_to_message(self, db_row: MessagesDBModel) -> dict:
        """
        Converts a MessagesDBModel object to a dictionary representation.

        Args:
            db_row (MessagesDBModel): The MessagesDBModel object to be converted.

        Returns:
            dict: A dictionary representing the MessagesDBModel object.
        """
        return db_row.__dict__


    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        """Retrieve all of the messages from MessagesDBModel"""
        message_model_list = self.__db.query(MessagesDBModel).filter(
            MessagesDBModel.window_id == self.window_id).all()
        model_to_dict= [self.__db_model_to_message(record) for record in message_model_list]
        message_list = [record["message"] for record in model_to_dict]
        messages = messages_from_dict(message_list)
        return messages

    def add_message(self, message: BaseMessage) -> None:
        """Add a self-created message to the store"""
        message_db_model = MessagesDBModel(
            window_id=self.window_id,
            message=_message_to_dict(message)
        )
        try:
            self.__db.add(message_db_model)
            self.__db.commit()
            self.__db.refresh(message_db_model)
        except IntegrityError:
            self.__db.rollback()
            raise ValueError("Message creation failed")
        finally:
            self.__db.close()

    def clear(self) -> None:
        """Clear all messages by window_id from the store"""
        try:
            self.__db.query(MessagesDBModel).filter(
                MessagesDBModel.window_id == self.window_id).delete()
            self.__db.commit()
        except IntegrityError:
            self.__db.rollback()
            raise ValueError("Message deletion failed")
        finally:
            self.__db.close()

    def __del__(self) -> None:
        """
        Destructor method that is automatically called when the object is about to be destroyed.
        
        Parameters:
            None
        
        Returns:
            None
        """
        if self.__db is not None:
            self.__db.close()