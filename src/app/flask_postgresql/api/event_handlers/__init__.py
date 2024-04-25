""" LineBot handler
"""
from flask import current_app
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from src.app.flask_postgresql.api.event_handlers.file_event_handler import FileEventHandler
from src.app.flask_postgresql.api.event_handlers.text_event_handler import TextEventHandler
from src.app.flask_postgresql.api.response import create_response
from src.app.flask_postgresql.configs import Config
from src.infrastructure.container.container import Container

handler = WebhookHandler(Config.CHANNEL_SECRET)
configuration = Configuration(access_token=Config.CHANNEL_ACCESS_TOKEN)


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent):
    container: Container = current_app.config["container"]
    text_handler = TextEventHandler(container)
    text_handler.get_event_info(event)
    result = text_handler.execute()

    return create_response(configuration, event.reply_token, result)


# @handler.add(MessageEvent, message=FileMessageContent)
# def handle_file_message(event: MessageEvent):
#     file_handler = FileEventHandler(
#         logger=current_app.config["logger"],
#         agent_repository=agent_repository,
#         configuration=configuration,
#     )
#     result = file_handler.execute(event)
#
#     return create_response(configuration, event.reply_token, result)


__all__ = ["handler"]
