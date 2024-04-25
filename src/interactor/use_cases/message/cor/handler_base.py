from abc import ABC, abstractmethod
from typing import List, cast

from linebot.v3.messaging.models.message import Message

from src.infrastructure.container.container import Container
from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.interactor.interfaces.repositories.agent_executor_repository import (
    AgentExecutorRepositoryInterface,
)
from src.interactor.interfaces.repositories.window_repository import WindowRepositoryInterface


class Handler(ABC):
    def __init__(self, container: Container = None):
        self._successor = None
        self.container = container
        self.logger = cast(LoggerInterface, container.resolve("logger"))
        self.agent_repository = cast(AgentExecutorRepositoryInterface, container.resolve("agent_repository"))
        self.window_repository = cast(WindowRepositoryInterface, container.resolve("window_repository"))

    def set_successor(self, successor: "Handler"):
        self._successor = successor

    @abstractmethod
    def handle(self, input_dto: EventInputDto, ) -> List[Message]:
        pass
