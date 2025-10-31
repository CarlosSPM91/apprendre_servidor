"""
Access Repository.

Implements data access methods for the AccessLog entity.

:author: Carlos S. Paredes Morillo
"""

from sqlalchemy.exc import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select
from src.infrastructure.entities.users.accces_logs import AccessLog


class AccessRepository:
    """Repository for managing AccessLog persistence.

    Provides methods for creating and retrieving access log records.

    :author: Carlos S. Paredes Morillo
    """

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, acces: AccessLog) -> None:
        """
        Create a new access log record in the database.

        Args:
            acces (AccessLog): The access log entity to be persisted.

        Raises:
            HTTPException: If a database integrity or server error occurs.
        """
        async for session in self.session():
            try:
                session.add(acces)
                await session.commit()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def find(self, acces_id: int) -> Optional[AccessLog]:
        """
        Retrieve an access log record by its ID.

        Args:
            acces_id (int): The unique identifier of the access log to retrieve.

        Returns:
            Optional[AccessLog]: The AccessLog entity if found, otherwise None.

        Raises:
            HTTPException: If a database error occurs during retrieval.
        """
        async for session in self.session():
            try:
                return (
                    await session.exec(
                        select(AccessLog).where(AccessLog.id == acces_id)
                    )
                ).first()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )
    
    async def get_all(self) -> List[AccessLog]:
        """
        Retrieve a list of access logs.

        Args:
            acces_id (int): The unique identifier of the access log to retrieve.

        Returns:
            List[AccessLog]: A list of the AccessLog entity if found, otherwise None.

        Raises:
            HTTPException: If a database error occurs during retrieval.
        """
        async for session in self.session():
            try:
                return (
                    await session.exec(
                        select(AccessLog).where()
                    )
                ).all()
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )
