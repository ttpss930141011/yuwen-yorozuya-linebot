""" This module implements the event handler for text message events.
"""

from src.app.flask_postgresql.presenters.message_reply_presenter import EventPresenter
from src.app.flask_postgresql.api.event_handlers.event_handler import EventHandler
from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.create_text_message_reply import CreateTextMessageReplyUseCase

class TextEventHandler(EventHandler):
    def __init__(self, logger, agent_repository):
        self.logger = logger
        self.agent_repository = agent_repository
        self.input_dto: EventInputDto

    def execute(self):
        presenter=EventPresenter()
        use_case = CreateTextMessageReplyUseCase(
            presenter=presenter,
            repository=self.agent_repository,
            logger=self.logger,
        )
        result = use_case.execute(self.input_dto)
        return result
        