from linebot.v3.messaging.models import TextMessage

from src.infrastructure.container.container import Container
from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.message.cor.handler_base import Handler


class VikiHandler(Handler):
    """
    The first handler in the chain of responsibility.

    This handler checks if the user input contains "Viki" or "viki".
    If it does, it will return an empty list.
    """

    def __init__(self, container: Container):
        super().__init__(container)

        # convert all words to lowercase and add in _mute_word_set
        self._trigger_words = {"Viki", "viki"}

    def handle(self, input_dto: EventInputDto):
        # if input_dto.user_input not include "Viki" or "viki", return, unless the source_type is "user"
        if input_dto.source_type != "user" and not any(word in input_dto.user_input for word in self._trigger_words):
            return []

        messages = []

        if self._successor is not None:
            messages.extend(self._successor.handle(input_dto))
        else:
            messages.extend([TextMessage(text="Something went wrong! >_<")])

        return messages
