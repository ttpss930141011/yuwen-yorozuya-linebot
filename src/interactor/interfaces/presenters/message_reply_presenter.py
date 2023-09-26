""" Module for the MessageReplyPresenterInterface
"""


from abc import ABC, abstractmethod
from typing import List

from linebot.v3.messaging.models.message import Message

from src.interactor.dtos.event_dto import EventOutputDto


class EventPresenterInterface(ABC):
    """Class for the Interface of the WindowPresenter"""

    @abstractmethod
    def present(self, output_dto: EventOutputDto) -> List[Message]:
        """Present the Window"""
