""" Main Flask PostgreSQL app
"""
from flask import Flask

from src.app.flask_postgresql.api.blueprints import setup_blueprints
from src.app.flask_postgresql.api.container import setup_container
from src.app.flask_postgresql.api.error_handler import setup_error_handler
from src.app.flask_postgresql.api.request_context import setup_request_context
from src.infrastructure.databases.sql_alchemy import setup_sqlalchemy


def create_flask_postgresql_app(config) -> Flask:
    """Create Main Flask PostgreSQL app"""
    app = Flask(__name__)
    app.config.from_object(config)
    app = setup_container(app)
    app = setup_blueprints(app)
    app = setup_sqlalchemy(app)
    app = setup_error_handler(app)
    app = setup_request_context(app)

    return app
