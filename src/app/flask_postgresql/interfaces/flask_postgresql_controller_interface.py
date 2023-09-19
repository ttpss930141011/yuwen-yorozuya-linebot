""" This module contains the FlaskPostgresqlControllerInterface class
"""


from typing import Dict
from abc import ABC, abstractmethod


class FlaskPostgresqlControllerInterface(ABC):
    """ This class is the interface for the Flask Postgresql Controller class
    """

    @abstractmethod
    def execute(self) -> Dict:
        """ Executes the controller
        :returns: Window created
        """
