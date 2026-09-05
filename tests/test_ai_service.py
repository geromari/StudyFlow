"""Unit tests for AI service and prompt templates."""

import pytest

from app.services.ai.client import AIService, clean_json_response


def test_clean_json_response() -> None:
    wrapped = "```json\n[{\"question\": \"What is 1+1?\"}]\n```"
    assert clean_json_response(wrapped) == '[{"question": "What is 1+1?"}]'

    clean = '[{"question": "What is 1+1?"}]'
    assert clean_json_response(clean) == clean


@pytest.mark.asyncio
async def test_mock_ai_service_chat() -> None:
    ai = AIService(api_key="")  # Unconfigured -> uses fallback mock
    assert not ai.is_configured

    response, tokens = await ai.chat(
        conversation_history=[],
        user_prompt="Explain recursion",
        mode="explain",
    )
    assert "StudyFlow AI Response" in response
    assert "recursion" in response
    assert tokens > 0


@pytest.mark.asyncio
async def test_mock_ai_quiz_generation() -> None:
    ai = AIService(api_key="")
    questions = await ai.generate_quiz(subject="Python", difficulty="easy", count=3)
    assert len(questions) == 3
    for q in questions:
        assert "question" in q
        assert "options" in q
        assert "correct_option" in q


@pytest.mark.asyncio
async def test_mock_ai_study_plan_generation() -> None:
    ai = AIService(api_key="")
    plan = await ai.generate_study_plan(
        goal="Master Python",
        target_minutes=60,
        subjects=["Python", "Algorithms"],
    )
    assert len(plan) == 2
    assert plan[0]["duration_minutes"] > 0
