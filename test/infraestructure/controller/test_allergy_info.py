from unittest.mock import AsyncMock
from fastapi import HTTPException
import pytest

from src.infrastructure.controllers.allergy_info import AllergyController
from src.infrastructure.entities.student_info.allergy_info import AllergyInfo


@pytest.fixture
def create_case():
    mock = AsyncMock()
    return mock


@pytest.fixture
def update_case():
    mock = AsyncMock()
    return mock


@pytest.fixture
def delete_case():
    mock = AsyncMock()
    return mock


@pytest.fixture
def find_case():
    mock = AsyncMock()
    return mock

@pytest.fixture
def fake_allergy():
    return AllergyInfo(
        id=1,
        user_id=1,
        description="Test description",
    )

@pytest.fixture
def allergy_controller(find_case, create_case, update_case, delete_case):
    return AllergyController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )

@pytest.mark.asyncio
async def test_init_allergy_controller(
    allergy_controller,
    find_case,
    create_case,
    update_case,
    delete_case,
):
    assert allergy_controller.find_case == find_case
    assert allergy_controller.create_case == create_case
    assert allergy_controller.update_case == update_case
    assert allergy_controller.delete_case == delete_case

@pytest.mark.asyncio
async def test_create_allergy(
    allergy_controller,
    create_case,
    fake_allergy,
):
    create_case.create.return_value = AsyncMock(
        item_id=1,
        event_date="2024-01-01T00:00:00",
    )

    response = await allergy_controller.create(fake_allergy)

    assert response["status"] == "success"
    assert response["data"]["id"] == "1"
    assert response["data"]["created_date"] == "2024-01-01T00:00:00"
    create_case.create.assert_awaited_once_with(fake_allergy)

@pytest.mark.asyncio
async def test_get_allergy_not_found(
    allergy_controller,
    find_case,
): 
    find_case.get_allergy.side_effect = HTTPException(status_code=404, detail="Not Found")

    with pytest.raises(HTTPException):
        await allergy_controller.get_allergy(medical_id=999)

    find_case.get_allergy.assert_awaited_once_with(999)

@pytest.mark.asyncio
async def test_update_allergy(
    allergy_controller,
    find_case,
    update_case,
    fake_allergy,
):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2025-10-10T12:00:00"
    find_case.get_allergy.return_value = fake_allergy
    update_case.update.return_value = mock_resp

    response = await allergy_controller.update(fake_allergy)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_resp.item_id)
    find_case.get_allergy.assert_awaited_once_with(fake_allergy.id)
    update_case.update.assert_awaited_once_with(fake_allergy)

@pytest.mark.asyncio
async def test_delete_allergy(
    allergy_controller,
    find_case,
    delete_case,
):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2025-10-10T12:00:00"
    find_case.get_allergy.return_value = AsyncMock()
    delete_case.delete.return_value = mock_resp

    response = await allergy_controller.delete(allergy_id=1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_resp.item_id)
    find_case.get_allergy.assert_awaited_once_with(1)
    delete_case.delete.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_get_allergy(
    allergy_controller,
    find_case,
    fake_allergy,
):
    find_case.get_allergy.return_value = fake_allergy

    response = await allergy_controller.get_allergy(allergy_id=1)

    assert response == fake_allergy
    find_case.get_allergy.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_get_allergy_not_found(
    allergy_controller,
    find_case,
): 
    find_case.get_allergy.side_effect = HTTPException(status_code=404, detail="Not Found")

    with pytest.raises(HTTPException):
        await allergy_controller.get_allergy(allergy_id=999)

    find_case.get_allergy.assert_awaited_once_with(999)

        