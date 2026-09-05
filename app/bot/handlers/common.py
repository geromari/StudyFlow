"""Common navigation and cancellation handlers."""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.keyboards.reply import get_main_menu_keyboard
from app.utils.i18n import t

logger = logging.getLogger(__name__)
router = Router(name="common_router")


@router.message(F.text.in_({"❌ Cancel", "❌ Bekor qilish", "❌ Отмена", "/cancel"}))
async def handle_cancel(message: Message, state: FSMContext, lang: str = "en") -> None:
    """Clear any active FSM state and return to main menu."""
    await state.clear()
    await message.answer(
        t("action_cancelled", lang),
        reply_markup=get_main_menu_keyboard(lang),
    )


@router.callback_query(F.data.in_({"cancel", "quiz_cancel", "focus_cancel"}))
async def handle_callback_cancel(callback: CallbackQuery, state: FSMContext, lang: str = "en") -> None:
    """Cancel via inline callback."""
    await state.clear()
    await callback.answer(t("action_cancelled", lang))
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer(
        t("action_cancelled", lang),
        reply_markup=get_main_menu_keyboard(lang),
    )
