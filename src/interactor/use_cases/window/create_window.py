""" This module is responsible for creating a new window.
"""


from typing import Dict

from src.interactor.dtos.window_dtos import CreateWindowInputDto, WindowOutputDto
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.interactor.interfaces.presenters.window_presenter import WindowPresenterInterface
from src.interactor.interfaces.repositories.window_repository import WindowRepositoryInterface
from src.interactor.validations.create_window_validator import CreateWindowInputDtoValidator


class CreateWindowUseCase:
    """This class is responsible for creating a new window."""

    def __init__(
        self,
        presenter: WindowPresenterInterface,
        repository: WindowRepositoryInterface,
        logger: LoggerInterface,
    ):
        self.presenter = presenter
        self.repository = repository
        self.logger = logger

    def execute(self, input_dto: CreateWindowInputDto) -> Dict:
        """This method is responsible for creating a new window.
        :param input_dto: The input data transfer object.
        :type input_dto: CreateWindowInputDto
        :return: Dict
        """
        validator = CreateWindowInputDtoValidator(input_dto.to_dict())
        validator.validate()
        window = self.repository.create(
            window_id=input_dto.window_id,
            is_muting=input_dto.is_muting,
            agent_language=input_dto.agent_language,
            system_message=input_dto.system_message,
            temperature=input_dto.temperature,
        )
        if window is None:
            self.logger.log_exception("Window creation failed")
            raise ValueError("Window creation failed")
        output_dto = WindowOutputDto(window)
        presenter_response = self.presenter.present(output_dto)
        self.logger.log_info("Window created successfully")
        return presenter_response
