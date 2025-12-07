from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select

from src.infrastructure.entities.course.subject_class import SubjectClass

"""
SubjectClass Repository.

Implements data access methods for the SubjectClass entity.

:author: Carlos S. Paredes Morillo
"""

class SubjectClassRepository:
    """Repository for managing SubjectClass persistence.

    Provides CRUD operations for interacting with the SubjectClass entity.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, session: Callable):
        """Initialize the repository with a session factory.

        Args:
            session (Callable): A callable that returns an async database session.
        """
        self.session = session

    async def create(self, subject_class: SubjectClass) -> SubjectClass:
        """Create a new subject-class association.

        Args:
            subject_class (SubjectClass): The SubjectClass entity to create.

        Returns:
            SubjectClass: The created subject-class entity.

        Raises:
            HTTPException: If a database integrity error occurs.
        """
        try:
            async for session in self.session():
                session.add(subject_class)
                await session.commit()
                await session.refresh(subject_class)
                return subject_class
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_all(self) -> List[SubjectClass]:
        """Retrieve all subject-class associations.

        Returns:
            List[SubjectClass]: A list of subject-class associations. Returns an empty list if none exist.

        Raises:
            HTTPException: If a database error occurs.
        """
        async for session in self.session():
            subject_classes: List[SubjectClass] = (await session.exec(select(SubjectClass))).all()
            return subject_classes or []

    async def get(self, subject_class_id: int) -> SubjectClass:
        """Retrieve a subject-class association by ID.

        Args:
            subject_class_id (int): The ID of the subject-class association.

        Returns:
            SubjectClass: The subject-class entity.

        Raises:
            HTTPException: If the entity is not found.
        """
        async for session in self.session():
            subject_class: SubjectClass = (
                await session.exec(
                    select(SubjectClass).where(SubjectClass.id == subject_class_id)
                )
            ).first()
            if not subject_class:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subject Class not found",
                )
            return subject_class

    async def update(self, subject_class_upt: SubjectClass) -> Optional[SubjectClass]:
        """Update a subject-class association.

        Args:
            subject_class_upt (SubjectClass): SubjectClass entity with updated fields.

        Returns:
            Optional[SubjectClass]: The updated entity, or None if not found.

        Raises:
            HTTPException: If a database error occurs.
        """
        async for session in self.session():
            subject: SubjectClass = (
                await session.exec(
                    select(SubjectClass).where(SubjectClass.id == subject_class_upt.id)
                )
            ).first()

            if subject:
                for field, value in subject_class_upt.model_dump(exclude_unset=True).items():
                    if field not in ["id", "subject_id"]:
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
        """Delete a subject-class association by ID.

        Args:
            subject_class_id (int): The ID of the subject-class association.

        Returns:
            bool: True if deletion succeeded.

        Raises:
            HTTPException: If the entity is not found or a database integrity error occurs.
        """
        async for session in self.session():
            subject_class: SubjectClass = (
                await session.exec(
                    select(SubjectClass).where(SubjectClass.id == subject_class_id)
                )
            ).first()
            if not subject_class:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Subject Class not found",
                )

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
