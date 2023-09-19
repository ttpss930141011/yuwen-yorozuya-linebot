""" This module implements the event handler for text message events.
"""

from src.app.flask_postgresql.interfaces.line_event_handler_interface import LineEventHandlerInterface
from src.app.flask_postgresql.controllers.text_message_content_controller import TextMessageContentController

from linebot.v3.webhooks import MessageEvent
from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

class TextEventHandler(LineEventHandlerInterface):
    def __init__(self, logger, agent_repository, configuration):
        self.logger = logger
        self.agent_repository = agent_repository
        self.configuration = configuration


    def execute(self, event: MessageEvent):
        controller = TextMessageContentController( self.logger, self.agent_repository)
        controller.get_window_id(event)
        controller.get_window_info()
        ret = controller.execute(event)

        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=ret)]
                )
            )

