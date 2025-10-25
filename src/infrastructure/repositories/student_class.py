from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.student_class import StudentClass
from src.infrastructure.entities.course.subject_class import SubjectClass


class StudentClassRepository:

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, student_class: StudentClass):
        try:
            async for session in self.session():
                session.add(student_class)
                await session.commit()
                await session.refreash(student_class)
                return student_class

        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_all(self, student_class_id:int) -> List[StudentClass]:
        async for session in self.session():
            student_class: List[StudentClass] = (
                await session.exec(select(StudentClass).where(StudentClass.class_id == student_class_id))
            ).all()
            if not student_class:
                return []
            return student_class

    async def get(self, subject_id: int) -> StudentClass:
        async for session in self.session():
            student_class: StudentClass = (
                await session.exec(
                    select(StudentClass).where(StudentClass.id == subject_id)
                )
            ).first()
            if not student_class:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student Class not found",
                )
            return student_class

    async def update_points(self, class_id:int, student_id:int, points:int) -> Optional[StudentClass]:
        async for session in self.session():
            student_class: StudentClass = (
                await session.exec(
                    select(StudentClass).where(StudentClass.class_id == class_id).where(StudentClass.student_id == student_id)
                )
            ).first()

            if student_class:
                student_class.points +=points

                try:
                    session.add(student_class)
                    await session.commit()
                    await session.refresh(student_class)
                    return student_class
                except IntegrityError:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )
            return None

    async def delete(self, student_class_id: int) -> bool:
        async for session in self.session():
            student_class: StudentClass = (
                await session.exec(
                    select(StudentClass).where(StudentClass.id == student_class_id)
                )
            ).first()
            if not student_class:
                raise HTTPException(status_code=404, detail="Student Class not found")

            try:
                await session.delete(student_class)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Student Class already in use. Foreign key constraint violation.",
                )
