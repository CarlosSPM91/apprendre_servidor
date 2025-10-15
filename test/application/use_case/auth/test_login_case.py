import pytest
from unittest.mock import AsyncMock, Mock
from fastapi import HTTPException, status
from datetime import datetime, timezone

from src.application.use_case.auth.login_use_case import LoginUseCase
from src.domain.objects.auth.login_req import LoginRequest
from src.domain.objects.user.user_update_dto import UserUpdateDTO


@pytest.fixture
def pwd_service():
    """
    @brief Fixture que crea un mock del servicio de passwords.
    @return Mock con hash_password simulado.
    """
    mock = Mock()
    mock.hash_password.return_value = "hashed_password"
    return mock


@pytest.fixture
def token_service():
    """
    @brief Fixture que crea un mock del servicio de tokens.
    @return AsyncMock con generate_token simulado.
    """
    mock = AsyncMock()
    mock.generate_token.return_value = "fake_jwt_token"
    return mock


@pytest.fixture
def find_user_case():
    """
    @brief Fixture que crea un mock de la búsqueda de usuario.
    @return AsyncMock para get_user_by_username.
    """
    return AsyncMock()


@pytest.fixture
def update_user_case():
    """
    @brief Fixture que crea un mock del caso de uso de actualización de usuario.
    @return AsyncMock con update_last_used simulado.
    """
    mock = AsyncMock()
    mock.update_last_used = AsyncMock()
    return mock


@pytest.fixture
def access_repo():
    """
    @brief Fixture que crea un mock del repositorio de accesos.
    @return AsyncMock con create simulado.
    """
    mock = AsyncMock()
    mock.create = AsyncMock()
    return mock


@pytest.fixture
def use_case(pwd_service, token_service, find_user_case, update_user_case, access_repo):
    """
    @brief Fixture que instancia LoginUseCase con todos los mocks necesarios.
    @param pwd_service Mock del servicio de passwords.
    @param token_service Mock del servicio de tokens.
    @param find_user_case Mock de búsqueda de usuario.
    @param update_user_case Mock de actualización de usuario.
    @param access_repo Mock del repositorio de accesos.
    @return Instancia de LoginUseCase lista para pruebas.
    """
    return LoginUseCase(
        pwd_service,
        token_service,
        find_user_case,
        update_user_case,
        access_repo,
    )


@pytest.mark.asyncio
async def test_login_success(use_case, pwd_service, token_service, find_user_case, update_user_case, access_repo):
    """
    @brief Verifica que login funciona correctamente con credenciales válidas.
    @param use_case Instancia de LoginUseCase.
    @param pwd_service Mock del servicio de passwords.
    @param token_service Mock del servicio de tokens.
    @param find_user_case Mock de búsqueda de usuario.
    @param update_user_case Mock de actualización de usuario.
    @param access_repo Mock del repositorio de accesos.
    """
    payload = LoginRequest(username="testuser", password="plainpass")

    user = UserUpdateDTO(
        user_id=1,
        username="testuser",
        name="Test",
        last_name="User",
        role_id=2,
        password="hashed_password"
    )

    find_user_case.get_user_by_username.return_value = user

    resp = await use_case.login(payload)
    pwd_service.hash_password.assert_called_once_with("plainpass")
    find_user_case.get_user_by_username.assert_awaited_once_with("testuser")
    token_service.generate_token.assert_awaited()
    update_user_case.update_last_used.assert_awaited_once_with(user.user_id)
    access_repo.create.assert_awaited()

    assert resp["access_token"] == "fake_jwt_token"
    assert resp["token_type"] == "bearer"
    assert resp["user_id"] == str(user.user_id)
    assert resp["username"] == user.username
    assert resp["role"] == user.role_id


@pytest.mark.asyncio
async def test_login_user_not_found(use_case, find_user_case):
    """
    @brief Verifica que login lanza HTTPException 404 si el usuario no existe.
    @param use_case Instancia de LoginUseCase.
    @param find_user_case Mock de búsqueda de usuario.
    """
    payload = LoginRequest(username="nouser", password="pass123")
    find_user_case.get_user_by_username.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await use_case.login(payload)

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "User not found"


@pytest.mark.asyncio
async def test_login_wrong_password(use_case, pwd_service, find_user_case):
    """
    @brief Verifica que login lanza HTTPException 401 si la contraseña es incorrecta.
    @param use_case Instancia de LoginUseCase.
    @param pwd_service Mock del servicio de passwords.
    @param find_user_case Mock de búsqueda de usuario.
    """
    payload = LoginRequest(username="testuser", password="wrongpass")

    user = UserUpdateDTO(
        user_id=1,
        username="testuser",
        name="Test",
        last_name="User",
        role_id=2,
        password="correct_hash"
    )

    find_user_case.get_user_by_username.return_value = user
    pwd_service.hash_password.return_value = "wrong_hash"

    with pytest.raises(HTTPException) as exc_info:
        await use_case.login(payload)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid username or password"
