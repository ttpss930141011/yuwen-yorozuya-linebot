from flask import Flask, g
from src.infrastructure.container.container import Container
from src.infrastructure.repositories.agent_chain.agent_chain_in_memory_repository import (
    AgentExecutorInMemoryRepository,
)
from src.infrastructure.repositories.window import WindowPostgresqlRepository
from src.infrastructure.loggers.logger_default import LoggerDefault


def setup_container(app: Flask) -> Flask:
    """Setup Container for the app"""
    container = Container()

    container.register("agent_repository", AgentExecutorInMemoryRepository())
    container.register("window_repository", WindowPostgresqlRepository())
    container.register("logger", LoggerDefault())

    app.config["container"] = container

    return app
