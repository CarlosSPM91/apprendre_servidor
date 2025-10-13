"""
Deletion Repository.

Implements data access methods for the DeletionLog entity.

:author: Carlos S. Paredes Morillo
"""

from sqlalchemy.exc import IntegrityError
from typing import Callable, Optional

from fastapi import HTTPException, status
from sqlmodel import select
from src.infrastructure.entities.users.deletion_logs import DeletionLog


class DeletionRepository:
    """Repository for managing DeletionLog persistence.

    Provides methods for creating and retrieving deletion logs.

    :author: Carlos S. Paredes Morillo
    """

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, delete: DeletionLog) -> None:
        """
        Create a new deletion log record in the database.

        Args:
            delete (DeletionLog): The deletion log entity to be persisted.

        Raises:
            HTTPException: If a database integrity or server error occurs.
        """
        async for session in self.session():
            try:
                session.add(delete)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def find(self, deletion_id: int) -> Optional[DeletionLog]:
        """
        Retrieve a deletion log record by its ID.

        Args:
            deletion_id (int): The unique identifier of the deletion log to retrieve.

        Returns:
            Optional[DeletionLog]: The DeletionLog entity if found, otherwise None.

        Raises:
            HTTPException: If a database error occurs during retrieval.
        """
        async for session in self.session():
            try:
                return (
                    await session.exec(
                        select(DeletionLog).where(DeletionLog.id == deletion_id)
                    )
                ).first()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )
