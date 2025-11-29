from datetime import datetime, timezone
from src.application.use_case.school_subject.find_school_subject_case import FindSchoolSubjectCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.school_subject import SchoolSubjectRepository



class DeleteSchoolSubjectCase:

    def __init__(
        self,
        repo: SchoolSubjectRepository,
        find_case: FindSchoolSubjectCase,
    ):
        self.repo = repo
        self.find_case = find_case

    async def delete(self, school_subject_id:int) -> CommonResponse:

        await self.find_case.get(school_subject_id)

        resp = await self.repo.delete(school_subject_id)
        if resp:
            return CommonResponse(
                item_id=school_subject_id, event_date=datetime.now(timezone.utc)
            )
