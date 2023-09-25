""" LineBot handler
"""
from flask import current_app
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration
from linebot.v3.webhooks import FileMessageContent, MessageEvent, TextMessageContent

from src.app.flask_postgresql.api.event_handlers.file_event_handler import FileEventHandler
from src.app.flask_postgresql.api.event_handlers.text_event_handler import TextEventHandler
from src.app.flask_postgresql.api.response import create_response
from src.app.flask_postgresql.configs import Config
from src.infrastructure.repositories.agent_chain.agent_chain_in_memory_repository import (
    AgentExecutorInMemoryRepository,
)

handler = WebhookHandler(Config.CHANNEL_SECRET)
configuration = Configuration(access_token=Config.CHANNEL_ACCESS_TOKEN)
agent_repository = AgentExecutorInMemoryRepository()


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent):
    handler = TextEventHandler(
        logger=current_app.config["logger"],
        agent_repository=agent_repository,
    )
    handler.get_event_info(event)
    result = handler.execute()

    return create_response(configuration, event.reply_token, result)


@handler.add(MessageEvent, message=FileMessageContent)
def handle_file_message(event: MessageEvent):
    handler = FileEventHandler(
        logger=current_app.config["logger"],
        agent_repository=agent_repository,
        configuration=configuration,
    )
    result = handler.execute(event)

    return create_response(configuration, event.reply_token, result)


__all__ = ["handler"]
