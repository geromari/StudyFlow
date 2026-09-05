"""Unit tests for streak logic."""

from datetime import date, timedelta

from app.services.progress.streak import calculate_streak_bonus_xp, evaluate_streak


def test_streak_evaluation() -> None:
    today = date(2026, 9, 5)
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)

    # First time studying
    streak, is_new = evaluate_streak(0, None, today)
    assert streak == 1
    assert is_new is True

    # Studied yesterday, increments today
    streak, is_new = evaluate_streak(5, yesterday, today)
    assert streak == 6
    assert is_new is True

    # Already studied today
    streak, is_new = evaluate_streak(5, today, today)
    assert streak == 5
    assert is_new is False

    # Missed a day
    streak, is_new = evaluate_streak(10, two_days_ago, today)
    assert streak == 1
    assert is_new is True


def test_streak_bonus_xp() -> None:
    assert calculate_streak_bonus_xp(1) == 10
    assert calculate_streak_bonus_xp(3) == 30
    assert calculate_streak_bonus_xp(7) == 70
    # Capped at 7 days for healthy study encouragement
    assert calculate_streak_bonus_xp(14) == 70
