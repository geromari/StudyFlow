"""Master router combining all StudyFlow bot handler routers."""

from aiogram import Router

from app.bot.handlers.achievements import router as achievements_router
from app.bot.handlers.admin import router as admin_router
from app.bot.handlers.ai_assistant import router as ai_assistant_router
from app.bot.handlers.common import router as common_router
from app.bot.handlers.focus import router as focus_router
from app.bot.handlers.goals import router as goals_router
from app.bot.handlers.pdf_learning import router as pdf_learning_router
from app.bot.handlers.profile import router as profile_router
from app.bot.handlers.progress import router as progress_router
from app.bot.handlers.quiz import router as quiz_router
from app.bot.handlers.referral import router as referral_router
from app.bot.handlers.settings import router as settings_router
from app.bot.handlers.start import router as start_router
from app.bot.handlers.streak import router as streak_router
from app.bot.handlers.study_plan import router as study_plan_router
from app.bot.handlers.subjects import router as subjects_router

master_router = Router(name="master_router")

# Include child routers in logical processing order
master_router.include_router(common_router)
master_router.include_router(start_router)
master_router.include_router(admin_router)
master_router.include_router(profile_router)
master_router.include_router(subjects_router)
master_router.include_router(ai_assistant_router)
master_router.include_router(quiz_router)
master_router.include_router(study_plan_router)
master_router.include_router(goals_router)
master_router.include_router(progress_router)
master_router.include_router(streak_router)
master_router.include_router(focus_router)
master_router.include_router(pdf_learning_router)
master_router.include_router(achievements_router)
master_router.include_router(referral_router)
master_router.include_router(settings_router)

__all__ = ["master_router"]
