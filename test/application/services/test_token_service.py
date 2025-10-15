import pytest
import jwt
import time
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone

from src.application.services.token_service import TokenService
from src.domain.objects.token.jwtPayload import JwtPayload


@pytest.fixture
def fake_settings(monkeypatch):
    """
    @brief Mock de configuración de la aplicación para pruebas.
    @param monkeypatch Herramienta de pytest para parchear atributos.
    """
    monkeypatch.setattr("src.application.services.token_service.settings.secret_key", "test_secret_key")
    monkeypatch.setattr("src.application.services.token_service.settings.algorithm", "HS256")


@pytest.fixture
def fake_payload():
    """
    @brief Crea un payload JWT falso para pruebas.
    @return JwtPayload instanciado con datos de prueba.
    """
    return JwtPayload(
        user_id=1,
        username="testuser",
        name="Test",
        last_name="User",
        role=1
    )


@pytest.fixture
def mock_redis():
    """
    @brief Generador de un mock asíncrono de Redis.
    @return Redis mock con métodos setex, get, set y delete simulados.
    """
    async def redis_generator():
        redis_mock = AsyncMock()
        redis_mock.setex = AsyncMock(return_value=True)
        redis_mock.get = AsyncMock(return_value=b"some_token")
        redis_mock.set = AsyncMock(return_value=True)
        redis_mock.delete = AsyncMock(return_value=True)
        yield redis_mock
    
    return redis_generator


@pytest.fixture
def mock_find_user():
    """
    @brief Mock para simular la búsqueda de un usuario.
    @return AsyncMock con método get_user_by_id que devuelve un usuario de prueba.
    """
    find_case = AsyncMock()
    find_case.get_user_by_id = AsyncMock(return_value=MagicMock(
        user_id=1,
        username="testuser",
        name="Test",
        last_name="User",
        role=1
    ))
    return find_case


@pytest.fixture
def token_service(mock_find_user, mock_redis):
    """
    @brief Crea una instancia de TokenService con dependencias mockeadas.
    @param mock_find_user Mock de búsqueda de usuario.
    @param mock_redis Mock de Redis.
    @return Instancia de TokenService lista para pruebas.
    """
    return TokenService(find_case=mock_find_user, redis_session=mock_redis, jwt_algorithm="HS256", jwt_expiration=24, jwt_secret="test_secret_key")


@pytest.mark.asyncio
async def test_generate_token(token_service, fake_payload):
    """
    @brief Prueba que generate_token retorna un JWT válido.
    @param token_service Instancia de TokenService.
    @param fake_payload Payload simulado.
    """
    token = await token_service.generate_token(fake_payload)
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    decoded = jwt.decode(token, "test_secret_key", algorithms=["HS256"])
    assert decoded["user_id"] == 1
    assert decoded["username"] == "testuser"
    assert "exp" in decoded
    assert "iat" in decoded


@pytest.mark.asyncio
async def test_generate_token_exception(token_service, fake_payload):
    """
    @brief Verifica que generate_token lanza HTTPException en caso de error al guardar token.
    """
    token_service.save_token = AsyncMock(side_effect=Exception("DB error"))

    with pytest.raises(HTTPException) as exc_info:
        await token_service.generate_token(fake_payload)

    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "DB error" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_decode_token(token_service, fake_payload):
    """
    @brief Verifica que decode_token decodifica correctamente un JWT.
    """
    token = await token_service.generate_token(fake_payload)
    decoded = token_service.decode_token(token)
    
    assert decoded["user_id"] == 1
    assert decoded["username"] == "testuser"
    assert decoded["name"] == "Test"
    assert decoded["last_name"] == "User"
    assert decoded["role"] == 1


@pytest.mark.asyncio
async def test_decode_token_verifies_expiration(token_service, fake_payload):
    """
    @brief Verifica que el token generado tenga tiempo de expiración correcto.
    """
    token = await token_service.generate_token(fake_payload)
    decoded = token_service.decode_token(token)
    iat = datetime.fromtimestamp(decoded["iat"], tz=timezone.utc)
    exp = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
    delta = exp - iat
    
    assert timedelta(hours=23, minutes=59) < delta < timedelta(hours=24, minutes=1)


@pytest.mark.asyncio
async def test_get_user_info(token_service, fake_payload):
    """
    @brief Verifica que get_user_info retorna correctamente un JwtPayload desde un token.
    """
    token = await token_service.generate_token(fake_payload)
    result = await token_service.get_user_info(token)
    
    assert isinstance(result, JwtPayload)
    assert result.user_id == 1
    assert result.username == "testuser"
    assert result.name == "Test"
    assert result.last_name == "User"
    assert result.role == 1


@pytest.mark.asyncio
async def test_decode_invalid_token_raises_exception(token_service):
    """
    @brief Verifica que decode_token lanza InvalidTokenError con un token inválido.
    """
    invalid_token = "invalid.token.here"
    
    with pytest.raises(jwt.InvalidTokenError):
        token_service.decode_token(invalid_token)


@pytest.mark.asyncio
async def test_decode_expired_token_raises_exception(token_service):
    """
    @brief Verifica que decode_token lanza ExpiredSignatureError con un token expirado.
    """
    expired_payload = {
        "user_id": "1",
        "username": "testuser",
        "exp": (datetime.now(timezone.utc) - timedelta(hours=1)).timestamp(),
        "iat": (datetime.now(timezone.utc) - timedelta(hours=2)).timestamp()
    }
    token = jwt.encode(expired_payload, "test_secret_key", algorithm="HS256")
    
    with pytest.raises(jwt.ExpiredSignatureError):
        token_service.decode_token(token)


@pytest.mark.asyncio
async def test_validate_token_with_expired_token(token_service):
    """
    @brief Verifica que validate_token lanza HTTPException con un token expirado.
    """
    expired_token_dict = {
        "user_id": "1",
        "exp": (datetime.now(timezone.utc) - timedelta(hours=1)).timestamp()
    }
    
    with pytest.raises(HTTPException) as exc_info:
        await token_service.validate_token(expired_token_dict)
    
    assert exc_info.value.status_code == 401
    assert "expired" in exc_info.value.detail.lower()


