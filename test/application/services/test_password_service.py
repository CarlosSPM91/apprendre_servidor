import hashlib
import pytest
from src.application.services.password_service import PasswordService

@pytest.fixture
def pass_service():
    """
    @brief Fixture que crea una instancia de PasswordService para pruebas.
    @return PasswordService instanciado.
    """
    return PasswordService()


def test_password_service(pass_service):
    """
    @brief Verifica que hash_password genera el hash SHA-256 esperado.
    @param pass_service Instancia de PasswordService.
    """
    password = "1234"
    expected_hash = hashlib.sha256(password.encode()).hexdigest()

    result = pass_service.hash_password(password)
    assert result == expected_hash


def test_password_service_deterministic(pass_service):
    """
    @brief Verifica que hash_password es determinístico, es decir,
           que el mismo input produce siempre el mismo hash.
    @param pass_service Instancia de PasswordService.
    """
    password = "1234"

    result = pass_service.hash_password(password)
    second_result = pass_service.hash_password(password)
    assert result == second_result


def test_password_service_different_inputs(pass_service):
    """
    @brief Verifica que hash_password genera hashes diferentes para inputs distintos.
    @param pass_service Instancia de PasswordService.
    """
    password = "1234"
    second_password = "4321"

    result = pass_service.hash_password(password)
    second_result = pass_service.hash_password(second_password)
    assert result != second_result
