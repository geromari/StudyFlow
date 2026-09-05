"""User profile view handler."""

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.models.user import User
from app.utils.i18n import DEFAULT_LANGUAGE, t

router = Router(name="profile_router")


@router.message(Command("profile"))
@router.message(F.text.in_({"👤 Profile", "👤 Profil", "👤 Профиль"}))
async def handle_profile_view(
    message: Message,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer(t("please_start_first", lang))
        return

    settings = user.settings
    timezone_str = settings.timezone if settings else "UTC"
    daily_target = settings.daily_study_target if settings else 30
    user_lang = settings.language if settings else lang

    text = t(
        "profile_title",
        user_lang,
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        language=user_lang.upper(),
        timezone=timezone_str,
        daily_target=daily_target,
        xp=user.xp,
        level=user.level,
        streak=user.streak,
        created_at=user.created_at.strftime("%Y-%m-%d"),
        last_activity=user.last_activity.strftime("%Y-%m-%d %H:%M"),
    )
    await message.answer(text, parse_mode="Markdown")
