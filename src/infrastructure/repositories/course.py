from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.course import Course

"""
Course Repository.

Implements data access methods for the Course entity.

:author: Carlos S. Paredes Morillo
"""

class CourseRepository:
    """Repository for managing Course persistence.

    Provides CRUD operations for interacting with the Course entity.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, session: Callable):
        """Initialize the repository with a session factory.

        Args:
            session (Callable): A callable that returns an async database session.
        """
        self.session = session

    async def create(self, course: Course) -> Course:
        """Create a new course.

        Args:
            course (Course): The course entity to create.

        Returns:
            Course: The created course.

        Raises:
            HTTPException: If a database integrity error occurs.
        """
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
        """Retrieve all courses.

        Returns:
            List[Course]: A list of course entities.

        Raises:
            HTTPException: If a database error occurs.
        """
        async for session in self.session():
            courses: List[Course] = (await session.exec(select(Course))).all()
            return courses

    async def get(self, course_id: int) -> Course:
        """Retrieve a course by ID.

        Args:
            course_id (int): The ID of the course.

        Returns:
            Course: The course entity.

        Raises:
            HTTPException: If the course is not found.
        """
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
        """Update a course's details.

        Args:
            course_upt (Course): Course entity with updated fields.

        Returns:
            Optional[Course]: The updated course, or None if not found.

        Raises:
            HTTPException: If the course is not found or a database integrity error occurs.
        """
        async for session in self.session():
            course: Course = (
                await session.exec(select(Course).where(Course.id == course_upt.id))
            ).first()

            if course is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Course not found",
                )

            for field, value in course_upt.model_dump(exclude_unset=True).items():
                if field != "id":
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

    async def delete(self, course_id: int) -> bool:
        """Delete a course by ID.

        Args:
            course_id (int): The ID of the course.

        Returns:
            bool: True if deletion succeeded.

        Raises:
            HTTPException: If the course is not found or a database integrity error occurs.
        """
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
