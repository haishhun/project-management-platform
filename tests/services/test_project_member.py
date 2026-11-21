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
    assert membership.role is ProjectRole.MEMBER

    saved_membership = ProjectMemberRepository(session).get_by_project_and_member(
        project_id=project.id,
        user_id=user.id,
    )
    assert saved_membership is not None
