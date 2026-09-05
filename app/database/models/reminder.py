"""Reminder model."""

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.database.models.user import User


class Reminder(Base, TimestampMixin):
    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    time_str: Mapped[str] = mapped_column(String(5), default="18:00", nullable=False)  # HH:MM
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_sent_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="reminders")
