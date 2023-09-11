""" This module contains the interface for the WindowRepository
"""


from abc import ABC, abstractmethod
from typing import Optional
from src.domain.value_objects import WindowId
from src.domain.entities.window import Window


class WindowRepositoryInterface(ABC):
    """ This class is the interface for the WindowRepository
    """

    @abstractmethod
    def get(self, window_id: WindowId) -> Optional[Window]:
        """ Get a Window by id

        :param window_id: WindowId
        :return: Window
        """

    @abstractmethod
    def create(self, name: str, description: str) -> Optional[Window]:
        """ Create a Window

        :param name: Window Name
        :param description: Window Description
        :return: WindowId
        """

    @abstractmethod
    def update(self, window: Window) -> Optional[Window]:
        """ Save a Window

        :param Window: Window
        :return: Window
        """
