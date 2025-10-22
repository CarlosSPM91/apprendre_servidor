from unittest.mock import AsyncMock
import pytest
from src.application.use_case.allergy_info.delete_allergy_case import DeleteAllergyCase
from src.application.use_case.allergy_info.find_allergy_case import FindAllergyCase
from src.infrastructure.repositories.allergy_info import AllergyRepository


@pytest.fixture
def repo():
    return AsyncMock(spec=AllergyRepository)


@pytest.fixture
def find_case(repo):
    return FindAllergyCase(repo)

@pytest.fixture
def use_case(repo, find_case):
    return DeleteAllergyCase(repo, find_case=find_case)

@pytest.mark.asyncio
async def test_delete_allergy(use_case, repo):
    allergy_id = 1

    repo.delete.return_value = True

    result = await use_case.delete(allergy_id)

    repo.delete.assert_awaited_once_with(allergy_id)
    assert result.item_id == allergy_id
    assert result.event_date is not None

@pytest.mark.asyncio
async def test_delete_allergy_not_found(use_case, repo):
    allergy_id = 999

    repo.delete.return_value = False

    result = await use_case.delete(allergy_id)

    repo.delete.assert_awaited_once_with(allergy_id)
    assert result is None

