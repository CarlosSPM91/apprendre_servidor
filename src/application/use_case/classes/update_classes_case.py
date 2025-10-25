
from datetime import datetime, timezone
from typing import List
from src.domain.objects.classes.class_subjects_dto import ClassSubjectsDTO
from src.domain.objects.classes.update_class_subjects_dto import UpdateClassSubjectsDTO
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.course.classes import Classes
from src.infrastructure.repositories.classes import ClassesRepository


class UpdateClassesCase:

    def __init__(self,repo: ClassesRepository):
        self.repo = repo

    async def update(self, payload: Classes) -> CommonResponse:
        classes = await self.repo.update(payload)
        if classes:
            return CommonResponse(
                item_id=classes.id,
                event_date=datetime.now(timezone.utc)
            )
        
    async def update_subjects(self, subjects:UpdateClassSubjectsDTO) -> ClassSubjectsDTO:
        classes: ClassSubjectsDTO = await self.repo.update_subjects(subjects)
        return CommonResponse(
                item_id=classes.id,
                event_date=datetime.now(timezone.utc)
            )