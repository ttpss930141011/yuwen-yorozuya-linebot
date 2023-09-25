""" Defines the validator for the create window input data.
"""


from typing import Dict

from src.interactor.validations.base_input_validator import BaseInputValidator


class GetWindowInputDtoValidator(BaseInputValidator):
    """Validates the create window input data.
    :param input_data: The input data to be validated.
    """

    def __init__(self, input_data: Dict) -> None:
        super().__init__(input_data)
        self.input_data = input_data
        self.__schema = {"window_id": {"type": "string", "required": True, "empty": False}}

    def validate(self) -> None:
        """Validates the input data"""
        # Verify the input data using BaseInputValidator method
        super().verify(self.__schema)
        # This is an example of a custom validation
        # if self.input_data["window_id"] == "Window":
        #     raise ValueError("Window_id: Window is not permitted")
