from sqlalchemy.exc import IntegrityError
from typing import Callable, List

from fastapi import HTTPException, status

from sqlmodel import select
from src.infrastructure.entities.users.deletion_logs import DeletionLog


class DeletionRepository:
    def __init__(self, session: Callable):
        self.session = session

    async def create(self, delete: DeletionLog) -> None:
        async for session in self.session():
            try:
                session.add(delete)
                await session.commit()
            except IntegrityError as e:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )