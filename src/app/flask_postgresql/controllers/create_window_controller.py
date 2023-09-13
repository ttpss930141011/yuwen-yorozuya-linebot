"""Create Window Controller Module"""

from typing import Dict

from src.interactor.use_cases.create_window import CreateWindowUseCase
from src.infrastructure.repositories.window.window_postgresql_repository import WindowPostgresqlRepository
from src.interactor.dtos.window_dtos import CreateWindowInputDto
from src.app.flask_postgresql.interfaces.flask_postgresql_controller_interface import FlaskPostgresqlControllerInterface
from src.interactor.interfaces.logger.logger import LoggerInterface
from app.flask_postgresql.presenters.window_presenter import WindowPresenter


class CreateWindowController(FlaskPostgresqlControllerInterface):
    """ Create Window Controller Class
    """

    def __init__(self, logger: LoggerInterface):
        self.logger = logger
        self.input_dto: CreateWindowInputDto

    def get_window_info(self, json_input) -> None:
        """ Get Window Info
        :param json_input: Input data
        :raises: ValueError if window window_id, is_muting, system_message, agent_language or temperature are missing.
        """
        if "window_id" in json_input:
            window_id = json_input["window_id"]
        else:
            raise ValueError("Missing Window Id")
        if "is_muting" in json_input:
            is_muting = json_input["is_muting"]
        else:
            raise ValueError("Missing Window is_muting")
        if "system_message" in json_input:
            system_message = json_input["system_message"]
        else:
            raise ValueError("Missing Window system_message")
        if "agent_language" in json_input:
            agent_language = json_input["agent_language"]
        else:
            raise ValueError("Missing Window agent_language")
        if "temperature" in json_input:
            temperature = json_input["temperature"]
        else:
            raise ValueError("Missing Window temperature")
        self.input_dto = CreateWindowInputDto(
            window_id,
            is_muting,
            system_message,
            agent_language,
            temperature
        )

    def execute(self) -> Dict:
        """ Execute the create window controller
        :returns: Window created
        """
        repository = WindowPostgresqlRepository()
        presenter = WindowPresenter()
        use_case = CreateWindowUseCase(presenter, repository, self.logger)
        result = use_case.execute(self.input_dto)
        return result
