from datetime import datetime, timezone
from src.application.use_case.student_class.find_student_class_case import FindStudentClassCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.student_class import StudentClassRepository



class DeleteStudentClassCase:

    def __init__(
        self,
        repo: StudentClassRepository,
        find_case: FindStudentClassCase,
    ):
        self.repo = repo
        self.find_case = find_case

    async def delete(self, student_class_id:int) -> CommonResponse:

        await self.find_case.get(student_class_id)

        resp = await self.repo.delete(student_class_id)
        if resp:
            return CommonResponse(
                item_id=student_class_id, event_date=datetime.now(timezone.utc)
            )
