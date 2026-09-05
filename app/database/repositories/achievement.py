"""Achievement repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.achievement import Achievement, UserAchievement
from app.database.repositories.base import BaseRepository

DEFAULT_ACHIEVEMENTS = [
    {
        "code": "first_quiz",
        "title": "First Quiz",
        "description": "Completed your first quiz test",
        "icon": "📝",
        "xp_reward": 50,
    },
    {
        "code": "first_study_session",
        "title": "First Study Session",
        "description": "Finished your first focus mode session",
        "icon": "⏱",
        "xp_reward": 50,
    },
    {
        "code": "streak_7",
        "title": "7 Day Streak",
        "description": "Maintained a 7-day consistent study streak",
        "icon": "🔥",
        "xp_reward": 150,
    },
    {
        "code": "xp_1000",
        "title": "1000 XP Club",
        "description": "Earned your first 1,000 XP points",
        "icon": "⭐",
        "xp_reward": 100,
    },
    {
        "code": "quizzes_10",
        "title": "Quiz Master",
        "description": "Completed 10 quizzes successfully",
        "icon": "🧠",
        "xp_reward": 150,
    },
    {
        "code": "tasks_50",
        "title": "Task Conqueror",
        "description": "Completed 50 study tasks",
        "icon": "🎯",
        "xp_reward": 200,
    },
    {
        "code": "first_goal",
        "title": "Goal Achiever",
        "description": "Completed your first study goal",
        "icon": "🏆",
        "xp_reward": 100,
    },
]


class AchievementRepository(BaseRepository[Achievement]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Achievement)

    async def seed_default_achievements(self) -> None:
        """Seed predefined achievements if they do not exist."""
        for item in DEFAULT_ACHIEVEMENTS:
            stmt = select(Achievement).where(Achievement.code == item["code"])
            res = await self.session.execute(stmt)
            if not res.scalar_one_or_none():
                ach = Achievement(**item)
                self.session.add(ach)
        await self.session.commit()

    async def get_all_achievements(self) -> list[Achievement]:
        stmt = select(Achievement).order_by(Achievement.id.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_user_unlocked_codes(self, user_id: int) -> set[str]:
        stmt = (
            select(Achievement.code)
            .join(UserAchievement, UserAchievement.achievement_id == Achievement.id)
            .where(UserAchievement.user_id == user_id)
        )
        res = await self.session.execute(stmt)
        return set(res.scalars().all())

    async def unlock_achievement(self, user_id: int, code: str) -> Achievement | None:
        stmt = select(Achievement).where(Achievement.code == code)
        res = await self.session.execute(stmt)
        ach = res.scalar_one_or_none()
        if not ach:
            return None

        # Check if already unlocked
        check_stmt = select(UserAchievement).where(
            UserAchievement.user_id == user_id, UserAchievement.achievement_id == ach.id
        )
        check_res = await self.session.execute(check_stmt)
        if check_res.scalar_one_or_none():
            return None  # Already unlocked

        user_ach = UserAchievement(user_id=user_id, achievement_id=ach.id)
        self.session.add(user_ach)
        await self.session.commit()
        return ach

    async def get_user_achievements_detail(self, user_id: int) -> list[tuple[Achievement, bool]]:
        """Return list of (Achievement, is_unlocked)."""
        all_ach = await self.get_all_achievements()
        unlocked_codes = await self.get_user_unlocked_codes(user_id)
        return [(ach, ach.code in unlocked_codes) for ach in all_ach]
