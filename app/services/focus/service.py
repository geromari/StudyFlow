"""Focus mode service for timer tracking, study sessions, and gamification rewards."""

from datetime import UTC, date, datetime, timedelta
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.study_session import StudySession
from app.database.repositories.study_session import StudySessionRepository
from app.database.repositories.user import UserRepository
from app.services.achievements.service import AchievementService
from app.services.progress.gamification import calculate_focus_xp


class FocusService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.session_repo = StudySessionRepository(session)
        self.user_repo = UserRepository(session)
        self.achievement_service = AchievementService(session)

    async def record_completed_session(
        self,
        user_id: int,
        duration_minutes: int,
        subject_id: int | None = None,
        mode: str = "focus",
    ) -> tuple[StudySession, int, list[Any]]:
        """Record completed focus session, award XP, update streak, check achievements.

        Returns (session, xp_earned, unlocked_achievements).
        """
        xp_earned = calculate_focus_xp(duration_minutes)
        now = datetime.now(UTC).replace(tzinfo=None)
        start_time = now - timedelta(minutes=duration_minutes)

        study_session = await self.session_repo.create_session(
            user_id=user_id,
            duration_minutes=duration_minutes,
            xp_earned=xp_earned,
            mode=mode,
            subject_id=subject_id,
            started_at=start_time,
            ended_at=now,
        )

        # Award XP
        await self.user_repo.add_xp(user_id, xp_earned)

        # Update streak
        await self.user_repo.update_streak(user_id, date.today())

        # Check achievements
        user = await self.user_repo.get_by_id(user_id)
        unlocked = []
        if user:
            unlocked = await self.achievement_service.check_and_unlock(user)

        return study_session, xp_earned, unlocked
