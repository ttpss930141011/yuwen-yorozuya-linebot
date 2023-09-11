""" Module for CreateWindow Dtos
"""


from dataclasses import dataclass, asdict
from src.domain.entities.window import Window


@dataclass
class CreateWindowInputDto:
    """ Input Dto for create window """
    window_id: str
    window: dict

    def to_dict(self):
        """ Convert data into dictionary
        """
        return asdict(self)


@dataclass
class CreateWindowOutputDto:
    """ Output Dto for create window """
    window: Window
