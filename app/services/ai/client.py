"""AI service client supporting OpenAI-compatible APIs and mock fallback."""

import json
import logging
import random
import re
import uuid
from typing import Any

from openai import AsyncOpenAI

from app.config.settings import settings
from app.services.ai.prompt_templates import (
    DIFFICULTY_GUIDELINES,
    DOCUMENT_QA_PROMPT,
    DOCUMENT_SUMMARY_PROMPT,
    MODE_PROMPTS,
    QUIZ_GENERATION_PROMPT,
    STUDY_ASSISTANT_SYSTEM_PROMPT,
    STUDY_PLAN_GENERATION_PROMPT,
)
from app.services.ai.topic_explainer import explain_topic_comprehensively

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
        self.api_key = settings.ai_api_key if api_key is None else api_key
        self.base_url = settings.ai_base_url if base_url is None else base_url
        self.model = settings.ai_model if model is None else model
        self.max_input_chars = (
            settings.ai_max_input_chars if max_input_chars is None else max_input_chars
        )
        self.max_output_tokens = (
            settings.ai_max_output_tokens if max_output_tokens is None else max_output_tokens
        )

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
        language: str = "uz",
    ) -> tuple[str, int]:
        """Send message to AI assistant with historical context and optional mode prefix."""
        prompt = self._truncate_input(user_prompt)
        if mode and mode in MODE_PROMPTS:
            prompt = MODE_PROMPTS[mode] + prompt

        messages: list[dict[str, str]] = [
            {"role": "system", "content": STUDY_ASSISTANT_SYSTEM_PROMPT + f"\nAlways respond in language: {language}."}
        ]
        # Include conversation context (already limited to latest messages)
        for msg in conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": prompt})

        if not self.is_configured:
            return explain_topic_comprehensively(user_prompt, mode, language), 50

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
            return explain_topic_comprehensively(user_prompt, mode, language), 50

    def _generate_fallback_study_plan(
        self, goal: str, target_minutes: int, subjects: list[str]
    ) -> list[dict[str, Any]]:
        task_time = target_minutes // max(1, len(subjects or ["Study"]))
        return [
            {
                "title": f"Review {subj} core concepts for '{goal}'",
                "scheduled_time": f"{9 + i * 3:02d}:00",
                "duration_minutes": max(15, task_time),
                "subject": subj,
            }
            for i, subj in enumerate(subjects or ["General Studies"])
        ]

    async def generate_quiz(
        self,
        subject: str,
        difficulty: str = "medium",
        count: int = 5,
        language: str = "uz",
        exclude_questions: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Generate multiple choice questions in structured JSON format with distinct difficulties and variety."""
        from app.services.quiz.quiz_bank import generate_curated_quiz

        norm_diff = (difficulty or "medium").lower().strip()
        if norm_diff not in ("easy", "medium", "hard"):
            norm_diff = "medium"

        if not self.is_configured:
            return generate_curated_quiz(
                subject=subject,
                difficulty=norm_diff,
                count=count,
                language=language,
                exclude_questions=exclude_questions,
            )

        diff_guideline = DIFFICULTY_GUIDELINES.get(
            norm_diff, DIFFICULTY_GUIDELINES["medium"]
        )
        variation_seed = f"{uuid.uuid4().hex[:8]}_{random.randint(1000, 9999)}"

        if exclude_questions:
            exclude_instruction = (
                "CRITICAL: Do NOT generate or repeat any of these previously asked questions:\n"
                + "\n".join(f"- {q.strip()[:120]}" for q in exclude_questions[:15] if q.strip())
            )
        else:
            exclude_instruction = "Ensure all questions in this session are fresh, varied, and unique."

        prompt = QUIZ_GENERATION_PROMPT.format(
            subject=subject,
            difficulty_guideline=diff_guideline,
            count=count,
            language=language,
            variation_seed=variation_seed,
            exclude_instruction=exclude_instruction,
        )

        try:
            assert self._client is not None
            response = await self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional academic quiz generator. Respond only in valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_output_tokens * 2,
                temperature=0.85,
            )
            raw = response.choices[0].message.content or "[]"
            cleaned = clean_json_response(raw)
            data = json.loads(cleaned)
            if isinstance(data, list) and len(data) > 0:
                unique_data: list[dict[str, Any]] = []
                seen_questions: set[str] = set()
                exclude_lower = {q.strip().lower() for q in (exclude_questions or [])}

                for item in data:
                    if not isinstance(item, dict) or "question" not in item:
                        continue
                    q_text = str(item["question"]).strip()
                    q_lower = q_text.lower()
                    if q_lower in seen_questions or q_lower in exclude_lower:
                        continue
                    seen_questions.add(q_lower)
                    unique_data.append(item)

                if len(unique_data) >= count:
                    return unique_data[:count]

                if unique_data:
                    remaining = count - len(unique_data)
                    supplement = generate_curated_quiz(
                        subject=subject,
                        difficulty=norm_diff,
                        count=remaining,
                        language=language,
                        exclude_questions=list(seen_questions | exclude_lower),
                    )
                    return unique_data + supplement

            return generate_curated_quiz(
                subject=subject,
                difficulty=norm_diff,
                count=count,
                language=language,
                exclude_questions=exclude_questions,
            )
        except Exception as e:
            logger.error(f"AI quiz generation failed: {e}")
            return generate_curated_quiz(
                subject=subject,
                difficulty=norm_diff,
                count=count,
                language=language,
                exclude_questions=exclude_questions,
            )

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
            if isinstance(data, list) and len(data) > 0:
                return data
            return self._generate_fallback_study_plan(goal, target_minutes, subjects)
        except Exception as e:
            logger.error(f"Study plan AI generation failed: {e}")
            if "insufficient_quota" in str(e) or "credit_balance_exhausted" in str(e):
                return self._generate_fallback_study_plan(goal, target_minutes, subjects)
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
