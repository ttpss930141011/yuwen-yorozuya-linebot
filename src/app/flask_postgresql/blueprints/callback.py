""" Flask PostgreSQL Blueprint Line Callback
"""

from flask import Blueprint, request, abort, current_app
from src.interactor.interfaces.logger.logger import LoggerInterface
from src.app.flask_postgresql.event_handlers import handler
from linebot.v3.exceptions import InvalidSignatureError
blueprint = Blueprint('callback', __name__)


@blueprint.route('/callback', methods=["POST"])
def callback_blueprint():
    """Function printing python version."""
    logger: LoggerInterface = current_app.config['logger']
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.log_exception(
            "Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'
