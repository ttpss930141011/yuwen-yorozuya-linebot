""" This module implements the event handler for file message events.
"""
from src.app.flask_postgresql.interfaces.event_handler_interface import EventHandlerInterface


class FileEventHandler(EventHandlerInterface):
    def __init__(self, logger, agent_repository, configuration):
        self.logger = logger
        self.agent_repository = agent_repository
        self.configuration = configuration

    def execute(self):
        return "我收到檔案了！"
