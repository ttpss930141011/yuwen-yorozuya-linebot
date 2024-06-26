""" This module is responsible for creating a new window.
"""

from src.infrastructure.container.container import Container
from src.interactor.dtos.event_dto import EventInputDto, EventOutputDto
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.interactor.interfaces.presenters.message_reply_presenter import EventPresenterInterface
from src.interactor.use_cases.message.cor import ReplyMessagesCOR
from src.interactor.validations.event_input_validator import EventInputDtoValidator


class CreateMessageReplyUseCase:
    """This class is responsible for creating a new window."""

    def __init__(self, presenter: EventPresenterInterface, container: Container):
        self.presenter = presenter
        self.container = container
        self.logger: LoggerInterface = container.resolve("logger")

    def execute(self, input_dto: EventInputDto):
        """
        Executes the given event input DTO.

        Args:
            input_dto (EventInputDto): The event input DTO containing the necessary information for execution.

        Returns:
            EventOutputDto: The output DTO containing the result of the execution.

        Raises:
            None.
        """
        validator = EventInputDtoValidator(input_dto.to_dict())
        validator.validate()

        reply_messages_cor = ReplyMessagesCOR(self.container)

        response = reply_messages_cor.handle(input_dto)

        output_dto = EventOutputDto(
            window=input_dto.window,
            user_input=input_dto.user_input,
            response=response,
        )

        presenter_response = self.presenter.present(output_dto)
        self.logger.log_info("Create reply successfully")
        return presenter_response
