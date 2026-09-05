"""Middleware to log update execution with sanitized info."""

import logging
import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

logger = logging.getLogger("StudyFlowBot")


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        start_time = time.time()
        user_id = None
        action_name = "Unknown"

        if isinstance(event, Message):
            user_id = event.from_user.id if event.from_user else None
            action_name = f"Message: {event.text[:30] if event.text else event.content_type}"
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id if event.from_user else None
            action_name = f"Callback: {event.data}"

        try:
            result = await handler(event, data)
            duration = time.time() - start_time
            logger.info(f"User {user_id} | {action_name} | {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"User {user_id} | {action_name} | Failed after {duration:.3f}s: {e}")
            raise
