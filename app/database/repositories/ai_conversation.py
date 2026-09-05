"""AI conversation repository."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.ai_conversation import AIConversation
from app.database.repositories.base import BaseRepository


class AIConversationRepository(BaseRepository[AIConversation]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AIConversation)

    async def add_message(
        self, user_id: int, role: str, content: str, tokens_used: int = 0
    ) -> AIConversation:
        msg = AIConversation(
            user_id=user_id,
            role=role,
            content=content,
            tokens_used=tokens_used,
        )
        self.session.add(msg)
        await self.session.commit()
        await self.session.refresh(msg)
        return msg

    async def get_recent_history(self, user_id: int, limit: int = 6) -> list[AIConversation]:
        """Fetch latest messages in chronological order."""
        stmt = (
            select(AIConversation)
            .where(AIConversation.user_id == user_id)
            .order_by(AIConversation.id.desc())
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        messages = list(res.scalars().all())
        messages.reverse()
        return messages

    async def clear_history(self, user_id: int) -> int:
        stmt = select(AIConversation).where(AIConversation.user_id == user_id)
        res = await self.session.execute(stmt)
        items = list(res.scalars().all())
        for item in items:
            await self.session.delete(item)
        await self.session.commit()
        return len(items)

    async def count_total_ai_requests(self) -> int:
        stmt = select(func.count(AIConversation.id)).where(AIConversation.role == "user")
        res = await self.session.execute(stmt)
        return res.scalar() or 0
