""" Module for Events Dtos
"""


from dataclasses import dataclass, asdict
from typing import Dict
# from src.domain.entities.window import Window


@dataclass
class EventInputDto:
    """ Input Dto for event call """
    window: Dict
    user_input: str

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)


@dataclass
class EventOutputDto:
    """ Output Dto for event call """
    window_id: str
    user_input: str
    response: str

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)
    
