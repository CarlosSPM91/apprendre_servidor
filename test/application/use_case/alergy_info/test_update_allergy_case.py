from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from src.application.use_case.allergy_info.update_allergy_case import UpdateAllergyCase
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.repositories.allergy_info import AllergyRepository


@pytest.fixture
def repo():
    return AsyncMock(spec=AllergyRepository)

@pytest.fixture
def use_case(repo):
    return UpdateAllergyCase(repo)

@pytest.mark.asyncio
async def test_update_allergy(use_case, repo):
    payload = AllergyInfo(id=1, name="Updated Allergy")
    

    updated_allergy = AllergyInfo(id=1, name="Updated Allergy")
    repo.update.return_value = updated_allergy

    result = await use_case.update(payload)

    repo.update.assert_awaited_once_with(payload)
    assert result.item_id == 1
    assert isinstance(result.event_date, datetime)

@pytest.mark.asyncio
async def test_update_allergy_not_found(use_case, repo):

    payload = AllergyInfo(id=999, name="Non-existent Allergy")
    

    repo.update.return_value = None

    result = await use_case.update(payload)

    repo.update.assert_awaited_once_with(payload)
    assert result is None