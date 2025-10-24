"""
Users Repository.

Implements data access methods for the User entity.

:author: Carlos S. Paredes Morillo
"""

from datetime import datetime, timezone
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_dto import UserDTO
from sqlmodel import select
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.infrastructure.entities.users.user import User


class UserRepository:
    """Repository for managing User persistence.

    Provides CRUD operations and auxiliary methods
    for interacting with the User entity in the database.

    :author: Carlos S. Paredes Morillo
    """

    def __init__(self, session: Callable):
        self.session = session

    async def create(
        self,
        payload: UserCreateDTO,
    ) -> UserDTO:
        """Create a new user in the database.

        Args:
            payload (UserCreateDTO): Data required to create a new user.

        Returns:
            UserDTO: The created user's data.

        Raises:
            HTTPException: If a database integrity error occurs during user creation.
        """
        async for session in self.session():
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
            session.add(user)
            try:
                await session.commit()
                await session.refresh(user)
                return UserDTO(
                    user_id=user.id,
                    username=user.username,
                    name=user.name,
                    last_name=user.last_name,
                    phone=user.phone,
                    dni=user.dni,
                    role=user.role_id,
                )
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def get_all(
        self,
    ) -> Optional[List[UserDTO]]:
        """Retrieve all users from the database.

        Returns:
            Optional[List[UserDTO]]: A list of users, or raises 404 if none are found.

        Raises:
            HTTPException: If no users are found in the database.
        """
        async for session in self.session():
            users: List[User] = (await session.exec(select(User))).all()

            if not users:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
                )

            return [
                UserDTO(
                    user_id=user.id,
                    username=user.username,
                    name=user.name,
                    last_name=user.last_name,
                    phone=user.phone,
                    email=user.email,
                    dni=user.dni,
                    role=user.role_id,
                )
                for user in users
            ]
    
    async def get_all_by_role(
        self,
        role_id:int
    ) -> Optional[List[UserDTO]]:
        """Retrieve all users by role from the database.

        Returns:
            Optional[List[UserDTO]]: A list of users, or raises 404 if none are found.

        Raises:
            HTTPException: If no users are found in the database.
        """
        async for session in self.session():
            users: List[User] = (await session.exec(select(User).where(User.role_id==role_id))).all()

            if not users:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
                )

            return [
                UserDTO(
                    user_id=user.id,
                    username=user.username,
                    name=user.name,
                    last_name=user.last_name,
                    phone=user.phone,
                    email=user.email,
                    dni=user.dni,
                    role=user.role_id,
                )
                for user in users
            ]

    async def get_user_by_id(
        self,
        user_id: int,
    ) -> Optional[UserDTO]:
        """Retrieve a user by their unique ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[UserDTO]: The matching user's data.

        Raises:
            HTTPException: If the user is not found.
        """
        async for session in self.session():
            user: User = (
                await session.exec(select(User).where(User.id == user_id))
            ).first()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

            return UserDTO(
                user_id=user.id,
                username=user.username,
                name=user.name,
                last_name=user.last_name,
                phone=user.phone,
                dni=user.dni,
                email=user.email,
                role=user.role_id,
            )

    async def get_user_by_username(
        self,
        username: str,
    ) -> Optional[UserUpdateDTO]:
        """Retrieve a user by their username.

        Args:
            username (str): The username of the user.

        Returns:
            Optional[UserUpdateDTO]: The user's full data if found, otherwise None.
        """
        async for session in self.session():
            user: User = (
                await session.exec(select(User).where(User.username == username))
            ).first()

            if not user:
                return None

            return UserUpdateDTO(
                user_id=user.id,
                name=user.name,
                last_name=user.last_name,
                username=user.username,
                dni=user.dni,
                email=user.email,
                phone=user.phone,
                role_id=user.role_id,
                password=user.password,
            )

    async def update_last_used(
        self,
        user_id: int,
    ) -> bool:
        """Update the 'last_used' timestamp for a user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            bool: True if the update succeeded.

        Raises:
            HTTPException: If the user is not found or a database error occurs.
        """
        async for session in self.session():
            user: User = (
                await session.exec(select(User).where(User.id == user_id))
            ).first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            try:
                user.last_used = datetime.now(timezone.utc)
                session.add(user)
                await session.commit()
                return True
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def update_user(
        self,
        user_update: UserUpdateDTO,
    ) -> UserDTO:
        """Update a user's information.

        Args:
            user_update (UserUpdateDTO): The new user data to update.

        Returns:
            UserDTO: The updated user's data.

        Raises:
            HTTPException: If the user is not found or an integrity error occurs.
        """
        async for session in self.session():
            user: User = (
                await session.exec(select(User).where(User.id == user_update.user_id))
            ).first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            try:
                for field, value in user_update.model_dump(exclude_unset=True).items():
                    if field != "user_id":
                        setattr(user, field, value)

                session.add(user)
                await session.commit()
                await session.refresh(user)
                return UserDTO(
                    user_id=user.id,
                    username=user.username,
                    name=user.name,
                    last_name=user.last_name,
                    phone=user.phone,
                    dni=user.dni,
                    email=user.email,
                    role=user.role_id,
                )
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def change_password(self, user_id: int, hash_pass: str) -> bool:
        """Change a user's password.

        Args:
            user_id (int): The ID of the user.
            hash_pass (str): The new hashed password.

        Returns:
            bool: True if the password was successfully updated.

        Raises:
            HTTPException: If the user is not found or a database error occurs.
        """
        async for session in self.session():
            user: User = (
                await session.exec(select(User).where(User.id == user_id))
            ).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            try:
                user.password = hash_pass
                session.add(user)
                await session.commit()
                return True
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def delete(self, user_id: int) -> bool:
        """Delete a user from the database.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the deletion succeeded.

        Raises:
            HTTPException: If the user is not found or a database error occurs.
        """
        async for session in self.session():
            user: User = (
                await session.exec(select(User).where(User.id == user_id))
            ).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            try:
                await session.delete(user)
                await session.commit()
                return True
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )
