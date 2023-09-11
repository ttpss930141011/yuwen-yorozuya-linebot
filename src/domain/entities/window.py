""" This module has definition of the Window entity
"""
from dataclasses import dataclass, asdict

@dataclass
class Window:
    """ Definition of the Window entity
    """
    window_id: str
    is_muting: bool=False

    @classmethod
    def from_dict(cls, data):
        """ Convert data from a dictionary
        """
        return cls(**data)

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)

    def set_muting(self, is_muting):
        """ Set muting status
        """
        self.is_muting = is_muting

    def __repr__(self):
        return f'<Window {self.window_id}>'

    def __str__(self):
        return f'<Window {self.window_id}>'
    