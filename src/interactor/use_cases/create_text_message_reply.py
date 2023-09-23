""" This module is responsible for creating a new window.
"""


from typing import Dict

from src.interactor.interfaces.repositories.agent_executor_repository import AgentExecutorRepositoryInterface
from src.interactor.interfaces.logger.logger import LoggerInterface
from langchain.agents import AgentExecutor
from src.interactor.dtos.event_dto import EventInputDto


class CreateTextMessageReplyUseCase():
    """ This class is responsible for creating a new window.
    """

    def __init__(
            self,
            repository: AgentExecutorRepositoryInterface,
            logger: LoggerInterface,

    ):
        self.repository = repository
        self.logger = logger
        self.agent_executor: AgentExecutor

    def _get_agent_executor(self, input_dto:EventInputDto ) -> None:
        """
        Retrieves the agent executor associated with the current window.

        :param None: This function does not take any parameters.
        :return: None
        """

        window_id = input_dto.window.get("window_id")

        self.agent_executor = self.repository.get(
            window_id=window_id,
        )
        if self.agent_executor is None:
            self.agent_executor = self.repository.create(
                window_id=window_id,
            )

    def execute(self, input_dto: EventInputDto) -> str:

        # TODO: 使用 validate_input_dto 來驗證 input_dto
        self._get_agent_executor(input_dto)
        response = self.agent_executor.run(input=input_dto.user_input)
        return response
