"""SQLAlchemy database models for StudyFlow."""

from app.database.models.achievement import Achievement, UserAchievement
from app.database.models.ai_conversation import AIConversation
from app.database.models.base import Base, TimestampMixin, utcnow
from app.database.models.document import Document
from app.database.models.goal import Goal
from app.database.models.quiz import Quiz, QuizAnswer, QuizQuestion
from app.database.models.referral import Referral
from app.database.models.reminder import Reminder
from app.database.models.study_session import StudySession
from app.database.models.study_task import StudyTask
from app.database.models.subject import Subject, Topic
from app.database.models.user import User, UserSettings

__all__ = [
    "Base",
    "TimestampMixin",
    "utcnow",
    "User",
    "UserSettings",
    "Subject",
    "Topic",
    "Goal",
    "StudyTask",
    "StudySession",
    "Quiz",
    "QuizQuestion",
    "QuizAnswer",
    "Achievement",
    "UserAchievement",
    "Reminder",
    "Document",
    "AIConversation",
    "Referral",
]
