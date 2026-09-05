"""PDF document learning handlers."""

import logging

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.inline import get_pdf_menu_keyboard
from app.bot.keyboards.reply import get_cancel_keyboard, get_main_menu_keyboard
from app.bot.states.states import PDFState
from app.database.models.user import User
from app.services.pdf.service import PDFService
from app.utils.i18n import DEFAULT_LANGUAGE, t

logger = logging.getLogger(__name__)
router = Router(name="pdf_learning_router")


@router.message(F.text.in_({"📄 PDF Learning", "📄 PDF O'rganish", "📄 Обучение по PDF"}))
async def handle_pdf_menu(
    message: Message,
    state: FSMContext,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user:
        await message.answer("Please /start the bot first.")
        return

    await state.set_state(PDFState.waiting_for_pdf)
    await message.answer(
        t("pdf_intro", lang),
        reply_markup=get_cancel_keyboard(lang),
    )


@router.message(PDFState.waiting_for_pdf, F.document)
async def handle_pdf_document_upload(
    message: Message,
    bot: Bot,
    state: FSMContext,
    session: AsyncSession,
    user: User | None = None,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    if not user or not message.document:
        return

    doc_name = message.document.file_name or "document.pdf"
    file_size = message.document.file_size or 0

    pdf_service = PDFService(session)
    valid, err_msg = pdf_service.validate_file(doc_name, file_size)
    if not valid:
        await message.answer(f"⚠️ {err_msg}")
        return

    processing_msg = await message.answer("⏳ Downloading and extracting document text...")

    try:
        # Download document into memory bytes
        file_info = await bot.get_file(message.document.file_id)
        if not file_info.file_path:
            raise ValueError("Could not obtain file path from Telegram.")

        file_bytes_io = await bot.download_file(file_info.file_path)
        file_bytes = file_bytes_io.read() if file_bytes_io else b""

        # Process and save in database
        doc = await pdf_service.process_and_save_pdf(
            user_id=user.id,
            file_id=message.document.file_id,
            filename=doc_name,
            file_bytes=file_bytes,
        )

        await processing_msg.delete()
        await state.update_data(active_pdf_id=doc.id)
        await state.set_state(PDFState.document_menu)

        await message.answer(
            t("pdf_processed", lang, filename=doc.filename, pages=doc.page_count),
            reply_markup=get_pdf_menu_keyboard(doc.id, lang),
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Failed to process PDF: {e}")
        try:
            await processing_msg.delete()
        except Exception:
            pass
        await message.answer(
            f"❌ Error processing PDF: {e}",
            reply_markup=get_main_menu_keyboard(lang),
        )
        await state.clear()


@router.callback_query(F.data.startswith("pdf_sum_"))
async def handle_pdf_summarize(
    callback: CallbackQuery,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    doc_id = int(callback.data.replace("pdf_sum_", ""))
    await callback.message.answer("📝 Generating comprehensive executive summary with AI...")

    pdf_service = PDFService(session)
    try:
        summary = await pdf_service.summarize_document(doc_id, language=lang)
        await callback.message.answer(summary, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error summarizing PDF: {e}")
        await callback.message.answer(t("generic_error", lang))
    await callback.answer()


@router.callback_query(F.data.startswith("pdf_qa_"))
async def handle_pdf_qa_prompt(
    callback: CallbackQuery,
    state: FSMContext,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    doc_id = int(callback.data.replace("pdf_qa_", ""))
    await state.set_state(PDFState.waiting_for_question)
    await state.update_data(active_pdf_id=doc_id)
    await callback.answer()
    await callback.message.answer(
        "❓ Ask any question about your uploaded document:",
        reply_markup=get_cancel_keyboard(lang),
    )


@router.message(PDFState.waiting_for_question)
async def handle_pdf_answer_question(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    question = (message.text or "").strip()
    if not question:
        return

    data = await state.get_data()
    doc_id = data.get("active_pdf_id")
    if not doc_id:
        await state.clear()
        return

    think_msg = await message.answer("🔍 Analyzing document for the answer...")
    pdf_service = PDFService(session)

    try:
        answer = await pdf_service.ask_question(doc_id, question, language=lang)
        await think_msg.delete()
        await message.answer(f"📖 **Answer:**\n\n{answer}", parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error answering PDF question: {e}")
        try:
            await think_msg.delete()
        except Exception:
            pass
        await message.answer(t("generic_error", lang))


@router.callback_query(F.data.startswith("pdf_quiz_"))
async def handle_pdf_quiz(
    callback: CallbackQuery,
    session: AsyncSession,
    lang: str = DEFAULT_LANGUAGE,
) -> None:
    doc_id = int(callback.data.replace("pdf_quiz_", ""))
    await callback.message.answer("⚡ Generating practice quiz from your document with AI...")

    pdf_service = PDFService(session)
    try:
        questions = await pdf_service.generate_quiz_from_doc(doc_id, count=3, language=lang)
        if not questions:
            await callback.message.answer("Could not generate quiz from document text.")
            return

        text = "📝 **Practice Questions from your Document:**\n\n"
        for i, q in enumerate(questions, 1):
            text += f"**{i}. {q.get('question')}**\n"
            for opt_k, opt_v in q.get("options", {}).items():
                text += f"  {opt_k}) {opt_v}\n"
            text += f"👉 *Correct: {q.get('correct_option')}*\n💡 _{q.get('explanation')}_\n\n"

        await callback.message.answer(text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error generating quiz from PDF: {e}")
        await callback.message.answer(t("generic_error", lang))
    await callback.answer()
