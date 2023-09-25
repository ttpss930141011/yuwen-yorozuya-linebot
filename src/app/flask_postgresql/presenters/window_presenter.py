""" Module for the WindowPresenter
"""


from typing import Dict

from src.interactor.dtos.window_dtos import WindowOutputDto
from src.interactor.interfaces.presenters.window_presenter import WindowPresenterInterface


class WindowPresenter(WindowPresenterInterface):
    """Class for the WindowPresenter"""

    def present(self, output_dto: WindowOutputDto) -> Dict:
        """Present the CreateWindow
        :param output_dto: WindowOutputDto
        :return: Dict
        """
        return {
            "window_id": output_dto.window.window_id,
            "is_muting": output_dto.window.is_muting,
            "agent_language": output_dto.window.agent_language,
            "system_message": output_dto.window.system_message,
            "temperature": output_dto.window.temperature,
        }
