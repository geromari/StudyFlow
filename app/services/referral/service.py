"""Referral service for link generation, invitation tracking, and rewards."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.referral import ReferralRepository
from app.database.repositories.user import UserRepository
from app.services.achievements.service import AchievementService
from app.services.progress.gamification import XP_REFERRAL_BONUS


class ReferralService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.referral_repo = ReferralRepository(session)
        self.user_repo = UserRepository(session)
        self.achievement_service = AchievementService(session)

    def generate_referral_link(self, bot_username: str, telegram_id: int) -> str:
        """Construct standard Telegram referral deep link."""
        return f"https://t.me/{bot_username}?start=ref_{telegram_id}"

    async def process_referral(
        self, referrer_telegram_id: int, new_user_telegram_id: int
    ) -> tuple[bool, int, list[Any]]:
        """Process referral when a new user registers with a referral code.

        Returns (success, xp_awarded, unlocked_achievements_for_referrer).
        """
        if referrer_telegram_id == new_user_telegram_id:
            return False, 0, []

        referrer = await self.user_repo.get_by_telegram_id(referrer_telegram_id)
        new_user = await self.user_repo.get_by_telegram_id(new_user_telegram_id)

        if not referrer or not new_user:
            return False, 0, []

        referral = await self.referral_repo.create_referral(
            referrer_id=referrer.id,
            referred_id=new_user.id,
            xp_awarded=XP_REFERRAL_BONUS,
        )

        if not referral:
            return False, 0, []

        # Award XP to both referrer and invited user
        await self.user_repo.add_xp(referrer.id, XP_REFERRAL_BONUS)
        await self.user_repo.add_xp(new_user.id, 25)  # Welcome bonus for invited friend

        # Check achievements for referrer
        unlocked = await self.achievement_service.check_and_unlock(referrer)

        return True, XP_REFERRAL_BONUS, unlocked

    async def get_referral_info(self, user_id: int, bot_username: str, telegram_id: int) -> dict[str, Any]:
        stats = await self.referral_repo.get_referral_stats(user_id)
        return {
            "link": self.generate_referral_link(bot_username, telegram_id),
            "count": stats["referrals_count"],
            "xp": stats["total_xp"],
        }
