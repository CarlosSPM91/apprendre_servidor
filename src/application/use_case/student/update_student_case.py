
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.profiles.student_update_dto import StudentUpdateDTO
from src.infrastructure.repositories.student import StudentRepository


class UpdateStudentCase:

    def __init__(self,repo: StudentRepository):
        self.repo = repo

    async def update_student(self, payload: StudentUpdateDTO) -> CommonResponse:
        student = await self.repo.update(payload)
        if student:
            return CommonResponse(
                item_id=student.id,
                event_date=datetime.now(timezone.utc)
            )