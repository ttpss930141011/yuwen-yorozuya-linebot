""" The above snippet is an example of a handler that implements the LineEventHandlerInterface.
"""

from abc import ABC, abstractmethod


class LineEventHandlerInterface(ABC):
    """ This class is the interface for the Line Event Handler class
    """

    @abstractmethod
    def execute(self) -> None:
        """ Executes the handler
        :returns None
        """
