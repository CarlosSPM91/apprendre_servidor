from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.application.use_case.allergy_info.update_allergy_case import UpdateAllergyCase
from src.application.use_case.medical_info.update_medical_case import UpdateMedicalCase
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.entities.student_info.medical_info import MedicalInfo
from src.infrastructure.repositories.allergy_info import AllergyRepository


@pytest.fixture
def repo():
    return AsyncMock()

@pytest.fixture
def use_case(repo):
    return UpdateMedicalCase(repo)

@pytest.mark.asyncio
async def test_update_medical(use_case, repo):
    payload = MedicalInfo(id=1, name="Updated Medical")
    

    updated_medical= MedicalInfo(id=1, name="Updated Medical")
    repo.update.return_value = updated_medical

    result = await use_case.update(payload)

    repo.update.assert_awaited_once_with(payload)
    assert result.item_id == 1
    assert isinstance(result.event_date, datetime)

@pytest.mark.asyncio
async def test_update_medical_not_found(use_case, repo):

    payload = MedicalInfo(id=999, name="Non-existent Medical")
    

    repo.update.return_value = None

    result = await use_case.update(payload)

    repo.update.assert_awaited_once_with(payload)
    assert result is None
