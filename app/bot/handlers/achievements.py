"""Achievements and Leaderboard handlers."""

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.user import User
from app.database.repositories.achievement import AchievementRepository
from app.database.repositories.user import UserRepository
from app.utils.i18n import DEFAULT_LANGUAGE, t

router = Router(name="achievements_router")


@router.message(F.text.in_({"🏆 Achievements", "🏆 Yutuqlar", "🏆 Достижения"}))
async def handle_achievements_menu(
    message: Message,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer("Please /start the bot first.")
        return

    ach_repo = AchievementRepository(session)
    achievements = await ach_repo.get_user_achievements_detail(user.id)

    unlocked_count = sum(1 for _, unlocked in achievements if unlocked)
    total_count = len(achievements)

    lines = []
    for ach, unlocked in achievements:
        if unlocked:
            lines.append(f"{ach.icon} **{ach.title}** (Unlocked)\n_{ach.description}_ (+{ach.xp_reward} XP)")
        else:
            lines.append(f"🔒 **{ach.title}**\n_{ach.description}_ (+{ach.xp_reward} XP)")

    list_str = "\n\n".join(lines)
    text = t(
        "achievements_title",
        lang,
        unlocked=unlocked_count,
        total=total_count,
        list=list_str,
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏆 View Leaderboard", callback_data="view_leaderboard")]
        ]
    )

    await message.answer(text, reply_markup=kb, parse_mode="Markdown")


@router.callback_query(F.data == "view_leaderboard")
async def handle_leaderboard_view(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return

    user_repo = UserRepository(session)
    top_users = await user_repo.get_top_users_by_xp(limit=10)
    user_rank = await user_repo.get_user_rank(user.id)

    ranking_lines = []
    for idx, u in enumerate(top_users, 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
        # Protect user privacy by masking username or using first name
        display_name = u.first_name[:15]
        ranking_lines.append(f"{medal} {display_name} — **{u.xp} XP** (Level {u.level})")

    ranking_str = "\n".join(ranking_lines) if ranking_lines else "No rankings yet."
    text = t(
        "leaderboard_title",
        lang,
        ranking=ranking_str,
        user_rank=user_rank,
        user_xp=user.xp,
    )
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()
