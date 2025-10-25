
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.course import Course
from src.infrastructure.repositories.course import CourseRepository


class UpdateCourseCase:

    def __init__(self,repo: CourseRepository):
        self.repo = repo

    async def update(self, payload: Course) -> CommonResponse:
        course = await self.repo.update(payload)
        if course:
            return CommonResponse(
                item_id=course.id,
                event_date=datetime.now(timezone.utc)
            )