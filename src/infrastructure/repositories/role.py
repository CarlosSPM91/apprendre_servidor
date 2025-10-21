"""
Role Repository.

Implements data access methods for the Role entity.

:author: Carlos S. Paredes Morillo
"""

from sqlalchemy.exc import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from src.domain.objects.role.role_dto import RoleDTO
from sqlmodel import select
from src.infrastructure.entities.users.roles import Role


class RoleRepository:
    """Repository for managing Role persistence.

    Provides CRUD operations over the Role entity.

    :author: Carlos S. Paredes Morillo
    """

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, role_name: str) -> RoleDTO:
        """
        Create a new role in the database.

        Args:
            role_name (str): The name of the new role.

        Returns:
            RoleDTO: The created role data transfer object.

        Raises:
            HTTPException: If an integrity or database error occurs.
        """
        async for session in self.session():
            role = Role(role_name=role_name)
            try:
                session.add(role)
                await session.commit()
                await session.refresh(role)
                return RoleDTO(role_id=role.id, role_name=role.role_name)
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def get_roles(self) -> List[RoleDTO]:
        """
        Retrieve all roles from the database.

        Returns:
            List[RoleDTO]: A list of all roles in the system. Returns an empty list if no roles exist.
        """
        async for session in self.session():
            roles: List[Role] = (await session.exec(select(Role))).all()
            if not roles:
                return []
            return [RoleDTO(role_id=role.id, role_name=role.role_name) for role in roles]

    async def find_role(self, role_id: int) -> Optional[RoleDTO]:
        """
        Retrieve a role by its ID.

        Args:
            role_id (int): The ID of the role to retrieve.

        Returns:
            Optional[RoleDTO]: The role if found, otherwise None.
        """
        async for session in self.session():
            role: Role = (
                await session.exec(select(Role).where(Role.id == role_id))
            ).first()
            if role:
                return RoleDTO(role_id=role.id, role_name=role.role_name)
            return None

    async def find_role_by_name(self, role_name: str) -> Optional[Role]:
        """
        Retrieve a role by its name.

        Args:
            role_name (str): The name of the role to retrieve.

        Returns:
            Optional[Role]: The Role entity if found, otherwise None.
        """
        async for session in self.session():
            role: Role = (
                await session.exec(select(Role).where(Role.role_name == role_name))
            ).first()
            if role:
                return role
            return None

    async def update_role(self, role_update: RoleDTO) -> Optional[RoleDTO]:
        """
        Update an existing role in the database.

        Args:
            role_update (RoleDTO): The updated role information.

        Returns:
            Optional[RoleDTO]: The updated role data transfer object if successful, otherwise None.

        Raises:
            HTTPException: If an integrity error occurs during the update.
        """
        async for session in self.session():
            role: Role = (
                await session.exec(select(Role).where(Role.id == role_update.role_id))
            ).first()

            if role:
                for field, value in role_update.model_dump(exclude_unset=True).items():
                    if field != "role_id":
                        setattr(role, field, value)

                try:
                    session.add(role)
                    await session.commit()
                    await session.refresh(role)
                    return RoleDTO(role_id=role.id, role_name=role.role_name)
                except IntegrityError:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )
            return None

    async def delete(self, role_id: int) -> bool:
        """
        Delete a role from the database.

        Args:
            role_id (int): The ID of the role to delete.

        Returns:
            bool: True if the role was deleted successfully.

        Raises:
            HTTPException: If the role does not exist or is referenced by other entities.
        """
        async for session in self.session():
            role: Role = (
                await session.exec(select(Role).where(Role.id == role_id))
            ).first()
            if not role:
                raise HTTPException(status_code=404, detail="Role not found")

            try:
                await session.delete(role)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Role already in use. Foreign key constraint violation.",
                )
