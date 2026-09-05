"""Document repository for PDF files."""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.document import Document
from app.database.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Document)

    async def save_document(
        self,
        user_id: int,
        file_id: str,
        filename: str,
        file_size: int,
        page_count: int,
        extracted_text: str | None = None,
        summary: str | None = None,
    ) -> Document:
        doc = Document(
            user_id=user_id,
            file_id=file_id,
            filename=filename,
            file_size=file_size,
            page_count=page_count,
            extracted_text=extracted_text,
            summary=summary,
        )
        self.session.add(doc)
        await self.session.commit()
        await self.session.refresh(doc)
        return doc

    async def get_user_documents(self, user_id: int, limit: int = 10) -> list[Document]:
        stmt = (
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(Document.id.desc())
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def get_document_by_id(self, doc_id: int) -> Document | None:
        return await self.get_by_id(doc_id)

    async def get_latest_document(self, user_id: int) -> Document | None:
        stmt = (
            select(Document)
            .where(Document.user_id == user_id)
            .order_by(Document.id.desc())
            .limit(1)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def count_total_documents(self) -> int:
        stmt = select(func.count(Document.id))
        res = await self.session.execute(stmt)
        return res.scalar() or 0
