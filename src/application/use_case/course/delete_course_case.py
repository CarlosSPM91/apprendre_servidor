from datetime import datetime, timezone
from src.application.use_case.course.find_course_case import FindCourseCase
from src.application.use_case.medical_info.find_medical_case import FindMedicalCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.course import CourseRepository
from src.infrastructure.repositories.medical_info import MedicalInfoRepository



class DeleteCourseCase:

    def __init__(
        self,
        repo: CourseRepository,
        find_case: FindCourseCase,
    ):
        self.repo = repo
        self.find_case = find_case

    async def delete(self, course_id:int) -> CommonResponse:

        await self.find_case.get(course_id)

        resp = await self.repo.delete(course_id)
        if resp:
            return CommonResponse(
                item_id=course_id, event_date=datetime.now(timezone.utc)
            )
