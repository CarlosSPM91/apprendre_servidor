from datetime import datetime, timezone
from src.application.use_case.subject_class.find_subject_class_case import FindSubjectClassCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.subject_class import SubjectClassRepository



class DeleteSubjectClassCase:

    def __init__(
        self,
        repo: SubjectClassRepository,
        find_case: FindSubjectClassCase,
    ):
        self.repo = repo
        self.find_case = find_case

    async def delete(self, subject_class_id:int) -> CommonResponse:

        await self.find_case.get(subject_class_id)

        resp = await self.repo.delete(subject_class_id)
        if resp:
            return CommonResponse(
                item_id=subject_class_id, event_date=datetime.now(timezone.utc)
            )
