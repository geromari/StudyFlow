"""Study Plan management handlers."""

import logging
from datetime import date

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import get_study_plan_keyboard
from app.bot.keyboards.reply import get_cancel_keyboard, get_main_menu_keyboard
from app.bot.states.states import StudyPlanState
from app.database.models.user import User
from app.database.repositories.study_task import StudyTaskRepository
from app.services.study_plan.service import StudyPlanService
from app.utils.i18n import DEFAULT_LANGUAGE, t

logger = logging.getLogger(__name__)
router = Router(name="study_plan_router")


@router.message(F.text.in_({"📅 Study Plan", "📅 O'quv rejasi", "📅 План учебы"}))
async def handle_study_plan_menu(
    message: Message,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer("Please /start the bot first.")
        return

    task_repo = StudyTaskRepository(session)
    tasks = await task_repo.get_tasks_for_date(user.id, date.today())

    if not tasks:
        await message.answer(
            t("no_plan_today", lang),
            reply_markup=get_study_plan_keyboard([], lang),
        )
        return

    await message.answer(
        t("plan_intro", lang, tasks=f"{len(tasks)} tasks scheduled for today"),
        reply_markup=get_study_plan_keyboard(tasks, lang),
    )


@router.callback_query(F.data == "plan_generate")
async def handle_plan_generate_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    await state.set_state(StudyPlanState.waiting_for_goal)
    await callback.answer()
    await callback.message.answer(
        "What is your study goal for today?\n(e.g., 'Prepare for English midterm', 'Understand dynamic programming'):",
        reply_markup=get_cancel_keyboard(lang),
    )


@router.message(StudyPlanState.waiting_for_goal)
async def handle_plan_goal_entered(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    goal_text = (message.text or "").strip()
    if not goal_text:
        return

    target_minutes = user.settings.daily_study_target if user.settings else 45
    wait_msg = await message.answer("⚡ Generating your personalized daily study schedule with AI...")

    plan_service = StudyPlanService(session)
    try:
        tasks = await plan_service.generate_daily_plan(
            user_id=user.id,
            goal=goal_text,
            target_minutes=target_minutes,
            language=lang,
        )
        await wait_msg.delete()
        await state.clear()

        await message.answer(
            t("plan_intro", lang, tasks=f"Generated {len(tasks)} tasks:"),
            reply_markup=get_study_plan_keyboard(tasks, lang),
        )
        await message.answer("🎓 Here is your schedule! Tap each task when done.", reply_markup=get_main_menu_keyboard(lang))
    except Exception as e:
        logger.error(f"Error generating study plan: {e}")
        try:
            await wait_msg.delete()
        except Exception:
            pass
        await message.answer(t("generic_error", lang), reply_markup=get_main_menu_keyboard(lang))


@router.callback_query(F.data.startswith("task_toggle_"))
async def handle_task_toggle(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return

    task_id = int(callback.data.replace("task_toggle_", ""))
    plan_service = StudyPlanService(session)
    is_completed, xp_awarded, unlocked = await plan_service.complete_task(task_id, user.id)

    # Refresh task list
    task_repo = StudyTaskRepository(session)
    tasks = await task_repo.get_tasks_for_date(user.id, date.today())
    await callback.message.edit_reply_markup(
        reply_markup=get_study_plan_keyboard(tasks, lang)
    )

    if is_completed:
        notice = t("task_completed", lang, xp=xp_awarded)
        for ach in unlocked:
            notice += f"\n🏆 Unlocked: {ach.icon} {ach.title} (+{ach.xp_reward} XP)!"
        await callback.answer(notice, show_alert=True)
    else:
        await callback.answer("Task marked as pending.")


@router.callback_query(F.data == "task_add")
async def handle_manual_task_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    await state.set_state(StudyPlanState.waiting_for_manual_task)
    await callback.answer()
    await callback.message.answer(
        "Enter task title:\n(e.g., 'Solve 10 algebra problems - 30 min')",
        reply_markup=get_cancel_keyboard(lang),
    )


@router.message(StudyPlanState.waiting_for_manual_task)
async def handle_save_manual_task(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    title = (message.text or "").strip()
    if not title:
        return

    task_repo = StudyTaskRepository(session)
    await task_repo.create_task(
        user_id=user.id,
        title=title,
        duration_minutes=25,
        plan_date=date.today(),
    )
    await state.clear()

    tasks = await task_repo.get_tasks_for_date(user.id, date.today())
    await message.answer("✅ Task added to today's plan!", reply_markup=get_main_menu_keyboard(lang))
    await message.answer(
        t("plan_intro", lang, tasks=f"{len(tasks)} tasks:"),
        reply_markup=get_study_plan_keyboard(tasks, lang),
    )
