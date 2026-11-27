from uuid import uuid4

import pytest

from app.core.exceptions import (
    ConflictException,
    ForbiddenException,
    ResourceDoesNotExistException,
)
from app.models import ProjectMember
from app.models.project_member import ProjectRole
from app.repositories import ProjectMemberRepository, UserRepository
from app.services.project import ProjectService
from app.services.project_member import ProjectMemberService


def test_add_member_as_owner(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    project_member_service = ProjectMemberService(session)
    owner = user_repo.create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    user = user_repo.create(
        email="member@example.com",
        password_hash="hashed_password",
        first_name="Member",
        last_name="User",
    )

    project = project_service.create(
        owner_id=owner.id,
        name="Test Project",
    )

    membership = project_member_service.add_member(
        project_id=project.id,
        actor_id=owner.id,
        user_id=user.id,
    )

    assert isinstance(membership, ProjectMember)
    assert membership.project_id == project.id
    assert membership.user_id == user.id
    assert membership.role == ProjectRole.MEMBER

    saved_membership = ProjectMemberRepository(session).get_by_project_and_member(
        project_id=project.id,
        user_id=user.id,
    )
    assert saved_membership is not None


def test_add_member_as_regular_member(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    project_member_service = ProjectMemberService(session)
    owner = user_repo.create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    user1 = user_repo.create(
        email="member@example.com",
        password_hash="hashed_password",
        first_name="Member",
        last_name="User",
    )
    user2 = user_repo.create(
        email="member2@example.com",
        password_hash="hashed_password2",
        first_name="Member2",
        last_name="User2",
    )

    project = project_service.create(
        owner_id=owner.id,
        name="Test Project",
    )
    project_member_service.add_member(
        project_id=project.id,
        actor_id=owner.id,
        user_id=user1.id,
    )
    with pytest.raises(ForbiddenException):
        project_member_service.add_member(
            project_id=project.id, actor_id=user1.id, user_id=user2.id
        )

    membership = project_member_service.project_member_repo.get_by_project_and_member(
        project_id=project.id,
        user_id=user2.id,
    )
    assert membership is None


def test_add_member_as_non_member(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    project_member_service = ProjectMemberService(session)

    owner = user_repo.create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    actor = user_repo.create(
        email="outsider@example.com",
        password_hash="hashed_password",
        first_name="Outsider",
        last_name="User",
    )
    target = user_repo.create(
        email="target@example.com",
        password_hash="hashed_password",
        first_name="Target",
        last_name="User",
    )

    project = project_service.create(
        owner_id=owner.id,
        name="Test Project",
    )

    with pytest.raises(ForbiddenException):
        project_member_service.add_member(
            project_id=project.id,
            actor_id=actor.id,
            user_id=target.id,
        )

    membership = project_member_service.project_member_repo.get_by_project_and_member(
        project_id=project.id,
        user_id=target.id,
    )
    assert membership is None


def test_add_member_project_not_found(session):
    user_repo = UserRepository(session)
    project_member_service = ProjectMemberService(session)

    owner = user_repo.create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    target = user_repo.create(
        email="target@example.com",
        password_hash="hashed_password",
        first_name="Target",
        last_name="User",
    )
    with pytest.raises(ResourceDoesNotExistException):
        project_member_service.add_member(
            project_id=uuid4(),
            actor_id=owner.id,
            user_id=target.id,
        )


def test_add_member_user_not_found(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    project_member_service = ProjectMemberService(session)

    owner = user_repo.create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    project = project_service.create(
        owner_id=owner.id,
        name="Test Project",
    )
    with pytest.raises(ResourceDoesNotExistException):
        project_member_service.add_member(
            project_id=project.id,
            actor_id=owner.id,
            user_id=uuid4(),
        )


def test_add_member_already_exists(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    project_member_service = ProjectMemberService(session)

    owner = user_repo.create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    target = user_repo.create(
        email="target@example.com",
        password_hash="hashed_password",
        first_name="Target",
        last_name="User",
    )
    project = project_service.create(
        owner_id=owner.id,
        name="Test Project",
    )
    project_member_service.add_member(
        project_id=project.id,
        actor_id=owner.id,
        user_id=target.id,
    )
    with pytest.raises(ConflictException):
        project_member_service.add_member(
            project_id=project.id,
            actor_id=owner.id,
            user_id=target.id,
        )


def test_remove_member_as_owner(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    project_member_service = ProjectMemberService(session)

    owner = user_repo.create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    target = user_repo.create(
        email="target@example.com",
        password_hash="hashed_password",
        first_name="Target",
        last_name="User",
    )
    project = project_service.create(
        owner_id=owner.id,
        name="Test Project",
    )
    membership = project_member_service.add_member(
        project_id=project.id,
        actor_id=owner.id,
        user_id=target.id,
    )
    assert membership is not None

    project_member_service.remove_member(
        project_id=project.id,
        actor_id=owner.id,
        user_id=target.id,
    )

    deleted = ProjectMemberRepository(session).get_by_project_and_member(
        project_id=project.id,
        user_id=target.id,
    )
    assert deleted is None


def test_remove_member_as_member(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    project_member_service = ProjectMemberService(session)

    owner = user_repo.create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    member = user_repo.create(
        email="member@example.com",
        password_hash="hashed_password1",
        first_name="Member",
        last_name="User",
    )
    target = user_repo.create(
        email="target@example.com",
        password_hash="hashed_password",
        first_name="Target",
        last_name="User",
    )
    project = project_service.create(
        owner_id=owner.id,
        name="Test Project",
    )
    project_member_service.add_member(
        project_id=project.id,
        actor_id=owner.id,
        user_id=member.id,
    )
    project_member_service.add_member(
        project_id=project.id,
        actor_id=owner.id,
        user_id=target.id,
    )

    with pytest.raises(ForbiddenException):
        project_member_service.remove_member(
            project_id=project.id,
            actor_id=member.id,
            user_id=target.id,
        )

    still_member = ProjectMemberRepository(session).get_by_project_and_member(
        project_id=project.id,
        user_id=target.id,
    )
    assert still_member is not None


def test_remove_member_as_non_member(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    project_member_service = ProjectMemberService(session)

    owner = user_repo.create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    member = user_repo.create(
        email="member@example.com",
        password_hash="hashed_password1",
        first_name="Member",
        last_name="User",
    )
    non_member = user_repo.create(
        email="non-member@example.com",
        password_hash="hashed_password",
        first_name="NonMember",
        last_name="User",
    )
    project = project_service.create(
        owner_id=owner.id,
        name="Test Project",
    )
    project_member_service.add_member(
        project_id=project.id,
        actor_id=owner.id,
        user_id=member.id,
    )

    with pytest.raises(ResourceDoesNotExistException):
        project_member_service.remove_member(
            project_id=project.id,
            actor_id=non_member.id,
            user_id=member.id,
        )

    still_member = ProjectMemberRepository(session).get_by_project_and_member(
        project_id=project.id,
        user_id=member.id,
    )
    assert still_member is not None


def test_remove_member_owner_self(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    project_member_service = ProjectMemberService(session)

    owner = user_repo.create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    project = project_service.create(
        owner_id=owner.id,
        name="Test Project",
    )

    with pytest.raises(ForbiddenException):
        project_member_service.remove_member(
            project_id=project.id,
            actor_id=owner.id,
            user_id=owner.id,
        )

    still_member = ProjectMemberRepository(session).get_by_project_and_member(
        project_id=project.id,
        user_id=owner.id,
    )
    assert still_member is not None
    assert still_member.role == ProjectRole.OWNER
