"""
Users Service.

Contains the business logic for user management, acting as the
application service layer.

:author: Carlos S. Paredes Morillo
"""

from typing import Optional

from fastapi import Depends
from src.application.services.password_service import PasswordService
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_dto import UserDTO
from src.infrastructure.entities.user import User
from src.infrastructure.repositories.user import UserRepository


class UserService:
    """Application service for user operations.

    Coordinates between the repository and higher-level controllers.

    :author: Carlos S. Paredes Morillo
    """

    async def __init__(self, repo: UserRepository, pwd_service: PasswordService):
        """Initialize the service with a UserRepository.

        Args:
            repo (UserRepository): Repository handling persistence.

        :author: Carlos S. Paredes Morillo
        """
        self.userRepo = repo
        self.pwdService = pwd_service

    async def create(
        self,
        payload: UserCreateDTO,
    ) -> UserDTO:
        """Create a new user.

        Args:
            payload (UserCreateDTO): Data for creating the user.

        Returns:
            UserDTO: Data Transfer Object representing the created user.

        :author: Carlos S. Paredes Morillo
        """
        pwd_hash= self.pwdService.hash_password(payload.password)
        payload.password= pwd_hash
        return self.userRepo.create(payload)

    async def getUserByUsermame(self, user_id: int) -> Optional[User]:

        self.userRepo.getUserByUsermame(user_id)

    async def getUserbyId(self, user_id: int) -> Optional[UserDTO]:

        self.userRepo.getById(user_id)

    async def updateLastUsed(self, user_id: int) -> bool:

        self.userRepo.updateLastUsed(user_id)
