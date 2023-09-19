""" Defines the window database model.
"""


from sqlalchemy import ForeignKey
from sqlalchemy import Column, DateTime, JSON, Integer, String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from src.infrastructure.db_models.db_base import Base
from datetime import datetime

from src.infrastructure.databases import sqlalchemy_db as db


class MessagesDBModel(db.Model):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    message = Column(JSON, nullable=False)
    insert_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    window_id = Column(String(100), ForeignKey('windows.window_id'), nullable=False)
    # window_id = Column(String(100), nullable=False)
    