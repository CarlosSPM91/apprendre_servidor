from typing import Literal
import pytest
from fastapi import HTTPException, status
from src.infrastructure.exceptions.except_manager import (
    manage_allergy_except,
    manage_classes_except,
    manage_course_except,
    manage_intolerance_except,
    manage_medical_except,
    manage_parent_except,
    manage_role_except,
    manage_student_except,
    manage_teacher_except,
    manage_user_except,
    manage_auth_except,
)


@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflict"),
            status.HTTP_409_CONFLICT,
            "Conflict",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorizad. Invalid Token or Expired",
        ),
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "Role not found",
        ),
    ],
)
def test_manage_role_except(
    exc: HTTPException,
    expected_status: Literal[409] | Literal[401] | Literal[404],
    expected_message: (
        Literal["Conflict"]
        | Literal["Unauthorizad. Invalid Token or Expired"]
        | Literal["Role not found"]
    ),
):
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
        (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail=""),
            status.HTTP_409_CONFLICT,
            "User already exist",
        ),
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "User not found",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorizad. Invalid Token or Expired",
        ),
    ],
)
def test_manage_user_except(
    exc: HTTPException,
    expected_status: Literal[409] | Literal[404] | Literal[401],
    expected_message: (
        Literal["User already exist"]
        | Literal["User not found"]
        | Literal["Unauthorizad. Invalid Token or Expired"]
    ),
):
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
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "User not found",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Invalid username or password",
        ),
    ],
)
def test_manage_auth_except(
    exc: HTTPException,
    expected_status: Literal[404] | Literal[401],
    expected_message: (
        Literal["User not found"] | Literal["Invalid username or password"]
    ),
):
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


@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail=""),
            status.HTTP_409_CONFLICT,
            "Parent already exist",
        ),
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "Parent not found",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorizad. Invalid Token or Expired",
        ),
    ],
)
def test_manage_parent_except(
    exc: HTTPException,
    expected_status: Literal[409] | Literal[404] | Literal[401],
    expected_message: (
        Literal["Parent already exist"]
        | Literal["Parent not found"]
        | Literal["Unauthorizad. Invalid Token or Expired"]
    ),
):
    with pytest.raises(HTTPException) as e:
        manage_parent_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)


def test_manage_parent_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected")
    with pytest.raises(HTTPException) as e:
        manage_parent_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected" in str(e.value.detail)


@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail=""),
            status.HTTP_409_CONFLICT,
            "Student already exist",
        ),
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "Student not found",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorizad. Invalid Token or Expired",
        ),
    ],
)
def test_manage_student_except(
    exc: HTTPException,
    expected_status: Literal[409] | Literal[404] | Literal[401],
    expected_message: (
        Literal["Student already exist"]
        | Literal["Student not found"]
        | Literal["Unauthorizad. Invalid Token or Expired"]
    ),
):
    with pytest.raises(HTTPException) as e:
        manage_student_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)


def test_manage_student_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected")
    with pytest.raises(HTTPException) as e:
        manage_student_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected" in str(e.value.detail)


@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail=""),
            status.HTTP_409_CONFLICT,
            "Medical info already exist",
        ),
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "Medical info not found",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorizad. Invalid Token or Expired",
        ),
    ],
)
def test_manage_medical_info_except(
    exc: HTTPException,
    expected_status: Literal[409] | Literal[404] | Literal[401],
    expected_message: (
        Literal["Medical info already exist"]
        | Literal["Medical info not found"]
        | Literal["Unauthorizad. Invalid Token or Expired"]
    ),
):
    with pytest.raises(HTTPException) as e:
        manage_medical_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)


def test_manage_medical_info_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected")
    with pytest.raises(HTTPException) as e:
        manage_medical_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected" in str(e.value.detail)


