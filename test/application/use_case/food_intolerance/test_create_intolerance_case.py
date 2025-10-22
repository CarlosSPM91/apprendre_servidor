from unittest.mock import AsyncMock
import pytest

from src.application.use_case.allergy_info.create_allergy_case import CreateAllergyCase
from src.application.use_case.food_intolerance.create_intolerance_case import CreateIntoleranceCase


@pytest.fixture
def repo():
    return AsyncMock()

@pytest.fixture
def use_case( repo):
    return CreateIntoleranceCase(repo)

@pytest.mark.asyncio
async def test_create_intolerance(use_case, repo):
    intolerance_info = AsyncMock()
    created_intolerance= AsyncMock()
    created_intolerance.id = 1

    repo.create.return_value= created_intolerance

    result = await use_case.create(intolerance_info)

    repo.create.assert_awaited_once_with(intolerance_info)
    assert result.item_id == created_intolerance.id
    assert result.event_date is not None

@pytest.mark.asyncio
async def test_create_intolerance_failure(use_case, repo):
    intolerance_info = AsyncMock()

    repo.create.side_effect = Exception("Database error")

    with pytest.raises(Exception) as exc_info:
        await use_case.create(intolerance_info)

    repo.create.assert_awaited_once_with(intolerance_info)
    assert str(exc_info.value) == "Database error"


