"""FSM states for all bot user flows."""

from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    waiting_for_language = State()
    waiting_for_interests = State()
    waiting_for_target = State()


class SubjectState(StatesGroup):
    waiting_for_subject_name = State()
    waiting_for_rename = State()
    waiting_for_topic_name = State()


class GoalState(StatesGroup):
    waiting_for_title = State()
    waiting_for_deadline = State()


class AIAssistantState(StatesGroup):
    waiting_for_prompt = State()


class QuizState(StatesGroup):
    choosing_subject = State()
    choosing_difficulty = State()
    choosing_count = State()
    active_quiz = State()


class StudyPlanState(StatesGroup):
    waiting_for_goal = State()
    waiting_for_target_minutes = State()
    waiting_for_manual_task = State()


class FocusState(StatesGroup):
    active_session = State()


class PDFState(StatesGroup):
    waiting_for_pdf = State()
    document_menu = State()
    waiting_for_question = State()


class SettingsState(StatesGroup):
    changing_target = State()
    changing_timezone = State()
    changing_reminder_time = State()


class AdminState(StatesGroup):
    waiting_for_broadcast_text = State()
    waiting_for_ban_user_id = State()
    waiting_for_unban_user_id = State()
