"""Goal repository."""

from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.goal import Goal
from app.database.repositories.base import BaseRepository


class GoalRepository(BaseRepository[Goal]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Goal)

    async def get_user_goals(self, user_id: int) -> list[Goal]:
        stmt = select(Goal).where(Goal.user_id == user_id).order_by(Goal.is_completed.asc(), Goal.id.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_goal(
        self, user_id: int, title: str, target_date: date | None = None
    ) -> Goal:
        goal = Goal(user_id=user_id, title=title, target_date=target_date)
        self.session.add(goal)
        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def update_goal(
        self,
        goal_id: int,
        title: str | None = None,
        target_date: date | None = None,
        progress_percent: int | None = None,
    ) -> Goal | None:
        goal = await self.get_by_id(goal_id)
        if not goal:
            return None

        if title is not None:
            goal.title = title
        if target_date is not None:
            goal.target_date = target_date
        if progress_percent is not None:
            goal.progress_percent = max(0, min(100, progress_percent))
            if goal.progress_percent == 100 and not goal.is_completed:
                goal.is_completed = True
                goal.completed_at = datetime.now(UTC).replace(tzinfo=None)

        await self.session.commit()
        await self.session.refresh(goal)
        return goal

    async def mark_completed(self, goal_id: int) -> Goal | None:
        goal = await self.get_by_id(goal_id)
        if goal:
            goal.is_completed = True
            goal.progress_percent = 100
            goal.completed_at = datetime.now(UTC).replace(tzinfo=None)
            await self.session.commit()
            await self.session.refresh(goal)
        return goal
