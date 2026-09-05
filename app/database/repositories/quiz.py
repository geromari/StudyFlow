"""Quiz repository."""

import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models.quiz import Quiz, QuizAnswer, QuizQuestion
from app.database.repositories.base import BaseRepository


class QuizRepository(BaseRepository[Quiz]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Quiz)

    async def create_quiz_with_questions(
        self,
        user_id: int,
        subject_id: int | None,
        title: str,
        difficulty: str,
        questions_data: list[dict[str, Any]],
    ) -> Quiz:
        quiz = Quiz(
            user_id=user_id,
            subject_id=subject_id,
            title=title,
            difficulty=difficulty,
            total_questions=len(questions_data),
        )
        self.session.add(quiz)
        await self.session.flush()

        for q in questions_data:
            question = QuizQuestion(
                quiz_id=quiz.id,
                question_text=q["question"],
                options=json.dumps(q["options"]),
                correct_option=q["correct_option"],
                explanation=q.get("explanation"),
            )
            self.session.add(question)

        await self.session.commit()
        await self.session.refresh(quiz, attribute_names=["questions"])
        return quiz

    async def get_quiz_with_questions(self, quiz_id: int) -> Quiz | None:
        stmt = (
            select(Quiz)
            .where(Quiz.id == quiz_id)
            .options(selectinload(Quiz.questions), selectinload(Quiz.answers))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def record_answer(
        self,
        quiz_id: int,
        question_id: int,
        user_id: int,
        selected_option: str,
        is_correct: bool,
    ) -> QuizAnswer:
        answer = QuizAnswer(
            quiz_id=quiz_id,
            question_id=question_id,
            user_id=user_id,
            selected_option=selected_option,
            is_correct=is_correct,
        )
        self.session.add(answer)
        await self.session.commit()
        return answer

    async def finish_quiz(self, quiz_id: int, score: int, xp_earned: int) -> Quiz | None:
        quiz = await self.get_by_id(quiz_id)
        if quiz:
            quiz.score = score
            quiz.xp_earned = xp_earned
            quiz.completed_at = datetime.now(UTC).replace(tzinfo=None)
            await self.session.commit()
            await self.session.refresh(quiz)
        return quiz

    async def get_user_quiz_stats(self, user_id: int) -> dict[str, Any]:
        stmt = select(
            func.count(Quiz.id),
            func.avg((Quiz.score * 100.0) / func.nullif(Quiz.total_questions, 0)),
        ).where(Quiz.user_id == user_id, Quiz.completed_at.is_not(None))
        result = await self.session.execute(stmt)
        row = result.first()
        count = row[0] if row else 0
        avg_score = round(float(row[1]), 1) if row and row[1] is not None else 0.0
        return {
            "completed_count": count,
            "average_score": avg_score,
        }

    async def count_total_quizzes(self) -> int:
        stmt = select(func.count(Quiz.id)).where(Quiz.completed_at.is_not(None))
        result = await self.session.execute(stmt)
        return result.scalar() or 0
