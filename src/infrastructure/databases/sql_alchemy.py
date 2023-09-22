from flask import Flask

from src.infrastructure.db_models.db_base import Base,engine
from src.domain.exceptions import OperationalException



class SQLAlchemyAdapter:

    def __init__(self, app: Flask):

        if app.config['SQLALCHEMY_DATABASE_URI'] is not None:
            Base.metadata.create_all(bind=engine)
        elif not app.config["TESTING"]:
            raise OperationalException("SQLALCHEMY_DATABASE_URI not set")


def setup_sqlalchemy(app, throw_exception_if_not_set=True):

    try:
        SQLAlchemyAdapter(app)
    except OperationalException as e:
        if throw_exception_if_not_set:
            raise e

    return app
