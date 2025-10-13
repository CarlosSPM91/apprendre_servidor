"""
Delete User Use Case.

Handles the deletion of users, including logging the deletion
with information about who performed the action.

:author: Carlos S. Paredes Morillo
"""

from datetime import datetime, timezone
from src.application.use_case.user.find_user_case import FindUserCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.users.deletion_logs import DeletionLog
from src.infrastructure.repositories.deletion_logs import DeletionRepository
from src.infrastructure.repositories.user import UserRepository


class DeleteUserCase:
    """Use case for deleting users and logging the deletion."""

    def __init__(
        self,
        repo: UserRepository,
        find_user_case: FindUserCase,
        deletion_repo: DeletionRepository,
    ):
        """
        Initialize the DeleteUserCase with required repositories and services.

        Args:
            repo (UserRepository): Repository for user persistence.
            find_user_case (FindUserCase): Use case for retrieving user information.
            deletion_repo (DeletionRepository): Repository for logging deletions.
        """
        self.userRepo = repo
        self.find_case = find_user_case
        self.deletion_repo = deletion_repo

    async def delete(self, user_id: int, user_who_delete: int) -> CommonResponse:
        """
        Delete a user and log the deletion action.

        Args:
            user_id (int): The ID of the user to delete.
            user_who_delete (int): The ID of the user performing the deletion.

        Returns:
            CommonResponse: Contains the deleted user's ID and the timestamp of the deletion.

        Raises:
            HTTPException: If the user or the deleting user does not exist.
        """
        user = await self.find_case.get_user_by_id(user_id)
        user_eraser = await self.find_case.get_user_by_id(user_who_delete)

        deletion_log = DeletionLog(
            user_id=user.user_id,
            name=user.name,
            last_name=user.last_name,
            deletion_date=datetime.now(timezone.utc),
            user_who_deleted=user_eraser.user_id,
            name_who_deleted=user_eraser.name,
            last_name_who_deleted=user_eraser.last_name,
        )
        await self.deletion_repo.create(deletion_log)
        resp = await self.userRepo.delete(user_id)
        if resp:
            return CommonResponse(
                item_id=user_id, event_date=datetime.now(timezone.utc)
            )
