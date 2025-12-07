from sqlalchemy.exc import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select
from src.infrastructure.entities.course.activity_type import ActivityType

"""
ActivityType Repository.

Implements data access methods for the ActivityType entity.

:author: Carlos S. Paredes Morillo
"""

class ActivityTypeRepository:
    """Repository for managing ActivityType persistence.

    Provides CRUD operations for interacting with the ActivityType entity.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, session: Callable):
        """Initialize the repository with a session factory.

        Args:
            session (Callable): A callable that returns an async database session.
        """
        self.session = session

    async def create(self, activity_name: str) -> ActivityType:
        """Create a new activity type.

        Args:
            activity_name (str): The name of the activity type.

        Returns:
            ActivityType: The created activity type entity.

        Raises:
            HTTPException: If a database integrity error occurs.
        """
        async for session in self.session():
            new_type = ActivityType(activity_name=activity_name)
            try:
                session.add(new_type)
                await session.commit()
                await session.refresh(new_type)
                return new_type
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def get_all(self) -> List[ActivityType]:
        """Retrieve all activity types.

        Returns:
            List[ActivityType]: A list of activity type entities. Returns an empty list if none exist.

        Raises:
            HTTPException: If a database error occurs.
        """
        async for session in self.session():
            types: List[ActivityType] = (await session.exec(select(ActivityType))).all()
            return types or []

    async def find_by_id(self, activity_id: int) -> Optional[ActivityType]:
        """Find an activity type by ID.

        Args:
            activity_id (int): The ID of the activity type.

        Returns:
            Optional[ActivityType]: The found activity type, or None if not found.
        """
        async for session in self.session():
            return (
                await session.exec(
                    select(ActivityType).where(ActivityType.id == activity_id)
                )
            ).first()

    async def find_by_name(self, activity_name: str) -> Optional[ActivityType]:
        """Find an activity type by name.

        Args:
            activity_name (str): The name of the activity type.

        Returns:
            Optional[ActivityType]: The found activity type, or None if not found.
        """
        async for session in self.session():
            return (
                await session.exec(
                    select(ActivityType).where(ActivityType.activity_name == activity_name)
                )
            ).first()

    async def update(self, type_upt: ActivityType) -> Optional[ActivityType]:
        """Update an activity type's details.

        Args:
            type_upt (ActivityType): ActivityType entity with updated fields.

        Returns:
            Optional[ActivityType]: The updated entity, or None if not found.

        Raises:
            HTTPException: If a database integrity error occurs.
        """
        async for session in self.session():
            existing_type: ActivityType = (
                await session.exec(
                    select(ActivityType).where(ActivityType.id == type_upt.id)
                )
            ).first()

            if existing_type:
                if type_upt.activity_name is not None:
                    existing_type.activity_name = type_upt.activity_name
                try:
                    session.add(existing_type)
                    await session.commit()
                    await session.refresh(existing_type)
                    return existing_type
                except IntegrityError:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )
            return None

    async def delete(self, type_id: int) -> bool:
        """Delete an activity type by ID.

        Args:
            type_id (int): The ID of the activity type.

        Returns:
            bool: True if deletion succeeded.

        Raises:
            HTTPException: If the entity is not found or a database integrity error occurs.
        """
        async for session in self.session():
            existing_type: ActivityType = (
                await session.exec(
                    select(ActivityType).where(ActivityType.id == type_id)
                )
            ).first()
            if not existing_type:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Activity Type not found",
                )
            try:
                await session.delete(existing_type)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Activity Type already in use. Foreign key constraint violation.",
                )
