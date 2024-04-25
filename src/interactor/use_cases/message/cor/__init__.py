from src.infrastructure.container.container import Container
from src.interactor.dtos.event_dto import EventInputDto
from src.interactor.use_cases.message.cor.addition_handler import AdditionHandler
from src.interactor.use_cases.message.cor.default_handler import DefaultHandler
from src.interactor.use_cases.message.cor.muting_handler import MutingHandler
from src.interactor.use_cases.message.cor.viki_handler import VikiHandler
from src.interactor.use_cases.message.cor.window_mutable_handler import WindowMutableHandler


class ReplyMessagesCOR:
    def __init__(self, container: Container):
        self.container = container
        self._chain = None
        self._initialize_chain()

    def _initialize_chain(self):
        # create the chain of responsibility
        viki_handler = VikiHandler(self.container)
        window_mutable_handler = WindowMutableHandler(self.container)
        muting_handler = MutingHandler(self.container)
        # addition_handler = AdditionHandler(self.container)
        default_handler = DefaultHandler(self.container)

        # set the successor of each handler
        viki_handler.set_successor(window_mutable_handler)
        window_mutable_handler.set_successor(muting_handler)
        muting_handler.set_successor(default_handler)

        # set the chain
        self._chain = viki_handler

    def handle(self, input_dto: EventInputDto):
        return self._chain.handle(input_dto)
