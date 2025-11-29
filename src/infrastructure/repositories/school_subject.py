from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.school_subject import SchoolSubject


class SchoolSubjectRepository:

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, subject: SchoolSubject):
        try:
            async for session in self.session():
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

    async def get_all(self) -> List[SchoolSubject]:
        async for session in self.session():
            subjects: List[SchoolSubject] = (
                await session.exec(select(SchoolSubject))
            ).all()
            if not subjects:
                return []
            return subjects

    async def get(self, subject_id: int) -> SchoolSubject:
        async for session in self.session():
            subject: SchoolSubject = (
                await session.exec(
                    select(SchoolSubject).where(SchoolSubject.id == subject_id)
                )
            ).first()
            if not subject:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="School Subject not found",
                )
            return subject

    async def update(self, subject_upt: SchoolSubject) -> Optional[SchoolSubject]:
        async for session in self.session():
            subject: SchoolSubject = (
                await session.exec(
                    select(SchoolSubject).where(SchoolSubject.id == subject_upt.id)
                )
            ).first()

            if subject:
                for field, value in subject_upt.model_dump(exclude_unset=True).items():
                    if field != "id":
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

    async def delete(self, subject_id: int) -> bool:
        async for session in self.session():
            subject: SchoolSubject = (
                await session.exec(
                    select(SchoolSubject).where(SchoolSubject.id == subject_id)
                )
            ).first()
            if not subject:
                raise HTTPException(status_code=404, detail="School Subject not found")

            try:
                await session.delete(subject)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="School Subject already in use. Foreign key constraint violation.",
                )
