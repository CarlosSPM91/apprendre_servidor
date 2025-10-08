import hashlib
import pytest
from src.application.services.password_service import PasswordService

@pytest.fixture
def pass_service():
    return PasswordService()

def test_password_service(pass_service):
    password="1234"
    expected_hash= hashlib.sha256(password.encode()).hexdigest()

    result = pass_service.hash_password(password)
    assert result == expected_hash


def test_password_service_deterministic(pass_service):
    password="1234"

    result = pass_service.hash_password(password)
    second_result = pass_service.hash_password(password)
    assert result == second_result

def test_password_service_different_inputs(pass_service):
    password="1234"
    second_password="4321"

    result = pass_service.hash_password(password)
    second_result = pass_service.hash_password(second_password)
    assert result != second_result