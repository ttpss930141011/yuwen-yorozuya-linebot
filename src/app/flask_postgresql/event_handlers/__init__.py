""" LineBot handler
"""
from flask import current_app
from linebot.v3 import WebhookHandler
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FileMessageContent
)
from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    Configuration
)
from src.app.flask_postgresql.configs import Config
from src.app.flask_postgresql.event_handlers.text_event_handler import TextEventHandler
from src.app.flask_postgresql.event_handlers.file_event_handler import FileEventHandler
from src.infrastructure.repositories.agent_chain.agent_chain_in_memory_repository import AgentExecutorInMemoryRepository

handler = WebhookHandler(Config.CHANNEL_SECRET)
configuration = Configuration(access_token=Config.CHANNEL_ACCESS_TOKEN)
agent_repository = AgentExecutorInMemoryRepository()


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event: MessageEvent):
    handler = TextEventHandler(
        logger=current_app.config['logger'],
        agent_repository=agent_repository,
    )
    handler.get_event_info(event)
    result = handler.execute()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=result)]
            )
        )


@handler.add(MessageEvent, message=FileMessageContent)
def handle_file_message(event):
    handler = FileEventHandler(
        logger=current_app.config['logger'],
        agent_repository=agent_repository,
        configuration=configuration
    )
    result = handler.execute(event)


__all__ = [
    'handler'
]
