""" Module for Events Dtos
"""


from dataclasses import dataclass, asdict
from typing import Dict


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
    window: Dict
    user_input: str
    response: str

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)
    
