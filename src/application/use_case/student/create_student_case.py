

from datetime import datetime, timezone
from fastapi import HTTPException, status
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.student_info.student import Student
from src.infrastructure.repositories.student import StudentRepository



class CreateStudenCase:


    def __init__(self, repo: StudentRepository):
        self.repo = repo

    async def create(self, payload: Student) -> CommonResponse:
        user_check = await self.userRepo.get_user_by_username(payload.username)
        if user_check:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Student already exist"
            )

        student_created = await self.repo.create(payload)

        return CommonResponse(
            item_id=student_created.id,
            event_date=datetime.now(timezone.utc)
        )
