from sqlalchemy.orm import DeclarativeBase, sessionmaker, scoped_session
from sqlalchemy import create_engine

from src.app.flask_postgresql.configs import Config


class Base(DeclarativeBase):
    """ Base class for all models
    """


engine = create_engine(
    url=Config.SQLALCHEMY_DATABASE_URI,
    pool_size=Config.SQLALCHEMY_POOL_SIZE,
    echo=Config.SQLALCHEMY_ECHO,
    max_overflow=Config.SQLALCHEMY_MAX_OVERFLOW,
    pool_recycle=Config.SQLALCHEMY_POOL_RECYCLE,
    pool_timeout=Config.SQLALCHEMY_POOL_TIMEOUT,
    connect_args={'connect_timeout': 300},
)
Session = scoped_session(sessionmaker(bind=engine))
