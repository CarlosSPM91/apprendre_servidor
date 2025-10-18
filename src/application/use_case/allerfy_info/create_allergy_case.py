from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.repositories.allergy_info import AllergyRepository



class CreateAllergyCase:


    def __init__(self, repo: AllergyRepository):
        self.repo = repo

    async def create(self, payload: AllergyInfo) -> CommonResponse:
        created = await self.repo.create(payload)

        return CommonResponse(
            item_id=created.id,
            event_date=datetime.now(timezone.utc)
        )
