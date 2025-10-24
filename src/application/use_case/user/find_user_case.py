"""
Find User Use Case.

Provides methods to retrieve users by ID, username, or fetch all users.

:author: Carlos S. Paredes Morillo
"""

from typing import List, Optional
from fastapi import HTTPException, status
from src.domain.objects.user.user_dto import UserDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.repositories.user import UserRepository


class FindUserCase:
    """Use case for retrieving user information from the repository."""

    def __init__(self, repo: UserRepository):
        """
        Initialize the FindUserCase with the user repository.

        Args:
            repo (UserRepository): Repository for accessing user data.
        """
        self.userRepo = repo

    async def get_user_by_username(self, username: str) -> Optional[UserUpdateDTO]:
        """
        Retrieve a user by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            Optional[UserUpdateDTO]: User data if found.

        Raises:
            HTTPException: If the user is not found (HTTP 404).
        """
        user = await self.userRepo.get_user_by_username(username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    async def get_user_by_id(self, user_id: int) -> Optional[UserDTO]:
        """
        Retrieve a user by their ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            Optional[UserDTO]: User data if found.

        Raises:
            HTTPException: If the user is not found (HTTP 404).
        """
        user = await self.userRepo.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user

    async def get_all(self) -> Optional[List[UserDTO]]:
        """
        Retrieve all users.

        Returns:
            Optional[List[UserDTO]]: List of users if any exist.

        Raises:
            HTTPException: If no users are found (HTTP 404).
        """
        users: Optional[List[UserDTO]] = await self.userRepo.get_all()
        if users is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Users not found"
            )
        return users
    
    async def get_all_by_role(self, role_id:int) -> Optional[List[UserDTO]]:
        """
        Retrieve all users.

        Returns:
            Optional[List[UserDTO]]: List of users if any exist.

        Raises:
            HTTPException: If no users are found (HTTP 404).
        """
        users: Optional[List[UserDTO]] = await self.userRepo.get_all_by_role(role_id=role_id)
        if users is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Users not found"
            )
        return users
