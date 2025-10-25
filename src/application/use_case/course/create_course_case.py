from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.course import Course
from src.infrastructure.repositories.course import CourseRepository



class CreateCourseCase:


    def __init__(self, repo: CourseRepository):
        self.repo = repo

    async def create(self, payload: Course) -> CommonResponse:
        created = await self.repo.create(payload)

        return CommonResponse(
            item_id=created.id,
            event_date=datetime.now(timezone.utc)
        )
