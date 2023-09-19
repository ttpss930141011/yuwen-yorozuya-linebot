""" Defines the window database model.
"""

from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import ForeignKey,  DateTime, JSON, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.infrastructure.databases import sqlalchemy_db as db

if TYPE_CHECKING:
    from src.infrastructure.db_models import WindowsDBModel


class MessagesDBModel(db.Model):
    __tablename__ = 'messages'

    message_id: Mapped[Integer] = mapped_column(
        Integer, primary_key=True, nullable=False, autoincrement=True)
    message: Mapped[JSON] = mapped_column(JSON, nullable=False)
    insert_time: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now)
    update_time: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    window_id: Mapped[str] = mapped_column(ForeignKey(
        "windows.window_id", ondelete="CASCADE"), nullable=False)
    window: Mapped["WindowsDBModel"] = relationship(
        back_populates="messages", uselist=False, lazy=True)
