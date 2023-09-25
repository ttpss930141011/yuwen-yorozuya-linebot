""" Module for the WindowPresenterInterface
"""


from abc import ABC, abstractmethod
from typing import Dict

from src.interactor.dtos.window_dtos import WindowOutputDto


class WindowPresenterInterface(ABC):
    """Class for the Interface of the WindowPresenter"""

    @abstractmethod
    def present(self, output_dto: WindowOutputDto) -> Dict:
        """Present the Window"""
