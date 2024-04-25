from typing import List

from linebot.v3.messaging.models import TextMessage
from linebot.v3.messaging.models.message import Message

from src.infrastructure.container.container import Container
from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.message.cor.handler_base import Handler

mute_word_set = {
    "Viki mute",
    "Viki shut up",
}

unmute_word_set = {
    "Viki unmute"
}


class WindowMutableHandler(Handler):
    def __init__(self, container: Container):
        super().__init__(container)

        # convert all words to lowercase and add in _mute_word_set
        self._all_mute_words = mute_word_set.union(
            {word.lower() for word in mute_word_set}
        )

        # convert all words to lowercase and add in _unmute_word_set
        self._all_unmute_words = unmute_word_set.union(
            {word.lower() for word in unmute_word_set}
        )

    def handle(self, input_dto: EventInputDto):
        """
        Check if the user input contains any mute words. If it does, set the window's is_muting to True.
        """
        messages: List[Message] = []

        # if input_dto.user_input include mute word, set is_muting to True
        if any(word in input_dto.user_input for word in self._all_mute_words):
            window_id = input_dto.window.get("window_id")
            window = self.window_repository.get(window_id)
            if window is not None:
                window.is_muting = True
                self.window_repository.update(window)
                messages.extend([TextMessage(text="Okay, bye (´•̥̥̥ω•̥̥̥`)")])
            else:
                messages.extend([TextMessage(text="Something went wrong! >_<")])

        # if input_dto.user_input include unmute word, set is_muting to False
        elif any(word in input_dto.user_input for word in self._all_unmute_words):
            window_id = input_dto.window.get("window_id")
            window = self.window_repository.get(window_id)
            if window is not None:
                window.is_muting = False
                self.window_repository.update(window)
                messages.extend([TextMessage(text="Hello again! ヾ(*´▽‘*)ﾉ")])
            else:
                messages.extend([TextMessage(text="Something went wrong! >_<")])

        elif self._successor is not None:
            messages.extend(self._successor.handle(input_dto))
        else:
            messages.extend([TextMessage(text="Something went wrong! >_<")])

        return messages
