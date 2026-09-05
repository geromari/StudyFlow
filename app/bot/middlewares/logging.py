"""Middleware to log update execution with sanitized info."""

import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject, Update

from app.bot.middlewares.user import extract_telegram_user

logger = logging.getLogger("StudyFlowBot")


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        start_time = time.time()
        telegram_user = extract_telegram_user(event, data)
        user_id = telegram_user.id if telegram_user else None
        action_name = "Update"

        real_event = event.event if isinstance(event, Update) else event
        if isinstance(real_event, Message):
            action_name = f"Message: {real_event.text[:30] if real_event.text else real_event.content_type}"
        elif isinstance(real_event, CallbackQuery):
            action_name = f"Callback: {real_event.data}"

        try:
            result = await handler(event, data)
            duration = time.time() - start_time
            logger.info(f"User {user_id} | {action_name} | {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"User {user_id} | {action_name} | Failed after {duration:.3f}s: {e}")
            raise
