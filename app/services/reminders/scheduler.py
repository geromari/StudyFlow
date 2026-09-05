"""Study reminder scheduler."""

import asyncio
import logging
from datetime import UTC, date, datetime

from aiogram import Bot

from app.database.models.reminder import Reminder
from app.database.repositories.reminder import ReminderRepository
from app.database.repositories.user import UserRepository
from app.database.session import async_session_factory
from app.utils.i18n import t

logger = logging.getLogger(__name__)


class ReminderScheduler:
    """Periodic reminder check loop."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self._running = False
        self._task: asyncio.Task[None] | None = None

    def start(self) -> None:
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run_loop())
            logger.info("Reminder scheduler started.")

    def stop(self) -> None:
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
            logger.info("Reminder scheduler stopped.")

    async def _run_loop(self) -> None:
        while self._running:
            try:
                await self.check_and_send_due_reminders()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in reminder loop: {e}", exc_info=True)

            # Sleep 60 seconds until next minute
            await asyncio.sleep(60)

    async def check_and_send_due_reminders(self) -> None:
        """Check all users with due reminders matching current UTC time."""
        now_utc = datetime.now(UTC)
        current_time_str = now_utc.strftime("%H:%M")
        today = date.today()

        async with async_session_factory() as session:
            reminder_repo = ReminderRepository(session)
            user_repo = UserRepository(session)

            due_reminders: list[Reminder] = await reminder_repo.get_due_reminders(
                current_time_str, today
            )

            for reminder in due_reminders:
                user = await user_repo.get_by_id(reminder.user_id)
                if not user or user.is_banned:
                    continue

                lang = user.settings.language if user.settings else "en"
                msg_text = t("reminder_alert", lang)

                try:
                    await self.bot.send_message(chat_id=user.telegram_id, text=msg_text)
                    await reminder_repo.mark_sent(reminder.id, today)
                    logger.info(f"Study reminder sent to user {user.telegram_id}")
                except Exception as e:
                    logger.warning(f"Failed to send reminder to user {user.telegram_id}: {e}")
