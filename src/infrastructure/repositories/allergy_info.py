from sqlite3 import IntegrityError
from typing import Callable, Optional

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.infrastructure.entities.student_info.allergy_info import AllergyInfo


class AllergyRepository:
    def __init__(self, session: Callable):
        self.session = session

    async def get(self, allergy_id: int) -> AllergyInfo:
        try:
            async for session in self.session():
                return (
                    await session.exec(
                        select(AllergyInfo).where(AllergyInfo.id == allergy_id)
                    )
                ).first()

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def create(self, allergy: AllergyInfo) -> AllergyInfo:
        try:
            created = AllergyInfo(
                name=allergy.name,
                description=allergy.description,
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

    async def update(self, allergy: AllergyInfo) -> Optional[AllergyInfo]:
        async for session in self.session():
            allergy_upt: AllergyInfo = (
                await session.exec(
                    select(AllergyInfo).where(AllergyInfo.id == allergy.id)
                )
            ).first()
            if allergy_upt is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Allergy not found"
                )
            
            for field, value in allergy.model_dump(exclude_unset=True).items():
                if field != "id":
                    setattr(allergy_upt, field, value)

            try:
                session.add(allergy_upt)
                await session.commit()
                await session.refresh(allergy_upt)
                return allergy_upt
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def delete(self, allergy_id: int) -> bool:
        try:
            async for session in self.session():
                allergy: AllergyInfo = (
                    await session.exec(
                        select(AllergyInfo).where(AllergyInfo.id == allergy_id)
                    )
                ).first()

                if not allergy:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Allergy not found",
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
