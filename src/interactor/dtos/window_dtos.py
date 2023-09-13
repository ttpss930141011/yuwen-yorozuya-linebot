""" Module for CreateWindow Dtos
"""


from dataclasses import dataclass, asdict
from src.domain.entities.window import Window


@dataclass
class CreateWindowInputDto:
    """ Input Dto for create window """
    window_id: str
    is_muting: bool
    system_message: str
    agent_language:str
    temperature: float

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)

@dataclass
class GetWindowInputDto:
    """ Input Dto for get window """
    window_id: str

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)

@dataclass
class WindowOutputDto:
    """ Output Dto for create window """
    window: Window
