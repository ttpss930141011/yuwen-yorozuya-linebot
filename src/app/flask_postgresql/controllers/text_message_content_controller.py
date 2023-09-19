"""This module implements the controller for text message content.
"""


from typing import Dict
from linebot.v3.webhooks import MessageEvent

from src.app.flask_postgresql.configs import Config
from src.app.flask_postgresql.presenters.window_presenter import WindowPresenter
from src.app.flask_postgresql.presenters.window_presenter import WindowPresenter
from src.app.flask_postgresql.interfaces.flask_postgresql_controller_interface import FlaskPostgresqlControllerInterface
from src.interactor.interfaces.repositories.agent_executor_repository import AgentExecutorRepositoryInterface
from src.interactor.use_cases.get_window import GetWindowUseCase
from src.interactor.use_cases.create_text_message_reply import CreateTextMessageReplyUseCase
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.interactor.use_cases.create_window import CreateWindowUseCase
from src.interactor.dtos.window_dtos import CreateWindowInputDto, GetWindowInputDto
from src.infrastructure.repositories.window.window_postgresql_repository import WindowPostgresqlRepository
from src.infrastructure.repositories.window.window_postgresql_repository import WindowPostgresqlRepository


class TextMessageContentController(FlaskPostgresqlControllerInterface):
    """ Text Message Content Controller Class
    """

    def __init__(self, logger: LoggerInterface, repository: AgentExecutorRepositoryInterface):
        self.logger = logger
        self.repository = repository
        self.window_id: str
        self.window: Dict

    def get_window_id(self, event: MessageEvent) -> None:
        """
        Set the window_id attribute based on the type of event source.

        Args:
            event (MessageEvent): The event object containing the source information.

        Returns:
            None
        """
        if event.source.type == "user":
            self.window_id = event.source.user_id
        elif event.source.type == "group":
            self.window_id = event.source.group_id
        else:
            self.window_id = event.source.room_id

    def get_window_info(self) -> None:
        """
        Get the window information.

        This function retrieves the window information by calling the
        private method `_get_window_info()`. If the window information is
        `None`, it creates a new window information by calling the private
        method `_create_window_info()`.

        Parameters:
            self: The instance of the class.

        Returns:
            None.
        """

        self.window = self._get_window_info()
        if self.window is None:
            self.window = self._create_window_info()

    def _get_window_info(self):
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
        get_window_input_dto = GetWindowInputDto(self.window_id)
        result = use_case.execute(get_window_input_dto)
        return result

    def _create_window_info(self):
        """
        Creates a new window info.

        Returns:
            The result of the create window use case execution.
        """
        repository = WindowPostgresqlRepository()
        presenter = WindowPresenter()
        create_window_input_dto = CreateWindowInputDto(
            window_id=self.window_id,
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

    def execute(self, event: MessageEvent) -> Dict:
        if self.window.get("is_muting"):
            return
        
        use_case = CreateTextMessageReplyUseCase(
            repository=self.repository,
            logger=self.logger,
            window=self.window
        )
        result = use_case.execute(event)
        return result
