"""Reminder repository."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.reminder import Reminder
from app.database.repositories.base import BaseRepository


class ReminderRepository(BaseRepository[Reminder]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Reminder)

    async def get_by_user_id(self, user_id: int) -> Reminder | None:
        stmt = select(Reminder).where(Reminder.user_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def set_reminder(
        self,
        user_id: int,
        time_str: str,
        timezone: str = "UTC",
        is_enabled: bool = True,
    ) -> Reminder:
        reminder = await self.get_by_user_id(user_id)
        if reminder:
            reminder.time_str = time_str
            reminder.timezone = timezone
            reminder.is_enabled = is_enabled
        else:
            reminder = Reminder(
                user_id=user_id,
                time_str=time_str,
                timezone=timezone,
                is_enabled=is_enabled,
            )
            self.session.add(reminder)

        await self.session.commit()
        await self.session.refresh(reminder)
        return reminder

    async def get_due_reminders(self, time_str: str, today: date) -> list[Reminder]:
        """Fetch active reminders matching time_str that haven't been sent today."""
        stmt = select(Reminder).where(
            Reminder.is_enabled.is_(True),
            Reminder.time_str == time_str,
            (Reminder.last_sent_date.is_(None)) | (Reminder.last_sent_date < today),
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def mark_sent(self, reminder_id: int, today: date) -> None:
        reminder = await self.get_by_id(reminder_id)
        if reminder:
            reminder.last_sent_date = today
            await self.session.commit()
