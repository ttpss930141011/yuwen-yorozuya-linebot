from typing import List

from linebot.v3.messaging.models import TextMessage
from linebot.v3.messaging.models.message import Message

from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.message.cor.handler_base import Handler


class MutingHandler(Handler):

    def handle(self, input_dto: EventInputDto):
        """
        Check if the window is currently muting. If it is, return an empty list.
        """

        messages: List[Message] = []

        if input_dto.window.get("is_muting") is True:
            return messages
        elif self._successor is not None:
            messages.extend(self._successor.handle(input_dto))
        else:
            messages.extend([TextMessage(text="Something went wrong! >_<")])

        return messages
