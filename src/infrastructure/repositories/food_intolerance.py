from sqlite3 import IntegrityError
from typing import Callable, Optional

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance



class FoodIntoleranceRepository:
    def __init__(self, session: Callable):
        self.session = session

    async def get(self, intolerance_id: int) -> FoodIntolerance:
        try:
            async for session in self.session():
                return (
                    await session.exec(
                        select(FoodIntolerance).where(FoodIntolerance.id == intolerance_id)
                    )
                ).first()

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def create(self, intolerance: FoodIntolerance) -> FoodIntolerance:
        try:
            created = FoodIntolerance(
                user_id=intolerance.name,
                observations=intolerance.description,
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

    async def update(self, intolerance: FoodIntolerance) -> Optional[FoodIntolerance]:
        async for session in self.session():
            intolerance_upt: FoodIntolerance = (
                await session.exec(
                    select(FoodIntolerance).where(FoodIntolerance.id == intolerance.id)
                )
            ).first()

            if intolerance_upt is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Food Intolerance not found"
                )

            for field, value in intolerance_upt.model_dump(exclude_unset=True).items():
                if field != "id":
                    setattr(intolerance_upt, field, value)

            try:
                session.add(intolerance_upt)
                await session.commit()
                await session.refresh(intolerance_upt)
                return intolerance_upt
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def delete(self, intolerance_id: int) -> bool:
        try:
            async for session in self.session():
                allergy: FoodIntolerance = (
                    await session.exec(
                        select(FoodIntolerance).where(FoodIntolerance.id == intolerance_id)
                    )
                ).first()

                if not allergy:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Food Intolerance not found",
                    )
                await session.delete(allergy)
                await session.commit()
                return True

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )
