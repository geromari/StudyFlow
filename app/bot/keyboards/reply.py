"""Reply keyboards for main menu and quick interactions."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.utils.i18n import t


def get_main_menu_keyboard(lang: str = "en") -> ReplyKeyboardMarkup:
    """Build the clean 11-button main user menu."""
    keyboard = [
        [
            KeyboardButton(text=t("menu_subjects", lang)),
            KeyboardButton(text=t("menu_ai", lang)),
        ],
        [
            KeyboardButton(text=t("menu_quiz", lang)),
            KeyboardButton(text=t("menu_study_plan", lang)),
        ],
        [
            KeyboardButton(text=t("menu_goals", lang)),
            KeyboardButton(text=t("menu_progress", lang)),
        ],
        [
            KeyboardButton(text=t("menu_streak", lang)),
            KeyboardButton(text=t("menu_focus", lang)),
        ],
        [
            KeyboardButton(text=t("menu_pdf", lang)),
            KeyboardButton(text=t("menu_achievements", lang)),
        ],
        [
            KeyboardButton(text=t("menu_settings", lang)),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_cancel_keyboard(lang: str = "en") -> ReplyKeyboardMarkup:
    """Cancel button reply keyboard to prevent getting stuck in states."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t("btn_cancel", lang))]],
        resize_keyboard=True,
    )


def get_skip_cancel_keyboard(lang: str = "en") -> ReplyKeyboardMarkup:
    """Skip and Cancel buttons reply keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="⏩ Skip"),
                KeyboardButton(text=t("btn_cancel", lang)),
            ]
        ],
        resize_keyboard=True,
    )
