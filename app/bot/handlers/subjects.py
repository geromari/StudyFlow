"""Subjects and Topics management handlers."""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import (
    get_confirm_delete_keyboard,
    get_subject_actions_keyboard,
    get_subject_study_menu_keyboard,
    get_subjects_keyboard,
    get_topics_keyboard,
)
from app.bot.keyboards.reply import get_cancel_keyboard, get_main_menu_keyboard
from app.bot.states.states import AIAssistantState, SubjectState
from app.database.models.subject import Topic
from app.database.models.user import User
from app.database.repositories.subject import SubjectRepository
from app.utils.i18n import DEFAULT_LANGUAGE, t

router = Router(name="subjects_router")


@router.message(F.text.in_({"📚 My Subjects", "📚 Fanlarim", "📚 Мои предметы"}))
async def handle_subjects_menu(
    message: Message,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer(t("please_start_first", lang))
        return

    subject_repo = SubjectRepository(session)
    subjects = await subject_repo.get_user_subjects(user.id)

    if not subjects:
        await message.answer(
            t("no_subjects", lang),
            reply_markup=get_subjects_keyboard([], lang),
        )
        return

    await message.answer(
        t("subjects_list_title", lang, count=len(subjects)),
        reply_markup=get_subjects_keyboard(subjects, lang),
    )


@router.callback_query(F.data == "subj_list")
async def handle_subjects_list_callback(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    subject_repo = SubjectRepository(session)
    subjects = await subject_repo.get_user_subjects(user.id)
    await callback.message.edit_text(
        t("subjects_list_title", lang, count=len(subjects)),
        reply_markup=get_subjects_keyboard(subjects, lang),
    )


@router.callback_query(F.data == "subj_add")
async def handle_add_subject_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    await state.set_state(SubjectState.waiting_for_subject_name)
    await callback.answer()
    await callback.message.answer(
        t("prompt_enter_subject_name", lang),
        reply_markup=get_cancel_keyboard(lang),
    )


@router.message(SubjectState.waiting_for_subject_name)
async def handle_save_subject(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    name = (message.text or "").strip()
    if not name:
        await message.answer(t("prompt_enter_subject_name", lang))
        return

    subject_repo = SubjectRepository(session)
    await subject_repo.create_subject(user.id, name)
    await state.clear()

    subjects = await subject_repo.get_user_subjects(user.id)
    await message.answer(
        t("subject_created", lang, name=name),
        reply_markup=get_main_menu_keyboard(lang),
    )
    await message.answer(
        t("subjects_list_title", lang, count=len(subjects)),
        reply_markup=get_subjects_keyboard(subjects, lang),
    )


@router.callback_query(F.data.startswith("subj_view_"))
async def handle_view_subject(
    callback: CallbackQuery,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    subj_id = int(callback.data.replace("subj_view_", ""))
    subject_repo = SubjectRepository(session)
    subject = await subject_repo.get_with_topics(subj_id)
    if not subject:
        await callback.answer(t("subject_not_found", lang))
        return

    topics_count = len(subject.topics)
    completed_count = sum(1 for t_item in subject.topics if t_item.is_completed)

    progress_info = t(
        "subject_view_progress",
        lang,
        percent=subject.progress_percent,
        completed=completed_count,
        total=topics_count,
    )

    text = f"{subject.color_icon} **{subject.name}**\n\n{progress_info}"
    await callback.message.edit_text(
        text,
        reply_markup=get_subject_actions_keyboard(subj_id, lang),
        parse_mode="Markdown",
    )


@router.callback_query(F.data.startswith("study_subj_"))
async def handle_study_subject(
    callback: CallbackQuery,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    subj_id = int(callback.data.replace("study_subj_", ""))
    subject_repo = SubjectRepository(session)
    subject = await subject_repo.get_by_id(subj_id)
    if not subject:
        await callback.answer(t("subject_not_found", lang))
        return

    text = t("study_subject_title", lang, name=subject.name)
    await callback.message.edit_text(
        text,
        reply_markup=get_subject_study_menu_keyboard(subj_id, lang),
        parse_mode="Markdown",
    )


@router.callback_query(F.data.startswith("ai_subj_"))
async def handle_ai_study_subject(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    subj_id = int(callback.data.replace("ai_subj_", ""))
    subject_repo = SubjectRepository(session)
    subject = await subject_repo.get_by_id(subj_id)
    if not subject:
        await callback.answer(t("subject_not_found", lang))
        return

    await state.set_state(AIAssistantState.waiting_for_prompt)
    await state.update_data(ai_mode="explain")
    await callback.answer()
    prompt_text = (
        f"🤖 **{subject.name}** bo'yicha AI yordamchi faollashdi.\n\n"
        f"Ushbu fan bo'yicha savolingizni yoki o'rganmoqchi bo'lgan mavzuni yozing:"
        if lang == "uz"
        else f"🤖 AI Assistant for **{subject.name}** is active.\n\nType your question or topic:"
    )
    await callback.message.answer(
        prompt_text,
        reply_markup=get_cancel_keyboard(lang),
    )


@router.callback_query(F.data.startswith("subj_del_conf_"))
async def handle_confirm_delete_subject(
    callback: CallbackQuery,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    subj_id = int(callback.data.replace("subj_del_conf_", ""))
    subject_repo = SubjectRepository(session)
    subject = await subject_repo.get_by_id(subj_id)
    if not subject:
        await callback.answer(t("subject_not_found", lang))
        return

    await callback.message.edit_text(
        t("confirm_delete_subject", lang, name=subject.name),
        reply_markup=get_confirm_delete_keyboard(subj_id, lang),
    )


@router.callback_query(F.data.startswith("subj_del_"))
async def handle_execute_delete_subject(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    subj_id = int(callback.data.replace("subj_del_", ""))
    subject_repo = SubjectRepository(session)
    subject = await subject_repo.get_by_id(subj_id)
    if subject:
        await subject_repo.delete(subject)

    subjects = await subject_repo.get_user_subjects(user.id)
    await callback.answer(t("subject_deleted", lang))
    await callback.message.edit_text(
        t("subjects_list_title", lang, count=len(subjects)),
        reply_markup=get_subjects_keyboard(subjects, lang),
    )


@router.callback_query(F.data.startswith("subj_rename_"))
async def handle_rename_subject_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    subj_id = int(callback.data.replace("subj_rename_", ""))
    await state.set_state(SubjectState.waiting_for_rename)
    await state.update_data(rename_subj_id=subj_id)
    await callback.answer()
    await callback.message.answer(
        t("prompt_enter_new_subject_name", lang),
        reply_markup=get_cancel_keyboard(lang),
    )


@router.message(SubjectState.waiting_for_rename)
async def handle_save_rename_subject(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    data = await state.get_data()
    subj_id = data.get("rename_subj_id")
    new_name = (message.text or "").strip()
    if not new_name or not subj_id:
        return

    subject_repo = SubjectRepository(session)
    await subject_repo.rename_subject(subj_id, new_name)
    await state.clear()
    await message.answer(
        t("subject_created", lang, name=new_name),
        reply_markup=get_main_menu_keyboard(lang),
    )


# Topics management
@router.callback_query(F.data.startswith("topics_view_"))
async def handle_view_topics(
    callback: CallbackQuery,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    subj_id = int(callback.data.replace("topics_view_", ""))
    subject_repo = SubjectRepository(session)
    subject = await subject_repo.get_with_topics(subj_id)
    if not subject:
        await callback.answer(t("subject_not_found", lang))
        return

    text = t("topics_list_title", lang, name=subject.name)
    await callback.message.edit_text(
        text,
        reply_markup=get_topics_keyboard(subj_id, subject.topics, lang),
        parse_mode="Markdown",
    )


@router.callback_query(F.data.startswith("topic_toggle_"))
async def handle_toggle_topic(
    callback: CallbackQuery,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    topic_id = int(callback.data.replace("topic_toggle_", ""))
    subject_repo = SubjectRepository(session)
    topic = await subject_repo.toggle_topic(topic_id)
    if not topic:
        return

    subject = await subject_repo.get_with_topics(topic.subject_id)
    if subject:
        await callback.message.edit_reply_markup(
            reply_markup=get_topics_keyboard(subject.id, subject.topics, lang)
        )
    await callback.answer("Topic updated!")


@router.callback_query(F.data.startswith("topic_del_"))
async def handle_delete_topic(
    callback: CallbackQuery,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    topic_id = int(callback.data.replace("topic_del_", ""))
    subject_repo = SubjectRepository(session)
    topic = await subject_repo.session.get(Topic, topic_id) if hasattr(subject_repo, "session") else None
    subj_id = topic.subject_id if topic else None

    await subject_repo.delete_topic(topic_id)
    if subj_id:
        subject = await subject_repo.get_with_topics(subj_id)
        if subject:
            await callback.message.edit_reply_markup(
                reply_markup=get_topics_keyboard(subject.id, subject.topics, lang)
            )
    await callback.answer("Topic deleted.")


@router.callback_query(F.data.startswith("topic_add_"))
async def handle_add_topic_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    subj_id = int(callback.data.replace("topic_add_", ""))
    await state.set_state(SubjectState.waiting_for_topic_name)
    await state.update_data(target_subject_id=subj_id)
    await callback.answer()
    await callback.message.answer(
        t("prompt_enter_topic_name", lang),
        reply_markup=get_cancel_keyboard(lang),
    )


@router.message(SubjectState.waiting_for_topic_name)
async def handle_save_topic(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    data = await state.get_data()
    subj_id = data.get("target_subject_id")
    name = (message.text or "").strip()
    if not name or not subj_id:
        return

    subject_repo = SubjectRepository(session)
    await subject_repo.add_topic(subj_id, name)
    await state.clear()
    await message.answer("✅ Topic added!", reply_markup=get_main_menu_keyboard(lang))
