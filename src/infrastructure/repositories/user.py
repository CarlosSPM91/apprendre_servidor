"""
Users Repository.

Implements data access methods for the User entity.

:author: Carlos S. Paredes Morillo
"""

from fastapi import Depends

from src.application.services.password_service import PasswordService
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_dto import UserDTO
from sqlmodel.ext.asyncio.session import AsyncSession

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
            user = User(
                username=payload.username,
                name=payload.name,
                last_names=payload.last_name,
                email=payload.email | None,
                phone=payload.phone | None,
                dni=payload.dni | None,
                password=payload.password,
                role=payload.role_id,
            )
        session.add(user)
        await session.commit()
        await session.refresh()

        return UserDTO(
            id=user.id, name=user.name, last_name=user.last_names, role=user.role
        )
