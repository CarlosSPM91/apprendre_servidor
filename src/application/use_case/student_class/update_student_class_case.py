
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.student_class import StudentClass
from src.infrastructure.repositories.student_class import StudentClassRepository


class UpdateStudentClassCase:

    def __init__(self,repo: StudentClassRepository):
        self.repo = repo

    async def update_points(self, payload: StudentClass) -> CommonResponse:
        student_class = await self.repo.update_points(payload)
        if student_class:
            return CommonResponse(
                item_id=student_class.id,
                event_date=datetime.now(timezone.utc)
            )