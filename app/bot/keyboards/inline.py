"""Inline keyboards for interactive actions and navigation."""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.database.models.goal import Goal
from app.database.models.study_task import StudyTask
from app.database.models.subject import Subject, Topic
from app.utils.i18n import SUPPORTED_LANGUAGES, t


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for selecting preferred language."""
    buttons = []
    for code, label in SUPPORTED_LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"lang_{code}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_target_presets_keyboard() -> InlineKeyboardMarkup:
    """Presets for daily study minutes during registration."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ 15 min", callback_data="target_15"),
                InlineKeyboardButton(text="🎯 30 min", callback_data="target_30"),
            ],
            [
                InlineKeyboardButton(text="🔥 45 min", callback_data="target_45"),
                InlineKeyboardButton(text="🚀 60 min", callback_data="target_60"),
            ],
        ]
    )


def get_subjects_keyboard(subjects: list[Subject], lang: str = "en") -> InlineKeyboardMarkup:
    """Keyboard displaying all subjects with option to add a new one."""
    keyboard = []
    for subj in subjects:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{subj.color_icon} {subj.name} ({subj.progress_percent}%)",
                callback_data=f"subj_view_{subj.id}",
            )
        ])
    keyboard.append([
        InlineKeyboardButton(text=t("btn_add_subject", lang), callback_data="subj_add")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_subject_actions_keyboard(subject_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    """Action menu for a single subject."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_topics", lang), callback_data=f"topics_view_{subject_id}"),
                InlineKeyboardButton(text=t("btn_start_study_subject", lang), callback_data=f"study_subj_{subject_id}"),
            ],
            [
                InlineKeyboardButton(text=t("btn_rename_subject", lang), callback_data=f"subj_rename_{subject_id}"),
                InlineKeyboardButton(text=t("btn_delete_subject", lang), callback_data=f"subj_del_conf_{subject_id}"),
            ],
            [
                InlineKeyboardButton(text=t("btn_back", lang), callback_data="subj_list"),
            ],
        ]
    )


def get_confirm_delete_keyboard(subject_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    """Confirmation before deleting a subject."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_delete_subject", lang), callback_data=f"subj_del_{subject_id}"),
                InlineKeyboardButton(text=t("btn_cancel", lang), callback_data=f"subj_view_{subject_id}"),
            ]
        ]
    )


def get_topics_keyboard(subject_id: int, topics: list[Topic], lang: str = "en") -> InlineKeyboardMarkup:
    """List topics with toggle completion and add new topic button."""
    keyboard = []
    for top in topics:
        icon = "✅" if top.is_completed else "⬜"
        keyboard.append([
            InlineKeyboardButton(
                text=f"{icon} {top.name}",
                callback_data=f"topic_toggle_{top.id}",
            ),
            InlineKeyboardButton(text="🗑", callback_data=f"topic_del_{top.id}"),
        ])
    keyboard.append([
        InlineKeyboardButton(text=t("btn_add_topic", lang), callback_data=f"topic_add_{subject_id}")
    ])
    keyboard.append([
        InlineKeyboardButton(text=t("btn_back", lang), callback_data=f"subj_view_{subject_id}")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_subject_study_menu_keyboard(subject_id: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Study options menu when clicking 'O'rganishni boshlash'."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_study_focus_15", lang), callback_data=f"focus_start_15_{subject_id}"),
                InlineKeyboardButton(text=t("btn_study_focus_25", lang), callback_data=f"focus_start_25_{subject_id}"),
            ],
            [
                InlineKeyboardButton(text=t("btn_study_focus_45", lang), callback_data=f"focus_start_45_{subject_id}"),
                InlineKeyboardButton(text=t("btn_study_quiz", lang), callback_data=f"quiz_subj_{subject_id}"),
            ],
            [
                InlineKeyboardButton(text=t("btn_study_ai_explain", lang), callback_data=f"ai_subj_{subject_id}"),
            ],
            [
                InlineKeyboardButton(text=t("btn_back", lang), callback_data=f"subj_view_{subject_id}"),
            ],
        ]
    )


def get_quiz_subject_select_keyboard(subjects: list[Subject], lang: str = "en") -> InlineKeyboardMarkup:
    """Select subject for quiz."""
    keyboard = []
    for subj in subjects:
        keyboard.append([
            InlineKeyboardButton(text=f"{subj.color_icon} {subj.name}", callback_data=f"quiz_subj_{subj.id}")
        ])
    keyboard.append([
        InlineKeyboardButton(text=t("quiz_general_knowledge", lang), callback_data="quiz_subj_0")
    ])
    keyboard.append([
        InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="quiz_cancel")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_quiz_difficulty_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Difficulty selector."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("diff_easy", lang), callback_data="quiz_diff_easy"),
                InlineKeyboardButton(text=t("diff_medium", lang), callback_data="quiz_diff_medium"),
                InlineKeyboardButton(text=t("diff_hard", lang), callback_data="quiz_diff_hard"),
            ],
            [
                InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="quiz_cancel")
            ],
        ]
    )


