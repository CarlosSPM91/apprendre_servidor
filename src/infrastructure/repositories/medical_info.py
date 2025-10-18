from sqlite3 import IntegrityError
from typing import Callable, Optional

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.infrastructure.entities.student_info.medical_info import MedicalInfo


class MedicalInfoRepository:
    def __init__(self, session: Callable):
        self.session = session

    async def get(self, medical_id: int) -> MedicalInfo:
        try:
            async for session in self.session():
                return (
                    await session.exec(
                        select(MedicalInfo).where(MedicalInfo.id == medical_id)
                    )
                ).first()

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def create(self, medical: MedicalInfo) -> MedicalInfo:
        try:
            created = MedicalInfo(
                user_id=medical.name,
                observations=medical.description,
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

    async def update(self, medical: MedicalInfo) -> Optional[MedicalInfo]:
        async for session in self.session():
            medical_upt: MedicalInfo = (
                await session.exec(
                    select(MedicalInfo).where(MedicalInfo.id == medical.id)
                )
            ).first()

            if medical_upt is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Medical Info not found",
                )

            for field, value in medical_upt.model_dump(exclude_unset=True).items():
                if field != "id":
                    setattr(medical_upt, field, value)

            try:
                session.add(medical_upt)
                await session.commit()
                await session.refresh(medical_upt)
                return medical_upt
            except IntegrityError:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Something wrong on server",
                )

    async def delete(self, medical_id: int) -> bool:
        try:
            async for session in self.session():
                allergy: MedicalInfo = (
                    await session.exec(
                        select(MedicalInfo).where(MedicalInfo.id == medical_id)
                    )
                ).first()

                if not allergy:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Medical Info not found",
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
