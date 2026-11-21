from app.models import ProjectMember
from app.models.project_member import ProjectRole
from app.repositories import ProjectMemberRepository, UserRepository
from app.services.project import ProjectService
from app.services.project_member import ProjectMemberService


def test_add_member_as_owner(db_session):
    owner = UserRepository(db_session).create(
        email="owner@example.com",
        password_hash="hashed_password",
        first_name="Owner",
        last_name="User",
    )
    user = UserRepository(db_session).create(
        email="member@example.com",
        password_hash="hashed_password",
        first_name="Member",
        last_name="User",
    )

    project = ProjectService(db_session).create(
        owner_id=owner.id,
        name="Test Project",
    )

    service = ProjectMemberService(db_session)

    membership = service.add_member(
        project_id=project.id,
        actor_id=owner.id,
        user_id=user.id,
    )

    assert isinstance(membership, ProjectMember)
    assert membership.project_id == project.id
    assert membership.user_id == user.id
    assert membership.role is ProjectRole.MEMBER

    saved_membership = ProjectMemberRepository(db_session).get_by_project_and_member(
        project_id=project.id,
        user_id=user.id,
    )
    assert saved_membership is not None
