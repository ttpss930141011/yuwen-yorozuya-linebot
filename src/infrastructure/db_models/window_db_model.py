""" Defines the window database model.
"""

from typing import TYPE_CHECKING, List
from sqlalchemy import  String, Boolean, Float, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime

from src.infrastructure.db_models.db_base import Base

if TYPE_CHECKING:
    from src.infrastructure.db_models import MessagesDBModel


class WindowsDBModel(Base):
    __tablename__ = 'windows'

    window_id: Mapped[String] = mapped_column(
        String(80), primary_key=True, nullable=False)
    is_muting: Mapped[Boolean] = mapped_column(Boolean, nullable=False)
    system_message: Mapped[String] = mapped_column(String(200), nullable=False)
    agent_language: Mapped[String] = mapped_column(String(50), nullable=False)
    temperature: Mapped[Float] = mapped_column(Float, nullable=False)
    insert_time: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now)
    update_time: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    messages: Mapped[List["MessagesDBModel"]] = relationship(
        back_populates="window", uselist=False, lazy=True)
