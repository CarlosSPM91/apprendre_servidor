from unittest.mock import AsyncMock, MagicMock
import pytest
from fastapi import HTTPException
from sqlmodel import select

from src.infrastructure.entities.users.teacher import Teacher
from src.infrastructure.entities.users.user import User
from src.infrastructure.entities.course.school_subject import SchoolSubject
from src.infrastructure.entities.course.subject_class import SubjectClass
from src.domain.objects.profiles.teacher_dto import TeacherDTO
from src.infrastructure.repositories.teacher import TeacherRepository
from src.domain.objects.subject_dto import SubjectDTO


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.add = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.rollback = AsyncMock()
    session.delete = AsyncMock()
    session.exec = AsyncMock()
    return session


@pytest.fixture
def teacher_repository(mock_session):
    async def session_gen():
        yield mock_session

    return TeacherRepository(session=session_gen)


@pytest.fixture
def fake_teacher():
    return Teacher(id=1, user_id=1)


@pytest.fixture
def fake_user():
    return User(
        id=1,
        username="t_user",
        name="Teacher",
        last_name="One",
        dni="00000000T",
        phone=123456,
        email="t1@test.com",
        password="hashed_pass",
        role_id=2,
    )


@pytest.mark.asyncio
async def test_init_teacher_repo():
    mock_session_test = MagicMock()
    repo = TeacherRepository(mock_session_test)
    assert repo.session == mock_session_test


@pytest.mark.asyncio
async def test_get_teacher_success(fake_teacher, teacher_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = fake_teacher
    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    result = await teacher_repository.get_teacher(1)

    assert result == fake_teacher
    mock_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_teacher_not_found(teacher_repository, mock_session):
    mock_result = MagicMock()
    mock_result.first.return_value = None
    mock_session.exec = AsyncMock(return_value=mock_result)

    with pytest.raises(HTTPException) as exc:
        await teacher_repository.get_teacher(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Teacher not found"
    mock_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_teacher_full_info_success(
    fake_teacher, fake_user, teacher_repository, mock_session
):

    mock_teacher_user = MagicMock()
    mock_teacher_user.first.return_value = (fake_teacher, fake_user)

    fake_subject = SchoolSubject(id=10, name="Math", description="Algebra I")
    fake_class = SubjectClass(id=1, class_id=101, subject_id=10, professor_id=1)

    mock_subjects_result = MagicMock()
    mock_subjects_result.all.return_value = [(fake_class, fake_subject)]

    mock_session.exec = AsyncMock(side_effect=[mock_teacher_user, mock_subjects_result])

    result = await teacher_repository.get_teacher_full_info(1)

    assert isinstance(result, TeacherDTO)
    assert result.teacher_id == 1
    assert result.user_id == 1
    assert result.name == "Teacher"
    assert len(result.subjects) == 1
    assert result.subjects[0].subject_name == "Math"
    assert mock_session.exec.await_count == 2


@pytest.mark.asyncio
async def test_get_teacher_full_info_not_found(teacher_repository, mock_session):
    mock_result = MagicMock()
    mock_result.first.return_value = None

    mock_session.exec = AsyncMock(return_value=mock_result)

    with pytest.raises(HTTPException) as exc:
        await teacher_repository.get_teacher_full_info(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Teacher not found"
    mock_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_success(teacher_repository, mock_session):

    t1 = Teacher(id=1, user_id=1)
    u1 = User(
        id=1,
        name="T1",
        last_name="L1",
        dni="X1",
        phone=111,
        email="t1@t.com",
        username="t1",
    )

    t2 = Teacher(id=2, user_id=2)
    u2 = User(
        id=2,
        name="T2",
        last_name="L2",
        dni="X2",
        phone=222,
        email="t2@t.com",
        username="t2",
    )

    mock_teachers_users = MagicMock()
    mock_teachers_users.all.return_value = [(t1, u1), (t2, u2)]

    sub = SchoolSubject(id=10, name="Math", description="Basic math")
    sub_class = SubjectClass(id=1, class_id=101, subject_id=10, professor_id=1)

    mock_subjects = MagicMock()
    mock_subjects.all.return_value = [(sub_class, sub, 1)]

    mock_session.exec = AsyncMock(side_effect=[mock_teachers_users, mock_subjects])

    result = await teacher_repository.get_all()

    assert isinstance(result, list)
    assert len(result) == 2

    assert len(result[0].subjects) == 1
    assert result[0].subjects[0].subject_name == "Math"

    assert len(result[1].subjects) == 0


@pytest.mark.asyncio
async def test_get_all_not_found(teacher_repository, mock_session):
    mock_empty = MagicMock()
    mock_empty.all.return_value = None

    mock_session.exec = AsyncMock(return_value=mock_empty)

    with pytest.raises(HTTPException) as exc:
        await teacher_repository.get_all()

    assert exc.value.status_code == 404
    assert exc.value.detail == "Teachers not found"
    mock_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_teacher_success(fake_teacher, teacher_repository, mock_session):
    mock_exists_result = MagicMock()
    mock_exists_result.first.return_value = None
    mock_session.exec = AsyncMock(return_value=mock_exists_result)

    result = await teacher_repository.create(user_id=1)

    assert isinstance(result, Teacher)
    assert result.user_id == 1
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_teacher_already_exists(
    fake_teacher, teacher_repository, mock_session
):
    mock_exists = MagicMock()
    mock_exists.first.return_value = fake_teacher

    mock_session.exec = AsyncMock(return_value=mock_exists)

    with pytest.raises(HTTPException) as exc:
        await teacher_repository.create(user_id=1)

    assert exc.value.status_code == 409
    assert exc.value.detail == "Teacher already exist"
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()


@pytest.mark.asyncio
async def test_delete_teacher_success(fake_teacher, teacher_repository, mock_session):
    mock_found = MagicMock()
    mock_found.first.return_value = fake_teacher
    mock_session.exec = AsyncMock(return_value=mock_found)

    result = await teacher_repository.delete(1)

    assert result is True
    mock_session.delete.assert_awaited_once()
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_teacher_not_found(teacher_repository, mock_session):
    mock_not_found = MagicMock()
    mock_not_found.first.return_value = None

    mock_session.exec = AsyncMock(return_value=mock_not_found)

    with pytest.raises(HTTPException) as exc:
        await teacher_repository.delete(999)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Teacher not found"
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()
