"""Settings configuration handlers."""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import (
    get_language_keyboard,
    get_settings_keyboard,
    get_target_presets_keyboard,
)
from app.bot.keyboards.reply import get_cancel_keyboard, get_main_menu_keyboard
from app.bot.states.states import SettingsState
from app.database.models.user import User
from app.database.repositories.reminder import ReminderRepository
from app.database.repositories.user import UserRepository
from app.utils.i18n import DEFAULT_LANGUAGE, t

router = Router(name="settings_router")


@router.message(F.text.in_({"⚙️ Settings", "⚙️ Sozlamalar", "⚙️ Настройки"}))
async def handle_settings_menu(
    message: Message,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user or not user.settings:
        await message.answer(t("please_start_first", lang))
        return

    rem_status = "Enabled" if user.settings.reminders_enabled else "Disabled"
    text = t(
        "settings_menu",
        lang,
        language=user.settings.language.upper(),
        timezone=user.settings.timezone,
        daily_target=user.settings.daily_study_target,
        reminders_status=f"{rem_status} ({user.settings.reminder_time})",
    )

    await message.answer(
        text,
        reply_markup=get_settings_keyboard(user.settings.reminders_enabled, lang),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "set_lang")
async def handle_settings_change_language(callback: CallbackQuery, lang: str = DEFAULT_LANGUAGE) -> None:
    await callback.message.edit_text(
        t("choose_lang_title", lang),
        reply_markup=get_language_keyboard(),
    )


@router.callback_query(F.data.startswith("lang_"))
async def handle_settings_save_language(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
) -> None:
    if not user:
        return
    chosen_lang = callback.data.replace("lang_", "")
    user_repo = UserRepository(session)
    await user_repo.update_settings(user.id, language=chosen_lang)

    await callback.answer(t("lang_updated", chosen_lang, lang=chosen_lang.upper()))
    await callback.message.answer(
        t("main_menu_title", chosen_lang),
        reply_markup=get_main_menu_keyboard(chosen_lang),
    )


@router.callback_query(F.data == "set_target")
async def handle_settings_change_target_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    await state.set_state(SettingsState.changing_target)
    await callback.message.edit_text(
        t("settings_select_target", lang),
        reply_markup=get_target_presets_keyboard(),
    )


@router.callback_query(SettingsState.changing_target, F.data.startswith("target_"))
async def handle_settings_save_target(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    target = int(callback.data.replace("target_", ""))
    user_repo = UserRepository(session)
    await user_repo.update_settings(user.id, daily_target=target)
    await state.clear()

    await callback.answer(t("target_updated", lang, target=target), show_alert=True)
    await callback.message.answer(
        t("main_menu_title", lang),
        reply_markup=get_main_menu_keyboard(lang),
    )


@router.callback_query(F.data == "set_toggle_rem")
async def handle_settings_toggle_reminders(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user or not user.settings:
        return

    new_status = not user.settings.reminders_enabled
    user_repo = UserRepository(session)
    reminder_repo = ReminderRepository(session)

    await user_repo.update_settings(user.id, reminders_enabled=new_status)
    await reminder_repo.set_reminder(
        user_id=user.id,
        time_str=user.settings.reminder_time,
        timezone=user.settings.timezone,
        is_enabled=new_status,
    )

    alert_text = t("reminders_enabled_alert", lang) if new_status else t("reminders_disabled_alert", lang)
    await callback.answer(alert_text)
    await callback.message.edit_reply_markup(
        reply_markup=get_settings_keyboard(new_status, lang)
    )


@router.callback_query(F.data == "set_rem_time")
async def handle_settings_change_time_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    await state.set_state(SettingsState.changing_reminder_time)
    await callback.answer()
    await callback.message.answer(
        t("settings_change_rem_prompt", lang),
        reply_markup=get_cancel_keyboard(lang),
    )


@router.message(SettingsState.changing_reminder_time)
async def handle_settings_save_time(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    time_val = (message.text or "").strip()
    # Simple validation HH:MM
    parts = time_val.split(":")
    if len(parts) != 2 or not parts[0].isdigit() or not parts[1].isdigit():
        await message.answer(t("time_invalid_format", lang))
        return

    hours, mins = int(parts[0]), int(parts[1])
    if not (0 <= hours <= 23 and 0 <= mins <= 59):
        await message.answer(t("time_invalid_range", lang))
        return

    formatted_time = f"{hours:02d}:{mins:02d}"
    user_repo = UserRepository(session)
    reminder_repo = ReminderRepository(session)

    await user_repo.update_settings(user.id, reminder_time=formatted_time)
    await reminder_repo.set_reminder(
        user_id=user.id,
        time_str=formatted_time,
        timezone=user.settings.timezone if user.settings else "UTC",
        is_enabled=user.settings.reminders_enabled if user.settings else True,
    )

    await state.clear()
    await message.answer(
        t("rem_time_saved", lang, time=formatted_time),
        reply_markup=get_main_menu_keyboard(lang),
    )
