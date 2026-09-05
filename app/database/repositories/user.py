"""User repository for user data and settings."""

from datetime import UTC, date, datetime, timedelta

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models.user import User, UserSettings
from app.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = (
            select(User)
            .where(User.telegram_id == telegram_id)
            .options(selectinload(User.settings))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user_with_settings(
        self,
        telegram_id: int,
        first_name: str,
        username: str | None = None,
        language: str = "en",
        daily_target: int = 30,
        referrer_id: int | None = None,
    ) -> User:
        user = User(
            telegram_id=telegram_id,
            first_name=first_name,
            username=username,
            referrer_id=referrer_id,
        )
        self.session.add(user)
        await self.session.flush()

        settings = UserSettings(
            user_id=user.id,
            language=language,
            daily_study_target=daily_target,
        )
        self.session.add(settings)
        await self.session.commit()
        await self.session.refresh(user, attribute_names=["settings"])
        return user

    async def update_activity(self, telegram_id: int) -> None:
        stmt = (
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(last_activity=datetime.now(UTC).replace(tzinfo=None))
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def add_xp(self, user_id: int, amount: int) -> tuple[int, int, bool]:
        """Add XP to user and update level. Returns (new_xp, new_level, level_up_boolean)."""
        user = await self.session.get(User, user_id)
        if not user:
            return 0, 1, False

        user.xp += amount
        # Level formula: Level = int((XP / 100) ** 0.5) + 1
        # E.g.: 0-99 XP -> Level 1; 100-399 XP -> Level 2; 400-899 XP -> Level 3; 900+ -> Level 4, etc.
        new_level = int((user.xp / 100) ** 0.5) + 1
        level_up = new_level > user.level
        user.level = new_level

        await self.session.commit()
        await self.session.refresh(user)
        return user.xp, user.level, level_up

    async def update_streak(self, user_id: int, today: date) -> int:
        """Update daily study streak following consistency rule."""
        user = await self.session.get(User, user_id)
        if not user:
            return 0

        if user.last_study_date == today:
            # Already studied today, streak stays intact
            return user.streak

        if user.last_study_date == today - timedelta(days=1):
            # Studied yesterday, increment streak
            user.streak += 1
        else:
            # Missed a day or first time studying
            user.streak = 1

        user.last_study_date = today
        await self.session.commit()
        await self.session.refresh(user)
        return user.streak

    async def get_settings(self, user_id: int) -> UserSettings | None:
        stmt = select(UserSettings).where(UserSettings.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_settings(
        self,
        user_id: int,
        language: str | None = None,
        timezone_str: str | None = None,
        daily_target: int | None = None,
        reminders_enabled: bool | None = None,
        reminder_time: str | None = None,
    ) -> UserSettings | None:
        settings = await self.get_settings(user_id)
        if not settings:
            return None

        if language is not None:
            settings.language = language
        if timezone_str is not None:
            settings.timezone = timezone_str
        if daily_target is not None:
            settings.daily_study_target = daily_target
        if reminders_enabled is not None:
            settings.reminders_enabled = reminders_enabled
        if reminder_time is not None:
            settings.reminder_time = reminder_time

        await self.session.commit()
        await self.session.refresh(settings)
        return settings

    async def get_top_users_by_xp(self, limit: int = 10) -> list[User]:
        stmt = (
            select(User)
            .where(User.is_banned.is_(False))
            .order_by(User.xp.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_user_rank(self, user_id: int) -> int:
        user = await self.session.get(User, user_id)
        if not user:
            return 0
        stmt = select(func.count(User.id)).where(User.xp > user.xp, User.is_banned.is_(False))
        result = await self.session.execute(stmt)
        return (result.scalar() or 0) + 1

    async def count_total_users(self) -> int:
        stmt = select(func.count(User.id))
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def count_active_users(self, days: int = 7) -> int:
        cutoff = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=days)
        stmt = select(func.count(User.id)).where(User.last_activity >= cutoff)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def count_new_users_today(self) -> int:
        start_of_day = datetime.now(UTC).replace(
            hour=0, minute=0, second=0, microsecond=0, tzinfo=None
        )
        stmt = select(func.count(User.id)).where(User.created_at >= start_of_day)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def get_all_broadcast_recipients(self) -> list[int]:
        stmt = select(User.telegram_id).where(User.is_banned.is_(False))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def set_ban_status(self, telegram_id: int, is_banned: bool) -> bool:
        stmt = (
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(is_banned=is_banned)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.rowcount > 0
