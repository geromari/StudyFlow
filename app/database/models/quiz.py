"""Quiz, QuizQuestion, and QuizAnswer models."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.database.models.subject import Subject
    from app.database.models.user import User


class Quiz(Base, TimestampMixin):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    subject_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), default="medium", nullable=False)  # easy, medium, hard
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    xp_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="quizzes")
    subject: Mapped["Subject | None"] = relationship("Subject", back_populates="quizzes")
    questions: Mapped[list["QuizQuestion"]] = relationship(
        "QuizQuestion", back_populates="quiz", cascade="all, delete-orphan"
    )
    answers: Mapped[list["QuizAnswer"]] = relationship(
        "QuizAnswer", back_populates="quiz", cascade="all, delete-orphan"
    )


class QuizQuestion(Base, TimestampMixin):
    __tablename__ = "quiz_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), index=True, nullable=False
    )
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[str] = mapped_column(Text, nullable=False)  # JSON-encoded dictionary of options {"A": "...", "B": "..."}
    correct_option: Mapped[str] = mapped_column(String(10), nullable=False)  # "A", "B", "C", "D"
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions")
    answers: Mapped[list["QuizAnswer"]] = relationship(
        "QuizAnswer", back_populates="question", cascade="all, delete-orphan"
    )


class QuizAnswer(Base, TimestampMixin):
    __tablename__ = "quiz_answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), index=True, nullable=False
    )
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quiz_questions.id", ondelete="CASCADE"), index=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    selected_option: Mapped[str] = mapped_column(String(10), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="answers")
    question: Mapped["QuizQuestion"] = relationship("QuizQuestion", back_populates="answers")
