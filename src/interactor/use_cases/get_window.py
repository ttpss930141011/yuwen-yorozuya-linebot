""" This module is responsible for creating a new window.
"""


from typing import Dict
from src.interactor.interfaces.presenters.window_presenter import WindowPresenterInterface
from src.interactor.dtos.window_dtos import GetWindowInputDto, WindowOutputDto
from src.interactor.interfaces.repositories.window_repository import WindowRepositoryInterface
from src.interactor.validations.get_window_validator import GetWindowInputDtoValidator
from src.interactor.interfaces.logger.logger import LoggerInterface


class GetWindowUseCase():
    """ This class is responsible for creating a new window.
    """

    def __init__(
            self,
            presenter: WindowPresenterInterface,
            repository: WindowRepositoryInterface,
            logger: LoggerInterface,
    ):
        self.presenter = presenter
        self.repository = repository
        self.logger = logger

    def execute(self, input_dto: GetWindowInputDto) -> Dict:
        """ This method is responsible for creating a new window.
        :param input_dto: The input data transfer object.
        :type input_dto: GetWindowInputDto
        :return: Dict
        """
        validator = GetWindowInputDtoValidator(input_dto.to_dict())
        validator.validate()
        window = self.repository.get(window_id=input_dto.window_id)
        if window is None:
            self.logger.log_exception("Window get failed")
            return None
        output_dto = WindowOutputDto(window)
        presenter_response = self.presenter.present(output_dto)
        self.logger.log_info("Window get successfully")
        return presenter_response
