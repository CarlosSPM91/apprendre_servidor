

from unittest.mock import AsyncMock
import pytest
from src.application.use_case.medical_info.create_medical_case import CreateMedicalCase



@pytest.fixture
def repo():
    return AsyncMock()

@pytest.fixture
def use_case( repo):
    return CreateMedicalCase(repo)

@pytest.mark.asyncio
async def test_create_medical(use_case, repo):
    medical_info = AsyncMock()
    created_medical = AsyncMock()
    created_medical.id = 1

    repo.create.return_value = created_medical

    result = await use_case.create(medical_info)

    repo.create.assert_awaited_once_with(medical_info)
    assert result.item_id == created_medical.id
    assert result.event_date is not None

@pytest.mark.asyncio
async def test_create_medical_failure(use_case, repo):
    medical_info = AsyncMock()

    repo.create.side_effect = Exception("Database error")

    with pytest.raises(Exception) as exc_info:
        await use_case.create(medical_info)

    repo.create.assert_awaited_once_with(medical_info)
    assert str(exc_info.value) == "Database error"

