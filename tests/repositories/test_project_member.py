from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.project_member import ProjectRole
from app.repositories import ProjectRepository, UserRepository
from app.repositories.project_member import ProjectMemberRepository


def test_create_project_membership_owner(session):
    user_repo = UserRepository(session)
    project_repo = ProjectRepository(session)
    project_member_repo = ProjectMemberRepository(session)
    user = user_repo.create(
        first_name="Test",
        last_name="User",
        email="test@test.com",
        password_hash="original_hash",
    )
    project = project_repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )
    project_member = project_member_repo.create(
        project_id=project.id, user_id=user.id, role=ProjectRole.OWNER
    )

    assert project_member.user_id == user.id
    assert project_member.project_id == project.id
    assert project_member.role == ProjectRole.OWNER


def test_get_by_project_and_member(session):
    user_repo = UserRepository(session)
    project_repo = ProjectRepository(session)
    project_member_repo = ProjectMemberRepository(session)

    user = user_repo.create(
        first_name="Test",
        last_name="User",
        email="test@test.com",
        password_hash="original_hash",
    )
    project = project_repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )
    project_member_repo.create(
        project_id=project.id,
        user_id=user.id,
        role=ProjectRole.OWNER,
    )

    search_result = project_member_repo.get_by_project_and_member(
        project_id=project.id,
        user_id=user.id,
    )

    assert search_result is not None
    assert search_result.project_id == project.id
    assert search_result.user_id == user.id
    assert search_result.role == ProjectRole.OWNER


def test_get_by_project_and_member_not_found(session):
    project_member_repo = ProjectMemberRepository(session)

    search_result = project_member_repo.get_by_project_and_member(
        project_id=uuid4(),
        user_id=uuid4(),
    )

    assert search_result is None


def test_create_project_membership_member(session):
    user_repo = UserRepository(session)
    project_repo = ProjectRepository(session)
    project_member_repo = ProjectMemberRepository(session)
    user = user_repo.create(
        first_name="Test",
        last_name="User",
        email="test@test.com",
        password_hash="original_hash",
    )
    project = project_repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )
    project_member = project_member_repo.create(
        project_id=project.id, user_id=user.id, role=ProjectRole.MEMBER
    )

    assert project_member.user_id == user.id
    assert project_member.project_id == project.id
    assert project_member.role == ProjectRole.MEMBER


def test_create_membership_defaults_to_member(session):
    user_repo = UserRepository(session)
    project_repo = ProjectRepository(session)
    project_member_repo = ProjectMemberRepository(session)
    user = user_repo.create(
        first_name="Test",
        last_name="User",
        email="test@test.com",
        password_hash="original_hash",
    )
    project = project_repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )
    project_member = project_member_repo.create(
        project_id=project.id,
        user_id=user.id,
    )

    assert project_member.user_id == user.id
    assert project_member.project_id == project.id
    assert project_member.role == ProjectRole.MEMBER


def test_create_duplicate_membership_raises_integrity_error(session):
    user_repo = UserRepository(session)
    project_repo = ProjectRepository(session)
    project_member_repo = ProjectMemberRepository(session)

    user = user_repo.create(
        first_name="Test",
        last_name="User",
        email="test@test.com",
        password_hash="original_hash",
    )
    project = project_repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )

    project_member_repo.create(
        project_id=project.id,
        user_id=user.id,
    )

    with pytest.raises(IntegrityError):
        project_member_repo.create(
            project_id=project.id,
            user_id=user.id,
        )

    session.rollback()
