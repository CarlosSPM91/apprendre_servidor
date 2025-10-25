from datetime import datetime, timezone
from src.application.use_case.classes.find_classes_case import FindClassesCase
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.repositories.classes import ClassesRepository




class DeleteClassesCase:

    def __init__(
        self,
        repo: ClassesRepository,
        find_case: FindClassesCase,
    ):
        self.repo = repo
        self.find_case = find_case

    async def delete(self, class_id:int) -> CommonResponse:

        await self.find_case.get(class_id)

        resp = await self.repo.delete(class_id)
        if resp:
            return CommonResponse(
                item_id=class_id, event_date=datetime.now(timezone.utc)
            )
