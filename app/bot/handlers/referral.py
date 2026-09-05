"""Referral system handlers."""

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.services.referral.service import ReferralService
from app.utils.i18n import DEFAULT_LANGUAGE, t

router = Router(name="referral_router")


@router.message(Command("referral"))
@router.message(F.text.in_({"🎁 Referral", "🎁 Taklif qilish", "🎁 Рефералы"}))
async def handle_referral_menu(
    message: Message,
    bot: Bot,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer(t("please_start_first", lang))
        return

    bot_info = await bot.get_me()
    bot_username = bot_info.username or "StudyFlowBot"

    referral_service = ReferralService(session)
    info = await referral_service.get_referral_info(
        user_id=user.id,
        bot_username=bot_username,
        telegram_id=user.telegram_id,
    )

    text = t(
        "referral_title",
        lang,
        link=info["link"],
        count=info["count"],
        xp=info["xp"],
    )
    await message.answer(text, parse_mode="Markdown")
