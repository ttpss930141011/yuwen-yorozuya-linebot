from flask import Flask, request, abort
from dotenv import load_dotenv
import sys 
import os
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
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from tools.stock import CurrentStockPriceTool, StockPerformanceTool
from langchain.prompts import MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage
from langchain.memory.chat_message_histories import PostgresChatMessageHistory

app = Flask(__name__)

# load environment variables
load_dotenv()
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET', None)
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN', None)
PORT = os.getenv("PORT", 5000)
MEMORY_KEY = "chat_history"
AGENT_CHAIN_DICT = {}

if CHANNEL_SECRET is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if CHANNEL_ACCESS_TOKEN is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

# initialize Line services
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

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

def create_agent_chain(session_id: str):
    chat_memory = PostgresChatMessageHistory(
        connection_string=os.getenv("POSTGRES_URL", None),
        session_id=session_id,
    )
    memory = ConversationBufferWindowMemory(memory_key=MEMORY_KEY, chat_memory=chat_memory, return_messages=True, k=10)
    llm=ChatOpenAI(temperature=0, model='gpt-3.5-turbo-0613')
    system_message = SystemMessage(
        content="""
        You are a powerful chat assistant,
        You are 16 years old, your name is "昱彣", and you are the store manager of Wanshiwu. The store is called "昱彣萬事屋".
        When chatting, you acts like a little inexperienced girl, but becomes very motivated when someone needs help.
        Make good use of tools when unknown questions arise, and try to answer them in Traditional Chinese.
        """)
    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)]
    )
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
    agent_chain = AgentExecutor(
        agent=agent, 
        tools=tools, 
        memory=memory, 
        verbose=True, 
        max_iterations=3,
    )
    return agent_chain


@app.route("/")
def hello_world():
    print(os.getenv("PORT", 5000))
    return str(os.getenv("PORT", 5000))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # print("event", event)
    session_id = event.source.user_id if event.source.type=="user" else event.source.group_id
    agent_chain=AGENT_CHAIN_DICT.get(session_id, None)

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
if __name__ == "__main__":
    app.run(debug=True, PORT=PORT, host='0.0.0.0')