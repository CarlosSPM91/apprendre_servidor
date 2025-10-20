from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.infrastructure.entities.users.parents import Parent

class ParentRepository:
    def __init__(self, session: Callable):
        self.session = session

    async def get (self, user_id: int) -> List[Parent]:
        async for session in self.session():
            parent = (
                await session.exec(
                    select(Parent).where(Parent.user_id == user_id)
                )
            ).all()
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Parent with id {user_id} not found",
                )
            return parent
        
        
    async def create(self, parent: Parent) -> Parent:
        try:
            async for session in self.session():
                session.add(parent)
                await session.commit()
                await session.refresh(parent)
                return parent

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )
    
    async def delete(self, user_id: int, student_id: int) -> bool:
        try:
            async for session in self.session():
                parent = (
                    await session.exec(
                        select(Parent).where(Parent.user_id == user_id and Parent.student_id == student_id)
                    )
                ).first()
                if not parent:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Parent with id {user_id} not found",
                    )
                await session.exec(
                    delete(Parent).where(Parent.id == parent.id)
                )
                await session.commit()
                return True

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )