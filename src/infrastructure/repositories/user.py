"""
Users Repository.

Implements data access methods for the User entity.

:author: Carlos S. Paredes Morillo
"""
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_dto import UserDTO
from sqlmodel.ext.asyncio.session import AsyncSession

from src.infrastructure.entities.user import User


class UserRepository:
    """Repository for managing User persistence.

    Provides CRUD operations over the User entity.

    :author: Carlos S. Paredes Morillo
    """
    async def create(self, session:AsyncSession, user: User) -> UserDTO:
        """Persist a new user in the database.

        Args:
            session (AsyncSession): Active asynchronous database session.
            user (User): User entity to be persisted.

        Returns:
            UserDTO: The newly created user with refreshed state.

        :author: Carlos S. Paredes Morillo
        """
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user