from unittest.mock import AsyncMock
import pytest
from fastapi import HTTPException, status
from src.application.use_case.allergy_info.find_allergy_case import FindAllergyCase
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo

@pytest.fixture
def repo():
    return AsyncMock() 

@pytest.fixture
def use_case(repo):
    return FindAllergyCase(repo)

@pytest.mark.asyncio
async def test_get_allergy(use_case, repo):
    allergy_id = 1
    expected_allergy = AllergyInfo(id=allergy_id, name="Peanuts")
    repo.get.return_value = expected_allergy
    
    result = await use_case.get_allergy(allergy_id)
    
    repo.get.assert_awaited_once_with(allergy_id)
    assert result == expected_allergy
    assert result.id == allergy_id
    assert result.name == "Peanuts"

@pytest.mark.asyncio
async def test_get_allergy_not_found(use_case, repo):
    allergy_id = 999
    repo.get.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        await use_case.get_allergy(allergy_id)
    
    repo.get.assert_awaited_once_with(allergy_id)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Allergy info not found"