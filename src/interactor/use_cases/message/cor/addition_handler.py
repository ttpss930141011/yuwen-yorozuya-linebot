from typing import List

from linebot.v3.messaging.models import TextMessage
from linebot.v3.messaging.models.message import Message

from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.interfaces.repositories.agent_executor_repository import (
    AgentExecutorRepositoryInterface,
)
from src.interactor.use_cases.message.cor.handler_base import Handler


class AdditionHandler(Handler):
    def handle(self, input_dto: EventInputDto):

        messages: List[Message] = []
        messages.extend([TextMessage(text="test handler")])
        if self._successor is not None:
            messages.extend(self._successor.handle(input_dto))
        else:
            messages.extend([TextMessage(text="Something went wrong! >_<")])

        return messages
