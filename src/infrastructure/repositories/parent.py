from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.domain.objects.profiles.parent_info import ParentDTO
from src.infrastructure.entities.users.parents import Parent
from src.infrastructure.entities.users.user import User


class ParentRepository:
    def __init__(self, session: Callable):
        self.session = session

    async def get(self, user_id: int) -> List[Parent]:
        async for session in self.session():
            parent = (
                await session.exec(select(Parent).where(Parent.user_id == user_id))
            ).all()
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent not found",
                )
            return parent

    async def get_all(self) -> List[ParentDTO]:
        try:
            async for session in self.session():
                users = (
                    await session.exec(select(User).where(User.role_id == 4))
                ).all()
                if not users:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Parents not found",
                    )
                parents = (await session.exec(select(Parent))).all()

                parent_by_user = {}
                for parent in parents:
                    if parent.user_id not in parent_by_user:
                        parent_by_user[parent.user_id] = []
                    parent_by_user[parent.user_id].append(parent.student_id)

                parent_dto = []
                for user in users:
                    parent_dto.append(
                        ParentDTO(
                            user_id=user.id,
                            name=user.name,
                            last_name=user.last_name,
                            dni=user.dni,
                            phone=user.phone,
                            email=user.email,
                            username=user.username,
                            students=parent_by_user.get(user.id, []),
                        )
                    )
                return parent_dto
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

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
                        select(Parent).where(
                            (Parent.user_id == user_id)
                            & (Parent.student_id == student_id)
                        )
                    )
                ).first()
                if not parent:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Parent not found",
                    )
                await session.exec(delete(Parent).where(Parent.id == parent.id))
                await session.commit()
                return True

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )
