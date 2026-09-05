"""Admin service for system statistics, broadcast messaging, and moderation."""

import asyncio
import logging
from typing import Any

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.ai_conversation import AIConversationRepository
from app.database.repositories.document import DocumentRepository
from app.database.repositories.quiz import QuizRepository
from app.database.repositories.study_session import StudySessionRepository
from app.database.repositories.user import UserRepository

logger = logging.getLogger(__name__)


class AdminService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.user_repo = UserRepository(session)
        self.quiz_repo = QuizRepository(session)
        self.session_repo = StudySessionRepository(session)
        self.ai_repo = AIConversationRepository(session)
        self.doc_repo = DocumentRepository(session)

    async def get_system_analytics(self) -> dict[str, Any]:
        """Aggregate high-level platform metrics for admin dashboard."""
        total_users = await self.user_repo.count_total_users()
        active_users = await self.user_repo.count_active_users(days=7)
        new_today = await self.user_repo.count_new_users_today()
        quizzes = await self.quiz_repo.count_total_quizzes()
        sessions = await self.session_repo.count_total_sessions()
        ai_requests = await self.ai_repo.count_total_ai_requests()
        pdf_requests = await self.doc_repo.count_total_documents()

        return {
            "total_users": total_users,
            "active_users": active_users,
            "new_today": new_today,
            "quizzes_count": quizzes,
            "sessions_count": sessions,
            "ai_requests": ai_requests,
            "pdf_requests": pdf_requests,
        }

    async def broadcast_message(
        self, bot: Bot, text: str, delay_between_messages: float = 0.05
    ) -> tuple[int, int]:
        """Safely broadcast message to all users with rate limit pacing and error handling.

        Returns (sent_count, failed_count).
        """
        recipients = await self.user_repo.get_all_broadcast_recipients()
        sent = 0
        failed = 0

        for telegram_id in recipients:
            try:
                await bot.send_message(chat_id=telegram_id, text=text)
                sent += 1
                await asyncio.sleep(delay_between_messages)
            except TelegramForbiddenError:
                # User blocked the bot
                failed += 1
                logger.info(f"Broadcast: user {telegram_id} has blocked the bot.")
            except TelegramAPIError as e:
                failed += 1
                logger.warning(f"Broadcast: failed to send to {telegram_id}: {e}")
            except Exception as e:
                failed += 1
                logger.error(f"Broadcast unexpected error for {telegram_id}: {e}")

        return sent, failed

    async def ban_user(self, telegram_id: int) -> bool:
        return await self.user_repo.set_ban_status(telegram_id, is_banned=True)

    async def unban_user(self, telegram_id: int) -> bool:
        return await self.user_repo.set_ban_status(telegram_id, is_banned=False)
