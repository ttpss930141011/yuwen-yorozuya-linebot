""" Module for the EventPresenter
"""

from src.interactor.dtos.event_dto \
    import EventOutputDto
from src.interactor.interfaces.presenters.message_reply_presenter \
    import EventPresenterInterface


class EventPresenter(EventPresenterInterface):
    """ Class for the EventPresenter
    """

    def present(self, output_dto: EventOutputDto) -> str:
        """
        Present the output DTO.

        Args:
            output_dto (EventOutputDto): The output DTO containing the response.

        Returns:
            str: The response from the output DTO.
        """
        
        return output_dto.response
