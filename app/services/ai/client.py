"""AI service client supporting OpenAI-compatible APIs and mock fallback."""

import json
import logging
import re
from typing import Any

from openai import AsyncOpenAI

from app.config.settings import settings
from app.services.ai.prompt_templates import (
    DOCUMENT_QA_PROMPT,
    DOCUMENT_SUMMARY_PROMPT,
    MODE_PROMPTS,
    QUIZ_GENERATION_PROMPT,
    STUDY_ASSISTANT_SYSTEM_PROMPT,
    STUDY_PLAN_GENERATION_PROMPT,
)

logger = logging.getLogger(__name__)


def clean_json_response(raw_text: str) -> str:
    """Strip markdown backticks or surrounding text to extract clean JSON."""
    raw_text = raw_text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_text)
    if match:
        return match.group(1).strip()
    return raw_text


class AIService:
    """Unified AI service for StudyFlow."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        max_input_chars: int | None = None,
        max_output_tokens: int | None = None,
    ) -> None:
        self.api_key = api_key or settings.ai_api_key
        self.base_url = base_url or settings.ai_base_url
        self.model = model or settings.ai_model
        self.max_input_chars = max_input_chars or settings.ai_max_input_chars
        self.max_output_tokens = max_output_tokens or settings.ai_max_output_tokens

        self._client: AsyncOpenAI | None = None
        if self.api_key and not self.api_key.startswith("sk-your-"):
            self._client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)

    @property
    def is_configured(self) -> bool:
        return self._client is not None

    def _truncate_input(self, text: str) -> str:
        if len(text) > self.max_input_chars:
            return text[: self.max_input_chars] + "... [truncated]"
        return text

    async def chat(
        self,
        conversation_history: list[dict[str, str]],
        user_prompt: str,
        mode: str | None = None,
    ) -> tuple[str, int]:
        """Send message to AI assistant with historical context and optional mode prefix."""
        prompt = self._truncate_input(user_prompt)
        if mode and mode in MODE_PROMPTS:
            prompt = MODE_PROMPTS[mode] + prompt

        messages: list[dict[str, str]] = [
            {"role": "system", "content": STUDY_ASSISTANT_SYSTEM_PROMPT}
        ]
        # Include conversation context (already limited to latest messages)
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": prompt})

        if not self.is_configured:
            # Fallback mock for testing or unconfigured API
            return f"[StudyFlow AI Response]: Regarding '{user_prompt}': This is a key academic concept. Remember to break it down into core principles and review regularly.", 50

        try:
            assert self._client is not None
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                max_tokens=self.max_output_tokens,
                temperature=0.7,
            )
            content = response.choices[0].message.content or ""
            tokens = response.usage.total_tokens if response.usage else 0
            return content, tokens
        except Exception as e:
            logger.error(f"AI API chat completion error: {e}")
            raise

    async def generate_quiz(
        self,
        subject: str,
        difficulty: str = "medium",
        count: int = 5,
        language: str = "en",
    ) -> list[dict[str, Any]]:
        """Generate multiple choice questions in structured JSON format."""
        prompt = QUIZ_GENERATION_PROMPT.format(
            subject=subject,
            difficulty=difficulty,
            count=count,
            language=language,
        )

        if not self.is_configured:
            # Mock questions for testing
            mock_questions = []
            for i in range(1, count + 1):
                mock_questions.append({
                    "question": f"Question {i} about {subject} ({difficulty})?",
                    "options": {
                        "A": f"Option A for {subject} {i}",
                        "B": f"Correct option B for {subject} {i}",
                        "C": f"Option C for {subject} {i}",
                        "D": f"Option D for {subject} {i}",
                    },
                    "correct_option": "B",
                    "explanation": f"Option B is the correct principle for {subject}.",
                })
            return mock_questions

        try:
            assert self._client is not None
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional quiz generator. Respond only in JSON."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_output_tokens * 2,
                temperature=0.6,
            )
            raw = response.choices[0].message.content or "[]"
            cleaned = clean_json_response(raw)
            data = json.loads(cleaned)
            if isinstance(data, list) and len(data) > 0:
                return data
            return []
        except Exception as e:
            logger.error(f"AI quiz generation failed: {e}")
            raise

    async def generate_study_plan(
        self,
        goal: str,
        target_minutes: int,
        subjects: list[str],
        language: str = "en",
    ) -> list[dict[str, Any]]:
        """Generate a structured daily study plan schedule."""
        prompt = STUDY_PLAN_GENERATION_PROMPT.format(
            goal=goal,
            target_minutes=target_minutes,
            subjects=", ".join(subjects) if subjects else "General Studies",
            language=language,
        )

        if not self.is_configured:
            # Mock plan
            task_time = target_minutes // max(1, len(subjects or ["Study"]))
            return [
                {
                    "title": f"Review {subj} core concepts",
                    "scheduled_time": f"{9 + i * 3:02d}:00",
                    "duration_minutes": max(15, task_time),
                    "subject": subj,
                }
                for i, subj in enumerate(subjects or ["General Studies"])
            ]

        try:
            assert self._client is not None
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a study scheduler. Output strictly valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_output_tokens,
                temperature=0.5,
            )
            raw = response.choices[0].message.content or "[]"
            cleaned = clean_json_response(raw)
            data = json.loads(cleaned)
            if isinstance(data, list):
                return data
            return []
        except Exception as e:
            logger.error(f"Study plan AI generation failed: {e}")
            raise

    async def ask_document(
        self, document_text: str, question: str, language: str = "en"
    ) -> str:
        """Answer question based on extracted document text."""
        excerpt = self._truncate_input(document_text)
        prompt = DOCUMENT_QA_PROMPT.format(
            document_excerpt=excerpt, question=question, language=language
        )

        if not self.is_configured:
            return f"[AI Document Q&A]: Based on the provided document, the answer to '{question}' is found in the main sections. Key concepts were covered."

        try:
            assert self._client is not None
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an accurate academic document analyst."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_output_tokens,
                temperature=0.4,
            )
            return response.choices[0].message.content or "No answer could be generated."
        except Exception as e:
            logger.error(f"Document Q&A failed: {e}")
            raise

    async def summarize_document(self, document_text: str, language: str = "en") -> str:
        """Summarize extracted document text."""
        excerpt = self._truncate_input(document_text)
        prompt = DOCUMENT_SUMMARY_PROMPT.format(
            document_excerpt=excerpt, language=language
        )

        if not self.is_configured:
            return "📌 **Document Summary**\n\n• **Main Theme**: Educational overview\n• **Key Concepts**: Core definitions and examples\n• **Takeaway**: Essential material for examination preparation."

        try:
            assert self._client is not None
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert document summarizer."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_output_tokens,
                temperature=0.5,
            )
            return response.choices[0].message.content or "Could not generate summary."
        except Exception as e:
            logger.error(f"Document summary failed: {e}")
            raise


# Global singleton instance
ai_service = AIService()
