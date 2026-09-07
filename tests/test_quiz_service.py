"""Unit tests for QuizService."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.user import UserRepository
from app.services.ai.client import AIService
from app.services.quiz.service import QuizService


@pytest.mark.asyncio
async def test_quiz_service_full_flow(
    db_session: AsyncSession, user_repo: UserRepository
) -> None:
    user = await user_repo.create_user_with_settings(
        telegram_id=999888, first_name="QuizTester"
    )

    ai = AIService(api_key="")  # mock
    quiz_service = QuizService(db_session, ai=ai)

    quiz = await quiz_service.generate_and_save_quiz(
        user_id=user.id,
        subject_id=None,
        subject_name="Physics",
        difficulty="medium",
        count=3,
    )

    assert quiz.id is not None
    assert quiz.total_questions == 3
    assert len(quiz.questions) == 3

    # Answer questions
    for q in quiz.questions:
        is_correct = await quiz_service.submit_answer(
            quiz_id=quiz.id,
            question_id=q.id,
            user_id=user.id,
            selected_option=q.correct_option,
            correct_option=q.correct_option,
        )
        assert is_correct is True

    # Finalize quiz
    xp, unlocked = await quiz_service.finalize_quiz(
        quiz_id=quiz.id,
        user_id=user.id,
        score=3,
        total_questions=3,
    )
    assert xp > 0

    # User XP and streak updated
    updated_user = await user_repo.get_by_id(user.id)
    assert updated_user is not None
    assert updated_user.xp >= xp
    assert updated_user.streak == 1


@pytest.mark.asyncio
async def test_quiz_service_difficulty_levels_and_variety(
    db_session: AsyncSession, user_repo: UserRepository
) -> None:
    user = await user_repo.create_user_with_settings(
        telegram_id=777666, first_name="DiffTester"
    )
    ai = AIService(api_key="")  # mock/fallback
    quiz_service = QuizService(db_session, ai=ai)

    # 1. Generate easy quiz
    quiz_easy = await quiz_service.generate_and_save_quiz(
        user_id=user.id,
        subject_id=None,
        subject_name="Physics",
        difficulty="easy",
        count=3,
        language="uz",
    )
    easy_questions = [q.question_text for q in quiz_easy.questions]
    assert len(easy_questions) == 3

    # 2. Generate hard quiz - should be distinctly different from easy questions
    quiz_hard = await quiz_service.generate_and_save_quiz(
        user_id=user.id,
        subject_id=None,
        subject_name="Physics",
        difficulty="hard",
        count=3,
        language="uz",
    )
    hard_questions = [q.question_text for q in quiz_hard.questions]
    assert len(hard_questions) == 3
    # Easy and hard question sets should have zero overlap
    assert set(easy_questions).isdisjoint(set(hard_questions))

    # 3. Generate another easy quiz - should avoid previously asked questions for this user
    quiz_easy_repeat = await quiz_service.generate_and_save_quiz(
        user_id=user.id,
        subject_id=None,
        subject_name="Physics",
        difficulty="easy",
        count=3,
        language="uz",
    )
    easy_repeat_questions = [q.question_text for q in quiz_easy_repeat.questions]
    assert len(easy_repeat_questions) == 3
    # Consecutive quizzes for the user should not duplicate questions
    assert set(easy_questions).isdisjoint(set(easy_repeat_questions))
