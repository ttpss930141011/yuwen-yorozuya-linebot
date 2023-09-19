""" Flask PostgreSQL Blueprint Line Callback
"""

from flask import Blueprint, request
from src.app.flask_postgresql.event_handlers import handler

blueprint = Blueprint('main', __name__)


@blueprint.route('/', methods=["GET"])
def main_blueprint():
    """Function printing python version."""

    return 'OK'