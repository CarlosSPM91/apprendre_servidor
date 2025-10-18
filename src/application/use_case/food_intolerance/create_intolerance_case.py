

from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
from src.infrastructure.repositories.food_intolerance import FoodIntoleranceRepository



class CreateIntoleranceCase:


    def __init__(self, repo: FoodIntoleranceRepository):
        self.repo = repo

    async def create(self, payload: FoodIntolerance) -> CommonResponse:
        created = await self.repo.create(payload)

        return CommonResponse(
            item_id=created.id,
            event_date=datetime.now(timezone.utc)
        )
