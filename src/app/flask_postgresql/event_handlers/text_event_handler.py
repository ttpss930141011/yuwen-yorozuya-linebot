""" This module implements the event handler for text message events.
"""
from src.app.flask_postgresql.configs import Config
from src.app.flask_postgresql.presenters.window_presenter import WindowPresenter
from src.app.flask_postgresql.interfaces.event_handler_interface import EventHandlerInterface
from src.app.flask_postgresql.controllers.text_message_content_controller import TextMessageContentController
from src.infrastructure.repositories.window.window_postgresql_repository import WindowPostgresqlRepository
from src.interactor.use_cases.create_window import CreateWindowUseCase
from src.interactor.dtos.window_dtos import CreateWindowInputDto, GetWindowInputDto
from src.interactor.use_cases.get_window import GetWindowUseCase
from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.create_text_message_reply import CreateTextMessageReplyUseCase


from linebot.v3.webhooks import MessageEvent


class TextEventHandler(EventHandlerInterface):
    def __init__(self, logger, agent_repository):
        self.logger = logger
        self.agent_repository = agent_repository
        self.window_id: str
        self.input_dto: EventInputDto

    def get_event_info(self, event: MessageEvent):
        
        if event.source.type == "user":
            self.window_id = event.source.user_id
        elif event.source.type == "group":
            self.window_id = event.source.group_id
        elif event.source.type == "room":
            self.window_id = event.source.room_id
        else:
            raise ValueError("Invalid event source type")
        
        if "text" in event.message:
            user_input = event.message.text
        
        self.input_dto = EventInputDto(
            user_input=user_input
        )

    def get_window_info(self, window_id: str) -> None:
        """
        Retrieves the information of a window.

        :param window_id: The id of the window.
        :return: None
        """
        window = self._get_window_info(window_id=window_id)
        if window is None:
            window = self._create_window_info(window_id=window_id)

        self.input_dto.window = window
   

    def execute(self):

        if self.input_dto.window.get("is_muting"):
            return "靜悄悄的，什麼都沒有發生。"

        use_case = CreateTextMessageReplyUseCase(
            repository=self.agent_repository,
            logger=self.logger,
        )
        result = use_case.execute(self.input_dto)
        return result
        

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