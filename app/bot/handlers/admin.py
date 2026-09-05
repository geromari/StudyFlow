"""Admin panel handlers."""

import logging

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters.admin import IsAdminFilter
from app.bot.keyboards.inline import get_admin_keyboard
from app.bot.keyboards.reply import get_cancel_keyboard, get_main_menu_keyboard
from app.bot.states.states import AdminState
from app.services.admin.service import AdminService
from app.utils.i18n import DEFAULT_LANGUAGE, t

logger = logging.getLogger(__name__)
router = Router(name="admin_router")
# Apply admin filter to all routes in this router
router.message.filter(IsAdminFilter())
router.callback_query.filter(IsAdminFilter())


@router.message(Command("admin"))
async def handle_admin_command(message: Message, lang: str = DEFAULT_LANGUAGE) -> None:
    await message.answer(
        t("admin_menu_title", lang),
        reply_markup=get_admin_keyboard(lang),
    )


@router.callback_query(F.data == "admin_stats")
async def handle_admin_analytics(
    callback: CallbackQuery,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    admin_service = AdminService(session)
    analytics = await admin_service.get_system_analytics()

    text = t(
        "admin_stats_title",
        lang,
        total_users=analytics["total_users"],
        active_users=analytics["active_users"],
        new_today=analytics["new_today"],
        quizzes_count=analytics["quizzes_count"],
        sessions_count=analytics["sessions_count"],
        ai_requests=analytics["ai_requests"],
        pdf_requests=analytics["pdf_requests"],
    )
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "admin_broadcast")
async def handle_admin_broadcast_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    await state.set_state(AdminState.waiting_for_broadcast_text)
    await callback.answer()
    await callback.message.answer(
        t("admin_broadcast_prompt", lang),
        reply_markup=get_cancel_keyboard(lang),
    )


@router.message(AdminState.waiting_for_broadcast_text)
async def handle_admin_broadcast_send(
    message: Message,
    bot: Bot,
    state: FSMContext,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    text_to_send = message.text or ""
    if not text_to_send.strip():
        return

    progress_msg = await message.answer("📢 Sending broadcast to all users...")
    admin_service = AdminService(session)

    sent, failed = await admin_service.broadcast_message(bot, text_to_send)
    await state.clear()

    await progress_msg.delete()
    result_text = t("admin_broadcast_result", lang, sent=sent, failed=failed)
    await message.answer(result_text, reply_markup=get_main_menu_keyboard(lang))


@router.callback_query(F.data == "admin_ban")
async def handle_admin_ban_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    await state.set_state(AdminState.waiting_for_ban_user_id)
    await callback.answer()
    await callback.message.answer(t("admin_ban_prompt", lang))


@router.message(AdminState.waiting_for_ban_user_id)
async def handle_admin_ban_execute(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    val = (message.text or "").strip()
    if not val.isdigit():
        await message.answer(t("admin_enter_numeric_id", lang))
        return

    target_id = int(val)
    admin_service = AdminService(session)
    success = await admin_service.ban_user(target_id)
    await state.clear()

    if success:
        await message.answer(t("admin_user_banned", lang, target_id=target_id), reply_markup=get_main_menu_keyboard(lang))
    else:
        await message.answer(t("admin_user_not_found", lang, target_id=target_id), reply_markup=get_main_menu_keyboard(lang))


@router.callback_query(F.data == "admin_unban")
async def handle_admin_unban_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    await state.set_state(AdminState.waiting_for_unban_user_id)
    await callback.answer()
    await callback.message.answer(t("admin_unban_prompt", lang))


@router.message(AdminState.waiting_for_unban_user_id)
async def handle_admin_unban_execute(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    val = (message.text or "").strip()
    if not val.isdigit():
        await message.answer(t("admin_enter_numeric_id", lang))
        return

    target_id = int(val)
    admin_service = AdminService(session)
    success = await admin_service.unban_user(target_id)
    await state.clear()

    if success:
        await message.answer(t("admin_user_unbanned", lang, target_id=target_id), reply_markup=get_main_menu_keyboard(lang))
    else:
        await message.answer(t("admin_user_not_found", lang, target_id=target_id), reply_markup=get_main_menu_keyboard(lang))
