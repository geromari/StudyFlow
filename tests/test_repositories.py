"""Integration tests for repositories."""

from datetime import date, timedelta

import pytest

from app.database.repositories import (
    AchievementRepository,
    GoalRepository,
    QuizRepository,
    ReferralRepository,
    SubjectRepository,
    UserRepository,
)


@pytest.mark.asyncio
async def test_user_registration_and_settings(user_repo: UserRepository) -> None:
    user = await user_repo.create_user_with_settings(
        telegram_id=12345678,
        first_name="Alice",
        username="alice_student",
        language="en",
        daily_target=45,
    )
    assert user.id is not None
    assert user.telegram_id == 12345678
    assert user.first_name == "Alice"
    assert user.xp == 0
    assert user.level == 1
    assert user.streak == 0
    assert user.settings.language == "en"
    assert user.settings.daily_study_target == 45

    # Fetch by telegram id
    fetched = await user_repo.get_by_telegram_id(12345678)
    assert fetched is not None
    assert fetched.username == "alice_student"


@pytest.mark.asyncio
async def test_xp_and_level_progression(user_repo: UserRepository) -> None:
    user = await user_repo.create_user_with_settings(
        telegram_id=222333,
        first_name="Bob",
    )
    xp, level, level_up = await user_repo.add_xp(user.id, 50)
    assert xp == 50
    assert level == 1
    assert not level_up

    # Add 100 more -> 150 XP -> Level 2
    xp, level, level_up = await user_repo.add_xp(user.id, 100)
    assert xp == 150
    assert level == 2
    assert level_up


@pytest.mark.asyncio
async def test_streak_tracking(user_repo: UserRepository) -> None:
    user = await user_repo.create_user_with_settings(
        telegram_id=333444,
        first_name="Charlie",
    )
    today = date(2026, 9, 1)

    # First study day -> streak 1
    streak = await user_repo.update_streak(user.id, today)
    assert streak == 1

    # Same day -> still 1
    streak = await user_repo.update_streak(user.id, today)
    assert streak == 1

    # Next day -> streak 2
    next_day = today + timedelta(days=1)
    streak = await user_repo.update_streak(user.id, next_day)
    assert streak == 2

    # Missed a day -> reset to 1
    missed_day = next_day + timedelta(days=2)
    streak = await user_repo.update_streak(user.id, missed_day)
    assert streak == 1


@pytest.mark.asyncio
async def test_subjects_and_topics(
    user_repo: UserRepository, subject_repo: SubjectRepository
) -> None:
    user = await user_repo.create_user_with_settings(telegram_id=444555, first_name="Dave")
    subj = await subject_repo.create_subject(user.id, "Mathematics", "📐")
    assert subj.name == "Mathematics"

    topic1 = await subject_repo.add_topic(subj.id, "Algebra")
    await subject_repo.add_topic(subj.id, "Calculus")

    topics = await subject_repo.get_topics(subj.id)
    assert len(topics) == 2

    # Toggle topic completion
    updated_topic = await subject_repo.toggle_topic(topic1.id)
    assert updated_topic is not None
    assert updated_topic.is_completed is True

    # Check subject progress updated
    updated_subj = await subject_repo.get_by_id(subj.id)
    assert updated_subj is not None
    assert updated_subj.progress_percent == 50


@pytest.mark.asyncio
async def test_goals_flow(user_repo: UserRepository, goal_repo: GoalRepository) -> None:
    user = await user_repo.create_user_with_settings(telegram_id=555666, first_name="Eve")
    goal = await goal_repo.create_goal(user.id, "Learn FastApi", date.today() + timedelta(days=30))
    assert not goal.is_completed

    await goal_repo.update_goal(goal.id, progress_percent=50)
    g = await goal_repo.get_by_id(goal.id)
    assert g is not None and g.progress_percent == 50

    await goal_repo.mark_completed(goal.id)
    g = await goal_repo.get_by_id(goal.id)
    assert g is not None and g.is_completed and g.progress_percent == 100


@pytest.mark.asyncio
async def test_quiz_and_answers(user_repo: UserRepository, quiz_repo: QuizRepository) -> None:
    user = await user_repo.create_user_with_settings(telegram_id=666777, first_name="Frank")
    questions = [
        {
            "question": "What is 2+2?",
            "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
            "correct_option": "B",
            "explanation": "2+2=4",
        }
    ]
    quiz = await quiz_repo.create_quiz_with_questions(
        user_id=user.id,
        subject_id=None,
        title="Math Basics",
        difficulty="easy",
        questions_data=questions,
    )
    assert quiz.total_questions == 1
    assert len(quiz.questions) == 1

    ans = await quiz_repo.record_answer(
        quiz_id=quiz.id,
        question_id=quiz.questions[0].id,
        user_id=user.id,
        selected_option="B",
        is_correct=True,
    )
    assert ans.is_correct

    finished = await quiz_repo.finish_quiz(quiz.id, score=1, xp_earned=20)
    assert finished is not None
    assert finished.score == 1
    assert finished.xp_earned == 20


@pytest.mark.asyncio
async def test_achievements_unlocking(
    user_repo: UserRepository, achievement_repo: AchievementRepository
) -> None:
    user = await user_repo.create_user_with_settings(telegram_id=777888, first_name="Grace")
    unlocked = await achievement_repo.unlock_achievement(user.id, "first_quiz")
    assert unlocked is not None
    assert unlocked.code == "first_quiz"

    # Trying to unlock same achievement again returns None
    second_try = await achievement_repo.unlock_achievement(user.id, "first_quiz")
    assert second_try is None


@pytest.mark.asyncio
async def test_referral_logic(user_repo: UserRepository, referral_repo: ReferralRepository) -> None:
    u1 = await user_repo.create_user_with_settings(telegram_id=888111, first_name="Inviter")
    u2 = await user_repo.create_user_with_settings(telegram_id=888222, first_name="Invited")

    # Valid referral
    ref = await referral_repo.create_referral(u1.id, u2.id, xp_awarded=50)
    assert ref is not None

    # Self-referral prevention
    self_ref = await referral_repo.create_referral(u1.id, u1.id)
    assert self_ref is None

    # Duplicate referral prevention
    dup_ref = await referral_repo.create_referral(u1.id, u2.id)
    assert dup_ref is None
