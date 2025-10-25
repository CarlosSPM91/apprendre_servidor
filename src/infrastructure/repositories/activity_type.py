

from sqlalchemy.exc import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import select
from src.infrastructure.entities.course.activity_type import ActivityType


class ActivityTypeRepository:

    def __init__(self, session: Callable):
        self.session = session

    async def create(self, activity_name: str) -> ActivityType:
        async for session in self.session():
            types = ActivityType(role_name=activity_name)
            try:
                session.add(types)
                await session.commit()
                await session.refresh(types)
                return types
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def get_all(self) -> List[ActivityType]:
        async for session in self.session():
            types: List[ActivityType] = (await session.exec(select(ActivityType))).all()
            if not types:
                return []
            return types

    async def find_by_id(self, activity_id: int) -> Optional[ActivityType]:
        async for session in self.session():
            type: ActivityType = (
                await session.exec(
                    select(ActivityType).where(ActivityType.id == activity_id)
                )
            ).first()
            return type

    async def find_by_name(self, activity_name: str) -> Optional[ActivityType]:
        async for session in self.session():
            type: ActivityType = (
                await session.exec(
                    select(ActivityType).where(
                        ActivityType.activity_name == activity_name
                    )
                )
            ).first()
            return type

    async def update(self, type_upt: ActivityType) -> Optional[ActivityType]:
        async for session in self.session():
            types: ActivityType = (
                await session.exec(
                    select(ActivityType).where(ActivityType.id == type.acti)
                )
            ).first()

            if types:
                if type_upt.activity_name is not None:
                    types.activity_name = type_upt.activity_name

                try:
                    session.add(types)
                    await session.commit()
                    await session.refresh(types)
                    return types
                except IntegrityError:
                    await session.rollback()
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Something wrong on server",
                    )
            return None

    async def delete(self, types_id: int) -> bool:
        async for session in self.session():
            types: ActivityType = (
                await session.exec(
                    select(ActivityType).where(ActivityType.id == types_id)
                )
            ).first()
            if not types:
                raise HTTPException(status_code=404, detail="Activity Type not found")

            try:
                await session.delete(types)
                await session.commit()
                return True
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Activity Type already in use. Foreign key constraint violation.",
                )
