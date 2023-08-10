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
from langchain.memory import ConversationBufferMemory
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor, load_tools
from langchain import LLMChain
# from langchain.utilities import GoogleSearchAPIWrapper

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
llm = ChatOpenAI(temperature=0.9, model='gpt-3.5-turbo')
memory = ConversationBufferMemory(memory_key='chat_history')
tools = load_tools(["serpapi"])
prefix = """盡可能回答以下問題。如果你不知道答案，就說你不知道，不要試圖亂回答。最後使用繁體中文回答。您可以使用以下工具："""
suffix = """開始!"

{chat_history}
Question: {input}
{agent_scratchpad}"""

prompt = ZeroShotAgent.create_prompt(
    tools,
    prefix=prefix,
    suffix=suffix,
    input_variables=["input", "chat_history", "agent_scratchpad"],
)
llm_chain = LLMChain(llm=llm, prompt=prompt)
agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
agent_chain = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
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
    ret = agent_chain.run(input=event.message.text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=ret)]
            )
        )

if __name__ == "__main__":
    app.run(debug=True, port=port, host='0.0.0.0')