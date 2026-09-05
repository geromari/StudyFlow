"""Database repositories for StudyFlow."""

from app.database.repositories.achievement import AchievementRepository
from app.database.repositories.ai_conversation import AIConversationRepository
from app.database.repositories.base import BaseRepository
from app.database.repositories.document import DocumentRepository
from app.database.repositories.goal import GoalRepository
from app.database.repositories.quiz import QuizRepository
from app.database.repositories.referral import ReferralRepository
from app.database.repositories.reminder import ReminderRepository
from app.database.repositories.study_session import StudySessionRepository
from app.database.repositories.study_task import StudyTaskRepository
from app.database.repositories.subject import SubjectRepository
from app.database.repositories.user import UserRepository

__all__ = [
    "BaseRepository",
    "UserRepository",
    "SubjectRepository",
    "GoalRepository",
    "StudyTaskRepository",
    "StudySessionRepository",
    "QuizRepository",
    "AchievementRepository",
    "ReminderRepository",
    "DocumentRepository",
    "AIConversationRepository",
    "ReferralRepository",
]
