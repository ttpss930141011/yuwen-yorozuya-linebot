""" Module for AgentExecutorInMemoryRepository
"""

from typing import Dict

from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.prompts import MessagesPlaceholder
from langchain.schema import BaseChatMessageHistory, SystemMessage

from src.app.flask_postgresql.configs import Config
from src.infrastructure.repositories.message_history.custom_postgres_message_history import (
    CustomPostgresMessageHistory,
)
from src.infrastructure.tools import tools
from src.interactor.interfaces.repositories.agent_executor_repository import (
    AgentExecutorRepositoryInterface,
)


class AgentExecutorInMemoryRepository(AgentExecutorRepositoryInterface):
    """InMemory Repository for AgentExecutor"""

    def __init__(self) -> None:
        self._data: Dict[str, AgentExecutor] = {}

    def _create_chat_memory(self, window_id: str) -> BaseChatMessageHistory:
        """
        Create a chat memory for the given window ID.

        Args:
            window_id (str): The ID of the window.

        Returns:
            BaseChatMessageHistory: An instance of the BaseChatMessageHistory class.
        """
        return CustomPostgresMessageHistory(window_id=window_id)

    def _create_memory(
        self, memory_key: str, chat_memory: BaseChatMessageHistory
    ) -> BaseChatMemory:
        """
        Creates a new chat memory with the given memory key and chat memory.

        Parameters:
            memory_key (str): The key for the new memory.
            chat_memory (BaseChatMessageHistory): The chat memory to be used.

        Returns:
            BaseChatMemory: The newly created chat memory.
        """
        return ConversationBufferWindowMemory(
            memory_key=memory_key, chat_memory=chat_memory, return_messages=True, k=10
        )

    def _create_agent(
        self,
        system_message: str,
        agent_language: str,
        temperature: float,
        memory_key: str,
        tools: list,
    ) -> OpenAIFunctionsAgent:
        """
        Creates an instance of the OpenAIFunctionsAgent class.

        Args:
            system_message (str): The system message to be used when generating responses.
            agent_language (str): The language in which the agent will try to answer.
            temperature (float): The temperature parameter for controlling the randomness of the generated responses.
            memory_key (str): The key to be used for storing the agent's memory.

        Returns:
            OpenAIFunctionsAgent: An instance of the OpenAIFunctionsAgent class.
        """
        llm = ChatOpenAI(temperature=temperature, model="gpt-3.5-turbo-0613")
        system_message = SystemMessage(content=system_message)
        system_language = SystemMessage(content=f"Normally, try to answer in {agent_language}")
        prompt = OpenAIFunctionsAgent.create_prompt(
            system_message=system_message,
            extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key), system_language],
        )
        return OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)

    def _create_agent_executor(
        self, agent: OpenAIFunctionsAgent, memory: BaseChatMemory, tools: list
    ) -> AgentExecutor:
        """
        Creates an agent executor using the provided agent, memory, and other optional arguments.

        Parameters:
            agent (OpenAIFunctionsAgent): The agent to be used for execution.
            memory (BaseChatMemory): The memory to be used for storing conversation history.

        Returns:
            AgentExecutor: The created agent executor.

        """
        return AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            verbose=True,
            max_iterations=3,
        )

    def get(self, window_id: str) -> AgentExecutor:
        """Get AgentExecutor by id

        :param window_id: str
        :return: AgentExecutor
        """
        if window_id not in self._data:
            return None
        return self._data[window_id]

    def create(
        self,
        window_id: str,
        agent_language: str = Config.CHATBOT_LANGUAGE,
        system_message: str = Config.CHATBOT_DESCRIPTION,
        temperature: float = 0,
        memory_key: str = Config.MEMORY_KEY,
    ) -> AgentExecutor:
        """
        Creates a new AgentExecutor object and stores it in the _data dictionary under the specified window_id.

        Parameters:
            window_id (str): The ID of the window.

            agent_language (str, optional): The language of the agent. Defaults to Config.CHATBOT_LANGUAGE.

            system_message (str, optional): The system message for the agent. Defaults to Config.CHATBOT_DESCRIPTION.

            temperature (float, optional): The temperature parameter for the agent. Defaults to 0.

            memory_key (str, optional): The key for storing the agent's memory. Defaults to Config.MEMORY_KEY.

        Returns:
            AgentExecutor: The newly created AgentExecutor object.

        """

        chat_memory = self._create_chat_memory(window_id=window_id)
        memory = self._create_memory(memory_key=memory_key, chat_memory=chat_memory)
        agent = self._create_agent(
            system_message=system_message,
            agent_language=agent_language,
            temperature=temperature,
            memory_key=memory_key,
            tools=tools,
        )
        agent_executor = self._create_agent_executor(agent=agent, memory=memory, tools=tools)

        self._data[window_id] = agent_executor
        return self._data[window_id]

    def update(
        self, window_id: str, agent_language: str, system_message: str, temperature: float
    ) -> AgentExecutor:
        pass
