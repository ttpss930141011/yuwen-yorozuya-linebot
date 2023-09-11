from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    FileMessageContent,
)
from src.agent_chain import create_agent_chain
from src.config import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET


handler = WebhookHandler(CHANNEL_SECRET)
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
AGENT_CHAIN_DICT = {}


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # print("event", event)
    session_id = event.source.user_id if event.source.type == "user" else event.source.group_id
    agent_chain = AGENT_CHAIN_DICT.get(session_id, None)

    if agent_chain is None:
        agent_chain = create_agent_chain(session_id=session_id)
        AGENT_CHAIN_DICT[session_id] = agent_chain

    ret = agent_chain.run(input=event.message.text)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=ret)]
            )
        )


@handler.add(MessageEvent, message=FileMessageContent)
def handle_message(event):
    print('event', event)
    # ret = agent_chain.run(input=f'{event.message.text}, 請用繁體中文回答。')
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="我收到你的檔案了")]
            )
        )
