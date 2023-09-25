from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    Configuration
)
from linebot.v3.messaging.api_response import ApiResponse


def create_response(configuration:Configuration, reply_token:str, *results) -> ApiResponse:

    messages = [TextMessage(text=result) for result in results]

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        return line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=messages
            )
        )
