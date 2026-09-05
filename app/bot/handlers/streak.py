"""Study streak status handler."""

from datetime import date

from aiogram import F, Router
from aiogram.types import Message

from app.database.models.user import User
from app.utils.i18n import DEFAULT_LANGUAGE, t

router = Router(name="streak_router")


@router.message(F.text.in_({"🔥 Streak", "🔥 Ketma-ketlik", "🔥 Серия"}))
async def handle_streak_menu(
    message: Message,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer("Please /start the bot first.")
        return

    today = date.today()
    studied_today = user.last_study_date == today
    status_str = t("streak_done_today", lang) if studied_today else t("streak_pending_today", lang)

    text = t("streak_info", lang, streak=user.streak, today_status=status_str)
    await message.answer(text, parse_mode="Markdown")
