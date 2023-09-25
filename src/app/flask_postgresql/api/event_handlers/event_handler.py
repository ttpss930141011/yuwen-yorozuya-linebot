""" This module implements the event handler for text message events.
"""
from abc import abstractmethod
from typing import Dict
from linebot.v3.webhooks import MessageEvent

from src.app.flask_postgresql.configs import Config
from src.app.flask_postgresql.presenters.window_presenter import WindowPresenter
from src.app.flask_postgresql.interfaces.event_handler_interface import EventHandlerInterface
from src.infrastructure.repositories.window.window_postgresql_repository import WindowPostgresqlRepository
from src.interactor.use_cases.create_window import CreateWindowUseCase
from src.interactor.dtos.window_dtos import CreateWindowInputDto, GetWindowInputDto
from src.interactor.use_cases.get_window import GetWindowUseCase
from src.interactor.dtos.event_dto import EventInputDto
from src.infrastructure.repositories.agent_chain.agent_chain_in_memory_repository import AgentExecutorInMemoryRepository
from src.interactor.interfaces.logger.logger import LoggerInterface




class EventHandler(EventHandlerInterface):
    def __init__(self, logger:LoggerInterface, agent_repository: AgentExecutorInMemoryRepository):
        self.logger = logger
        self.agent_repository = agent_repository
        self.input_dto: EventInputDto

    
    def get_event_info(self, event: MessageEvent):

        if event.source.type == "user":
            window_id = event.source.user_id
        elif event.source.type == "group":
            window_id = event.source.group_id
        elif event.source.type == "room":
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
        repository = WindowPostgresqlRepository()
        presenter = WindowPresenter()
        use_case = GetWindowUseCase(
            presenter=presenter,
            repository=repository,
            logger=self.logger
        )
        get_window_input_dto = GetWindowInputDto(window_id)
        result = use_case.execute(get_window_input_dto)
        return result
    
    def _create_window_info(self, window_id: str):
        """
        Creates a new window info.

        Returns:
            The result of the create window use case execution.
        """
        repository = WindowPostgresqlRepository()
        presenter = WindowPresenter()
        create_window_input_dto = CreateWindowInputDto(
            window_id=window_id,
            is_muting=False,
            system_message=Config.CHATBOT_DESCRIPTION,
            agent_language=Config.CHATBOT_LANGUAGE,
            temperature=0
        )
        use_case = CreateWindowUseCase(
            presenter=presenter,
            repository=repository,
            logger=self.logger
        )
        result = use_case.execute(create_window_input_dto)
        return result
    
    @abstractmethod
    def execute(self):
        """
        A description of the entire function, its parameters, and its return types.
        """
            