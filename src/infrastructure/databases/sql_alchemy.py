from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.domain.exceptions import OperationalException

sqlalchemy_db = SQLAlchemy()


class SQLAlchemyAdapter:

    def __init__(self, app: Flask):

        if app.config['SQLALCHEMY_DATABASE_URI'] is not None:
            sqlalchemy_db.init_app(app)
            with app.app_context():
                sqlalchemy_db.create_all()
        elif not app.config["TESTING"]:
            raise OperationalException("SQLALCHEMY_DATABASE_URI not set")


def setup_sqlalchemy(app, throw_exception_if_not_set=True):

    try:
        SQLAlchemyAdapter(app)
    except OperationalException as e:
        if throw_exception_if_not_set:
            raise e

    return app
