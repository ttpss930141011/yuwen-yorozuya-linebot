from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from langchain.schema import SystemMessage
from langchain.memory.chat_message_histories import PostgresChatMessageHistory
from config import CHATBOT_DESCRIPTION, POSTGRES_URL
from tools import toolslist


MEMORY_KEY = "chat_history"
# initialize LangChain services


def create_agent_chain(session_id: str):
    chat_memory = PostgresChatMessageHistory(
        connection_string=POSTGRES_URL,
        session_id=session_id,
    )
    memory = ConversationBufferWindowMemory(
        memory_key=MEMORY_KEY, chat_memory=chat_memory, return_messages=True, k=10)
    llm = ChatOpenAI(temperature=0, model='gpt-3.5-turbo-0613')
    system_message = SystemMessage(
        content=f"You are a powerful chat assistant,{CHATBOT_DESCRIPTION}")
    prompt = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=MEMORY_KEY)]
    )
    agent = OpenAIFunctionsAgent(llm=llm, tools=toolslist, prompt=prompt)
    agent_chain = AgentExecutor(
        agent=agent,
        tools=toolslist,
        memory=memory,
        verbose=True,
        max_iterations=3,
    )
    return agent_chain
