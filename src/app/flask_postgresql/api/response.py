from typing import List

from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
)
from linebot.v3.messaging.api_response import ApiResponse
from linebot.v3.messaging.models.message import Message


def create_response(configuration: Configuration, reply_token: str, messages: List[Message]) -> ApiResponse:
    if not messages:
        return
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        return line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=reply_token, messages=messages)
        )
