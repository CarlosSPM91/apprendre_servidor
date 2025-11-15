from sqlite3 import IntegrityError
from unittest.mock import AsyncMock, MagicMock

from fastapi import HTTPException
import pytest

from src.infrastructure.entities.student_info.medical_info import MedicalInfo
from src.infrastructure.repositories.medical_info import MedicalInfoRepository


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def medical_repository(mock_session):
    async def session_gen():
        yield mock_session

    return MedicalInfoRepository(session=session_gen)


@pytest.fixture
def medical_mock():
    return MedicalInfo(
        id=1, name="Hipertension", description="More tension than normal", medication="None"
    )


@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    medical_repository = MedicalInfoRepository(mock_session_test)
    assert medical_repository.session == mock_session_test


@pytest.mark.asyncio
async def test_get_medical_success(
    medical_repository, mock_session, medical_mock
):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = medical_mock
    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    result = await medical_repository.get(1)

    assert result.id == 1
    assert result.name == "Hipertension"
    assert result.description == "More tension than normal"
    mock_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_medical_success(
    medical_repository, mock_session, medical_mock
):
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    new_medical_info = medical_mock

    result = await medical_repository.create(new_medical_info)

    assert result.name == "Hipertension"
    assert result.description == "More tension than normal"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_medical_success(
    medical_repository, mock_session, medical_mock
):
    existing_medical_info = medical_mock

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = existing_medical_info
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    updated_intolerance= MedicalInfo(
        id=1, name="Asma", description="Breath problems"
    )

    result = await medical_repository.update(updated_intolerance)

    assert result.name == "Asma"
    assert result.description == "Breath problems"
    mock_session.exec.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_medical_not_found(medical_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = None
    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    non_existent_medical_info= MedicalInfo(
        id=999, name="Asma", description="Breath problems", medication="None"
    )

    with pytest.raises(Exception) as exc_info:
        await medical_repository.update(non_existent_medical_info)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Medical Info not found"
    mock_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_medical_success(medical_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    await medical_repository.delete(1)

    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_awaited_once()
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_medical_not_found(medical_repository, mock_session):
    mock_result_select = MagicMock()
    mock_result_select.first = MagicMock(return_value=None)
    
    mock_session.exec = AsyncMock(return_value=mock_result_select)
    mock_session.delete = AsyncMock()

    with pytest.raises(HTTPException) as exc_info:
        await medical_repository.delete(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Medical Info not found"
    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()

    
@pytest.mark.asyncio
async def test_get_all_medical_info_success(mock_session):
    fake_items = [MedicalInfo(id=1), MedicalInfo(id=2)]
    mock_exec_result = AsyncMock()
    mock_exec_result = MagicMock()
    mock_exec_result.all.return_value = fake_items
    mock_session.exec = AsyncMock(return_value=mock_exec_result)



    async def fake_session_gen():
        yield mock_session
    repo = MedicalInfoRepository(session=fake_session_gen)
    result = await repo.get_all()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2
    mock_session.exec.assert_awaited_once()