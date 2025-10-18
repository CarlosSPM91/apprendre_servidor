

from datetime import datetime, timezone
from src.application.use_case.food_intolerance.find_intolerance_case import FindIntoleranceCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.food_intolerance import FoodIntoleranceRepository


class DeleteIntoleranceCase:

    def __init__(
        self,
        repo: FoodIntoleranceRepository,
        find_intolerance_case: FindIntoleranceCase,
    ):
        self.repo = repo
        self.find_case = find_intolerance_case

    async def delete(self, intolerance_id:int) -> CommonResponse:

        student = await self.find_case.get_intolerance(intolerance_id)

        resp = await self.repo.delete(intolerance_id)
        if resp:
            return CommonResponse(
                item_id=intolerance_id, event_date=datetime.now(timezone.utc)
            )
