"""This module implements the controller for text message content.
"""


from typing import Dict

from src.app.flask_postgresql.presenters.window_presenter import WindowPresenter
from src.app.flask_postgresql.interfaces.flask_postgresql_controller_interface import FlaskPostgresqlControllerInterface
from src.interactor.interfaces.repositories.agent_executor_repository import AgentExecutorRepositoryInterface
from src.interactor.use_cases.create_text_message_reply import CreateTextMessageReplyUseCase
from src.interactor.interfaces.logger.logger import LoggerInterface


class TextMessageContentController(FlaskPostgresqlControllerInterface):
    """ Text Message Content Controller Class
    """

    def __init__(self, logger: LoggerInterface, repository: AgentExecutorRepositoryInterface):
        self.logger = logger
        self.repository = repository
        self.window_id: str
        self.window: Dict



    def execute(self, user_input :str) -> Dict:
        if self.window.get("is_muting"):
            return "靜悄悄的，什麼都沒有發生。"
        
        use_case = CreateTextMessageReplyUseCase(
            repository=self.repository,
            logger=self.logger,
            window=self.window
        )
        result = use_case.execute(user_input)
        return result
    
