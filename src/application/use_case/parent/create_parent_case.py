
from datetime import datetime, timezone
from src.domain.objects.common.common_resp import CommonResponse
from src.infrastructure.entities.users.parents import Parent
from src.infrastructure.repositories.parent import ParentRepository


class CreateParentCase:
    def __init__(
        self,
        repo: ParentRepository,
    ):
        self.repo = repo

    async def create(self, parent: Parent) -> Parent:
        created_parent = await self.repo.create(parent)
        return CommonResponse(
            item_id=created_parent.id,
            event_date=datetime.now(timezone.utc)
        )