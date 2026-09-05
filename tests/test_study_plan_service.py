"""Unit tests for StudyPlanService."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.subject import SubjectRepository
from app.database.repositories.user import UserRepository
from app.services.ai.client import AIService
from app.services.study_plan.service import StudyPlanService


@pytest.mark.asyncio
async def test_study_plan_service_flow(
    db_session: AsyncSession,
    user_repo: UserRepository,
    subject_repo: SubjectRepository,
) -> None:
    user = await user_repo.create_user_with_settings(
        telegram_id=555111, first_name="Planner"
    )
    await subject_repo.create_subject(user.id, "Chemistry")

    ai = AIService(api_key="")
    plan_service = StudyPlanService(db_session, ai=ai)

    tasks = await plan_service.generate_daily_plan(
        user_id=user.id,
        goal="Ace Chemistry Exam",
        target_minutes=45,
    )
    assert len(tasks) > 0

    first_task = tasks[0]
    assert not first_task.is_completed

    # Complete task
    completed, xp, _ = await plan_service.complete_task(first_task.id, user.id)
    assert completed is True
    assert xp == 25

    # Check user gained XP
    updated_user = await user_repo.get_by_id(user.id)
    assert updated_user is not None
    assert updated_user.xp >= 25
