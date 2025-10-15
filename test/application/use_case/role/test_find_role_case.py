"""
@file test_find_role_case.py
@brief Unit tests for FindRoleCase.
@details This file contains tests for the FindRoleCase class, verifying correct behavior for role retrieval by ID, name, and listing all roles.
"""

import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException, status
from src.application.use_case.role.find_role_case import FindRoleCase
from src.domain.objects.role.role_dto import RoleDTO

@pytest.fixture
def role_repo():
    """
    @brief Fixture that creates a mock RoleRepository.
    @return AsyncMock instance of RoleRepository.
    """
    repo = AsyncMock()
    return repo

@pytest.fixture
def find_role_case(role_repo):
    """
    @brief Fixture that instantiates FindRoleCase with the mocked RoleRepository.
    @param role_repo Mocked RoleRepository.
    @return Instance of FindRoleCase.
    """
    return FindRoleCase(role_repo)

@pytest.mark.asyncio
async def test_get_all_roles(find_role_case, role_repo):
    """
    @brief Verifies that get_all returns all roles from the repository.
    @param find_role_case Instance of FindRoleCase.
    @param role_repo Mocked RoleRepository.
    """
    mock_roles = [RoleDTO(role_id=1, role_name="Admin"), RoleDTO(role_id=2, role_name="User")]
    role_repo.get_roles.return_value = mock_roles

    result = await find_role_case.get_all()
    assert result == mock_roles
    role_repo.get_roles.assert_awaited_once()

@pytest.mark.asyncio
async def test_find_by_id_success(find_role_case, role_repo):
    """
    @brief Verifies that find_by_id returns the correct role when found.
    @param find_role_case Instance of FindRoleCase.
    @param role_repo Mocked RoleRepository.
    """
    role_repo.find_role.return_value = RoleDTO(role_id=1, role_name="Admin")

    result = await find_role_case.find_by_id(1)
    assert result.role_id == 1
    assert result.role_name == "Admin"
    role_repo.find_role.assert_awaited_once_with(1)

@pytest.mark.asyncio
async def test_find_by_id_not_found(find_role_case, role_repo):
    """
    @brief Verifies that find_by_id raises HTTPException when the role is not found.
    @param find_role_case Instance of FindRoleCase.
    @param role_repo Mocked RoleRepository.
    """
    role_repo.find_role.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await find_role_case.find_by_id(1)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail["message"] == "Role not found"

@pytest.mark.asyncio
async def test_find_by_name_success(find_role_case, role_repo):
    """
    @brief Verifies that find_by_name returns the correct role when found.
    @param find_role_case Instance of FindRoleCase.
    @param role_repo Mocked RoleRepository.
    """
    role_repo.find_role_by_name.return_value = RoleDTO(role_id=1, role_name="Admin")

    result = await find_role_case.find_by_name("Admin")
    assert result.role_name == "Admin"
    role_repo.find_role_by_name.assert_awaited_once_with("Admin")

@pytest.mark.asyncio
async def test_find_by_name_not_found(find_role_case, role_repo):
    """
    @brief Verifies that find_by_name raises HTTPException when the role is not found.
    @param find_role_case Instance of FindRoleCase.
    @param role_repo Mocked RoleRepository.
    """
    role_repo.find_role_by_name.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await find_role_case.find_by_name("Admin")
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail["message"] == "Role not found"
