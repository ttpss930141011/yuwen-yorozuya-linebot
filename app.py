from flask import Flask, request, abort
from dotenv import load_dotenv
import sys 
import os
import aiohttp
from linebot.aiohttp_async_http_client import AiohttpAsyncHttpClient
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
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
    TextMessageContent
)
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory

app = Flask(__name__)

# load environment variables
load_dotenv()
channel_secret = os.getenv('CHANNEL_SECRET', None)
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN', None)
port = os.getenv("PORT", 5000)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)
session = aiohttp.ClientSession()
async_http_client = AiohttpAsyncHttpClient(session)
llm = ChatOpenAI(temperature=0.9, model='gpt-3.5-turbo')
# 透過 ConversationBufferWindowMemory 快速打造一個具有「記憶力」的聊天機器人，可以記住至少五回。
# 通常來說 5 回還蠻夠的
memory = ConversationBufferWindowMemory(k=5)
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False
)



@app.route("/")
def hello_world():
    print(os.getenv("PORT", 5000))
    return str(os.getenv("PORT", 5000))


@app.route("/callback", methods=['POST'])
def callback():
    print("callback")
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        print("handle", body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    print(event)
    # 將使用者傳來的訊息 event.message.text 當成輸入，等 LangChain 傳回結果。
    ret = conversation.predict(input=event.message.text)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=ret)]
            )
        )

if __name__ == "__main__":
    app.run(debug=False, port=port, host='0.0.0.0')