from uuid import UUID, uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import ForbiddenException, ResourceDoesNotExistException
from app.models import Project
from app.models.project_member import ProjectRole
from app.repositories import ProjectMemberRepository, UserRepository
from app.services.project import ProjectService


def test_create_project_and_assign_owner(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    user = user_repo.create(
        email="a@test.com",
        password_hash="test_password_hash",
        first_name="Test1",
        last_name="Test2",
    )
    project = project_service.create(
        owner_id=user.id,
        name="Backend Platform",
        description="A project management platform",
    )
    membership = ProjectMemberRepository(session).get_by_project_and_member(
        project.id,
        user.id,
    )
    assert project.id is not None
    assert membership is not None
    assert project.name == "Backend Platform"
    assert project.description == "A project management platform"
    assert membership.user_id == user.id
    assert membership.role == ProjectRole.OWNER


def test_create_project_and_transaction_rollback(session):
    project_service = ProjectService(session)

    with pytest.raises(IntegrityError):
        project_service.create(
            owner_id=UUID(int=0),
            name="Project with invalid user",
        )

    project = session.scalar(
        select(Project).where(Project.name == "Project with invalid user")
    )

    assert project is None


def test_get_project_by_id_as_owner(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    user = user_repo.create(
        email="a@test.com",
        password_hash="test_password_hash",
        first_name="Test1",
        last_name="Test2",
    )
    project = project_service.create(
        owner_id=user.id,
        name="Backend Platform",
        description="A project management platform",
    )
    retrieved_project = project_service.get_by_id(
        project_id=project.id, user_id=user.id
    )

    assert retrieved_project.id == project.id
    assert retrieved_project.name == project.name
    assert retrieved_project.description == project.description


def test_get_project_by_id_as_member(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    project_member_repo = ProjectMemberRepository(session)
    user = user_repo.create(
        email="a@test.com",
        password_hash="test_password_hash",
        first_name="Test1",
        last_name="Test2",
    )
    member = user_repo.create(
        email="a2@test.com",
        password_hash="test_password_hash2",
        first_name="Test3",
        last_name="Test4",
    )
    project = project_service.create(
        owner_id=user.id,
        name="Backend Platform",
        description="A project management platform",
    )
    project_member_repo.create(
        project_id=project.id, user_id=member.id, role=ProjectRole.MEMBER
    )
    retrieved_project = project_service.get_by_id(
        project_id=project.id, user_id=member.id
    )

    assert retrieved_project.id == project.id
    assert retrieved_project.name == project.name
    assert retrieved_project.description == project.description


def test_get_project_by_id_as_non_member(session):
    user_repo = UserRepository(session)
    project_service = ProjectService(session)
    user = user_repo.create(
        email="a@test.com",
        password_hash="test_password_hash",
        first_name="Test1",
        last_name="Test2",
    )
    non_member = user_repo.create(
        email="a2@test.com",
        password_hash="test_password_hash2",
        first_name="Test3",
        last_name="Test4",
    )
    project = project_service.create(
        owner_id=user.id,
        name="Backend Platform",
        description="A project management platform",
    )
    with pytest.raises(ForbiddenException):
        project_service.get_by_id(project_id=project.id, user_id=non_member.id)


def test_get_project_by_id_not_found(session):
    project_service = ProjectService(session)

    with pytest.raises(ResourceDoesNotExistException):
        project_service.get_by_id(project_id=uuid4(), user_id=uuid4())


def test_list_by_user_returns_only_memberships(session):
    project_service = ProjectService(session)
    user_repo = UserRepository(session)
    project_member_repo = ProjectMemberRepository(session)
    user1 = user_repo.create(
        email="a@test.com",
        password_hash="test_password_hash",
        first_name="Test1",
        last_name="Test2",
    )
    user2 = user_repo.create(
        email="a2@test.com",
        password_hash="test_password_hash2",
        first_name="Test3",
        last_name="Test4",
    )

    project1 = project_service.create(
        owner_id=user1.id,
        name="Backend Platform",
        description="A project management platform",
    )

    project2 = project_service.create(
        owner_id=user2.id,
        name="2 Backend Platform",
        description="A project management platform",
    )
    project3 = project_service.create(
        owner_id=user2.id,
        name="3 Backend Platform",
        description="A project management platform",
    )

    project_member_repo.create(
        project_id=project2.id,
        user_id=user1.id,
        role=ProjectRole.MEMBER,
    )
    projects = project_service.list_by_user(user_id=user1.id)

    assert len(projects) == 2
    assert {project.id for project in projects} == {
        project1.id,
        project2.id,
    }
    assert project3.id not in {project.id for project in projects}


def test_list_by_user_returns_empty_list(session):
    project_service = ProjectService(session)
    user_repo = UserRepository(session)
    user1 = user_repo.create(
        email="a@test.com",
        password_hash="test_password_hash",
        first_name="Test1",
        last_name="Test2",
    )
    user2 = user_repo.create(
        email="a2@test.com",
        password_hash="test_password_hash2",
        first_name="Test3",
        last_name="Test4",
    )

    project_service.create(
        owner_id=user2.id,
        name="Backend Platform",
        description="A project management platform",
    )

    project_service.create(
        owner_id=user2.id,
        name="2 Backend Platform",
        description="A project management platform",
    )

    projects = project_service.list_by_user(user_id=user1.id)

    assert projects == []
