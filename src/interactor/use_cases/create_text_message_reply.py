""" This module is responsible for creating a new window.
"""
from langchain.agents import AgentExecutor

from src.interactor.interfaces.presenters.message_reply_presenter import EventPresenterInterface
from src.interactor.validations.event_input_validator import EventInputDtoValidator
from src.interactor.interfaces.repositories.agent_executor_repository import AgentExecutorRepositoryInterface
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.interactor.dtos.event_dto import EventInputDto, EventOutputDto


class CreateTextMessageReplyUseCase():
    """ This class is responsible for creating a new window.
    """

    def __init__(
            self,
            presenter: EventPresenterInterface,
            repository: AgentExecutorRepositoryInterface,
            logger: LoggerInterface,

    ):
        self.presenter = presenter
        self.repository = repository
        self.logger = logger

    def _get_agent_executor(self, input_dto: EventInputDto) -> AgentExecutor:
        """
        Retrieves the agent executor associated with the current window.

        :param None: This function does not take any parameters.
        :return: None
        """

        window_id = input_dto.window.get("window_id")

        agent_executor = self.repository.get(
            window_id=window_id,
        )
        if agent_executor is None:
            agent_executor = self.repository.create(
                window_id=window_id,
            )
        return agent_executor

    def execute(self, input_dto: EventInputDto) -> str:
        validator = EventInputDtoValidator(input_dto.to_dict())
        validator.validate()

        if input_dto.window.get("is_muting") is True:
            response = "靜悄悄的，什麼都沒有發生。"
        else:
            agent_executor = self._get_agent_executor(input_dto)
            response = agent_executor.run(input=input_dto.user_input)
        
        output_dto = EventOutputDto(
            window=input_dto.window,
            user_input=input_dto.user_input,
            response=response,
        )
        
        presenter_response = self.presenter.present(output_dto)
        self.logger.log_info("Create reply successfully")
        return presenter_response
