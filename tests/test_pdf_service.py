"""Unit tests for PDFService."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.user import UserRepository
from app.services.ai.client import AIService
from app.services.pdf.service import PDFService


@pytest.mark.asyncio
async def test_pdf_validation(db_session: AsyncSession) -> None:
    service = PDFService(db_session)
    valid, msg = service.validate_file("document.txt", 100)
    assert not valid
    assert "Only PDF" in msg

    valid, msg = service.validate_file("document.pdf", 100)
    assert valid


@pytest.mark.asyncio
async def test_pdf_service_mock_workflow(
    db_session: AsyncSession, user_repo: UserRepository
) -> None:
    user = await user_repo.create_user_with_settings(
        telegram_id=444222, first_name="Reader"
    )

    ai = AIService(api_key="")
    service = PDFService(db_session, ai=ai)

    # Mock text and save document via repo directly
    doc = await service.doc_repo.save_document(
        user_id=user.id,
        file_id="tg_file_123",
        filename="notes.pdf",
        file_size=2048,
        page_count=2,
        extracted_text="Chapter 1: Principles of Machine Learning. Supervised and unsupervised methods.",
    )
    assert doc.id is not None

    summary = await service.summarize_document(doc.id)
    assert "Summary" in summary

    answer = await service.ask_question(doc.id, "What is Chapter 1 about?")
    assert len(answer) > 0
