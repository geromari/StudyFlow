"""Main entrypoint for StudyFlow Telegram Bot."""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from app.bot.handlers import master_router
from app.bot.middlewares import (
    DatabaseMiddleware,
    LoggingMiddleware,
    ThrottlingMiddleware,
    UserMiddleware,
)
from app.config.settings import settings
from app.database.repositories.achievement import AchievementRepository
from app.database.session import async_session_factory, engine
from app.services.reminders.scheduler import ReminderScheduler
from app.utils.logging import setup_logging

logger = logging.getLogger("StudyFlow")


async def init_services() -> None:
    """Initialize startup hooks, such as default achievements seeding."""
    async with async_session_factory() as session:
        ach_repo = AchievementRepository(session)
        await ach_repo.seed_default_achievements()
    logger.info("Default achievements verified/seeded.")


async def create_dispatcher() -> tuple[Dispatcher, RedisStorage | MemoryStorage]:
    """Configure Dispatcher with Redis FSM or MemoryStorage fallback."""
    storage: RedisStorage | MemoryStorage
    try:
        if settings.redis_url:
            storage = RedisStorage.from_url(settings.redis_url)
            # Ping redis to ensure connection
            await storage.redis.ping()
            logger.info("Connected to Redis for FSM and caching.")
        else:
            storage = MemoryStorage()
            logger.info("Using in-memory FSM storage.")
    except Exception as e:
        logger.warning(f"Could not connect to Redis ({e}). Falling back to MemoryStorage.")
        storage = MemoryStorage()

    dp = Dispatcher(storage=storage)

    # Register Middlewares in order: DB -> User Auth -> Rate Limiting -> Logging
    dp.update.outer_middleware(DatabaseMiddleware())
    dp.update.outer_middleware(UserMiddleware())
    dp.update.outer_middleware(ThrottlingMiddleware())
    dp.update.outer_middleware(LoggingMiddleware())

    # Include routers
    dp.include_router(master_router)

    return dp, storage


async def main() -> None:
    setup_logging(settings.log_level)
    logger.info("Starting StudyFlow Telegram Bot...")

    if not settings.bot_token or settings.bot_token == "TEST_BOT_TOKEN":
        logger.error("BOT_TOKEN is not configured! Please set BOT_TOKEN in .env.")
        sys.exit(1)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )

    dp, storage = await create_dispatcher()

    # Seed default data
    try:
        await init_services()
    except Exception as e:
        logger.warning(f"Startup DB init error (database might be initializing): {e}")

    # Start study reminder background scheduler
    reminder_scheduler = ReminderScheduler(bot)
    reminder_scheduler.start()

    try:
        # Drop pending updates to start clean
        await bot.delete_webhook(drop_pending_updates=True)
        bot_info = await bot.get_me()
        logger.info(f"Bot @{bot_info.username} (ID: {bot_info.id}) started successfully.")

        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logger.info("Bot polling cancelled.")
    finally:
        logger.info("Shutting down StudyFlow bot...")
        reminder_scheduler.stop()
        await bot.session.close()
        if isinstance(storage, RedisStorage):
            await storage.close()
        await engine.dispose()
        logger.info("Shutdown completed cleanly.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped by user.")
