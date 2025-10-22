from datetime import datetime
from unittest.mock import AsyncMock
import pytest

from src.application.use_case.food_intolerance.update_intolerance_case import UpdateIntoleranceCase
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance


@pytest.fixture
def repo():
    return AsyncMock()

@pytest.fixture
def use_case(repo):
    return UpdateIntoleranceCase(repo)

@pytest.mark.asyncio
async def test_update_intolerance(use_case, repo):
    payload = FoodIntolerance(id=1, name="Updated Intolerance")
    

    updated_intolerance = FoodIntolerance(id=1, name="Updated Intolerance")
    repo.update.return_value = updated_intolerance

    result = await use_case.update(payload)

    repo.update.assert_awaited_once_with(payload)
    assert result.item_id == 1
    assert isinstance(result.event_date, datetime)

@pytest.mark.asyncio
async def test_update_intolerance_not_found(use_case, repo):

    payload = FoodIntolerance(id=999, name="Non-existent Intolerance")
    

    repo.update.return_value = None

    result = await use_case.update(payload)

    repo.update.assert_awaited_once_with(payload)
    assert result is None