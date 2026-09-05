"""Progress service for aggregating user study analytics."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.database.repositories.quiz import QuizRepository
from app.database.repositories.study_session import StudySessionRepository
from app.database.repositories.study_task import StudyTaskRepository
from app.database.repositories.subject import SubjectRepository


def format_minutes(total_minutes: int) -> str:
    """Format minutes to a clean human-readable string: e.g. 12h 35m."""
    if total_minutes <= 0:
        return "0m"
    hours = total_minutes // 60
    mins = total_minutes % 60
    if hours > 0 and mins > 0:
        return f"{hours}h {mins}m"
    elif hours > 0:
        return f"{hours}h"
    return f"{mins}m"


class ProgressService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.task_repo = StudyTaskRepository(session)
        self.session_repo = StudySessionRepository(session)
        self.quiz_repo = QuizRepository(session)
        self.subject_repo = SubjectRepository(session)

    async def get_user_progress_summary(self, user: User) -> dict[str, Any]:
        """Aggregate all user study statistics."""
        total_minutes = await self.session_repo.get_user_total_study_minutes(user.id)
        completed_tasks = await self.task_repo.count_completed_tasks(user.id)
        quiz_stats = await self.quiz_repo.get_user_quiz_stats(user.id)
        subjects = await self.subject_repo.get_user_subjects(user.id)

        subject_breakdown_lines = []
        for s in subjects:
            subject_breakdown_lines.append(f"• {s.color_icon} {s.name} — {s.progress_percent}%")

        subject_stats_str = (
            "\n".join(subject_breakdown_lines)
            if subject_breakdown_lines
            else "No subjects added yet."
        )

        return {
            "study_time": format_minutes(total_minutes),
            "tasks_count": completed_tasks,
            "quiz_avg": quiz_stats["average_score"],
            "streak": user.streak,
            "xp": user.xp,
            "level": user.level,
            "subject_stats": subject_stats_str,
        }
