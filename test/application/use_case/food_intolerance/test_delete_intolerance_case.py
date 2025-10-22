from unittest.mock import AsyncMock
import pytest

from src.application.use_case.food_intolerance.delete_intolerance_case import DeleteIntoleranceCase
from src.application.use_case.food_intolerance.find_intolerance_case import FindIntoleranceCase


@pytest.fixture
def repo():
    return AsyncMock()


@pytest.fixture
def find_case(repo):
    return FindIntoleranceCase(repo)

@pytest.fixture
def use_case(repo, find_case):
    return DeleteIntoleranceCase(repo, find_case=find_case)

@pytest.mark.asyncio
async def test_delete_intolerance(use_case, repo):
    intolerance_id = 1

    repo.delete.return_value = True

    result = await use_case.delete(intolerance_id)

    repo.delete.assert_awaited_once_with(intolerance_id)
    assert result.item_id == intolerance_id
    assert result.event_date is not None

@pytest.mark.asyncio
async def test_delete_intolerance_not_found(use_case, repo):
    intolerance_id = 999

    repo.delete.return_value = False

    result = await use_case.delete(intolerance_id)

    repo.delete.assert_awaited_once_with(intolerance_id)
    assert result is None

