import pytest
from unittest.mock import AsyncMock, patch
from fastapi import HTTPException, status

from src.infrastructure.controllers.role import RoleController
from src.domain.objects.role.role_dto import RoleDTO

@pytest.fixture
def create_role_case():
    return AsyncMock()

@pytest.fixture
def find_role_case():
    return AsyncMock()

@pytest.fixture
def update_role_case():
    return AsyncMock()

@pytest.fixture
def delete_role_case():
    return AsyncMock()

@pytest.fixture
def role_controller(create_role_case, find_role_case, update_role_case, delete_role_case):
    return RoleController(
        create_role_case=create_role_case,
        find_role_case=find_role_case,
        update_role_case=update_role_case,
        delete_role_case=delete_role_case
    )

@pytest.mark.asyncio
async def test_create_role_success(role_controller, create_role_case):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2025-10-10T12:00:00"
    create_role_case.create.return_value = mock_resp

    result = await role_controller.create_role("Admin")
    assert result["status"] == "success"
    assert result["data"]["id"] == str(mock_resp.item_id)

@pytest.mark.asyncio
async def test_create_role_exception(role_controller, create_role_case):
    create_role_case.create.side_effect = HTTPException(status_code=400, detail="Error")
    with patch("src.infrastructure.controllers.role.sentry_sdk.capture_exception") as mock_sentry, \
         patch("src.infrastructure.controllers.role.manage_role_except") as mock_manage:
        result = await role_controller.create_role("Admin")
        assert result is None
        mock_sentry.assert_called()
        mock_manage.assert_called()

@pytest.mark.asyncio
async def test_update_role_success(role_controller, update_role_case, find_role_case):
    role = RoleDTO(role_id=1, role_name="Admin")
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2025-10-10T12:00:00"
    update_role_case.update.return_value = mock_resp
    find_role_case.find_by_id.return_value = AsyncMock()

    result = await role_controller.update_role(role)
    assert result["status"] == "success"
    assert result["data"]["id"] == str(mock_resp.item_id)

@pytest.mark.asyncio
async def test_deleterole_success(role_controller, delete_role_case):
    mock_resp = AsyncMock()
    mock_resp.item_id = 1
    mock_resp.event_date = "2025-10-10T12:00:00"
    delete_role_case.delete.return_value = mock_resp

    result = await role_controller.deleterole(1)
    assert result["status"] == "success"
    assert result["data"]["id"] == str(mock_resp.item_id)
