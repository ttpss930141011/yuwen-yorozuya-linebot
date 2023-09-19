""" Flask PostgreSQL Process Handler
"""


from src.app.flask_postgresql.create_flask_postgresql_app import create_flask_postgresql_app
from src.infrastructure.loggers.logger_default import LoggerDefault
from src.app.flask_postgresql.configs import Config

logger = LoggerDefault()


if __name__ == "__main__":
    flask_memory_app = create_flask_postgresql_app(Config, logger)
    flask_memory_app.run(debug=True)
