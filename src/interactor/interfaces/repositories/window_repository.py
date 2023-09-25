""" This module contains the interface for the WindowRepository
"""


from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.window import Window


class WindowRepositoryInterface(ABC):
    """This class is the interface for the WindowRepository"""

    @abstractmethod
    def get(self, window_id: str) -> Optional[Window]:
        """Get a Window by id

        :param window_id: str
        :return: Window
        """

    @abstractmethod
    def create(
        self,
        window_id: str,
        is_muting: bool,
        agent_language: str,
        system_message: str,
        temperature: float,
    ) -> Optional[Window]:
        """
        Create a new window.

        Args:
            window_id (str): The ID of the window.
            is_muting (bool): Whether the window is muted or not.
            agent_language (str): The language of the agent.
            system_message (str): The system message to be displayed.
            temperature (int): The temperature value.

        Returns:
            Optional[Window]: The created window object, or None if creation fails.
        """

    @abstractmethod
    def update(self, window: Window) -> Optional[Window]:
        """Save a Window

        :param Window: Window
        :return: Window
        """
