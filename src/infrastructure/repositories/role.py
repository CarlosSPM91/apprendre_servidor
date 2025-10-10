"""
Role Repository.

Implements data access methods for the Role entity.

:author: Carlos S. Paredes Morillo
"""

from sqlalchemy.exc import IntegrityError
from typing import Callable, List

from fastapi import HTTPException, status
from src.domain.objects.role.role_dto import RoleDTO
from sqlmodel import select
from src.infrastructure.entities.users.roles import Role


class RoleRepository:
    """Repository for managing User persistence.

    Provides CRUD operations over the Role entity.

    :author: Carlos S. Paredes Morillo
    """

    def __init__(self, session: Callable):
        self.session = session

    async def create(
        self,
        role_name: str,
    ) -> RoleDTO:
        async for session in self.session():
            role = Role(
                role_name=role_name,
            )
            session.add(role)
            try:
                await session.commit()
                await session.refresh(role)
                return RoleDTO(role_id=role.id, role_name=role.role_name)
            except IntegrityError as e:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )
            
    async def get_roles(
        self,
    ) -> List[RoleDTO]:
        async for session in self.session():
            roles: Role = (await session.exec(select(Role))).all()
            if not roles:
                return []
            return [
                RoleDTO(role_id=role.id, role_name=role.role_name) for role in roles
            ]

    async def find_role(self, role_id: int) -> RoleDTO:
        async for session in self.session():
            role: Role = (
                await session.exec(select(Role).where(Role.id == role_id))
            ).first()
            if role:
                return RoleDTO(role_id=role.id, role_name=role.role_name)
            return None

    async def find_role_by_name(self, role_name: str) -> RoleDTO:
        async for session in self.session():
            role: Role = (
                await session.exec(select(Role).where(Role.role_name == role_name))
            ).first()
            if role:
                return role
            return None

    async def update_role(
        self,
        role_update: RoleDTO,
    ) -> RoleDTO:
        async for session in self.session():
            role: Role = (
                (await session.exec(select(Role).where(Role.id == role_update.role_id)))
            ).first()

            if role:
                for field, value in role_update.model_dump(exclude_unset=True).items():
                    if field != "role_id":
                        setattr(role, field, value)

                session.add(role)
                try:
                    await session.commit()
                    await session.refresh(role)
                    return RoleDTO(role_id=role.id, role_name=role.role_name)

                except IntegrityError as e:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )

    async def delete(self, role_id: int) -> bool:
        async for session in self.session():
            role: Role = (
                (await session.exec(select(Role).where(Role.id == role_id)))
            ).first()
            if not role:
                raise HTTPException(status_code=404, detail="Role not found")

            try:
                await session.delete(role)
                await session.commit()
                return True
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Role already in Use. Foreign key constraint",
                )
