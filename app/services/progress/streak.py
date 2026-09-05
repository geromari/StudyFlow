"""Streak logic emphasizing daily consistency and healthy study habits."""

from datetime import date, timedelta


def evaluate_streak(current_streak: int, last_study_date: date | None, today: date) -> tuple[int, bool]:
    """Evaluate streak transition for today.

    Returns:
        (new_streak, is_new_study_day)
    """
    if last_study_date == today:
        # Already counted today
        return current_streak, False

    if last_study_date == today - timedelta(days=1):
        # Studied yesterday -> increment
        return current_streak + 1, True

    # Missed a day or first day -> reset to 1
    return 1, True


def calculate_streak_bonus_xp(streak: int) -> int:
    """Calculate streak bonus XP (max 7 days scaling to avoid excessive pressure)."""
    effective_days = min(streak, 7)
    return effective_days * 10
