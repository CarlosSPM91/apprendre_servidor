from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.infrastructure.entities.course.calendary_activity import CalendarActivity

"""
CalendarActivity Repository.

Implements data access methods for the AllergyInfo entity.

:author: Carlos S. Paredes Morillo
"""

class CalendarActivityRepository:
    """Repository for managing CalendarActivity persistence.

    Provides CRUD operations for interacting with the AllergyInfo entity.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, session: Callable):
        self.session = session

    async def get(self, calendar_id: int) -> CalendarActivity:
        try:
            async for session in self.session():
                return (
                    await session.exec(
                        select(CalendarActivity).where(CalendarActivity.id == calendar_id)
                    )
                ).first()

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def get_all(self) -> List[CalendarActivity]:
        try:
            async for session in self.session():
                return (await session.exec(select(CalendarActivity))).all()

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def create(self, calendar: CalendarActivity) -> CalendarActivity:
        try:
            created = CalendarActivity(
                course_id=calendar.course_id,
                activity_name=calendar.activity_name,
                activity_type_id=calendar.activity_type_id,
                date=calendar.date
            )
            async for session in self.session():
                session.add(created)
                await session.commit()
                await session.refresh(created)
                return created

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def update(self, calendar: CalendarActivity) -> Optional[CalendarActivity]:
        async for session in self.session():
            calendar_upt: CalendarActivity = (
                await session.exec(
                    select(CalendarActivity).where(CalendarActivity.id == calendar.id)
                )
            ).first()
            if calendar_upt is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Calendar Activity not found"
                )

            for field, value in calendar.model_dump(exclude_unset=True).items():
                if field != "id":
                    setattr(calendar_upt, field, value)

            try:
                session.add(calendar_upt)
                await session.commit()
                await session.refresh(calendar_upt)
                return calendar_upt
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def delete(self, calendar_id: int) -> bool:
        try:
            async for session in self.session():
                calendar: CalendarActivity = (
                    await session.exec(
                        select(CalendarActivity).where(CalendarActivity.id == calendar_id)
                    )
                ).first()

                if not calendar:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Calendar Activity not found",
                    )
                await session.delete(calendar)
                await session.commit()
                return True

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )
