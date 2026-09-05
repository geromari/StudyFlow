"""Unit tests for gamification calculations."""

from app.services.progress.gamification import (
    XP_GOAL_COMPLETED,
    XP_QUIZ_CORRECT_ANSWER,
    XP_QUIZ_PERFECT_BONUS,
    XP_REFERRAL_BONUS,
    XP_TASK_COMPLETION,
    calculate_focus_xp,
    calculate_level,
    calculate_quiz_xp,
    xp_for_level,
)


def test_level_calculation() -> None:
    assert calculate_level(0) == 1
    assert calculate_level(99) == 1
    assert calculate_level(100) == 2
    assert calculate_level(399) == 2
    assert calculate_level(400) == 3
    assert calculate_level(900) == 4
    assert calculate_level(1600) == 5


def test_xp_threshold_for_level() -> None:
    assert xp_for_level(1) == 0
    assert xp_for_level(2) == 100
    assert xp_for_level(3) == 400
    assert xp_for_level(4) == 900


def test_quiz_xp_calculation() -> None:
    # 3 out of 5 correct
    assert calculate_quiz_xp(3, 5) == 3 * XP_QUIZ_CORRECT_ANSWER

    # Perfect score: 5 out of 5
    expected_perfect = (5 * XP_QUIZ_CORRECT_ANSWER) + XP_QUIZ_PERFECT_BONUS
    assert calculate_quiz_xp(5, 5) == expected_perfect


def test_focus_xp_calculation() -> None:
    assert calculate_focus_xp(25) == 25
    assert calculate_focus_xp(0) == 0


def test_constant_xp_values() -> None:
    assert XP_TASK_COMPLETION == 25
    assert XP_GOAL_COMPLETED == 100
    assert XP_REFERRAL_BONUS == 50
