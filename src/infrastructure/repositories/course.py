from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.course import Course


class CourseRepository:

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, course: Course):
        try:
            async for session in self.session():
                session.add(course)
                await session.commit()
                await session.refresh(course)
                return course

        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_all(self) -> List[Course]:
        async for session in self.session():
            courses: List[Course] = (await session.exec(select(Course))).all()
            return courses

    async def get(self, course_id: int) -> Course:
        async for session in self.session():
            course: Course = (
                await session.exec(select(Course).where(Course.id == course_id))
            ).first()
            if not course:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Course not found"
                )
            return course

    async def update(self, course_upt: Course) -> Optional[Course]:
        async for session in self.session():
            course: Course = (
                await session.exec(select(Course).where(Course.id == course_upt.id))
            ).first()

            if course:
                for field, value in course_upt.model_dump(exclude_unset=True).items():
                    if field != "id" or field != "year":
                        setattr(course, field, value)

                try:
                    session.add(course)
                    await session.commit()
                    await session.refresh(course)
                    return course
                except IntegrityError:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )
            return None

    async def delete(self, course_id: int) -> bool:
        async for session in self.session():
            course: Course = (
                await session.exec(select(Course).where(Course.id == course_id))
            ).first()
            if not course:
                raise HTTPException(status_code=404, detail="Course not found")

            try:
                await session.delete(course)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Course already in use. Foreign key constraint violation.",
                )
