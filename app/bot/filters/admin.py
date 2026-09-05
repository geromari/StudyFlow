"""Admin permission filter."""

from aiogram.filters import Filter
from aiogram.types import Message

from app.config.settings import settings


class IsAdminFilter(Filter):
    """Filter that allows only administrators configured in ADMIN_IDS."""

    async def __call__(self, message: Message) -> bool:
        if not message.from_user:
            return False
        return message.from_user.id in settings.admin_ids
