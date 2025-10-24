from typing import List, Optional
from fastapi import HTTPException, status
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.repositories.allergy_info import AllergyRepository




class FindAllergyCase:

    def __init__(self, repo: AllergyRepository):
        self.repo = repo

    async def get_allergy(self, intolerance_id: int) -> Optional[AllergyInfo]:
        allergy = await self.repo.get(intolerance_id)
        if allergy is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Allergy info not found"
            )
        return allergy
    
    async def get_all(self):
        return await self.repo.get_all()

