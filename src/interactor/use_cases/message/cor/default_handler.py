from langchain.agents import AgentExecutor
from linebot.v3.messaging.models import TextMessage

from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.message.cor.handler_base import Handler


class DefaultHandler(Handler):
    """
    The last handler in the chain of responsibility.

    This handler uses the agent executor to process the user input.
    """

    def _get_agent_executor(self, input_dto: EventInputDto) -> AgentExecutor:
        """
        Retrieves the agent executor associated with the current window.

        :param None: This function does not take any parameters.
        :return: None
        """
        window_id = input_dto.window.get("window_id")

        agent_executor = self.agent_repository.get(
            window_id=window_id,
        )
        if agent_executor is None:
            agent_executor = self.agent_repository.create(window_id=window_id)
        return agent_executor

    def handle(self, input_dto: EventInputDto):
        messages = []
        try:
            agent_executor = self._get_agent_executor(input_dto)
            result = agent_executor.run(input=input_dto.user_input)
            messages.extend([TextMessage(text=result)])
        except Exception as e:
            self.logger.error(e)
            messages.extend([TextMessage(text="Something went wrong! >_<")])
        finally:
            return messages
