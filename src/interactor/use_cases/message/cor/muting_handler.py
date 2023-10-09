from typing import List

from linebot.v3.messaging.models import TextMessage
from linebot.v3.messaging.models.message import Message

from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.interfaces.repositories.agent_executor_repository import (
    AgentExecutorRepositoryInterface,
)
from src.interactor.use_cases.message.cor.handler_base import Handler


class MutingHandler(Handler):
    def handle(
        self,
        input_dto: EventInputDto,
        repository: AgentExecutorRepositoryInterface,
        response: List[Message],
    ):
        if input_dto.window.get("is_muting") is True:
            return response
        elif self._successor is not None:
            return self._successor.handle(input_dto, repository, response)
        else:
            response.append(TextMessage(text="靜悄悄的，什麼都沒有發生。"))
