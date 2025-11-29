from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.infrastructure.repositories.school_subject import SchoolSubjectRepository



class CreateSchoolSubjectCase:

    def __init__(self, repo: SchoolSubjectRepository):
        self.repo = repo

    async def create(self, payload: SchoolSubject) -> CommonResponse:
        created = await self.repo.create(payload)

        return CommonResponse(
            item_id=created.id,
            event_date=datetime.now(timezone.utc)
        )
