"""
Users Repository.

Implements data access methods for the User entity.

:author: Carlos S. Paredes Morillo
"""

from datetime import datetime, timezone
from typing import Optional
from fastapi import Depends

from src.application.services.password_service import PasswordService
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_dto import UserDTO
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.entities.user import User


class UserRepository:
    """Repository for managing User persistence.

    Provides CRUD operations over the User entity.

    :author: Carlos S. Paredes Morillo
    """

    def __init__(self, session):
        self.session = session

    async def create(
        self,
        payload: UserCreateDTO,
    ) -> UserDTO:
        """Persist a new user in the database.

        Args:
            session (AsyncSession): Active asynchronous database session.
            user (User): User entity to be persisted.

        Returns:
            UserDTO: The newly created user with refreshed state.

        :author: Carlos S. Paredes Morillo
        """
        async with self.session as session:
            user = User(
                username=payload.username,
                name=payload.name,
                last_names=payload.last_name,
                email=payload.email or None,
                phone=payload.phone or None,
                dni=payload.dni or None,
                password=payload.password,
                role=payload.role_id,
            )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        return UserDTO(
            id=user.id, name=user.name, last_name=user.last_names, role=user.role
        )

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> Optional[UserDTO]:
        async with self.session as session:
            user: User = await session.exec(select(User).where(User.id == user_id)).first()

        return UserDTO(
            user_id=user.id,
            username=user.username,
            name=user.name,
            last_name=user.last_names,
            role=user.role_id,
        )

    async def get_user_by_username(
        self,
        username: str,
    ) -> Optional[User]:
        async with self.session as session:
            return await session.exec(
                select(User).where(User.username == username)
            ).first()

    async def update_last_used(
        self,
        user_id: int,
    ) -> bool:
        async with self.session as session:
            user: User = await session.exec(select(User).where(User.id == user_id)).first()

            if user:
                user.last_used = datetime.now(timezone.utc)
                session.add(user)
                await session.commit()
                return True
            return False

    async def update_user(
        self,
        user_update: UserUpdateDTO,
    ) -> bool:
        async with self.session as session:
            user: User = await session.exec(select(User).where(User.id == user.id)).first()

            if user:
                for field, value in user_update.model_dump(exclude_unset=True).items():
                    setattr(user, field, value)

                session.add(user)
                await session.commit()
                await session.refresh(user)
                return UserDTO(
                    user_id=user.id,
                    name=user.name,
                    last_name=user.last_names,
                    role=user.role,
                )

    async def change_password(self, user_id: int, hash_pass: str) -> bool:
        async with self.session as session:
            user: User = await session.exec(select(User).where(User.id == user_id)).first()
            if user:
                user.password = hash_pass
                session.add(user)
                await session.commit()
                return True
            return False
        
    async def delete(self, user_id: int) -> bool:
        async with self.session as session:
            user: User = await session.exec(select(User).where(User.id == user_id)).first()
            if user:
                session.delete(user)
                await session.commit()
                return True
            return False