"""User study analytics and progress handlers."""

from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.services.progress.service import ProgressService
from app.utils.i18n import DEFAULT_LANGUAGE, t

router = Router(name="progress_router")


@router.message(F.text.in_({"📊 Progress", "📊 Statistika", "📊 Прогресс"}))
async def handle_progress_menu(
    message: Message,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer("Please /start the bot first.")
        return

    progress_service = ProgressService(session)
    stats = await progress_service.get_user_progress_summary(user)

    text = t(
        "progress_summary",
        lang,
        study_time=stats["study_time"],
        tasks_count=stats["tasks_count"],
        quiz_avg=stats["quiz_avg"],
        streak=stats["streak"],
        xp=stats["xp"],
        level=stats["level"],
        subject_stats=stats["subject_stats"],
    )

    await message.answer(text, parse_mode="Markdown")
