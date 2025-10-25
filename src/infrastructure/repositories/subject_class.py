from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.subject_class import SubjectClass


class SubjectClassRepository:

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, subject_class: SubjectClass):
        try:
            async for session in self.session():
                session.add(subject_class)
                await session.commit()
                await session.refreash(subject_class)
                return subject_class

        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_all(self) -> List[SubjectClass]:
        async for session in self.session():
            subject_classes: List[SubjectClass] = (
                await session.exec(select(SubjectClass))
            ).all()
            if not subject_classes:
                return []
            return subject_classes

    async def get(self, subject_id: int) -> SubjectClass:
        async for session in self.session():
            subject_class: SubjectClass = (
                await session.exec(
                    select(SubjectClass).where(SubjectClass.id == subject_id)
                )
            ).first()
            if not subject_class:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subject Class not found",
                )
            return subject_class

    async def update(self, subject_class_upt: SubjectClass) -> Optional[SubjectClass]:
        async for session in self.session():
            subject: SubjectClass = (
                await session.exec(
                    select(SubjectClass).where(SubjectClass.id == subject_class_upt.id)
                )
            ).first()

            if subject:
                for field, value in subject_class_upt.model_dump(
                    exclude_unset=True
                ).items():
                    if field != "id" or field != "subject_id":
                        setattr(subject, field, value)

                try:
                    session.add(subject)
                    await session.commit()
                    await session.refresh(subject)
                    return subject
                except IntegrityError:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )
            return None

    async def delete(self, subject_class_id: int) -> bool:
        async for session in self.session():
            subject_class: SubjectClass = (
                await session.exec(
                    select(SubjectClass).where(SubjectClass.id == subject_class_id)
                )
            ).first()
            if not subject_class:
                raise HTTPException(status_code=404, detail="Subject Class not found")

            try:
                await session.delete(subject_class)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Subject Class already in use. Foreign key constraint violation.",
                )
