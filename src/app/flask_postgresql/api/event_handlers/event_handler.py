""" This module implements the event handler for text message events.
"""
from abc import abstractmethod
from typing import Dict, cast

from linebot.v3.webhooks import MessageEvent

from src.app.flask_postgresql.configs import Config
from src.app.flask_postgresql.interfaces.event_handler_interface import EventHandlerInterface
from src.app.flask_postgresql.presenters.window_presenter import WindowPresenter
from src.infrastructure.container.container import Container
from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.dtos.window_dtos import CreateWindowInputDto, GetWindowInputDto
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.interactor.interfaces.repositories.agent_executor_repository import AgentExecutorRepositoryInterface
from src.interactor.interfaces.repositories.window_repository import WindowRepositoryInterface
from src.interactor.use_cases.window.create_window import CreateWindowUseCase
from src.interactor.use_cases.window.get_window import GetWindowUseCase


class EventHandler(EventHandlerInterface):
    def __init__(self, container: Container):
        self.container = container
        self.logger = cast(LoggerInterface, container.resolve("logger"))
        self.agent_repository = cast(AgentExecutorRepositoryInterface, container.resolve("agent_repository"))
        self.window_repository = cast(WindowRepositoryInterface, container.resolve("window_repository"))
        self.input_dto = None
        self.event = None

    def get_event_info(self, event: MessageEvent):
        """
        Retrieves the information of an event.
        """
        self.event = event
        source_type = event.source.type

        if source_type == "user":
            window_id = event.source.user_id
        elif source_type == "group":
            window_id = event.source.group_id
        elif source_type == "room":
            window_id = event.source.room_id
        else:
            raise ValueError("Invalid event source type")

        if "text" in event.message.to_json():
            user_input = event.message.text
        else:
            user_input = ""

        self.input_dto = EventInputDto(
            window=self.get_window_info(window_id=window_id),
            user_input=user_input,
            source_type=source_type,
        )

    def get_window_info(self, window_id: str) -> Dict:
        """
        Retrieves the information of a window.

        :param window_id: The id of the window.
        :return: None
        """
        window = self._get_window_info(window_id=window_id)
        if window is None:
            window = self._create_window_info(window_id=window_id)

        return window

    def _get_window_info(self, window_id: str):
        """
        Retrieves the information of a window.

        :return: The result of executing the use case.
        """
        presenter = WindowPresenter()
        use_case = GetWindowUseCase(presenter=presenter, repository=self.window_repository, logger=self.logger)
        get_window_input_dto = GetWindowInputDto(window_id)
        result = use_case.execute(get_window_input_dto)
        return result

    def _create_window_info(self, window_id: str):
        """
        Creates a new window info.

        Returns:
            The result of the create window use case execution.
        """
        presenter = WindowPresenter()
        create_window_input_dto = CreateWindowInputDto(
            window_id=window_id,
            is_muting=False,
            system_message=Config.CHATBOT_DESCRIPTION,
            agent_language=Config.CHATBOT_LANGUAGE,
            temperature=0,
        )
        use_case = CreateWindowUseCase(
            presenter=presenter, repository=self.window_repository, logger=self.logger
        )
        result = use_case.execute(create_window_input_dto)
        return result

    @abstractmethod
    def execute(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
