from typing import List, Optional
from fastapi import HTTPException, status
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
from src.infrastructure.repositories.food_intolerance import FoodIntoleranceRepository



class FindIntoleranceCase:

    def __init__(self, repo: FoodIntoleranceRepository):
        self.repo = repo

    async def get_intolerance(self, intolerance_id: int) -> Optional[FoodIntolerance]:
        intolerance = await self.repo.get(intolerance_id)
        if intolerance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Intolerance not found"
            )
        return intolerance
