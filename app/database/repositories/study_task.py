"""StudyTask repository."""

from datetime import UTC, date, datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models.study_task import StudyTask
from app.database.repositories.base import BaseRepository


class StudyTaskRepository(BaseRepository[StudyTask]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, StudyTask)

    async def get_tasks_for_date(self, user_id: int, plan_date: date) -> list[StudyTask]:
        stmt = (
            select(StudyTask)
            .where(StudyTask.user_id == user_id, StudyTask.plan_date == plan_date)
            .options(selectinload(StudyTask.subject))
            .order_by(StudyTask.scheduled_time.asc().nulls_last(), StudyTask.id.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_task(
        self,
        user_id: int,
        title: str,
        scheduled_time: str | None = None,
        duration_minutes: int = 20,
        subject_id: int | None = None,
        plan_date: date | None = None,
    ) -> StudyTask:
        task = StudyTask(
            user_id=user_id,
            title=title,
            scheduled_time=scheduled_time,
            duration_minutes=duration_minutes,
            subject_id=subject_id,
            plan_date=plan_date or date.today(),
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def toggle_completed(self, task_id: int) -> StudyTask | None:
        task = await self.get_by_id(task_id)
        if task:
            task.is_completed = not task.is_completed
            task.completed_at = datetime.now(UTC).replace(tzinfo=None) if task.is_completed else None
            await self.session.commit()
            await self.session.refresh(task)
        return task

    async def count_completed_tasks(self, user_id: int) -> int:
        stmt = select(func.count(StudyTask.id)).where(
            StudyTask.user_id == user_id, StudyTask.is_completed.is_(True)
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0
