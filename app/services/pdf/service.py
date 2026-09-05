"""PDF processing and learning service."""

import io
import logging
from typing import Any

from pypdf import PdfReader
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.database.models.document import Document
from app.database.repositories.document import DocumentRepository
from app.services.ai.client import AIService, ai_service

logger = logging.getLogger(__name__)


class PDFService:
    def __init__(
        self,
        session: AsyncSession,
        ai: AIService | None = None,
    ) -> None:
        self.session = session
        self.doc_repo = DocumentRepository(session)
        self.ai = ai or ai_service
        self.max_size_bytes = settings.max_pdf_size_mb * 1024 * 1024

    def validate_file(self, filename: str, file_size: int) -> tuple[bool, str]:
        """Validate PDF file extension and size limit."""
        if not filename.lower().endswith(".pdf"):
            return False, "Only PDF files are supported."
        if file_size > self.max_size_bytes:
            return False, f"File exceeds maximum allowed size of {settings.max_pdf_size_mb} MB."
        return True, ""

    def extract_text_from_bytes(self, file_bytes: bytes) -> tuple[str, int]:
        """Extract plain text and page count from PDF in-memory bytes."""
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            page_count = len(reader.pages)
            text_parts = []
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text_parts.append(extracted)

            full_text = "\n\n".join(text_parts).strip()
            return full_text, page_count
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            raise ValueError(f"Failed to read PDF file: {e}") from e

    async def process_and_save_pdf(
        self,
        user_id: int,
        file_id: str,
        filename: str,
        file_bytes: bytes,
    ) -> Document:
        """Extract text and metadata from PDF and save in database."""
        valid, err = self.validate_file(filename, len(file_bytes))
        if not valid:
            raise ValueError(err)

        text, pages = self.extract_text_from_bytes(file_bytes)
        if not text:
            text = "No readable text extracted (scanned or image PDF)."

        doc = await self.doc_repo.save_document(
            user_id=user_id,
            file_id=file_id,
            filename=filename,
            file_size=len(file_bytes),
            page_count=pages,
            extracted_text=text[:25000],  # Limit stored text to reasonable bounds
        )
        return doc

    async def summarize_document(self, document_id: int, language: str = "en") -> str:
        doc = await self.doc_repo.get_document_by_id(document_id)
        if not doc or not doc.extracted_text:
            return "Document has no readable text to summarize."

        if doc.summary:
            return doc.summary

        summary = await self.ai.summarize_document(doc.extracted_text, language=language)
        doc.summary = summary
        await self.session.commit()
        return summary

    async def ask_question(
        self, document_id: int, question: str, language: str = "en"
    ) -> str:
        doc = await self.doc_repo.get_document_by_id(document_id)
        if not doc or not doc.extracted_text:
            return "Document content is unavailable."

        return await self.ai.ask_document(
            document_text=doc.extracted_text,
            question=question,
            language=language,
        )

    async def generate_quiz_from_doc(
        self, document_id: int, count: int = 5, language: str = "en"
    ) -> list[dict[str, Any]]:
        doc = await self.doc_repo.get_document_by_id(document_id)
        if not doc or not doc.extracted_text:
            raise ValueError("Document has no readable text.")

        prompt_subject = f"Document: {doc.filename}\nContent excerpt: {doc.extracted_text[:3000]}"
        return await self.ai.generate_quiz(
            subject=prompt_subject,
            difficulty="medium",
            count=count,
            language=language,
        )
