from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ResourceDoesNotExistException
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


def test_get_project_memberships(session):
    user_repo = UserRepository(session)
    project_repo = ProjectRepository(session)
    project_member_repo = ProjectMemberRepository(session)

    user1 = user_repo.create(
        first_name="Test1",
        last_name="User1",
        email="test1@test.com",
        password_hash="original_hash1",
    )
    user2 = user_repo.create(
        first_name="Test2",
        last_name="User2",
        email="test2@test.com",
        password_hash="original_hash2",
    )
    project1 = project_repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )
    project2 = project_repo.create(
        name="Test Project 2",
        description="Test Description 2",
    )
    project_member_repo.create(
        project_id=project1.id,
        user_id=user1.id,
        role=ProjectRole.OWNER,
    )
    project_member_repo.create(
        project_id=project1.id,
        user_id=user2.id,
        role=ProjectRole.MEMBER,
    )
    project_member_repo.create(
        project_id=project2.id,
        user_id=user1.id,
        role=ProjectRole.OWNER,
    )
    project_member_repo.create(
        project_id=project2.id,
        user_id=user2.id,
        role=ProjectRole.MEMBER,
    )
    search_result = project_member_repo.get_project_memberships(project_id=project1.id)

    assert len(search_result) == 2
    assert search_result[0].project_id == project1.id
    assert search_result[0].user_id == user1.id
    assert search_result[1].project_id == project1.id
    assert search_result[1].user_id == user2.id


def test_get_project_memberships_ordered_by_joined_at(session):
    user_repo = UserRepository(session)
    project_repo = ProjectRepository(session)
    project_member_repo = ProjectMemberRepository(session)

    user1 = user_repo.create(
        first_name="Test1",
        last_name="User1",
        email="test1@test.com",
        password_hash="original_hash1",
    )
    user2 = user_repo.create(
        first_name="Test2",
        last_name="User2",
        email="test2@test.com",
        password_hash="original_hash2",
    )
    project1 = project_repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )
    project_member_1 = project_member_repo.create(
        project_id=project1.id,
        user_id=user1.id,
        role=ProjectRole.OWNER,
    )
    project_member_2 = project_member_repo.create(
        project_id=project1.id,
        user_id=user2.id,
        role=ProjectRole.MEMBER,
    )
    project_member_1.joined_at = datetime(2026, 2, 1, tzinfo=UTC)
    project_member_2.joined_at = datetime(2026, 1, 2, tzinfo=UTC)
    session.flush()

    search_result = project_member_repo.get_project_memberships(project_id=project1.id)

    assert len(search_result) == 2
    assert search_result[0].user_id == user2.id
    assert search_result[1].user_id == user1.id
    assert search_result[0].joined_at < search_result[1].joined_at


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


def test_update_project_membership_role(session):
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
        project_id=project.id, user_id=user.id, role=ProjectRole.MEMBER
    )
    updated_member = project_member_repo.update(
        project_id=project.id, user_id=user.id, role=ProjectRole.OWNER
    )

    assert updated_member.role == ProjectRole.OWNER
    assert updated_member.project_id == project.id
    assert updated_member.user_id == user.id


def test_update_project_membership_not_found(session):
    project_member_repo = ProjectMemberRepository(session)

    with pytest.raises(ResourceDoesNotExistException):
        project_member_repo.update(
            project_id=uuid4(), user_id=uuid4(), role=ProjectRole.OWNER
        )


def test_delete_project_membership(session):
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
        project_id=project.id, user_id=user.id, role=ProjectRole.MEMBER
    )
    project_member_repo.delete(project_id=project.id, user_id=user.id)

    search_result = project_member_repo.get_by_project_and_member(
        project_id=project.id, user_id=user.id
    )

    assert search_result is None


def test_delete_project_membership_not_found(session):
    project_member_repo = ProjectMemberRepository(session)

    with pytest.raises(ResourceDoesNotExistException):
        project_member_repo.delete(project_id=uuid4(), user_id=uuid4())
