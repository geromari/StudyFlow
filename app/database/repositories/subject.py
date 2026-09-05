"""Subject and Topic repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models.subject import Subject, Topic
from app.database.repositories.base import BaseRepository


class SubjectRepository(BaseRepository[Subject]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Subject)

    async def get_user_subjects(self, user_id: int) -> list[Subject]:
        stmt = (
            select(Subject)
            .where(Subject.user_id == user_id)
            .options(selectinload(Subject.topics))
            .order_by(Subject.id.asc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_with_topics(self, subject_id: int) -> Subject | None:
        stmt = (
            select(Subject)
            .where(Subject.id == subject_id)
            .options(selectinload(Subject.topics))
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_subject(self, user_id: int, name: str, color_icon: str = "📚") -> Subject:
        subject = Subject(user_id=user_id, name=name, color_icon=color_icon)
        self.session.add(subject)
        await self.session.commit()
        await self.session.refresh(subject)
        return subject

    async def rename_subject(self, subject_id: int, new_name: str) -> Subject | None:
        subject = await self.get_by_id(subject_id)
        if subject:
            subject.name = new_name
            await self.session.commit()
            await self.session.refresh(subject)
        return subject

    async def update_progress(self, subject_id: int, percent: int) -> Subject | None:
        subject = await self.get_by_id(subject_id)
        if subject:
            subject.progress_percent = max(0, min(100, percent))
            await self.session.commit()
            await self.session.refresh(subject)
        return subject

    # Topic methods
    async def add_topic(self, subject_id: int, name: str) -> Topic:
        topic = Topic(subject_id=subject_id, name=name)
        self.session.add(topic)
        await self.session.commit()
        await self.session.refresh(topic)
        return topic

    async def get_topics(self, subject_id: int) -> list[Topic]:
        stmt = select(Topic).where(Topic.subject_id == subject_id).order_by(Topic.id.asc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def toggle_topic(self, topic_id: int) -> Topic | None:
        topic = await self.session.get(Topic, topic_id)
        if topic:
            topic.is_completed = not topic.is_completed
            await self.session.commit()
            await self.session.refresh(topic)

            # Recalculate subject progress percentage
            subject_topics = await self.get_topics(topic.subject_id)
            if subject_topics:
                completed = sum(1 for t in subject_topics if t.is_completed)
                percent = int((completed / len(subject_topics)) * 100)
                await self.update_progress(topic.subject_id, percent)

        return topic

    async def delete_topic(self, topic_id: int) -> bool:
        topic = await self.session.get(Topic, topic_id)
        if topic:
            subject_id = topic.subject_id
            await self.session.delete(topic)
            await self.session.commit()

            # Recalculate subject progress
            remaining = await self.get_topics(subject_id)
            percent = int((sum(1 for t in remaining if t.is_completed) / len(remaining)) * 100) if remaining else 0
            await self.update_progress(subject_id, percent)
            return True
        return False
