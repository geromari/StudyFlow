"""Study plan service for creating and tracking personal study schedules."""

from datetime import date
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.study_task import StudyTask
from app.database.repositories.study_task import StudyTaskRepository
from app.database.repositories.subject import SubjectRepository
from app.database.repositories.user import UserRepository
from app.services.achievements.service import AchievementService
from app.services.ai.client import AIService, ai_service
from app.services.progress.gamification import XP_TASK_COMPLETION


class StudyPlanService:
    def __init__(
        self,
        session: AsyncSession,
        ai: AIService | None = None,
    ) -> None:
        self.session = session
        self.task_repo = StudyTaskRepository(session)
        self.user_repo = UserRepository(session)
        self.subject_repo = SubjectRepository(session)
        self.ai = ai or ai_service
        self.achievement_service = AchievementService(session)

    async def generate_daily_plan(
        self,
        user_id: int,
        goal: str,
        target_minutes: int,
        language: str = "en",
        plan_date: date | None = None,
    ) -> list[StudyTask]:
        """Generate AI daily schedule and persist study tasks."""
        subjects = await self.subject_repo.get_user_subjects(user_id)
        subject_names = [s.name for s in subjects]

        tasks_data = await self.ai.generate_study_plan(
            goal=goal,
            target_minutes=target_minutes,
            subjects=subject_names,
            language=language,
        )

        created_tasks: list[StudyTask] = []
        name_to_id = {s.name.lower(): s.id for s in subjects}

        for item in tasks_data:
            subject_name = item.get("subject", "")
            subj_id = name_to_id.get(subject_name.lower()) if subject_name else None

            task = await self.task_repo.create_task(
                user_id=user_id,
                title=item.get("title", "Study Session"),
                scheduled_time=item.get("scheduled_time"),
                duration_minutes=item.get("duration_minutes", 20),
                subject_id=subj_id,
                plan_date=plan_date or date.today(),
            )
            created_tasks.append(task)

        return created_tasks

    async def complete_task(self, task_id: int, user_id: int) -> tuple[bool, int, list[Any]]:
        """Toggle task completion. If marked completed, award XP, update streak, and check achievements."""
        task = await self.task_repo.toggle_completed(task_id)
        if not task:
            return False, 0, []

        xp_awarded = 0
        unlocked = []
        if task.is_completed:
            xp_awarded = XP_TASK_COMPLETION
            await self.user_repo.add_xp(user_id, xp_awarded)
            await self.user_repo.update_streak(user_id, date.today())

            user = await self.user_repo.get_by_id(user_id)
            if user:
                unlocked = await self.achievement_service.check_and_unlock(user)

        return task.is_completed, xp_awarded, unlocked
