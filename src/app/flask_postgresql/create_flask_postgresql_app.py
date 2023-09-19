""" Main Flask PostgreSQL app
"""
from flask import Flask
from src.app.flask_postgresql.blueprints.callback_blueprint import blueprint_callback
from src.app.flask_postgresql.error_handler import setup_error_handler
from src.infrastructure.databases.sql_alchemy import setup_sqlalchemy
from src.interactor.interfaces.logger.logger import LoggerInterface


def format_error_response(
        error: Exception,
        error_code: int,
        logger: LoggerInterface
):
    """ Format Error Response """
    logger.log_exception(f"500 - Internal Server Error: {str(error)}")

    response = {
        'status_code': error_code,
        'error': error.__class__.__name__,
        'message': str(error)
    }
    return response, error_code


def create_flask_postgresql_app(config, logger: LoggerInterface) -> Flask:
    """ Create Main Flask PostgreSQL app
    """
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['logger'] = logger
    app.register_blueprint(blueprint_callback)
    app = setup_sqlalchemy(app)
    app = setup_error_handler(app)

    return app
