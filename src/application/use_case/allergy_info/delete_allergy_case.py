

from datetime import datetime, timezone
from src.application.use_case.allergy_info.find_allergy_case import FindAllergyCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.allergy_info import AllergyRepository



class DeleteAllergyCase:

    def __init__(
        self,
        repo: AllergyRepository,
        find_case: FindAllergyCase,
    ):
        self.repo = repo
        self.find_case = find_case

    async def delete(self, allergy_id:int) -> CommonResponse:

        allergy = await self.find_case.get_allergy(allergy_id)

        resp = await self.repo.delete(allergy_id)
        if resp:
            return CommonResponse(
                item_id=allergy_id, event_date=datetime.now(timezone.utc)
            )
