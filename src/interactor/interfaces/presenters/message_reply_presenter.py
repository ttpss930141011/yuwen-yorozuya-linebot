""" Module for the MessageReplyPresenterInterface
"""


from typing import Dict
from abc import ABC, abstractmethod
from src.interactor.dtos.event_dto import EventOutputDto


class EventPresenterInterface(ABC):
    """ Class for the Interface of the WindowPresenter
    """
    @abstractmethod
    def present(self, output_dto: EventOutputDto) -> Dict:
        """ Present the Window
        """
