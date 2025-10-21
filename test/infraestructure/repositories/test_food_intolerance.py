from unittest.mock import AsyncMock, MagicMock

import pytest

from src.infrastructure.entities.student_info.food_intolerance import FoodIntolerance
from src.infrastructure.repositories.food_intolerance import FoodIntoleranceRepository


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def intolerance_repository(mock_session):
    async def session_gen():
        yield mock_session

    return FoodIntoleranceRepository(session=session_gen)


@pytest.fixture
def intolerance_mock():
    return FoodIntolerance(id=1, name="Milk", description="Milk intolerance")


@pytest.mark.asyncio
async def test_init():
    mock_session_test = MagicMock()
    allergy_repo = FoodIntoleranceRepository(mock_session_test)
    assert allergy_repo.session == mock_session_test


@pytest.mark.asyncio
async def test_get_intolerance_success(
    intolerance_repository, mock_session, intolerance_mock
):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = intolerance_mock
    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    result = await intolerance_repository.get(1)

    assert result.id == 1
    assert result.name == "Milk"
    assert result.description == "Milk intolerance"
    mock_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_intolerance_success(
    intolerance_repository, mock_session, intolerance_mock
):
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    new_intolerance = intolerance_mock

    result = await intolerance_repository.create(new_intolerance)

    assert result.name == "Milk"
    assert result.description == "Milk intolerance"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_intolerance_success(
    intolerance_repository, mock_session, intolerance_mock
):
    existing_intolerance = intolerance_mock

    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = existing_intolerance
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.commit = AsyncMock()
    mock_session.refresh = AsyncMock()

    updated_intolerance= FoodIntolerance(
        id=1, name="Grain", description="Grain intolerance"
    )

    result = await intolerance_repository.update(updated_intolerance)

    assert result.name == "Grain"
    assert result.description == "Grain intolerance"
    mock_session.exec.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_intolerance_not_found(intolerance_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_exec_result.first.return_value = None
    mock_session.exec = AsyncMock(return_value=mock_exec_result)

    non_existent_intolerance = FoodIntolerance(
        id=999, name="Grain", description="Grain intolerance"
    )

    with pytest.raises(Exception) as exc_info:
        await intolerance_repository.update(non_existent_intolerance)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Food Intolerance not found"
    mock_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_intolerance_success(intolerance_repository, mock_session):
    mock_exec_result = MagicMock()
    mock_session.exec = AsyncMock(return_value=mock_exec_result)
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    await intolerance_repository.delete(1)

    mock_session.exec.assert_awaited_once()
    mock_session.delete.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
