
from fastapi import HTTPException, status
import pytest
from unittest.mock import AsyncMock

from src.application.use_case.food_intolerance.find_intolerance_case import FindIntoleranceCase
from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance


@pytest.fixture
def repo():
    return AsyncMock() 

@pytest.fixture
def use_case(repo):
    return FindIntoleranceCase(repo)

@pytest.mark.asyncio
async def test_get_intolerance(use_case, repo):
    intolerance_id = 1
    expected_intolerance= FoodIntolerance(id=intolerance_id, name="Peanuts")
    repo.get.return_value = expected_intolerance
    
    result = await use_case.get_intolerance(intolerance_id)
    
    repo.get.assert_awaited_once_with(intolerance_id)
    assert result == expected_intolerance
    assert result.id == intolerance_id
    assert result.name == "Peanuts"

@pytest.mark.asyncio
async def test_get_intolerance_not_found(use_case, repo):
    intolerance_id = 999
    repo.get.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        await use_case.get_intolerance(intolerance_id)
    
    repo.get.assert_awaited_once_with(intolerance_id)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Intolerance not found"