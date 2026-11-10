from app.models.project_member import ProjectRole
from app.repositories import ProjectMemberRepository, UserRepository
from app.services.project import ProjectService


def test_create_project_and_assign_owner(session):
    user_repo = UserRepository(session)

    user = user_repo.create(
        email="a@test.com",
        password_hash="test_password_hash",
        first_name="Test1",
        last_name="Test2",
    )
    project_service = ProjectService(session)
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
