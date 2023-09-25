""" Flask PostgreSQL Blueprint Line Callback
"""

from flask import Blueprint

blueprint = Blueprint('main', __name__)


@blueprint.route('/', methods=["GET"])
def main_blueprint():
    """Function printing python version."""

    return 'OK'