""" Flask PostgreSQL Process Handler
"""

from src.app.flask_postgresql.configs import Config
from src.app.flask_postgresql.create_flask_postgresql_app import create_flask_postgresql_app

if __name__ == "__main__":
    app = create_flask_postgresql_app(Config)
    app.run(host="0.0.0.0", port=Config.PORT, debug=True)
