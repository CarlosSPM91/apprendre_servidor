"""
Create User Use Case.

Handles the creation of new users, including password hashing
and duplicate username checks.

:author: Carlos S. Paredes Morillo
"""

from datetime import datetime, timezone
from fastapi import HTTPException, status
from src.application.services.password_service import PasswordService
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.infrastructure.repositories.user import UserRepository


class CreateUserCase:
    """Use case for creating new users in the system."""

    def __init__(self, pwd_service: PasswordService, repo: UserRepository):
        """
        Initialize the CreateUserCase with required services and repository.

        Args:
            pwd_service (PasswordService): Service for hashing passwords.
            repo (UserRepository): Repository for user persistence.
        """
        self.pwdService = pwd_service
        self.userRepo = repo

    async def create(self, payload: UserCreateDTO) -> CommonResponse:
        """
        Create a new user, ensuring the username is unique and hashing the password.

        Args:
            payload (UserCreateDTO): Data transfer object containing user information.

        Returns:
            CommonResponse: Response containing the new user's ID and the event timestamp.

        Raises:
            HTTPException: If the username already exists (HTTP 409 Conflict).
        """
        user_check = await self.userRepo.get_user_by_username(payload.username)
        if user_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exist"
            )

        pwd_hash = self.pwdService.hash_password(payload.password)
        payload.password = pwd_hash

        user_created = await self.userRepo.create(payload)

        return CommonResponse(
            item_id=user_created.user_id,
            event_date=datetime.now(timezone.utc)
        )
