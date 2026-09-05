"""Gamification rules and XP calculation formulas."""

XP_TASK_COMPLETION = 25
XP_QUIZ_CORRECT_ANSWER = 10
XP_QUIZ_PERFECT_BONUS = 20
XP_GOAL_COMPLETED = 100
XP_REFERRAL_BONUS = 50


def calculate_level(xp: int) -> int:
    """Calculate level from XP.
    Formula: Level = int((XP / 100) ** 0.5) + 1
    0 XP -> Level 1
    100 XP -> Level 2
    400 XP -> Level 3
    900 XP -> Level 4
    1600 XP -> Level 5
    """
    if xp <= 0:
        return 1
    return int((xp / 100) ** 0.5) + 1


def xp_for_level(level: int) -> int:
    """Calculate the minimum XP required to reach a specific level."""
    if level <= 1:
        return 0
    return ((level - 1) ** 2) * 100


def calculate_focus_xp(minutes: int) -> int:
    """Award 1 XP per minute studied in focus mode."""
    return max(0, minutes)


def calculate_quiz_xp(score: int, total: int) -> int:
    """Calculate XP for quiz performance."""
    xp = score * XP_QUIZ_CORRECT_ANSWER
    if score == total and total > 0:
        xp += XP_QUIZ_PERFECT_BONUS
    return xp
