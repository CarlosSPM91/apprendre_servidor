"""
Update User Use Case.

Handles updating user data, last login timestamp, and password changes.

:author: Carlos S. Paredes Morillo
"""

from datetime import datetime, timezone
from src.application.services.password_service import PasswordService
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.auth.change_pass_dto import ChangePasswordDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.repositories.user import UserRepository


class UpdateUserCase:
    """Use case for updating user information."""

    def __init__(self, pwd_service: PasswordService, repo: UserRepository):
        """
        Initialize the UpdateUserCase with required services and repository.

        Args:
            pwd_service (PasswordService): Service for password hashing.
            repo (UserRepository): Repository for user persistence.
        """
        self.pwdService = pwd_service
        self.userRepo = repo

    async def update_user(self, userUpt: UserUpdateDTO) -> CommonResponse:
        """
        Update user details.

        Args:
            userUpt (UserUpdateDTO): Data transfer object containing updated user info.

        Returns:
            CommonResponse: Contains the updated user's ID and timestamp.
        """
        user = await self.userRepo.update_user(userUpt)
        if user:
            return CommonResponse(
                item_id=userUpt.user_id,
                event_date=datetime.now(timezone.utc)
            )

    async def update_last_used(self, user_id: int) -> CommonResponse:
        """
        Update the last login timestamp for a user.

        Args:
            user_id (int): The ID of the user to update.

        Returns:
            CommonResponse: Contains the user's ID and timestamp of the update.
        """
        user = await self.userRepo.update_last_used(user_id)
        if user:
            return CommonResponse(
                item_id=user_id,
                event_date=datetime.now(timezone.utc)
            )

    async def change_password(self, payload: ChangePasswordDTO) -> CommonResponse:
        """
        Change a user's password after hashing it.

        Args:
            payload (ChangePasswordDTO): Contains user ID and new password.

        Returns:
            CommonResponse: Contains the user's ID and timestamp of the password change.
        """
        pwd: str = self.pwdService.hash_password(payload.password)
        is_changed = await self.userRepo.change_password(payload.user_id, pwd)
        if is_changed:
            return CommonResponse(
                item_id=payload.user_id,
                event_date=datetime.now(timezone.utc)
            )
