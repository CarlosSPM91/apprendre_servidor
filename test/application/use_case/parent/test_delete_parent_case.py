import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.application.use_case.parent.delete_parent_case import DeleteParentCase
from src.infrastructure.repositories.parent import ParentRepository
from src.domain.objects.common.common_resp import CommonResponse

@pytest.fixture
def mock_repo():
    return AsyncMock(spec=ParentRepository)

@pytest.fixture
def delete_parent_case(mock_repo):
    return DeleteParentCase(repo=mock_repo)

@pytest.mark.asyncio
async def test_delete_parent_success(delete_parent_case, mock_repo):
    user_id = 1
    student_id = 101

    mock_repo.get.return_value = [MagicMock(student_id=student_id)]

    result = await delete_parent_case.delete(user_id=user_id, student_id=student_id)

    assert isinstance(result, CommonResponse)
    assert result.item_id == user_id
    assert isinstance(result.event_date, datetime)

    mock_repo.get.assert_awaited_once_with(user_id)
    mock_repo.delete.assert_awaited_once_with(user_id=user_id, student_id=student_id)

@pytest.mark.asyncio
async def test_delete_parent_not_found_raises(delete_parent_case, mock_repo):
    user_id = 1
    student_id = 101

    mock_repo.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await delete_parent_case.delete(user_id=user_id, student_id=student_id)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Parent not found"

