"""Pytest fixtures for StudyFlow."""

from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database.models import Base
from app.database.repositories import (
    AchievementRepository,
    AIConversationRepository,
    DocumentRepository,
    GoalRepository,
    QuizRepository,
    ReferralRepository,
    ReminderRepository,
    StudySessionRepository,
    StudyTaskRepository,
    SubjectRepository,
    UserRepository,
)


@pytest_asyncio.fixture
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    session_maker = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session_maker() as session:
        yield session


@pytest_asyncio.fixture
async def user_repo(db_session: AsyncSession) -> UserRepository:
    return UserRepository(db_session)


@pytest_asyncio.fixture
async def subject_repo(db_session: AsyncSession) -> SubjectRepository:
    return SubjectRepository(db_session)


@pytest_asyncio.fixture
async def goal_repo(db_session: AsyncSession) -> GoalRepository:
    return GoalRepository(db_session)


@pytest_asyncio.fixture
async def task_repo(db_session: AsyncSession) -> StudyTaskRepository:
    return StudyTaskRepository(db_session)


@pytest_asyncio.fixture
async def session_repo(db_session: AsyncSession) -> StudySessionRepository:
    return StudySessionRepository(db_session)


@pytest_asyncio.fixture
async def quiz_repo(db_session: AsyncSession) -> QuizRepository:
    return QuizRepository(db_session)


@pytest_asyncio.fixture
async def achievement_repo(db_session: AsyncSession) -> AchievementRepository:
    repo = AchievementRepository(db_session)
    await repo.seed_default_achievements()
    return repo


@pytest_asyncio.fixture
async def reminder_repo(db_session: AsyncSession) -> ReminderRepository:
    return ReminderRepository(db_session)


@pytest_asyncio.fixture
async def doc_repo(db_session: AsyncSession) -> DocumentRepository:
    return DocumentRepository(db_session)


@pytest_asyncio.fixture
async def ai_repo(db_session: AsyncSession) -> AIConversationRepository:
    return AIConversationRepository(db_session)


@pytest_asyncio.fixture
async def referral_repo(db_session: AsyncSession) -> ReferralRepository:
    return ReferralRepository(db_session)
