
from unittest.mock import AsyncMock
import pytest
from src.application.use_case.allergy_info.create_allergy_case import CreateAllergyCase
from src.infrastructure.repositories.allergy_info import AllergyRepository


@pytest.fixture
def repo():
    return AsyncMock()

@pytest.fixture
def use_case( repo):
    return CreateAllergyCase(repo)

@pytest.mark.asyncio
async def test_create_allergy(use_case, repo):
    allergy_info = AsyncMock()
    created_allergy = AsyncMock()
    created_allergy.id = 1

    repo.create.return_value = created_allergy

    result = await use_case.create(allergy_info)

    repo.create.assert_awaited_once_with(allergy_info)
    assert result.item_id == created_allergy.id
    assert result.event_date is not None

@pytest.mark.asyncio
async def test_create_allergy_failure(use_case, repo):
    allergy_info = AsyncMock()

    repo.create.side_effect = Exception("Database error")

    with pytest.raises(Exception) as exc_info:
        await use_case.create(allergy_info)

    repo.create.assert_awaited_once_with(allergy_info)
    assert str(exc_info.value) == "Database error"

