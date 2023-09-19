from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine

from src.app.flask_postgresql.configs import Config

class Base(DeclarativeBase):
    """ Base class for all models
    """

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Session = scoped_session(sessionmaker(bind=engine))
