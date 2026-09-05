"""Unit tests for ReferralService."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.user import UserRepository
from app.services.referral.service import ReferralService


@pytest.mark.asyncio
async def test_referral_service_flow(
    db_session: AsyncSession, user_repo: UserRepository
) -> None:
    u1 = await user_repo.create_user_with_settings(telegram_id=111, first_name="User1")
    await user_repo.create_user_with_settings(telegram_id=222, first_name="User2")

    service = ReferralService(db_session)
    link = service.generate_referral_link("StudyFlowBot", 111)
    assert link == "https://t.me/StudyFlowBot?start=ref_111"

    success, xp, _ = await service.process_referral(
        referrer_telegram_id=111, new_user_telegram_id=222
    )
    assert success is True
    assert xp == 50

    # Inviter should have received 50 XP
    updated_u1 = await user_repo.get_by_id(u1.id)
    assert updated_u1 is not None and updated_u1.xp == 50

    # Self referral should fail
    fail, _, _ = await service.process_referral(
        referrer_telegram_id=111, new_user_telegram_id=111
    )
    assert fail is False
