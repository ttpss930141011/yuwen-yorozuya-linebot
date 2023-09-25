""" The above snippet is an example of a handler that implements the LineEventHandlerInterface.
"""

from abc import ABC, abstractmethod


class EventHandlerInterface(ABC):
    """This class is the interface for the Line Event Handler class"""

    @abstractmethod
    def get_event_info(self, event) -> None:
        """
        Set the window_id attribute based on the type of event source.

        Args:
            event (MessageEvent): The event object containing the source information.

        Returns:
            None
        """

    @abstractmethod
    def execute(self) -> None:
        """Executes the handler
        :returns None
        """
