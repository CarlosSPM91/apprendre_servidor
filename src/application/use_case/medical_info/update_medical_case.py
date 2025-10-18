
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.student_info.medical_info import MedicalInfo
from src.infrastructure.repositories.medical_info import MedicalInfoRepository


class UpdateMedicalCase:

    def __init__(self,repo: MedicalInfoRepository):
        self.repo = repo

    async def update(self, payload: MedicalInfo) -> CommonResponse:
        medical = await self.repo.update(payload)
        if medical:
            return CommonResponse(
                item_id=medical.id,
                event_date=datetime.now(timezone.utc)
            )