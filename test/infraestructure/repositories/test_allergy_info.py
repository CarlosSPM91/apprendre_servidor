from unittest.mock import AsyncMock, MagicMock

import pytest

from src.infrastructure.entities.student_info.allergy_info import AllergyInfo
from src.infrastructure.repositories.allergy_info import AllergyRepository


@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def allergy_repository(mock_session):
    async def session_gen():
        yield mock_session
    return AllergyRepository(session=session_gen)


@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    allergy_repo = AllergyRepository(mock_session_test)
    assert allergy_repo.session == mock_session_test

@pytest.mark.asyncio
async def test_get_allergy_success(allergy_repository, mock_session):
    mock_exec_result = MagicMock() 
    mock_exec_result.first.return_value = AllergyInfo(
        id=1,
        name="Peanuts",
        description="Allergy to peanuts"
    )
    mock_session.exec = AsyncMock(return_value=mock_exec_result) 

    result = await allergy_repository.get(1)  

    assert result.id == 1
    assert result.name == "Peanuts"
    assert result.description == "Allergy to peanuts"
    mock_session.exec.assert_awaited_once() 

@pytest.mark.asyncio
async def test_create_allergy_success(allergy_repository, mock_session):
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    new_allergy = AllergyInfo(
        name="Pollen",
        description="Allergy to pollen"
    )

    result = await allergy_repository.create(new_allergy)

    assert result.name == "Pollen"
    assert result.description == "Allergy to pollen"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_allergy_success(allergy_repository, mock_session):
    existing_allergy = AllergyInfo(
        id=1,
        name="Dust",
        description="Allergy to dust"
    )

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = existing_allergy
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    updated_allergy = AllergyInfo(
        id=1,
        name="Dust Mites",
        description="Severe allergy to dust mites"
    )

    result = await allergy_repository.update(updated_allergy)

    assert result.name == "Dust Mites"
    assert result.description == "Severe allergy to dust mites"
    mock_session.exec.assert_awaited_once()
    mock_session.commit.assert_awaited_once() 
    mock_session.refresh.assert_awaited_once()

@pytest.mark.asyncio
async def test_update_allergy_not_found(allergy_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = None
    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    non_existent_allergy = AllergyInfo(
        id=999,
        name="NonExistent",
        description="This allergy does not exist"
    )

    with pytest.raises(Exception) as exc_info:
        await allergy_repository.update(non_existent_allergy)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Allergy not found"
    mock_session.exec.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_allergy_success(allergy_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    await allergy_repository.delete(1)

    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_awaited_once()
    mock_session.commit.assert_awaited_once()