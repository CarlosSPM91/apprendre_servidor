
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.student_info.medical_info import MedicalInfo
from src.infrastructure.repositories.medical_info import MedicalInfoRepository


class UpdateIntoleranceCase:

    def __init__(self,repo: MedicalInfoRepository):
        self.repo = repo

    async def update(self, payload: MedicalInfo) -> CommonResponse:
        student = await self.repo.update(payload)
        if student:
            return CommonResponse(
                item_id=student.id,
                event_date=datetime.now(timezone.utc)
            )