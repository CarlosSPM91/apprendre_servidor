import pytest
from unittest.mock import AsyncMock, Mock
from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.application.use_case.user.create_user_case import CreateUserCase
from src.domain.objects.common.common_resp import CommonResponse
from src.domain.objects.user.user_create_dto import UserCreateDTO


@pytest.fixture
def user_repo():
    return AsyncMock()

@pytest.fixture
def pwd_service():
    mock = Mock()
    mock.hash_password.return_value = "hashed_password"
    return mock

@pytest.fixture
def create_student_case():
    return AsyncMock()

@pytest.fixture
def create_teacher_case():
    return AsyncMock()

@pytest.fixture
def find_role_case():
    mock = AsyncMock()
    mock_roles = [
        Mock(role_id=1, role_name="Admin"),
        Mock(role_id=2, role_name="Teacher"),
        Mock(role_id=3, role_name="Student"),
        Mock(role_id=4, role_name="Parent"),
    ]
    mock.get_all.return_value = mock_roles
    return mock

@pytest.fixture
def use_case(pwd_service, user_repo, create_student_case,create_teacher_case, find_role_case):
    return CreateUserCase(
        pwd_service,
        user_repo,
        create_student_case,
        create_teacher_case,
        find_role_case
    )


@pytest.mark.asyncio
async def test_create_user_success(use_case, user_repo, pwd_service, find_role_case):
    payload = UserCreateDTO(
        name="Test",
        last_name="User",
        username="testuser",
        dni="12345678A",
        email="test@example.com",
        phone="123456789",
        role_id=1,  
        password="plainpass"
    )


    mock_roles = [
        Mock(role_id=1, role_name="Admin"),
        Mock(role_id=2, role_name="Teacher"),
        Mock(role_id=3, role_name="Student"),
        Mock(role_id=4, role_name="Parent"),
    ]
    find_role_case.get_all.return_value = mock_roles

    user_repo.get_user_by_username.return_value = None

    user_created = Mock()
    user_created.user_id = 42
    user_created.role = 1  
    user_repo.create.return_value = user_created

    resp = await use_case.create(payload)

    user_repo.get_user_by_username.assert_awaited_once_with(payload.username)
    pwd_service.hash_password.assert_called_once_with("plainpass")
    user_repo.create.assert_awaited_once()
    find_role_case.get_all.assert_awaited_once()

    assert payload.password == "hashed_password"
    assert isinstance(resp, CommonResponse)
    assert resp.item_id == 42
    assert isinstance(resp.event_date, datetime)
    assert resp.event_date.tzinfo == timezone.utc


@pytest.mark.asyncio
async def test_create_user_student_success(use_case, user_repo, pwd_service, find_role_case, create_student_case):
    payload = UserCreateDTO(
        name="Student",
        last_name="Test",
        username="studentuser",
        dni="87654321B",
        email="student@example.com",
        phone="987654321",
        role_id=3, 
        password="plainpass"
    )

    mock_roles = [
        Mock(role_id=1, role_name="Admin"),
        Mock(role_id=2, role_name="Teacher"),
        Mock(role_id=3, role_name="Student"),
        Mock(role_id=4, role_name="Parent"),
    ]
    find_role_case.get_all.return_value = mock_roles

    user_repo.get_user_by_username.return_value = None

    user_created = Mock()
    user_created.user_id = 99
    user_created.role = 3 
    user_repo.create.return_value = user_created

    resp = await use_case.create(payload)


    create_student_case.create.assert_awaited_once()
    assert resp.item_id == 99


@pytest.mark.asyncio
async def test_create_user_already_exists(use_case, user_repo, find_role_case):
    payload = UserCreateDTO(
        name="Existing",
        last_name="User",
        username="existinguser",
        dni="11111111B",
        email="exist@example.com",
        phone="987654321",
        role_id=2,
        password="somepass"
    )

 
    user_repo.get_user_by_username.return_value = Mock()

    with pytest.raises(HTTPException) as exc_info:
        await use_case.create(payload)

    assert exc_info.value.status_code == status.HTTP_409_CONFLICT
    assert exc_info.value.detail == "User already exist"
    user_repo.create.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_user_invalid_role(use_case, user_repo, pwd_service, find_role_case):
    """Test para rol inválido"""
    payload = UserCreateDTO(
        name="Test",
        last_name="User",
        username="testuser",
        dni="12345678A",
        email="test@example.com",
        phone="123456789",
        role_id=999,  
        password="plainpass"
    )

    mock_roles = [
        Mock(role_id=1, role_name="Admin"),
        Mock(role_id=2, role_name="Teacher"),
        Mock(role_id=3, role_name="Student"),
        Mock(role_id=4, role_name="Parent"),
    ]
    find_role_case.get_all.return_value = mock_roles

    user_repo.get_user_by_username.return_value = None

    user_created = Mock()
    user_created.user_id = 42
    user_created.role = 999 
    user_repo.create.return_value = user_created

    with pytest.raises(HTTPException) as exc_info:
        await use_case.create(payload)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Role not valid"