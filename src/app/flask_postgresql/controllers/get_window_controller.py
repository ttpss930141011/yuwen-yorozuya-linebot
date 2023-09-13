"""Get Window Controller Module"""


from typing import Dict
from src.interactor.use_cases.get_window import GetWindowUseCase
from infrastructure.repositories.window.window_postgresql_repository import WindowPostgresqlRepository
from src.interactor.dtos.window_dtos import GetWindowInputDto
from src.app.flask_postgresql.interfaces.flask_postgresql_controller_interface\
    import FlaskPostgresqlControllerInterface
from src.interactor.interfaces.logger.logger import LoggerInterface
from app.flask_postgresql.presenters.window_presenter import WindowPresenter


class GetWindowController(FlaskPostgresqlControllerInterface):
    """ Get Window Controller Class
    """

    def __init__(self, logger: LoggerInterface):
        self.logger = logger
        self.input_dto: GetWindowInputDto

    def get_window_info(self, query_params) -> None:
        if "window_id" in query_params:
            window_id = query_params["window_id"]
        else:
            raise ValueError("Missing Window Id")
        self.input_dto = GetWindowInputDto(window_id)

    def execute(self) -> Dict:
        """ Execute the get window controller
        :returns: Window
        """
        repository = WindowPostgresqlRepository()
        presenter = WindowPresenter()
        use_case = GetWindowUseCase(presenter, repository, self.logger)
        result = use_case.execute(self.input_dto)
        return result
