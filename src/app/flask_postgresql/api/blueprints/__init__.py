from flask import Flask

from .callback import blueprint as callback_blueprint
from .main import blueprint as main_blueprint


def setup_blueprints(app: Flask) -> Flask:
    """
    Register the necessary blueprints for the Flask app.

    Parameters:
        app (Flask): The Flask app instance.

    Returns:
        None: The Flask app instance with the blueprints registered.
    """
    app.register_blueprint(callback_blueprint)
    app.register_blueprint(main_blueprint)
    return app


__all__ = ["setup_blueprints"]
