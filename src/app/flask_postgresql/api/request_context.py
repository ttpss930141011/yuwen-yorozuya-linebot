from flask import Flask, g
from sqlalchemy.orm import scoped_session

from src.infrastructure.db_models.db_base import Session


def setup_request_context(app: Flask):
    """Setup Request Context"""

    @app.before_request
    def before_request():
        """Before Request"""
        # print("before_request")
        g.db = Session()

    @app.teardown_request
    def teardown_request(_unused=False):
        """After Request"""
        dbc: scoped_session = getattr(g, "db", None)
        # print("teardown_request")
        if dbc is not None:
            dbc.close()

    return app
