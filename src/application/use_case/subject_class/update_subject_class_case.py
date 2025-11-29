
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.subject_class import SubjectClass
from src.infrastructure.repositories.subject_class import SubjectClassRepository


class UpdateSubjectClassCase:

    def __init__(self,repo: SubjectClassRepository):
        self.repo = repo

    async def update(self, payload: SubjectClass) -> CommonResponse:
        subject_class = await self.repo.update(payload)
        if subject_class:
            return CommonResponse(
                item_id=subject_class.id,
                event_date=datetime.now(timezone.utc)
            )