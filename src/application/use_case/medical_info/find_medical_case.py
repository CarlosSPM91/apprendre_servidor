from typing import Optional
from fastapi import HTTPException, status
from src.infrastructure.entities.student_info.medical_info import MedicalInfo
from src.infrastructure.repositories.medical_info import MedicalInfoRepository



class FindMedicalCase:

    def __init__(self, repo: MedicalInfoRepository):
        self.repo = repo

    async def get_medical(self, intolerance_id: int) -> Optional[MedicalInfo]:
        intolerance = await self.repo.get(intolerance_id)
        if intolerance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Medical info not found"
            )
        return intolerance

    async def get_all(self):
        return await self.repo.get_all()