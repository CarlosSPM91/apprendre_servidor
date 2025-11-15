import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime, timezone

from src.application.use_case.parent.create_parent_case import CreateParentCase
from src.infrastructure.repositories.parent import ParentRepository
from src.infrastructure.entities.users.parents import Parent
from src.domain.objects.common.common_resp import CommonResponse

@pytest.fixture
def mock_repo():
    return AsyncMock(spec=ParentRepository)

@pytest.fixture
def create_parent_case(mock_repo):
    return CreateParentCase(repo=mock_repo)

@pytest.mark.asyncio
async def test_create_parent_success(create_parent_case, mock_repo):

    parent_input = Parent(id=None, user_id=1, student_id=101)
    
    created_parent = MagicMock()
    created_parent.id = 123
    mock_repo.create.return_value = created_parent

    result = await create_parent_case.create(parent_input)

    assert isinstance(result, CommonResponse)
    assert result.item_id == created_parent.id
    assert isinstance(result.event_date, datetime)

    mock_repo.create.assert_awaited_once_with(parent_input)
