"""Subject and Topic models."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.database.models.quiz import Quiz
    from app.database.models.study_session import StudySession
    from app.database.models.study_task import StudyTask
    from app.database.models.user import User


class Subject(Base, TimestampMixin):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    color_icon: Mapped[str] = mapped_column(String(10), default="📚", nullable=False)
    progress_percent: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="subjects")
    topics: Mapped[list["Topic"]] = relationship(
        "Topic", back_populates="subject", cascade="all, delete-orphan"
    )
    study_tasks: Mapped[list["StudyTask"]] = relationship(
        "StudyTask", back_populates="subject"
    )
    study_sessions: Mapped[list["StudySession"]] = relationship(
        "StudySession", back_populates="subject"
    )
    quizzes: Mapped[list["Quiz"]] = relationship(
        "Quiz", back_populates="subject"
    )


class Topic(Base, TimestampMixin):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subjects.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    subject: Mapped["Subject"] = relationship("Subject", back_populates="topics")
