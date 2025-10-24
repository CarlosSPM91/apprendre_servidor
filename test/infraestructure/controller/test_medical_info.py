from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException
import pytest
from src.infrastructure.controllers.medical_info import MedicalInfoController
from src.infrastructure.entities.student_info.medical_info import MedicalInfo


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
def fake_medical():
    return MedicalInfo(
        id=1,
        user_id=1,
        observations="Test observations",
    )

@pytest.fixture
def medical_controller(find_case, create_case, update_case, delete_case):
    return MedicalInfoController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )


@pytest.mark.asyncio
async def test_init_medical_controller(
    medical_controller,
    find_case,
    create_case,
    update_case,
    delete_case,
):
    assert medical_controller.find_case == find_case
    assert medical_controller.create_case == create_case
    assert medical_controller.update_case == update_case
    assert medical_controller.delete_case == delete_case

@pytest.mark.asyncio
async def test_create_medical_info(
    medical_controller,
    create_case,
    fake_medical,
):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2025-10-10T12:00:00"
    create_case.create.return_value = mock_resp

    response = await medical_controller.create(fake_medical)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_resp.item_id)
    create_case.create.assert_awaited_once_with(fake_medical)

@pytest.mark.asyncio
async def test_update_medical_info(
    medical_controller,
    find_case,
    update_case,
    fake_medical,
):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2025-10-10T12:00:00"
    find_case.get_medical.return_value = fake_medical
    update_case.update.return_value = mock_resp

    response = await medical_controller.update(fake_medical)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_resp.item_id)
    find_case.get_medical.assert_awaited_once_with(fake_medical.id)
    update_case.update.assert_awaited_once_with(fake_medical)

@pytest.mark.asyncio
async def test_delete_medical_info(
    medical_controller,
    find_case,
    delete_case,
):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2025-10-10T12:00:00"
    find_case.get_medical.return_value = AsyncMock()
    delete_case.delete.return_value = mock_resp

    response = await medical_controller.delete(medical_id=1)

    assert response["status"] == "success"
    assert response["data"]["id"] == str(mock_resp.item_id)
    find_case.get_medical.assert_awaited_once_with(1)
    delete_case.delete.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_get_medical_info(
    medical_controller,
    find_case,
    fake_medical,
):
    find_case.get_medical.return_value = fake_medical

    response = await medical_controller.get_medical(medical_id=1)

    assert response["data"] == fake_medical
    find_case.get_medical.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_get_medical_info_not_found(
    medical_controller,
    find_case,
):
    find_case.get_medical.side_effect = HTTPException(status_code=404, detail="Not Found")

    with pytest.raises(HTTPException):
        await medical_controller.get_medical(medical_id=999)

    find_case.get_medical.assert_awaited_once_with(999)

@pytest.mark.asyncio
async def test_create_medical_info_exception(
    medical_controller,
    create_case,
    fake_medical,
):
    create_case.create.side_effect = HTTPException(status_code=400, detail="Bad Request")

    with pytest.raises(HTTPException):
        await medical_controller.create(fake_medical)

    create_case.create.assert_awaited_once_with(fake_medical)

@pytest.mark.asyncio
async def test_update_medical_info_exception(
    medical_controller,
    find_case,
    update_case,
    fake_medical,
):
    find_case.get_medical.side_effect = HTTPException(status_code=404, detail="Not Found")

    with pytest.raises(HTTPException):
        await medical_controller.update(fake_medical)

    find_case.get_medical.assert_awaited_once_with(fake_medical.id)

@pytest.mark.asyncio
async def test_delete_medical_info_exception(
    medical_controller,
    find_case,
    delete_case,
):
    find_case.get_medical.side_effect = HTTPException(status_code=404, detail="Not Found")

    with pytest.raises(HTTPException):
        await medical_controller.delete(medical_id=999)

    find_case.get_medical.assert_awaited_once_with(999)