""" Flask PostgreSQL Blueprint Line Callback
"""

from flask import Blueprint, request
from src.app.flask_postgresql.event_handlers import handler

blueprint = Blueprint('callback', __name__)


@blueprint.route('/callback', methods=["POST"])
def callback_blueprint():
    """Function printing python version."""

    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return 'OK'