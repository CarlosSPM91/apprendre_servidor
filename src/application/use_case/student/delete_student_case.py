

from datetime import datetime, timezone
from src.application.use_case.student.find_student_case import FindStudentCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.student import StudentRepository


class DeleteStudentCase:

    def __init__(
        self,
        repo: StudentRepository,
        find_student_case: FindStudentCase,
    ):
        self.repo = repo
        self.find_case = find_student_case

    async def delete(self, student_id:int) -> CommonResponse:

        student = await self.find_case.get_student_by_id(student_id)

        resp = await self.repo.delete(student_id)
        if resp:
            return CommonResponse(
                item_id=student_id, event_date=datetime.now(timezone.utc)
            )
