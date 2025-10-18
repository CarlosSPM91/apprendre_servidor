from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.student_info.medical_info import MedicalInfo
from src.infrastructure.repositories.medical_info import MedicalInfoRepository



class CreateMedicalCase:


    def __init__(self, repo: MedicalInfoRepository):
        self.repo = repo

    async def create(self, payload: MedicalInfo) -> CommonResponse:
        created = await self.repo.create(payload)

        return CommonResponse(
            item_id=created.id,
            event_date=datetime.now(timezone.utc)
        )
