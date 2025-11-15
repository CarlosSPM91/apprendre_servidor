
from unittest.mock import AsyncMock
import pytest
from fastapi import HTTPException, status
from src.application.use_case.medical_info.find_medical_case import FindMedicalCase
from src.infrastructure.entities.student_info.medical_info import MedicalInfo

@pytest.fixture
def repo():
    return AsyncMock() 

@pytest.fixture
def use_case(repo):
    return FindMedicalCase(repo)

@pytest.mark.asyncio
async def test_get_allergy(use_case, repo):
    medical_id = 1
    expected_medical = MedicalInfo(id=medical_id, name="Peanuts")
    repo.get.return_value = expected_medical
    
    result = await use_case.get_medical(medical_id)
    
    repo.get.assert_awaited_once_with(medical_id)
    assert result == expected_medical
    assert result.id == medical_id
    assert result.name == "Peanuts"

@pytest.mark.asyncio
async def test_get_medical_not_found(use_case, repo):
    medical_id = 999
    repo.get.return_value = None
    
    with pytest.raises(HTTPException) as exc_info:
        await use_case.get_medical(medical_id)
    
    repo.get.assert_awaited_once_with(medical_id)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "Medical info not found"