from sqlite3 import IntegrityError
from typing import Callable, List, Optional

from fastapi import HTTPException, status
from sqlmodel import delete, select

from src.infrastructure.entities.student_info.medical_info import MedicalInfo

"""Delete a parent association.

        Args:
            user_id (int): The parent user ID.
            student_id (int): The associated student ID.

        Returns:
            bool: True if deletion succeeded.

        Raises:
            HTTPException: If the parent association is not found or a database error occurs.
        """
class MedicalInfoRepository:
    """Repository for managing MedicalInfo persistence.

    Provides CRUD operations for interacting with the MedicalInfo entity.

    :author: Carlos S. Paredes Morillo
    """
    def __init__(self, session: Callable):
        self.session = session

    async def get(self, medical_id: int) -> MedicalInfo:
        """Retrieve medical info by ID."""
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
    
    async def get_all(self) -> List[MedicalInfo]:
        """Retrieve medical all."""
        try:
            async for session in self.session():
                return (
                    await session.exec(
                        select(MedicalInfo)
                    )
                ).all()

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Something wrong on server",
            )

    async def create(self, medical: MedicalInfo) -> MedicalInfo:
        """Create a new medical info entry."""
        try:
            created = MedicalInfo(
                name=medical.name,
                description=medical.description,
                medication=medical.medication,
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
        """Update an existing medical info entry."""
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

            for field, value in medical.model_dump(exclude_unset=True).items():
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
        """Delete a medical info entry by ID."""
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
