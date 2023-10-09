""" Module for Events Dtos
"""


from dataclasses import asdict, dataclass
from typing import Dict, List

from linebot.v3.messaging.models.message import Message


@dataclass
class EventInputDto:
    """Input Dto for event call"""

    window: Dict
    user_input: str

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)


@dataclass
class EventOutputDto:
    """Output Dto for event call"""

    window: Dict
    user_input: str
    response: List[Message]

    def to_dict(self):
        """Convert data into dictionary"""
        return asdict(self)
