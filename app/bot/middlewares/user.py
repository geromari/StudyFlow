"""Middleware to authenticate user, track activity, check ban status, and provide language."""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject, Update
from aiogram.types import User as TgUser
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.user import UserRepository
from app.utils.i18n import DEFAULT_LANGUAGE


def extract_telegram_user(event: TelegramObject, data: dict[str, Any]) -> TgUser | None:
    """Extract Telegram user from event context or Update object."""
    if "event_from_user" in data and data["event_from_user"] is not None:
        return data["event_from_user"]

    if isinstance(event, (Message, CallbackQuery)) and event.from_user:
        return event.from_user

    if isinstance(event, Update):
        if event.message and event.message.from_user:
            return event.message.from_user
        if event.callback_query and event.callback_query.from_user:
            return event.callback_query.from_user
        if hasattr(event, "event") and hasattr(event.event, "from_user"):
            return getattr(event.event, "from_user", None)

    return None


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        telegram_user = extract_telegram_user(event, data)
        if not telegram_user:
            return await handler(event, data)

        session: AsyncSession = data["session"]
        user_repo = UserRepository(session)
        user = await user_repo.get_by_telegram_id(telegram_user.id)

        if user:
            if user.is_banned:
                real_event = event.event if isinstance(event, Update) else event
                if isinstance(real_event, Message):
                    await real_event.answer("🚫 Your account is suspended. Contact administrator.")
                elif isinstance(real_event, CallbackQuery):
                    await real_event.answer("🚫 Your account is suspended.", show_alert=True)
                return

            # Update last activity timestamp
            await user_repo.update_activity(user.telegram_id)
            lang = user.settings.language if user.settings else DEFAULT_LANGUAGE
        else:
            lang = (
                telegram_user.language_code
                if telegram_user.language_code in ["uz", "en", "ru"]
                else DEFAULT_LANGUAGE
            )

        data["user"] = user
        data["lang"] = lang
        return await handler(event, data)
