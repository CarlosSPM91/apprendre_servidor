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
        async for session in self.session:
            print("------REPO---->"+(str(payload.role_id)))
            user = User(
                username=payload.username,
                name=payload.name,
                last_name=payload.last_name,
                email=payload.email or None,
                phone=payload.phone or None,
                dni=payload.dni or None,
                password=payload.password,
                role_id=payload.role_id,
            )
            print("------REPO---->"+(str(user.role_id)))
            session.add(user)
            await session.commit()
            await session.refresh(user)

            return UserDTO(
                user_id=user.id,
                username=user.username,
                name=user.name,
                last_name=user.last_name,
                role=user.role_id
            )

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> Optional[UserDTO]:
        async for session in self.session:
            user: User = (await session.exec(select(User).where(User.id == user_id))).first()
            
            if not user:
                return None
                
            return UserDTO(
                user_id=user.id,
                username=user.username,
                name=user.name,
                last_name=user.last_names,
                role=user.role,
            )

    async def get_user_by_username(
        self,
        username: str,
    ) -> Optional[UserUpdateDTO]:
        async for session in self.session:
            user: User = (await session.exec(
                select(User).where(User.username == username)
            )).first()
            
            if user:
                return UserUpdateDTO(
                    user_id=user.id,
                    name=user.name,
                    last_name=user.last_name,
                    username=user.username,
                    dni=user.dni,
                    email=user.email,
                    phone=user.phone,
                    role_id=user.role_id
                )
            return None

    async def update_last_used(
        self,
        user_id: int,
    ) -> bool:
        async for session in self.session:
            user: User = (await session.exec(select(User).where(User.id == user_id))).first()

            if user:
                user.last_used = datetime.now(timezone.utc)
                session.add(user)
                await session.commit()
                return True
            return False

    async def update_user(
        self,
        user_update: UserUpdateDTO,
    ) -> UserDTO:
        async for session in self.session:
            user: User = (await session.exec(select(User).where(User.id == user_update.user_id))).first()

            if user:
                for field, value in user_update.model_dump(exclude_unset=True).items():
                    if field != 'user_id':  # No actualizar el ID
                        setattr(user, field, value)

                session.add(user)
                await session.commit()
                await session.refresh(user)
                return UserDTO(
                    user_id=user.id,
                    username=user.username,
                    name=user.name,
                    last_name=user.last_name,
                    role=user.role_id,
                )
            return None

    async def change_password(self, user_id: int, hash_pass: str) -> bool:
        async for session in self.session:
            user: User = (await session.exec(select(User).where(User.id == user_id))).first()
            if user:
                user.password = hash_pass
                session.add(user)
                await session.commit()
                return True
            return False
        
    async def delete(self, user_id: int) -> bool:
        async for session in self.session:
            user: User = (await session.exec(select(User).where(User.id == user_id))).first()
            if user:
                session.delete(user)
                await session.commit()
                return True
            return False