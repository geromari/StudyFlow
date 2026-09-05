"""Middleware to authenticate user, track activity, check ban status, and provide language."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.user import UserRepository
from app.utils.i18n import DEFAULT_LANGUAGE


class UserMiddleware(BaseMiddleware):
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

        session: AsyncSession = data["session"]
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(telegram_user.id)

        if user:
            if user.is_banned:
                if isinstance(event, Message):
                    await event.answer("🚫 Your account is suspended. Contact administrator.")
                elif isinstance(event, CallbackQuery):
                    await event.answer("🚫 Your account is suspended.", show_alert=True)
                return

            # Update last activity
            await user_repo.update_activity(user.telegram_id)
            lang = user.settings.language if user.settings else DEFAULT_LANGUAGE
        else:
            lang = telegram_user.language_code if telegram_user.language_code in ["uz", "en", "ru"] else DEFAULT_LANGUAGE

        data["user"] = user
        data["lang"] = lang
        return await handler(event, data)
