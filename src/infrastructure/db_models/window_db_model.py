""" Defines the window database model.
"""


from sqlalchemy import Column, String, Boolean, Float, DateTime, Integer, JSON
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from src.infrastructure.db_models.message_db_model import MessagesDBModel
from src.infrastructure.db_models.db_base import Base
from datetime import datetime
from src.infrastructure.databases import sqlalchemy_db as db

class WindowsDBModel(db.Model):
    __tablename__ = 'windows'

    window_id = Column(String(50), primary_key=True, nullable=False)
    is_muting = Column(Boolean, nullable=False)
    system_message = Column(String(200), nullable=False)
    agent_language = Column(String(50), nullable=False)
    temperature = Column(Float, nullable=False)
    insert_time = Column(DateTime, nullable=False, default=datetime.now)
    update_time = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # Foreign key
    messages = relationship("MessagesDBModel", backref="window", uselist=True, lazy=True)

    