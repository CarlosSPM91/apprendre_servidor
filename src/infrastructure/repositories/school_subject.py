from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.school_subject import SchoolSubject

"""
SchoolSubject Repository.

Implements data access methods for the SchoolSubject entity.

:author: Carlos S. Paredes Morillo
"""

class SchoolSubjectRepository:
    """Repository for managing SchoolSubject persistence.

    Provides CRUD operations for interacting with the SchoolSubject entity.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, session: Callable):
        """Initialize the repository with a session factory.

        Args:
            session (Callable): A callable that returns an async database session.
        """
        self.session = session

    async def create(self, subject: SchoolSubject) -> SchoolSubject:
        """Create a new school subject.

        Args:
            subject (SchoolSubject): The school subject entity to create.

        Returns:
            SchoolSubject: The created school subject.

        Raises:
            HTTPException: If a database error occurs.
        """
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
        """Retrieve all school subjects.

        Returns:
            List[SchoolSubject]: A list of school subject entities. Returns an empty list if none exist.

        Raises:
            HTTPException: If a database error occurs.
        """
        try:
            async for session in self.session():
                subjects: List[SchoolSubject] = (await session.exec(select(SchoolSubject))).all()
                return subjects or []
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get(self, subject_id: int) -> SchoolSubject:
        """Retrieve a school subject by ID.

        Args:
            subject_id (int): The ID of the school subject.

        Returns:
            SchoolSubject: The school subject entity.

        Raises:
            HTTPException: If the subject is not found.
        """
        async for session in self.session():
            subject: SchoolSubject = (
                await session.exec(select(SchoolSubject).where(SchoolSubject.id == subject_id))
            ).first()
            if not subject:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="School Subject not found",
                )
            return subject

    async def update(self, subject_upt: SchoolSubject) -> Optional[SchoolSubject]:
        """Update a school subject's details.

        Args:
            subject_upt (SchoolSubject): School subject entity with updated fields.

        Returns:
            Optional[SchoolSubject]: The updated subject, or None if not found.

        Raises:
            HTTPException: If a database error occurs.
        """
        async for session in self.session():
            subject: SchoolSubject = (
                await session.exec(select(SchoolSubject).where(SchoolSubject.id == subject_upt.id))
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
        """Delete a school subject by ID.

        Args:
            subject_id (int): The ID of the school subject.

        Returns:
            bool: True if deletion succeeded.

        Raises:
            HTTPException: If the subject is not found or a database integrity error occurs.
        """
        async for session in self.session():
            subject: SchoolSubject = (
                await session.exec(select(SchoolSubject).where(SchoolSubject.id == subject_id))
            ).first()
            if not subject:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="School Subject not found",
                )

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
