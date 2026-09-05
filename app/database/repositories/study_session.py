"""StudySession repository."""

from datetime import UTC, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models.study_session import StudySession
from app.database.repositories.base import BaseRepository


class StudySessionRepository(BaseRepository[StudySession]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, StudySession)

    async def create_session(
        self,
        user_id: int,
        duration_minutes: int,
        xp_earned: int,
        mode: str = "focus",
        subject_id: int | None = None,
        started_at: datetime | None = None,
        ended_at: datetime | None = None,
    ) -> StudySession:
        now = datetime.now(UTC).replace(tzinfo=None)
        session = StudySession(
            user_id=user_id,
            duration_minutes=duration_minutes,
            xp_earned=xp_earned,
            mode=mode,
            subject_id=subject_id,
            started_at=started_at or now,
            ended_at=ended_at or now,
        )
        self.session.add(session)
        await self.session.commit()
        await self.session.refresh(session)
        return session

    async def get_user_total_study_minutes(self, user_id: int) -> int:
        stmt = select(func.sum(StudySession.duration_minutes)).where(
            StudySession.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def count_user_sessions(self, user_id: int) -> int:
        stmt = select(func.count(StudySession.id)).where(StudySession.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def count_total_sessions(self) -> int:
        stmt = select(func.count(StudySession.id))
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def get_recent_sessions(self, user_id: int, limit: int = 10) -> list[StudySession]:
        stmt = (
            select(StudySession)
            .where(StudySession.user_id == user_id)
            .options(selectinload(StudySession.subject))
            .order_by(StudySession.id.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
