from datetime import datetime, timezone
from src.application.use_case.teacher.find_teacher_case import FindTeacherCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.teacher import TeacherRepository


class DeleteTeacherCase:

    def __init__(
        self,
        repo: TeacherRepository,
        find_case: FindTeacherCase,
    ):
        self.repo = repo
        self.find_case = find_case

    async def delete(self, teacher_id:int) -> CommonResponse:

        await self.find_case.get(teacher_id)

        resp = await self.repo.delete(teacher_id)
        if resp:
            return CommonResponse(
                item_id=teacher_id, event_date=datetime.now(timezone.utc)
            )
