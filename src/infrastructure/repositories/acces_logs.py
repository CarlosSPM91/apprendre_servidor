from sqlalchemy.exc import IntegrityError
from typing import Callable, List

from fastapi import HTTPException, status
from sqlmodel import select
from src.infrastructure.entities.users.accces_logs import AccessLog


class AccessRepository:
    def __init__(self, session: Callable):
        self.session = session

    async def create(self, acces: AccessLog) -> None:
        async for session in self.session():
            try:
                session.add(acces)
                await session.commit()
            except IntegrityError as e:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )
            
    async def find(self, acces_id) -> AccessLog:
        async for session in self.session():
            try:
                return (await session.exec(select(AccessLog).where(AccessLog.id == acces_id))).first()
            except IntegrityError as e:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )