""" This module implements the event handler for text message events.
"""

from src.app.flask_postgresql.api.event_handlers.event_handler import EventHandler
from src.app.flask_postgresql.presenters.message_reply_presenter import EventPresenter
from src.infrastructure.container.container import Container
from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.message.create_message_reply import CreateMessageReplyUseCase


class TextEventHandler(EventHandler):
    def __init__(self, container: Container):
        super().__init__(container)
        self.input_dto: EventInputDto

    def execute(self):
        presenter = EventPresenter()
        use_case = CreateMessageReplyUseCase(presenter=presenter, container=self.container)
        result = use_case.execute(self.input_dto)
        return result
