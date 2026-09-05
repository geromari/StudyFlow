"""Start command and onboarding registration flow."""

import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import get_language_keyboard, get_target_presets_keyboard
from app.bot.keyboards.reply import get_cancel_keyboard, get_main_menu_keyboard
from app.bot.states.states import RegistrationState
from app.database.models.user import User
from app.database.repositories.subject import SubjectRepository
from app.database.repositories.user import UserRepository
from app.services.referral.service import ReferralService
from app.utils.i18n import DEFAULT_LANGUAGE, t

logger = logging.getLogger(__name__)
router = Router(name="start_router")


@router.message(CommandStart())
async def handle_start(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not message.from_user:
        return

    # Check for referral code in start payload e.g. /start ref_12345
    referrer_telegram_id: int | None = None
    args = message.text.split(maxsplit=1) if message.text else []
    if len(args) > 1 and args[1].startswith("ref_"):
        ref_str = args[1].replace("ref_", "").strip()
        if ref_str.isdigit():
            referrer_telegram_id = int(ref_str)

    if user:
        # Existing user: greet and show main menu
        await state.clear()
        await message.answer(
            f"👋 Welcome back, {user.first_name}!\n\n" + t("main_menu_title", user.settings.language if user.settings else lang),
            reply_markup=get_main_menu_keyboard(user.settings.language if user.settings else lang),
        )
        return

    # New user: start registration flow
    await state.clear()
    await state.set_state(RegistrationState.waiting_for_language)
    if referrer_telegram_id:
        await state.update_data(referrer_telegram_id=referrer_telegram_id)

    name = message.from_user.first_name or "Friend"
    await message.answer(
        t("welcome_new_user", DEFAULT_LANGUAGE, name=name),
        reply_markup=get_language_keyboard(),
    )


@router.callback_query(RegistrationState.waiting_for_language, F.data.startswith("lang_"))
async def handle_registration_language(callback: CallbackQuery, state: FSMContext) -> None:
    chosen_lang = callback.data.replace("lang_", "")
    await state.update_data(chosen_lang=chosen_lang)
    await state.set_state(RegistrationState.waiting_for_interests)

    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        t("reg_ask_interests", chosen_lang),
        reply_markup=get_cancel_keyboard(chosen_lang),
    )


@router.message(RegistrationState.waiting_for_interests)
async def handle_registration_interests(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    chosen_lang = data.get("chosen_lang", DEFAULT_LANGUAGE)
    interests_text = message.text or ""

    await state.update_data(interests_text=interests_text)
    await state.set_state(RegistrationState.waiting_for_target)

    await message.answer(
        t("reg_ask_daily_target", chosen_lang),
        reply_markup=get_target_presets_keyboard(),
    )


@router.callback_query(RegistrationState.waiting_for_target, F.data.startswith("target_"))
async def handle_registration_target(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if not callback.from_user:
        return

    target_minutes = int(callback.data.replace("target_", ""))
    data = await state.get_data()
    chosen_lang = data.get("chosen_lang", DEFAULT_LANGUAGE)
    interests_text = data.get("interests_text", "")
    referrer_telegram_id = data.get("referrer_telegram_id")

    user_repo = UserRepository(session)
    subject_repo = SubjectRepository(session)

    # 1. Create User and UserSettings in DB
    new_user = await user_repo.create_user_with_settings(
        telegram_id=callback.from_user.id,
        first_name=callback.from_user.first_name or "Student",
        username=callback.from_user.username,
        language=chosen_lang,
        daily_target=target_minutes,
    )

    # 2. Add initial subject(s) based on user's interests input
    if interests_text and interests_text.strip():
        items = [s.strip() for s in interests_text.split(",") if s.strip()]
        existing_subjects = await subject_repo.get_user_subjects(new_user.id)
        existing_names = {s.name.strip().lower() for s in existing_subjects}
        for item in items[:4]:  # limit to first 4
            if item.strip().lower() not in existing_names:
                await subject_repo.create_subject(new_user.id, item)

    # 3. Process referral if applicable
    if referrer_telegram_id:
        referral_service = ReferralService(session)
        await referral_service.process_referral(
            referrer_telegram_id=referrer_telegram_id,
            new_user_telegram_id=callback.from_user.id,
        )

    await state.clear()
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass

    await callback.message.answer(
        t("reg_completed", chosen_lang) + "\n\n" + t("main_menu_title", chosen_lang),
        reply_markup=get_main_menu_keyboard(chosen_lang),
    )
