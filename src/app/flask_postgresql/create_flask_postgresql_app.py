""" Main Flask PostgreSQL app
"""
from flask import Flask
from src.app.flask_postgresql.blueprints import setup_blueprints
from src.app.flask_postgresql.error_handler import setup_error_handler
from src.infrastructure.databases.sql_alchemy import setup_sqlalchemy
from src.interactor.interfaces.logger.logger import LoggerInterface

def create_flask_postgresql_app(config, logger: LoggerInterface) -> Flask:
    """ Create Main Flask PostgreSQL app
    """
    app = Flask(__name__)
    app.config.from_object(config)
    app.config['logger'] = logger
    app = setup_blueprints(app)
    app = setup_sqlalchemy(app)
    app = setup_error_handler(app)

    return app
