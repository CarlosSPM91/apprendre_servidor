
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.course import Course
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.infrastructure.repositories.course import CourseRepository
from src.infrastructure.repositories.school_subject import SchoolSubjectRepository


class UpdateSchoolSubjectCase:

    def __init__(self,repo: SchoolSubjectRepository):
        self.repo = repo

    async def update(self, payload: SchoolSubject) -> CommonResponse:
        school_subject = await self.repo.update(payload)
        if school_subject:
            return CommonResponse(
                item_id=school_subject.id,
                event_date=datetime.now(timezone.utc)
            )