def get_quiz_count_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    """Number of questions selector."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="3", callback_data="quiz_cnt_3"),
                InlineKeyboardButton(text="5", callback_data="quiz_cnt_5"),
                InlineKeyboardButton(text="10", callback_data="quiz_cnt_10"),
            ],
            [
                InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="quiz_cancel")
            ],
        ]
    )


def get_quiz_options_keyboard(options: dict[str, str], current_index: int, total: int) -> InlineKeyboardMarkup:
    """Render compact, clearly visible options buttons A, B, C, D."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🅰️ A", callback_data=f"quiz_ans_A_{current_index}"),
                InlineKeyboardButton(text="🅱️ B", callback_data=f"quiz_ans_B_{current_index}"),
            ],
            [
                InlineKeyboardButton(text="🅲 C", callback_data=f"quiz_ans_C_{current_index}"),
                InlineKeyboardButton(text="🅳 D", callback_data=f"quiz_ans_D_{current_index}"),
            ],
        ]
    )


def get_quiz_next_keyboard(next_index: int, total: int, lang: str = "uz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=t("btn_quiz_next", lang, next=next_index + 1, total=total), callback_data=f"quiz_next_{next_index}")]
        ]
    )


def get_study_plan_keyboard(tasks: list[StudyTask], lang: str = "en") -> InlineKeyboardMarkup:
    keyboard = []
    for task in tasks:
        icon = "✅" if task.is_completed else "⬜"
        time_prefix = f"[{task.scheduled_time}] " if task.scheduled_time else ""
        keyboard.append([
            InlineKeyboardButton(
                text=f"{icon} {time_prefix}{task.title} ({task.duration_minutes}m)",
                callback_data=f"task_toggle_{task.id}",
            )
        ])
    keyboard.append([
        InlineKeyboardButton(text=t("btn_generate_plan", lang), callback_data="plan_generate"),
        InlineKeyboardButton(text=t("btn_add_task", lang), callback_data="task_add"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_goals_keyboard(goals: list[Goal], lang: str = "en") -> InlineKeyboardMarkup:
    keyboard = []
    for goal in goals:
        icon = "🏆" if goal.is_completed else "🎯"
        keyboard.append([
            InlineKeyboardButton(
                text=f"{icon} {goal.title} [{goal.progress_percent}%]",
                callback_data=f"goal_view_{goal.id}",
            )
        ])
    keyboard.append([
        InlineKeyboardButton(text=t("btn_add_goal", lang), callback_data="goal_add")
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_goal_actions_keyboard(goal_id: int, is_completed: bool, lang: str = "en") -> InlineKeyboardMarkup:
    keyboard = []
    if not is_completed:
        keyboard.append([
            InlineKeyboardButton(text="✅ Mark Completed", callback_data=f"goal_complete_{goal_id}"),
            InlineKeyboardButton(text="+25% Progress", callback_data=f"goal_prog_{goal_id}_25"),
        ])
    keyboard.append([
        InlineKeyboardButton(text="🗑 Delete Goal", callback_data=f"goal_del_{goal_id}"),
        InlineKeyboardButton(text=t("btn_back", lang), callback_data="goals_list"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_focus_presets_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ 15 min", callback_data="focus_start_15"),
                InlineKeyboardButton(text="🍅 25 min", callback_data="focus_start_25"),
            ],
            [
                InlineKeyboardButton(text="🎯 45 min", callback_data="focus_start_45"),
                InlineKeyboardButton(text="☕ 5 min Break", callback_data="focus_break_5"),
            ],
        ]
    )


def get_focus_running_keyboard(lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Finish Early", callback_data="focus_finish_now"),
                InlineKeyboardButton(text=t("btn_stop_focus", lang), callback_data="focus_cancel"),
            ]
        ]
    )


def get_pdf_menu_keyboard(doc_id: int, lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_pdf_summary", lang), callback_data=f"pdf_sum_{doc_id}"),
                InlineKeyboardButton(text=t("btn_pdf_qa", lang), callback_data=f"pdf_qa_{doc_id}"),
            ],
            [
                InlineKeyboardButton(text=t("btn_pdf_quiz", lang), callback_data=f"pdf_quiz_{doc_id}"),
            ],
        ]
    )


def get_settings_keyboard(reminders_enabled: bool, lang: str = "uz") -> InlineKeyboardMarkup:
    rem_text = t("btn_disable_reminders", lang) if reminders_enabled else t("btn_enable_reminders", lang)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_change_language", lang), callback_data="set_lang"),
                InlineKeyboardButton(text=t("btn_change_target", lang), callback_data="set_target"),
            ],
            [
                InlineKeyboardButton(text=rem_text, callback_data="set_toggle_rem"),
                InlineKeyboardButton(text=t("btn_change_rem_time", lang), callback_data="set_rem_time"),
            ],
        ]
    )


def get_admin_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_admin_stats", lang), callback_data="admin_stats"),
                InlineKeyboardButton(text=t("btn_admin_broadcast", lang), callback_data="admin_broadcast"),
            ],
            [
                InlineKeyboardButton(text=t("btn_admin_ban", lang), callback_data="admin_ban"),
                InlineKeyboardButton(text=t("btn_admin_unban", lang), callback_data="admin_unban"),
            ],
        ]
    )
