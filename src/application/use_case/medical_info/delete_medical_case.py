from datetime import datetime, timezone
from src.application.use_case.medical_info.find_medical_case import FindMedicalCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.medical_info import MedicalInfoRepository



class DeleteMedicalCase:

    def __init__(
        self,
        repo: MedicalInfoRepository,
        find_case: FindMedicalCase,
    ):
        self.repo = repo
        self.find_case = find_case

    async def delete(self, medical_id:int) -> CommonResponse:

        medical = await self.find_case.get_medical(medical_id)

        resp = await self.repo.delete(medical_id)
        if resp:
            return CommonResponse(
                item_id=medical_id, event_date=datetime.now(timezone.utc)
            )
