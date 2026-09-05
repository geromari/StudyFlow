"""AI Assistant Telegram handlers."""

import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.reply import get_cancel_keyboard, get_main_menu_keyboard
from app.bot.states.states import AIAssistantState
from app.database.models.user import User
from app.database.repositories.ai_conversation import AIConversationRepository
from app.services.ai.client import ai_service
from app.utils.i18n import DEFAULT_LANGUAGE, t
from app.utils.rate_limiter import default_limiter

logger = logging.getLogger(__name__)
router = Router(name="ai_assistant_router")


def get_ai_quick_actions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💡 Explain", callback_data="ai_mode_explain"),
                InlineKeyboardButton(text="📝 Summarize", callback_data="ai_mode_summarize"),
            ],
            [
                InlineKeyboardButton(text="🔍 Examples", callback_data="ai_mode_examples"),
                InlineKeyboardButton(text="📑 Study Notes", callback_data="ai_mode_study_notes"),
            ],
            [
                InlineKeyboardButton(text="🔢 Step-by-Step", callback_data="ai_mode_step_by_step"),
                InlineKeyboardButton(text="🧹 Clear History", callback_data="ai_clear_history"),
            ],
        ]
    )


@router.message(F.text.in_({"🤖 AI Assistant", "🤖 AI Yordamchi", "🤖 AI Помощник"}))
async def handle_ai_menu(
    message: Message,
    state: FSMContext,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer("Please /start the bot first.")
        return

    await state.set_state(AIAssistantState.waiting_for_prompt)
    await state.update_data(ai_mode=None)

    await message.answer(
        t("ai_assistant_intro", lang),
        reply_markup=get_ai_quick_actions_keyboard(),
    )
    await message.answer(
        "Type your question or study topic below:",
        reply_markup=get_cancel_keyboard(lang),
    )


@router.callback_query(AIAssistantState.waiting_for_prompt, F.data.startswith("ai_mode_"))
async def handle_ai_mode_select(callback: CallbackQuery, state: FSMContext) -> None:
    mode = callback.data.replace("ai_mode_", "")
    await state.update_data(ai_mode=mode)
    await callback.answer(f"Mode set: {mode.replace('_', ' ').capitalize()}")
    await callback.message.answer(f"Mode **{mode.replace('_', ' ').capitalize()}** active. Enter your topic:")


@router.callback_query(F.data == "ai_clear_history")
async def handle_clear_ai_history(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    ai_repo = AIConversationRepository(session)
    await ai_repo.clear_history(user.id)
    await callback.answer(t("ai_context_cleared", lang), show_alert=True)


@router.message(AIAssistantState.waiting_for_prompt)
async def handle_ai_query(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return

    prompt = (message.text or "").strip()
    if not prompt:
        return

    # Rate limiting: max 10 requests per minute
    key = f"ai_rate_{user.id}"
    if not await default_limiter.is_allowed(key, limit=10, period_seconds=60):
        await message.answer(t("rate_limit_exceeded", lang))
        return

    data = await state.get_data()
    mode = data.get("ai_mode")

    ai_repo = AIConversationRepository(session)

    # 1. Fetch recent conversation context (last 6 messages)
    history_records = await ai_repo.get_recent_history(user.id, limit=6)
    history = [{"role": h.role, "content": h.content} for h in history_records]

    # 2. Show thinking indicator
    thinking_msg = await message.answer(t("ai_thinking", lang))

    try:
        # 3. Call AI Service
        response_text, tokens = await ai_service.chat(
            conversation_history=history,
            user_prompt=prompt,
            mode=mode,
        )

        # 4. Save to conversation history
        await ai_repo.add_message(user.id, "user", prompt, tokens_used=0)
        await ai_repo.add_message(user.id, "assistant", response_text, tokens_used=tokens)

        # 5. Delete thinking indicator and answer user
        await thinking_msg.delete()
        await message.answer(response_text, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error answering AI query: {e}")
        try:
            await thinking_msg.delete()
        except Exception:
            pass
        await message.answer(t("generic_error", lang), reply_markup=get_main_menu_keyboard(lang))
