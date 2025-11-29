from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.subject_class import SubjectClass
from src.infrastructure.repositories.subject_class import SubjectClassRepository



class CreateSubjectClassCase:

    def __init__(self, repo: SubjectClassRepository):
        self.repo = repo

    async def create(self, payload: SubjectClass) -> CommonResponse:
        created = await self.repo.create(payload)

        return CommonResponse(
            item_id=created.id,
            event_date=datetime.now(timezone.utc)
        )
