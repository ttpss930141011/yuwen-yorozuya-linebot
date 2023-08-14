from flask import Flask, request, abort
from dotenv import load_dotenv
import sys 
import os
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
    TextMessageContent,
    FileMessageContent,
)
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from tools.stock import CurrentStockPriceTool, StockPerformanceTool
from langchain.prompts import MessagesPlaceholder
from langchain.prompts import ChatPromptTemplate

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

# initialize Line services
configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

# initialize LangChain services
search = SerpAPIWrapper()
tools = [
    Tool(
        name = "Search",
        func=search.run,
        description="useful for when you need to answer questions about current events. You should ask targeted questions"
    ),
    CurrentStockPriceTool(), 
    StockPerformanceTool()
]
agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")],
}
# message_history = RedisChatMessageHistory(url='redis://localhost:6379/0', ttl=600, session_id='my-session')
# memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=message_history)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm=ChatOpenAI(temperature=0, model='gpt-3.5-turbo-0613')
agent_chain = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.OPENAI_FUNCTIONS, 
    verbose=True, 
    agent_kwargs=agent_kwargs,
    memory=memory,
    max_iterations=2,
    early_stopping_method="generate",
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
        # print("handle", body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    print('event', event)
    ret = agent_chain.run(input=f'{event.message.text}, 請用繁體中文回答。')
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
if __name__ == "__main__":
    app.run(debug=True, port=port, host='0.0.0.0')