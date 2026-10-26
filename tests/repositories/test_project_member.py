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
