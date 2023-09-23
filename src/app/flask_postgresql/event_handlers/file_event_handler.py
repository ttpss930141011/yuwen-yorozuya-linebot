""" This module implements the event handler for file message events.
"""
from src.app.flask_postgresql.interfaces.event_handler_interface import EventHandlerInterface
from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)


class FileEventHandler(EventHandlerInterface):
    def __init__(self, logger, agent_repository, configuration):
        self.logger = logger
        self.agent_repository = agent_repository
        self.configuration = configuration


    def execute(self, event):
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="我收到你的檔案了")]
                )
            )