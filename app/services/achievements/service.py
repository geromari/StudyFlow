"""Achievement service to verify conditions and trigger unlocks."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.achievement import Achievement
from app.database.models.user import User
from app.database.repositories.achievement import AchievementRepository
from app.database.repositories.quiz import QuizRepository
from app.database.repositories.study_session import StudySessionRepository
from app.database.repositories.study_task import StudyTaskRepository
from app.database.repositories.user import UserRepository


class AchievementService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.ach_repo = AchievementRepository(session)
        self.user_repo = UserRepository(session)
        self.quiz_repo = QuizRepository(session)
        self.session_repo = StudySessionRepository(session)
        self.task_repo = StudyTaskRepository(session)

    async def check_and_unlock(self, user: User) -> list[Achievement]:
        """Check all achievement thresholds and return newly unlocked achievements."""
        unlocked: list[Achievement] = []

        # 1. 1000 XP Club
        if user.xp >= 1000:
            ach = await self.ach_repo.unlock_achievement(user.id, "xp_1000")
            if ach:
                unlocked.append(ach)

        # 2. 7 Day Streak
        if user.streak >= 7:
            ach = await self.ach_repo.unlock_achievement(user.id, "streak_7")
            if ach:
                unlocked.append(ach)

        # 3. First Study Session
        session_count = await self.session_repo.count_user_sessions(user.id)
        if session_count >= 1:
            ach = await self.ach_repo.unlock_achievement(user.id, "first_study_session")
            if ach:
                unlocked.append(ach)

        # 4. Quizzes
        quiz_stats = await self.quiz_repo.get_user_quiz_stats(user.id)
        quiz_count = quiz_stats["completed_count"]
        if quiz_count >= 1:
            ach = await self.ach_repo.unlock_achievement(user.id, "first_quiz")
            if ach:
                unlocked.append(ach)
        if quiz_count >= 10:
            ach = await self.ach_repo.unlock_achievement(user.id, "quizzes_10")
            if ach:
                unlocked.append(ach)

        # 5. Completed Tasks
        completed_tasks = await self.task_repo.count_completed_tasks(user.id)
        if completed_tasks >= 50:
            ach = await self.ach_repo.unlock_achievement(user.id, "tasks_50")
            if ach:
                unlocked.append(ach)

        # Award XP for each newly unlocked achievement
        for ach in unlocked:
            await self.user_repo.add_xp(user.id, ach.xp_reward)

        return unlocked

    async def unlock_goal_achievement(self, user_id: int) -> Achievement | None:
        """Specifically called when a goal is completed."""
        ach = await self.ach_repo.unlock_achievement(user_id, "first_goal")
        if ach:
            await self.user_repo.add_xp(user_id, ach.xp_reward)
        return ach
