import pytest
from fastapi import HTTPException, status
from src.domain.exceptions.except_manager import (
    manage_role_except,
    manage_user_except,
    manage_auth_except,
)

@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflict"), status.HTTP_409_CONFLICT, "Conflict"),
        (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""), status.HTTP_401_UNAUTHORIZED, "Unauthorizad. Invalid Token or Expired"),
        (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""), status.HTTP_404_NOT_FOUND, "Role not found"),
    ],
)
def test_manage_role_except(exc, expected_status, expected_message):
    with pytest.raises(HTTPException) as e:
        manage_role_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)

def test_manage_role_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected")
    with pytest.raises(HTTPException) as e:
        manage_role_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected" in str(e.value.detail)

@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (HTTPException(status_code=status.HTTP_409_CONFLICT, detail=""), status.HTTP_409_CONFLICT, "User already exist"),
        (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""), status.HTTP_404_NOT_FOUND, "User not found"),
        (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""), status.HTTP_401_UNAUTHORIZED, "Unauthorizad. Invalid Token or Expired"),
    ],
)
def test_manage_user_except(exc, expected_status, expected_message):
    with pytest.raises(HTTPException) as e:
        manage_user_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)

def test_manage_user_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected")
    with pytest.raises(HTTPException) as e:
        manage_user_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected" in str(e.value.detail)


@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""), status.HTTP_404_NOT_FOUND, "User not found"),
        (HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""), status.HTTP_401_UNAUTHORIZED, "Invalid username or password"),
    ],
)
def test_manage_auth_except(exc, expected_status, expected_message):
    with pytest.raises(HTTPException) as e:
        manage_auth_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)

def test_manage_auth_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected")
    with pytest.raises(HTTPException) as e:
        manage_auth_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected" in str(e.value.detail)
