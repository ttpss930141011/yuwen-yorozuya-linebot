""" This module has definition of the Window entity
"""
from dataclasses import dataclass, asdict


@dataclass
class Window:
    """ Definition of the Window entity
    """
    window_id: str
    is_muting: bool = False
    temperature: float = 0
    agent_language:str = "繁體中文"
    system_message: str = """
        You are 18 years old girl called '昱彣',
        and you are the store manager of All Things shop called '昱彣萬事屋'.
        You are positive when someone needs help.
        Make good use of tools when unknown questions arise."""

    def __post_init__(self):
        if not isinstance(self.window_id, str):
            raise TypeError('window_id should be of type str')
        if not isinstance(self.is_muting, bool):
            raise TypeError('is_muting should be of type bool')
        if not isinstance(self.system_message, str):
            raise TypeError('system_message should be of type str')
        if not isinstance(self.agent_language, str):
            raise TypeError('agent_language should be of type str')
        if not isinstance(self.temperature, float):
            raise TypeError('temperature should be of type float')

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
