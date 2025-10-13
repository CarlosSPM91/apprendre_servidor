import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi import HTTPException
from datetime import datetime, timezone

from src.infrastructure.controllers.user import UserController
from src.domain.objects.user.user_create_dto import UserCreateDTO
from src.domain.objects.user.user_update_dto import UserUpdateDTO
from src.domain.objects.auth.change_pass_dto import ChangePasswordDTO
from src.domain.objects.user.user_dto import UserDTO
from src.domain.objects.common.common_resp import CommonResponse


@pytest.fixture
def fake_user():
    return UserDTO(
        user_id=1,
        username="test",
        name="Test",
        last_name="User",
        email="a@b.com",
        phone="123",
        dni="12345678A",
        role=1,
    )


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
def user_controller(find_case, create_case, update_case, delete_case):
    return UserController(
        find_case=find_case,
        create_case=create_case,
        update_case=update_case,
        delete_case=delete_case,
    )


@pytest.mark.asyncio
async def test_create_user_success(user_controller, create_case):
    payload = UserCreateDTO(
        username="testuser",
        name="Test",
        last_name="User",
        email="test@example.com",
        phone="123456789",
        dni="12345678A",
        password="pass123",
        role_id=1,
    )
    create_case.create.return_value = CommonResponse(
        item_id=1, event_date=datetime.now(timezone.utc)
    )

    resp = await user_controller.create_user(payload)

    assert resp["status"] == "success"
    assert resp["data"]["id"] == "1"
    assert "created_date" in resp["data"]
    create_case.create.assert_awaited_once_with(payload)


@pytest.mark.asyncio
async def test_update_user_success(user_controller, find_case, update_case):
    payload = UserUpdateDTO(
        user_id=1,
        name="TestUpdated",
        last_name="User",
        username="testuser",
        dni="12345678A",
        email="test@example.com",
        phone="123456789",
        role_id=1,
        password="newpass",
    )
    find_case.get_user_by_id.return_value = AsyncMock(user_id=1)
    update_case.update_user.return_value = CommonResponse(
        item_id=1, event_date=datetime.now(timezone.utc)
    )

    resp = await user_controller.update_user(payload)
    assert resp["status"] == "success"
    assert resp["data"]["id"] == "1"
    assert "updated_date" in resp["data"]


@pytest.mark.asyncio
async def test_change_password_success(user_controller, find_case, update_case):
    payload = ChangePasswordDTO(user_id=1, password="newpass")
    find_case.get_user_by_id.return_value = AsyncMock(user_id=1)
    update_case.change_password.return_value = CommonResponse(
        item_id=1, event_date=datetime.now(timezone.utc)
    )

    resp = await user_controller.change_password(payload)
    assert resp["status"] == "success"
    assert resp["data"]["id"] == "1"
    assert "update_date" in resp["data"]


@pytest.mark.asyncio
async def test_delete_user_success(user_controller, find_case, delete_case):
    user_id = 1
    user_eraser_id = 2
    find_case.get_user_by_id.return_value = AsyncMock(user_id=user_id)
    delete_case.delete.return_value = CommonResponse(
        item_id=user_id, event_date=datetime.now(timezone.utc)
    )

    resp = await user_controller.delete_user(user_id, user_eraser_id)
    assert resp["status"] == "success"
    assert resp["data"]["id"] == str(user_id)
    assert "deletion_date" in resp["data"]


@pytest.mark.asyncio
async def test_me_exception(user_controller, find_case):
    find_case.get_user_by_id.side_effect = HTTPException(
        status_code=404, detail="Not found"
    )
    with (
        patch(
            "src.infrastructure.controllers.user.sentry_sdk.capture_exception"
        ) as mock_sentry,
        patch("src.infrastructure.controllers.user.manage_user_except") as mock_manager,
    ):
        await user_controller.me("1")
        mock_sentry.assert_called_once()
        mock_manager.assert_called_once()


@pytest.mark.asyncio
async def test_me_success(user_controller, find_case, fake_user):
    fake_user
    find_case.get_user_by_id.return_value = fake_user

    resp = await user_controller.me(user_id="1")
    assert resp.username == "test"
    find_case.get_user_by_id.assert_awaited_once_with("1")


@pytest.mark.asyncio
async def test_get_all_success(user_controller, find_case, fake_user):
    find_case.get_all.return_value = [
        fake_user
    ]

    resp = await user_controller.get_all()
    assert resp["status"] == "success"
    assert len(resp["data"]) == 1
    assert resp["data"][0].username == "test"


@pytest.mark.asyncio
async def test_get_user_success(user_controller, find_case, fake_user):

    find_case.get_user_by_id.return_value = fake_user

    resp = await user_controller.get_user(user_id="1")
    assert resp.username == "test"
    find_case.get_user_by_id.assert_awaited_once_with("1")


@pytest.mark.asyncio
async def test_get_all_exception(user_controller, find_case):
    find_case.get_all.side_effect = HTTPException(status_code=404, detail="Not found")
    with (
        patch(
            "src.infrastructure.controllers.user.sentry_sdk.capture_exception"
        ) as mock_sentry,
        patch("src.infrastructure.controllers.user.manage_user_except") as mock_manager,
    ):
        await user_controller.get_all()
        mock_sentry.assert_called_once()
        mock_manager.assert_called_once()


@pytest.mark.asyncio
async def test_get_user_exception(user_controller, find_case):
    find_case.get_user_by_id.side_effect = HTTPException(
        status_code=404, detail="Not found"
    )
    with (
        patch(
            "src.infrastructure.controllers.user.sentry_sdk.capture_exception"
        ) as mock_sentry,
        patch("src.infrastructure.controllers.user.manage_user_except") as mock_manager,
    ):
        await user_controller.get_user("1")
        mock_sentry.assert_called_once()
        mock_manager.assert_called_once()
