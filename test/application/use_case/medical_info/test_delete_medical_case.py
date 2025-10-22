
from unittest.mock import AsyncMock
import pytest
from src.application.use_case.allergy_info.delete_allergy_case import DeleteAllergyCase
from src.application.use_case.allergy_info.find_allergy_case import FindAllergyCase
from src.application.use_case.medical_info.delete_medical_case import DeleteMedicalCase
from src.application.use_case.medical_info.find_medical_case import FindMedicalCase
from src.infrastructure.repositories.allergy_info import AllergyRepository


@pytest.fixture
def repo():
    return AsyncMock()


@pytest.fixture
def find_case(repo):
    return FindMedicalCase(repo)

@pytest.fixture
def use_case(repo, find_case):
    return DeleteMedicalCase(repo, find_case=find_case)

@pytest.mark.asyncio
async def test_delete_medical(use_case, repo):
    medical_id = 1

    repo.delete.return_value = True

    result = await use_case.delete(medical_id)

    repo.delete.assert_awaited_once_with(medical_id)
    assert result.item_id == medical_id
    assert result.event_date is not None

@pytest.mark.asyncio
async def test_delete_medical_not_found(use_case, repo):
    medical_id = 999

    repo.delete.return_value = False

    result = await use_case.delete(medical_id)

    repo.delete.assert_awaited_once_with(medical_id)
    assert result is None