@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail=""),
            status.HTTP_409_CONFLICT,
            "Allergy already exist",
        ),
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "Allergy not found",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorizad. Invalid Token or Expired",
        ),
    ],
)
def test_manage_allergy_info_except(
    exc: HTTPException,
    expected_status: Literal[409] | Literal[404] | Literal[401],
    expected_message: (
        Literal["Allergy already exist"]
        | Literal["Allergy not found"]
        | Literal["Unauthorizad. Invalid Token or Expired"]
    ),
):
    with pytest.raises(HTTPException) as e:
        manage_allergy_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)


def test_manage_allergy_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected")
    with pytest.raises(HTTPException) as e:
        manage_allergy_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected" in str(e.value.detail)


@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail=""),
            status.HTTP_409_CONFLICT,
            "Food Intolerance info already exist",
        ),
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "Food Intolerance info not found",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorizad. Invalid Token or Expired",
        ),
    ],
)
def test_manage_intolerance_info_except(
    exc: HTTPException,
    expected_status: Literal[409] | Literal[404] | Literal[401],
    expected_message: (
        Literal["Food Intolerance info already exist"]
        | Literal["Food Intolerance info not found"]
        | Literal["Unauthorizad. Invalid Token or Expired"]
    ),
):
    with pytest.raises(HTTPException) as e:
        manage_intolerance_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)


def test_manage_intolerance_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected")
    with pytest.raises(HTTPException) as e:
        manage_intolerance_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected" in str(e.value.detail)


@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail=""),
            status.HTTP_409_CONFLICT,
            "Teacher already exist",
        ),
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "Teacher not found",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorizad. Invalid Token or Expired",
        ),
    ],
)
def test_manage_teacher_info_except(
    exc: HTTPException,
    expected_status: Literal[409] | Literal[404] | Literal[401],
    expected_message: (
        Literal["Teacher already exist"]
        | Literal["Teacher not found"]
        | Literal["Unauthorizad. Invalid Token or Expired"]
    ),
):
    with pytest.raises(HTTPException) as e:
        manage_teacher_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)


def test_manage_teacher_info_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected")
    with pytest.raises(HTTPException) as e:
        manage_teacher_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected" in str(e.value.detail)

import pytest
from fastapi import HTTPException, status
from typing import Literal

@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail=""),
            status.HTTP_409_CONFLICT,
            "Course already exist",
        ),
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "Course not found",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorizad. Invalid Token or Expired",
        ),
    ],
)
def test_manage_course_except(
    exc: HTTPException,
    expected_status: Literal[409] | Literal[404] | Literal[401],
    expected_message: (
        Literal["Course already exist"]
        | Literal["Course not found"]
        | Literal["Unauthorizad. Invalid Token or Expired"]
    ),
):
    with pytest.raises(HTTPException) as e:
        manage_course_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)


def test_manage_course_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected Error")
    with pytest.raises(HTTPException) as e:
        manage_course_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected Error" in str(e.value.detail)


@pytest.mark.parametrize(
    "exc, expected_status, expected_message",
    [
        (
            HTTPException(status_code=status.HTTP_409_CONFLICT, detail=""),
            status.HTTP_409_CONFLICT,
            "Classes already exist",
        ),
        (
            HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=""),
            status.HTTP_404_NOT_FOUND,
            "Classes not found",
        ),
        (
            HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=""),
            status.HTTP_401_UNAUTHORIZED,
            "Unauthorizad. Invalid Token or Expired",
        ),
    ],
)
def test_manage_classes_except(
    exc: HTTPException,
    expected_status: Literal[409] | Literal[404] | Literal[401],
    expected_message: (
        Literal["Classes already exist"]
        | Literal["Classes not found"]
        | Literal["Unauthorizad. Invalid Token or Expired"]
    ),
):
    with pytest.raises(HTTPException) as e:
        manage_classes_except(exc)
    assert e.value.status_code == expected_status
    assert expected_message in str(e.value.detail)


def test_manage_classes_except_default():
    exc = HTTPException(status_code=999, detail="Unexpected Classes Error")
    with pytest.raises(HTTPException) as e:
        manage_classes_except(exc)
    assert e.value.status_code == 500
    assert "Unexpected Classes Error" in str(e.value.detail)
