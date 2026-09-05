"""Unit and integration tests for Telegram bot handlers."""

from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage, StorageKey
from aiogram.types import Chat, Message
from aiogram.types import User as TgUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.common import handle_cancel
from app.bot.handlers.goals import handle_goals_menu
from app.bot.handlers.progress import handle_progress_menu
from app.bot.handlers.start import handle_start
from app.bot.handlers.streak import handle_streak_menu
from app.bot.handlers.subjects import handle_subjects_menu
from app.bot.states.states import RegistrationState
from app.database.repositories.user import UserRepository


def make_tg_user(id: int = 12345, first_name: str = "TestUser", username: str = "testuser") -> TgUser:
    return TgUser(
        id=id,
        is_bot=False,
        first_name=first_name,
        last_name=None,
        username=username,
        language_code="en",
    )


def make_message(text: str, user: TgUser | None = None) -> Message:
    tg_user = user or make_tg_user()
    chat = Chat(id=tg_user.id, type="private")
    msg = MagicMock(spec=Message)
    msg.text = text
    msg.from_user = tg_user
    msg.chat = chat
    msg.answer = AsyncMock()
    return msg


@pytest.mark.asyncio
async def test_handle_cancel() -> None:
    storage = MemoryStorage()
    key = StorageKey(bot_id=1, chat_id=123, user_id=123)
    state = FSMContext(storage=storage, key=key)
    await state.set_state(RegistrationState.waiting_for_language)

    msg = make_message(text="❌ Cancel")
    await handle_cancel(msg, state, lang="en")

    # State should be cleared
    current_state = await state.get_state()
    assert current_state is None
    msg.answer.assert_called_once()


@pytest.mark.asyncio
async def test_handle_start_new_user(db_session: AsyncSession) -> None:
    storage = MemoryStorage()
    key = StorageKey(bot_id=1, chat_id=10001, user_id=10001)
    state = FSMContext(storage=storage, key=key)

    msg = make_message(text="/start", user=make_tg_user(id=10001, first_name="Newbie"))
    await handle_start(msg, state, session=db_session, user=None, lang="en")

    # State should now be waiting for language
    current_state = await state.get_state()
    assert current_state == RegistrationState.waiting_for_language.state
    msg.answer.assert_called_once()


@pytest.mark.asyncio
async def test_handle_start_existing_user(
    db_session: AsyncSession, user_repo: UserRepository
) -> None:
    db_user = await user_repo.create_user_with_settings(
        telegram_id=20002, first_name="OldFriend"
    )

    storage = MemoryStorage()
    key = StorageKey(bot_id=1, chat_id=20002, user_id=20002)
    state = FSMContext(storage=storage, key=key)

    msg = make_message(text="/start", user=make_tg_user(id=20002))
    await handle_start(msg, state, session=db_session, user=db_user, lang="en")

    msg.answer.assert_called_once()
    call_args = msg.answer.call_args[0][0]
    assert "Welcome back" in call_args


@pytest.mark.asyncio
async def test_handle_subjects_menu(
    db_session: AsyncSession, user_repo: UserRepository
) -> None:
    db_user = await user_repo.create_user_with_settings(
        telegram_id=30003, first_name="SubjectLearner"
    )
    msg = make_message(text="📚 My Subjects", user=make_tg_user(id=30003))

    await handle_subjects_menu(msg, session=db_session, user=db_user, lang="en")
    msg.answer.assert_called_once()


@pytest.mark.asyncio
async def test_handle_goals_menu(
    db_session: AsyncSession, user_repo: UserRepository
) -> None:
    db_user = await user_repo.create_user_with_settings(
        telegram_id=40004, first_name="GoalSetter"
    )
    msg = make_message(text="🎯 My Goals", user=make_tg_user(id=40004))

    await handle_goals_menu(msg, session=db_session, user=db_user, lang="en")
    msg.answer.assert_called_once()


@pytest.mark.asyncio
async def test_handle_progress_menu(
    db_session: AsyncSession, user_repo: UserRepository
) -> None:
    db_user = await user_repo.create_user_with_settings(
        telegram_id=50005, first_name="ProgressTracker"
    )
    msg = make_message(text="📊 Progress", user=make_tg_user(id=50005))

    await handle_progress_menu(msg, session=db_session, user=db_user, lang="en")
    msg.answer.assert_called_once()
    call_text = msg.answer.call_args[0][0]
    assert "Your Progress" in call_text


@pytest.mark.asyncio
async def test_handle_streak_menu(
    db_session: AsyncSession, user_repo: UserRepository
) -> None:
    db_user = await user_repo.create_user_with_settings(
        telegram_id=60006, first_name="StreakKeeper"
    )
    msg = make_message(text="🔥 Streak", user=make_tg_user(id=60006))

    await handle_streak_menu(msg, user=db_user, lang="en")
    msg.answer.assert_called_once()
    call_text = msg.answer.call_args[0][0]
    assert "Streak" in call_text
