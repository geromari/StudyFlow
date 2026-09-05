"""Focus mode timer handlers."""

import logging
from datetime import UTC, datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import get_focus_presets_keyboard, get_focus_running_keyboard
from app.bot.keyboards.reply import get_main_menu_keyboard
from app.bot.states.states import FocusState
from app.database.models.user import User
from app.services.focus.service import FocusService
from app.utils.i18n import DEFAULT_LANGUAGE, t

logger = logging.getLogger(__name__)
router = Router(name="focus_router")


@router.message(F.text.in_({"⏱ Focus Mode", "⏱ Diqqat rejimi", "⏱ Режим фокуса"}))
async def handle_focus_menu(
    message: Message,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer("Please /start the bot first.")
        return

    await message.answer(
        t("focus_menu", lang),
        reply_markup=get_focus_presets_keyboard(lang),
    )


@router.callback_query(F.data.startswith("focus_start_"))
async def handle_start_focus_session(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    minutes = int(callback.data.replace("focus_start_", ""))
    now_str = datetime.now(UTC).strftime("%H:%M")

    await state.set_state(FocusState.active_session)
    await state.update_data(
        focus_minutes=minutes,
        focus_start_timestamp=datetime.now(UTC).timestamp(),
    )

    await callback.message.edit_text(
        t("focus_running", lang, minutes=minutes, start_time=now_str),
        reply_markup=get_focus_running_keyboard(lang),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "focus_break_5")
async def handle_focus_break(callback: CallbackQuery) -> None:
    await callback.answer("☕ Take a deep breath and relax for 5 minutes!", show_alert=True)


@router.callback_query(FocusState.active_session, F.data == "focus_finish_now")
async def handle_finish_focus_early(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return

    data = await state.get_data()
    minutes = data.get("focus_minutes", 25)

    focus_service = FocusService(session)
    _, xp_earned, unlocked = await focus_service.record_completed_session(
        user_id=user.id,
        duration_minutes=minutes,
    )
    await state.clear()

    finish_text = t("focus_completed", lang, minutes=minutes, xp=xp_earned)
    for ach in unlocked:
        finish_text += f"\n\n🏆 **Achievement Unlocked**: {ach.icon} {ach.title} (+{ach.xp_reward} XP)!"

    await callback.message.edit_text(finish_text, parse_mode="Markdown")
    await callback.message.answer(
        "🎉 Great study session! Keep the momentum going!",
        reply_markup=get_main_menu_keyboard(lang),
    )
