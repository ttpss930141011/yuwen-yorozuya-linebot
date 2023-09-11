""" This module has definition of the Message entity
"""
from dataclasses import dataclass, asdict

@dataclass
class Message:
    """ Definition of the Message entity
    """
    window_id: str
    message: dict

    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)

    def __repr__(self):
        return f'<Message {self.window_id}>'

    def __str__(self):
        return f'<Message {self.window_id}>'
