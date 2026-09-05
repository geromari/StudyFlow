"""StudyTask model for daily study plans."""

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.database.models.subject import Subject
    from app.database.models.user import User


class StudyTask(Base, TimestampMixin):
    __tablename__ = "study_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    subject_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    scheduled_time: Mapped[str | None] = mapped_column(String(10), nullable=True)  # e.g., "09:00"
    duration_minutes: Mapped[int] = mapped_column(Integer, default=20, nullable=False)
    plan_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="study_tasks")
    subject: Mapped["Subject | None"] = relationship("Subject", back_populates="study_tasks")
