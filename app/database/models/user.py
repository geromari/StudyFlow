"""User and UserSettings models."""

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin, utcnow

if TYPE_CHECKING:
    from app.database.models.achievement import UserAchievement
    from app.database.models.ai_conversation import AIConversation
    from app.database.models.document import Document
    from app.database.models.goal import Goal
    from app.database.models.quiz import Quiz
    from app.database.models.reminder import Reminder
    from app.database.models.study_session import StudySession
    from app.database.models.study_task import StudyTask
    from app.database.models.subject import Subject


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)

    xp: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    streak: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_study_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    last_activity: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    is_banned: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    referrer_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    settings: Mapped["UserSettings"] = relationship(
        "UserSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    subjects: Mapped[list["Subject"]] = relationship(
        "Subject", back_populates="user", cascade="all, delete-orphan"
    )
    goals: Mapped[list["Goal"]] = relationship(
        "Goal", back_populates="user", cascade="all, delete-orphan"
    )
    study_tasks: Mapped[list["StudyTask"]] = relationship(
        "StudyTask", back_populates="user", cascade="all, delete-orphan"
    )
    study_sessions: Mapped[list["StudySession"]] = relationship(
        "StudySession", back_populates="user", cascade="all, delete-orphan"
    )
    quizzes: Mapped[list["Quiz"]] = relationship(
        "Quiz", back_populates="user", cascade="all, delete-orphan"
    )
    achievements: Mapped[list["UserAchievement"]] = relationship(
        "UserAchievement", back_populates="user", cascade="all, delete-orphan"
    )
    reminders: Mapped[list["Reminder"]] = relationship(
        "Reminder", back_populates="user", cascade="all, delete-orphan"
    )
    documents: Mapped[list["Document"]] = relationship(
        "Document", back_populates="user", cascade="all, delete-orphan"
    )
    ai_conversations: Mapped[list["AIConversation"]] = relationship(
        "AIConversation", back_populates="user", cascade="all, delete-orphan"
    )


class UserSettings(Base, TimestampMixin):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), default="UTC", nullable=False)
    daily_study_target: Mapped[int] = mapped_column(Integer, default=30, nullable=False)  # in minutes
    reminders_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    reminder_time: Mapped[str] = mapped_column(String(5), default="18:00", nullable=False)  # HH:MM format

    user: Mapped["User"] = relationship("User", back_populates="settings")
