"""Study Goals management handlers."""

from datetime import date, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import get_goal_actions_keyboard, get_goals_keyboard
from app.bot.keyboards.reply import get_cancel_keyboard, get_main_menu_keyboard
from app.bot.states.states import GoalState
from app.database.models.user import User
from app.database.repositories.goal import GoalRepository
from app.database.repositories.user import UserRepository
from app.services.achievements.service import AchievementService
from app.services.progress.gamification import XP_GOAL_COMPLETED
from app.utils.i18n import DEFAULT_LANGUAGE, t

router = Router(name="goals_router")


@router.message(F.text.in_({"🎯 My Goals", "🎯 Maqsadlarim", "🎯 Мои цели"}))
async def handle_goals_menu(
    message: Message,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer(t("please_start_first", lang))
        return

    goal_repo = GoalRepository(session)
    goals = await goal_repo.get_user_goals(user.id)

    if not goals:
        await message.answer(
            t("no_goals", lang),
            reply_markup=get_goals_keyboard([], lang),
        )
        return

    await message.answer(
        t("goals_title", lang, count=len(goals)),
        reply_markup=get_goals_keyboard(goals, lang),
    )


@router.callback_query(F.data == "goals_list")
async def handle_goals_list_callback(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    goal_repo = GoalRepository(session)
    goals = await goal_repo.get_user_goals(user.id)
    await callback.message.edit_text(
        t("goals_title", lang, count=len(goals)),
        reply_markup=get_goals_keyboard(goals, lang),
    )


@router.callback_query(F.data == "goal_add")
async def handle_goal_add_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    await state.set_state(GoalState.waiting_for_title)
    await callback.answer()
    await callback.message.answer(
        t("prompt_goal_title", lang),
        reply_markup=get_cancel_keyboard(lang),
    )


@router.message(GoalState.waiting_for_title)
async def handle_goal_title_entered(
    message: Message,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    title = (message.text or "").strip()
    if not title:
        return
    await state.update_data(goal_title=title)
    await state.set_state(GoalState.waiting_for_deadline)
    await message.answer(t("prompt_goal_deadline", lang))


@router.message(GoalState.waiting_for_deadline)
async def handle_goal_deadline_entered(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return

    days_str = (message.text or "").strip()
    days = int(days_str) if days_str.isdigit() else 30
    target_date = date.today() + timedelta(days=days)

    data = await state.get_data()
    title = data.get("goal_title", "Study Goal")

    goal_repo = GoalRepository(session)
    await goal_repo.create_goal(user.id, title=title, target_date=target_date)
    await state.clear()

    goals = await goal_repo.get_user_goals(user.id)
    await message.answer(
        t("goal_created", lang, title=title, days=days),
        reply_markup=get_main_menu_keyboard(lang),
    )
    await message.answer(
        t("goals_title", lang, count=len(goals)),
        reply_markup=get_goals_keyboard(goals, lang),
    )


@router.callback_query(F.data.startswith("goal_view_"))
async def handle_view_goal(
    callback: CallbackQuery,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    goal_id = int(callback.data.replace("goal_view_", ""))
    goal_repo = GoalRepository(session)
    goal = await goal_repo.get_by_id(goal_id)
    if not goal:
        return

    if lang == "uz":
        status = "✅ Bajarildi" if goal.is_completed else f"⏳ Jarayonda ({goal.progress_percent}%)"
        status_lbl, dline_lbl, no_dline, goal_lbl = "Holat", "Muddat", "Muddatsiz", "Maqsad"
    elif lang == "ru":
        status = "✅ Выполнено" if goal.is_completed else f"⏳ В процессе ({goal.progress_percent}%)"
        status_lbl, dline_lbl, no_dline, goal_lbl = "Статус", "Срок", "Без срока", "Цель"
    else:
        status = "✅ Completed" if goal.is_completed else f"⏳ In Progress ({goal.progress_percent}%)"
        status_lbl, dline_lbl, no_dline, goal_lbl = "Status", "Deadline", "No deadline", "Goal"

    deadline_str = goal.target_date.strftime("%Y-%m-%d") if goal.target_date else no_dline

    text = (
        f"🎯 **{goal_lbl}: {goal.title}**\n\n"
        f"{status_lbl}: {status}\n"
        f"{dline_lbl}: {deadline_str}"
    )
    await callback.message.edit_text(
        text,
        reply_markup=get_goal_actions_keyboard(goal_id, goal.is_completed, lang),
        parse_mode="Markdown",
    )


@router.callback_query(F.data.startswith("goal_prog_"))
async def handle_increment_goal_progress(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    parts = callback.data.split("_")
    goal_id = int(parts[2])
    increment = int(parts[3])

    goal_repo = GoalRepository(session)
    goal = await goal_repo.get_by_id(goal_id)
    if not goal:
        return

    new_prog = min(100, goal.progress_percent + increment)
    await goal_repo.update_goal(goal_id, progress_percent=new_prog)

    if new_prog == 100:
        ach_service = AchievementService(session)
        user_repo = UserRepository(session)
        await user_repo.add_xp(user.id, XP_GOAL_COMPLETED)
        unlocked = await ach_service.unlock_goal_achievement(user.id)
        msg = f"🎉 Goal completed! +{XP_GOAL_COMPLETED} XP" if lang == "en" else f"🎉 Maqsad bajarildi! +{XP_GOAL_COMPLETED} XP"
        if unlocked:
            msg += f"\n🏆 Unlocked: {unlocked.icon} {unlocked.title}!"
        await callback.answer(msg, show_alert=True)
    else:
        await callback.answer(f"{new_prog}%")

    goal = await goal_repo.get_by_id(goal_id)
    if goal:
        if lang == "uz":
            status = "✅ Bajarildi" if goal.is_completed else f"⏳ Jarayonda ({goal.progress_percent}%)"
            status_lbl, dline_lbl, no_dline, goal_lbl = "Holat", "Muddat", "Muddatsiz", "Maqsad"
        elif lang == "ru":
            status = "✅ Выполнено" if goal.is_completed else f"⏳ В процессе ({goal.progress_percent}%)"
            status_lbl, dline_lbl, no_dline, goal_lbl = "Статус", "Срок", "Без срока", "Цель"
        else:
            status = "✅ Completed" if goal.is_completed else f"⏳ In Progress ({goal.progress_percent}%)"
            status_lbl, dline_lbl, no_dline, goal_lbl = "Status", "Deadline", "No deadline", "Goal"

        deadline_str = goal.target_date.strftime("%Y-%m-%d") if goal.target_date else no_dline
        await callback.message.edit_text(
            f"🎯 **{goal_lbl}: {goal.title}**\n\n{status_lbl}: {status}\n{dline_lbl}: {deadline_str}",
            reply_markup=get_goal_actions_keyboard(goal_id, goal.is_completed, lang),
            parse_mode="Markdown",
        )


@router.callback_query(F.data.startswith("goal_complete_"))
async def handle_mark_goal_completed(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    goal_id = int(callback.data.replace("goal_complete_", ""))
    goal_repo = GoalRepository(session)
    goal = await goal_repo.mark_completed(goal_id)
    if not goal:
        return

    ach_service = AchievementService(session)
    user_repo = UserRepository(session)
    await user_repo.add_xp(user.id, XP_GOAL_COMPLETED)
    unlocked = await ach_service.unlock_goal_achievement(user.id)

    msg = t("goal_completed_msg", lang, title=goal.title, xp=XP_GOAL_COMPLETED)
    if unlocked:
        msg += f"\n🏆 Unlocked: {unlocked.icon} {unlocked.title}!"

    await callback.answer(msg, show_alert=True)
    goals = await goal_repo.get_user_goals(user.id)
    await callback.message.edit_text(
        t("goals_title", lang, count=len(goals)),
        reply_markup=get_goals_keyboard(goals, lang),
    )


@router.callback_query(F.data.startswith("goal_del_"))
async def handle_delete_goal(
    callback: CallbackQuery,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        return
    goal_id = int(callback.data.replace("goal_del_", ""))
    goal_repo = GoalRepository(session)
    goal = await goal_repo.get_by_id(goal_id)
    if goal:
        await goal_repo.delete(goal)

    goals = await goal_repo.get_user_goals(user.id)
    del_msg = "Maqsad o'chirildi." if lang == "uz" else ("Цель удалена." if lang == "ru" else "Goal deleted.")
    await callback.answer(del_msg)
    await callback.message.edit_text(
        t("goals_title", lang, count=len(goals)),
        reply_markup=get_goals_keyboard(goals, lang),
    )
