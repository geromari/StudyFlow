"""Base repository with generic database operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.base import Base


class BaseRepository[T: Base]:
    """Generic async repository providing common CRUD operations."""


    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, item_id: int) -> T | None:
        return await self.session.get(self.model, item_id)

    async def get_all(self, limit: int = 100, offset: int = 0) -> list[T]:
        stmt = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, item: T) -> T:
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def update(self, item: T) -> T:
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def delete(self, item: T) -> None:
        await self.session.delete(item)
        await self.session.commit()
