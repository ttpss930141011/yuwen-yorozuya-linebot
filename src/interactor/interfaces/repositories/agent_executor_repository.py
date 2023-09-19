""" This module contains the interface for the WindowRepository
"""


from abc import ABC, abstractmethod
from langchain.agents import AgentExecutor


class AgentExecutorRepositoryInterface(ABC):
    """ This class is the interface for the AgentExecutorRepository
    """

    @abstractmethod
    def get(self, window_id: str) -> AgentExecutor:
        """
        Get the agent executor for the specified window ID.

        Args:
            window_id (str): The ID of the window.

        Returns:
            AgentExecutor: The agent executor object.
        """

    @abstractmethod
    def create(self, window_id: str, agent_language: str, system_message: str, temperature: float) -> AgentExecutor:
        """
        Creates an AgentExecutor for the given window.

        Args:
            window (Window): The window to create the AgentExecutor for.

        Returns:
            AgentExecutor: The created AgentExecutor.
        """

    @abstractmethod
    def update(self, window_id: str, agent_language: str, system_message: str, temperature: float) -> AgentExecutor:
        """
        Update the agent executor with the given window.

        Args:
            window (Window): The window to update the agent executor with.

        Returns:
            AgentExecutor: The updated agent executor.
        """
