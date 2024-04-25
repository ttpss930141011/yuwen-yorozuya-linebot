""" Flask PostgreSQL Blueprint Line Callback
"""

from flask import Blueprint, abort, current_app, request
from linebot.v3.exceptions import InvalidSignatureError

from src.app.flask_postgresql.api.event_handlers import handler
from src.interactor.interfaces.logger.logger import LoggerInterface

blueprint = Blueprint("callback", __name__)


@blueprint.route("/callback", methods=["POST"])
def callback_blueprint():
    """Function printing python version."""
    logger: LoggerInterface = current_app.config["container"].resolve("logger")
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logger.log_exception(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)
    return "OK"
