
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.repositories.allergy_info import AllergyRepository


class UpdateAllergyCase:

    def __init__(self,repo: AllergyRepository):
        self.repo = repo

    async def update(self, payload: AllergyInfo) -> CommonResponse:
        allergy = await self.repo.update(payload)
        if allergy:
            return CommonResponse(
                item_id=allergy.id,
                event_date=datetime.now(timezone.utc)
            )