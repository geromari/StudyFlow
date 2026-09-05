"""Quiz generator and interactive quiz flow handlers."""

import html
import json
import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import (
    get_quiz_count_keyboard,
    get_quiz_difficulty_keyboard,
    get_quiz_next_keyboard,
    get_quiz_options_keyboard,
    get_quiz_subject_select_keyboard,
)
from app.bot.keyboards.reply import get_main_menu_keyboard
from app.bot.states.states import QuizState
from app.database.models.user import User
from app.database.repositories.quiz import QuizRepository
from app.database.repositories.subject import SubjectRepository
from app.services.quiz.service import QuizService
from app.utils.i18n import DEFAULT_LANGUAGE, t

logger = logging.getLogger(__name__)
router = Router(name="quiz_router")


@router.message(F.text.in_({"📝 Quiz", "📝 Test", "📝 Викторина"}))
async def handle_quiz_menu(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer(t("please_start_first", lang))
        return

    subject_repo = SubjectRepository(session)
    subjects = await subject_repo.get_user_subjects(user.id)

    await state.set_state(QuizState.choosing_subject)
    await message.answer(
        t("quiz_intro", lang),
        reply_markup=get_quiz_subject_select_keyboard(subjects, lang),
    )


@router.callback_query(QuizState.choosing_subject, F.data.startswith("quiz_subj_"))
async def handle_quiz_subject_chosen(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    subj_id_val = int(callback.data.replace("quiz_subj_", ""))
    subject_name = "General Knowledge"
    if subj_id_val != 0:
        subject_repo = SubjectRepository(session)
        subj = await subject_repo.get_by_id(subj_id_val)
        if subj:
            subject_name = subj.name

    await state.update_data(
        quiz_subject_id=subj_id_val if subj_id_val != 0 else None,
        quiz_subject_name=subject_name,
    )
    await state.set_state(QuizState.choosing_difficulty)

    await callback.message.edit_text(
        t("quiz_select_difficulty", lang),
        reply_markup=get_quiz_difficulty_keyboard(lang),
    )


@router.callback_query(QuizState.choosing_difficulty, F.data.startswith("quiz_diff_"))
async def handle_quiz_difficulty_chosen(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    difficulty = callback.data.replace("quiz_diff_", "")
    await state.update_data(quiz_difficulty=difficulty)
    await state.set_state(QuizState.choosing_count)

    await callback.message.edit_text(
        t("quiz_select_count", lang),
        reply_markup=get_quiz_count_keyboard(lang),
    )


@router.callback_query(QuizState.choosing_count, F.data.startswith("quiz_cnt_"))
async def handle_quiz_count_chosen_and_start(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return

    count = int(callback.data.replace("quiz_cnt_", ""))
    data = await state.get_data()
    subject_id = data.get("quiz_subject_id")
    subject_name = data.get("quiz_subject_name", "General Studies")
    difficulty = data.get("quiz_difficulty", "medium")

    await callback.message.edit_text(t("quiz_generating", lang))

    quiz_service = QuizService(session)
    try:
        quiz = await quiz_service.generate_and_save_quiz(
            user_id=user.id,
            subject_id=subject_id,
            subject_name=subject_name,
            difficulty=difficulty,
            count=count,
            language=lang,
        )
    except Exception as e:
        logger.error(f"Quiz generation failed: {e}")
        await callback.message.edit_text(
            t("generic_error", lang),
            reply_markup=None,
        )
        await state.clear()
        return

    # Store quiz session state in FSM
    await state.set_state(QuizState.active_quiz)
    await state.update_data(
        active_quiz_id=quiz.id,
        current_question_index=0,
        score=0,
        total_questions=len(quiz.questions),
    )

    # Show question 0
    await send_quiz_question(callback.message, quiz.id, 0, session, lang)


async def send_quiz_question(
    message: Message,
    quiz_id: int,
    question_index: int,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    quiz_repo = QuizRepository(session)
    quiz = await quiz_repo.get_quiz_with_questions(quiz_id)
    if not quiz or question_index >= len(quiz.questions):
        return

    question = quiz.questions[question_index]
    options_dict = json.loads(question.options)

    q_header = t("quiz_question_header", lang)
    opts_header = t("quiz_options_title", lang)
    pick_prompt = t("quiz_select_answer", lang)

    text = (
        f"📝 <b>{q_header} {question_index + 1}/{len(quiz.questions)}</b>:\n\n"
        f"<b>{html.escape(question.question_text)}</b>\n\n"
        f"📌 <i>{opts_header}</i>\n"
        f"🇦 <b>A)</b> {html.escape(str(options_dict.get('A', '')))}\n"
        f"🇧 <b>B)</b> {html.escape(str(options_dict.get('B', '')))}\n"
        f"🇨 <b>C)</b> {html.escape(str(options_dict.get('C', '')))}\n"
        f"🇩 <b>D)</b> {html.escape(str(options_dict.get('D', '')))}\n\n"
        f"👇 <i>{pick_prompt}</i>"
    )

    await message.edit_text(
        text,
        reply_markup=get_quiz_options_keyboard(options_dict, question_index, len(quiz.questions)),
        parse_mode="HTML",
    )


@router.callback_query(QuizState.active_quiz, F.data.startswith("quiz_ans_"))
async def handle_quiz_answer(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return

    parts = callback.data.split("_")
    selected_option = parts[2]
    current_index = int(parts[3])

    data = await state.get_data()
    quiz_id = data["active_quiz_id"]
    score = data.get("score", 0)
    total_questions = data["total_questions"]

    quiz_repo = QuizRepository(session)
    quiz = await quiz_repo.get_quiz_with_questions(quiz_id)
    if not quiz or current_index >= len(quiz.questions):
        return

    question = quiz.questions[current_index]
    quiz_service = QuizService(session)
    is_correct = await quiz_service.submit_answer(
        quiz_id=quiz_id,
        question_id=question.id,
        user_id=user.id,
        selected_option=selected_option,
        correct_option=question.correct_option,
    )

    if is_correct:
        score += 1
        await state.update_data(score=score)
        result_text = t(
            "quiz_correct",
            lang,
            explanation=question.explanation or ("Ajoyib!" if lang == "uz" else "Well done!"),
        )
    else:
        result_text = t(
            "quiz_wrong",
            lang,
            correct=question.correct_option,
            explanation=question.explanation or ("Ushbu mavzuni mustahkamlang." if lang == "uz" else "Review this topic."),
        )

    next_index = current_index + 1
    if next_index < total_questions:
        # Show feedback with button to advance to next question
        await callback.message.edit_text(
            result_text,
            reply_markup=get_quiz_next_keyboard(next_index, total_questions, lang),
            parse_mode="Markdown",
        )
    else:
        # Finalize Quiz
        xp_earned, unlocked = await quiz_service.finalize_quiz(
            quiz_id=quiz_id,
            user_id=user.id,
            score=score,
            total_questions=total_questions,
        )
        wrong_count = total_questions - score
        percentage = int((score / total_questions) * 100) if total_questions > 0 else 0

        final_msg = t(
            "quiz_finished",
            lang,
            score=score,
            total=total_questions,
            percentage=percentage,
            correct_count=score,
            wrong_count=wrong_count,
            xp=xp_earned,
        )

        for ach in unlocked:
            final_msg += "\n\n" + t(
                "achievement_unlocked_notification",
                lang,
                icon=ach.icon,
                title=ach.title,
                xp=ach.xp_reward,
            )

        await callback.message.edit_text(final_msg, parse_mode="Markdown")
        await callback.message.answer(
            t("quiz_keep_it_up", lang),
            reply_markup=get_main_menu_keyboard(lang),
        )
        await state.clear()


@router.callback_query(QuizState.active_quiz, F.data.startswith("quiz_next_"))
async def handle_quiz_next_question(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    next_index = int(callback.data.replace("quiz_next_", ""))
    data = await state.get_data()
    quiz_id = data["active_quiz_id"]
    await state.update_data(current_question_index=next_index)

    await send_quiz_question(callback.message, quiz_id, next_index, session, lang)
