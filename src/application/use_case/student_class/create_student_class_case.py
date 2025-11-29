from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.student_class import StudentClass
from src.infrastructure.repositories.student_class import StudentClassRepository



class CreateStudentClassCase:

    def __init__(self, repo: StudentClassRepository):
        self.repo = repo

    async def create(self, payload: StudentClass) -> CommonResponse:
        created = await self.repo.create(payload)

        return CommonResponse(
            item_id=created.id,
            event_date=datetime.now(timezone.utc)
        )
