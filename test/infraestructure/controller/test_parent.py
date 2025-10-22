
from unittest.mock import AsyncMock
from fastapi import HTTPException
import pytest

from src.infrastructure.controllers.parent import ParentController
from src.infrastructure.entities.users.parents import Parent


@pytest.fixture
def create_case():
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
def fake_parent():
    return Parent(
        id=1,
        user_id=1,
        student_id=2,
    )

@pytest.fixture
def parent_controller(find_case, create_case, delete_case):
    return ParentController(
        find_case=find_case,
        create_case=create_case,
        delete_case=delete_case,
    )

@pytest.mark.asyncio
async def test_create_parent_success(parent_controller, create_case, fake_parent):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2025-10-10T12:00:00"
    create_case.create.return_value = mock_resp

    result = await parent_controller.create(fake_parent)
    assert result["status"] == "success"
    assert result["data"]["id"] == str(mock_resp.item_id)

@pytest.mark.asyncio
async def test_delete_parent_success(parent_controller, delete_case):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2025-10-10T12:00:00"
    delete_case.delete.return_value = mock_resp

    result = await parent_controller.delete(user_id=1, student_id=2)
    assert result["status"] == "success"
    assert result["data"]["id"] == str(mock_resp.item_id)

@pytest.mark.asyncio
async def test_get_parent_success(parent_controller, find_case, fake_parent):
    find_case.get.return_value = fake_parent

    result = await parent_controller.get_parent(user_id=1)
    assert result["status"] == "success"
    assert result["data"] == fake_parent

@pytest.mark.asyncio
async def test_get_parent_exception(parent_controller, find_case):
    find_case.get.side_effect = HTTPException(status_code=404, detail="Parent not found")

    with pytest.raises(HTTPException):
        await parent_controller.get_parent(user_id=999)
    find_case.get.assert_awaited_once_with(user_id=999)

@pytest.mark.asyncio
async def test_delete_parent_exception(parent_controller, delete_case):
    delete_case.delete.side_effect = HTTPException(status_code=404, detail="Parent not found")

    with pytest.raises(HTTPException):
        await parent_controller.delete(user_id=999, student_id=888)
    delete_case.delete.assert_awaited_once_with(user_id=999, student_id=888)