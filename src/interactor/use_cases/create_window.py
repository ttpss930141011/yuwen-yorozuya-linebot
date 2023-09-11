""" This module is responsible for creating a new window.
"""


from typing import Dict
from src.interactor.dtos.create_window_dtos import CreateWindowInputDto, CreateWindowOutputDto
from src.interactor.interfaces.repositories.window_repository \
    import WindowRepositoryInterface
from src.interactor.validations.create_window_validator \
    import CreateWindowInputDtoValidator
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.interactor.errors.error_classes import ItemNotCreatedException


class CreateWindowUseCase():
    """ This class is responsible for creating a new window.
    """

    def __init__(
            self,
            repository: WindowRepositoryInterface,
            logger: LoggerInterface
    ):
        self.presenter = presenter
        self.repository = repository
        self.logger = logger

    def execute(
            self,
            input_dto: CreateWindowInputDto
    ) -> Dict:
        """ This method is responsible for creating a new window.
        :param input_dto: The input data transfer object.
        :type input_dto: CreateWindowInputDto
        :return: Dict
        """

        validator = CreateWindowInputDtoValidator(input_dto.to_dict())
        validator.validate()
        window = self.repository.create(
            input_dto.name,
            input_dto.description
        )
        if window is None:
            self.logger.log_exception("Window creation failed")
            raise ItemNotCreatedException(input_dto.name, "Window")
        output_dto = CreateWindowOutputDto(window)
        presenter_response = self.presenter.present(output_dto)
        self.logger.log_info("Window created successfully")
        return presenter_response
