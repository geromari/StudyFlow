"""Middleware for rate limiting incoming updates."""

import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from app.utils.i18n import t
from app.utils.rate_limiter import default_limiter

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 5, period_seconds: int = 2) -> None:
        self.limit = limit
        self.period_seconds = period_seconds

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        telegram_user = None
        if isinstance(event, Message):
            telegram_user = event.from_user
        elif isinstance(event, CallbackQuery):
            telegram_user = event.from_user

        if not telegram_user:
            return await handler(event, data)

        key = f"user_update_{telegram_user.id}"
        allowed = await default_limiter.is_allowed(key, self.limit, self.period_seconds)

        if not allowed:
            lang = data.get("lang", "en")
            warning = t("rate_limit_exceeded", lang)
            if isinstance(event, Message):
                await event.answer(warning)
            elif isinstance(event, CallbackQuery):
                await event.answer(warning, show_alert=True)
            return

        return await handler(event, data)
