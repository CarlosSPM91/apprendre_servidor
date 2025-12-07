from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.student_class import StudentClass

"""
StudentClass Repository.

Implements data access methods for the StudentClass entity.

:author: Carlos S. Paredes Morillo
"""

class StudentClassRepository:
    """Repository for managing StudentClass persistence.

    Provides CRUD operations for interacting with the StudentClass entity.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, session: Callable):
        """Initialize the repository with a session factory.

        Args:
            session (Callable): A callable that returns an async database session.
        """
        self.session = session

    async def create(self, student_class: StudentClass) -> StudentClass:
        """Create a new student-class association.

        Args:
            student_class (StudentClass): The StudentClass entity to create.

        Returns:
            StudentClass: The created student-class entity.

        Raises:
            HTTPException: If a database integrity error occurs.
        """
        try:
            async for session in self.session():
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

    async def get_all(self, class_id: int) -> List[StudentClass]:
        """Retrieve all students associated with a given class.

        Args:
            class_id (int): The ID of the class.

        Returns:
            List[StudentClass]: A list of student-class associations. Returns an empty list if none exist.

        Raises:
            HTTPException: If a database error occurs.
        """
        async for session in self.session():
            student_class: List[StudentClass] = (
                await session.exec(
                    select(StudentClass).where(StudentClass.class_id == class_id)
                )
            ).all()
            return student_class or []

    async def get(self, student_class_id: int) -> StudentClass:
        """Retrieve a student-class association by ID.

        Args:
            student_class_id (int): The ID of the student-class association.

        Returns:
            StudentClass: The student-class entity.

        Raises:
            HTTPException: If the entity is not found.
        """
        async for session in self.session():
            student_class: StudentClass = (
                await session.exec(
                    select(StudentClass).where(StudentClass.id == student_class_id)
                )
            ).first()
            if not student_class:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student Class not found",
                )
            return student_class

    async def update_points(self, payload: StudentClass) -> Optional[StudentClass]:
        """Update the points of a student in a class.

        Args:
            payload (StudentClass): StudentClass entity containing class_id, student_id, and points to add.

        Returns:
            Optional[StudentClass]: The updated student-class entity, or None if not found.

        Raises:
            HTTPException: If the student-class association is not found or a database error occurs.
        """
        async for session in self.session():
            student_class: StudentClass = (
                await session.exec(
                    select(StudentClass)
                    .where(StudentClass.class_id == payload.class_id)
                    .where(StudentClass.student_id == payload.student_id)
                )
            ).first()

            if student_class is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student Class not found",
                )

            student_class.points += payload.points

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

    async def delete(self, student_class_id: int) -> bool:
        """Delete a student-class association by ID.

        Args:
            student_class_id (int): The ID of the student-class association.

        Returns:
            bool: True if deletion succeeded.

        Raises:
            HTTPException: If the entity is not found or a database integrity error occurs.
        """
        async for session in self.session():
            student_class: StudentClass = (
                await session.exec(
                    select(StudentClass).where(StudentClass.id == student_class_id)
                )
            ).first()
            if not student_class:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Student Class not found",
                )

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
