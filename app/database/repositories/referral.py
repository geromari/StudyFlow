"""Referral repository."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.referral import Referral
from app.database.repositories.base import BaseRepository


class ReferralRepository(BaseRepository[Referral]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Referral)

    async def is_already_referred(self, referred_id: int) -> bool:
        stmt = select(Referral).where(Referral.referred_id == referred_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none() is not None

    async def create_referral(
        self, referrer_id: int, referred_id: int, xp_awarded: int = 50
    ) -> Referral | None:
        if referrer_id == referred_id:
            # Self-referral prevention
            return None

        if await self.is_already_referred(referred_id):
            return None

        ref = Referral(
            referrer_id=referrer_id,
            referred_id=referred_id,
            xp_awarded=xp_awarded,
            status="completed",
        )
        self.session.add(ref)
        await self.session.commit()
        await self.session.refresh(ref)
        return ref

    async def get_referral_stats(self, user_id: int) -> dict[str, int]:
        count_stmt = select(func.count(Referral.id)).where(Referral.referrer_id == user_id)
        count_res = await self.session.execute(count_stmt)
        count = count_res.scalar() or 0

        xp_stmt = select(func.sum(Referral.xp_awarded)).where(Referral.referrer_id == user_id)
        xp_res = await self.session.execute(xp_stmt)
        total_xp = xp_res.scalar() or 0

        return {
            "referrals_count": count,
            "total_xp": total_xp,
        }
