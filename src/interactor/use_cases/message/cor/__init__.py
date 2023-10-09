from typing import List

from linebot.v3.messaging.models.message import Message

from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.interfaces.repositories.agent_executor_repository import (
    AgentExecutorRepositoryInterface,
)
from src.interactor.use_cases.message.cor.addition_handler import AdditionHandler
from src.interactor.use_cases.message.cor.default_handler import DefaultHandler
from src.interactor.use_cases.message.cor.muting_handler import MutingHandler


class ReplyMessagesCOR:
    def __init__(self):
        self._chain = MutingHandler(AdditionHandler(DefaultHandler()))

    def handle(self, input_dto: EventInputDto, repository: AgentExecutorRepositoryInterface):
        response: List[Message] = []
        self._chain.handle(input_dto, repository, response)
        return response
