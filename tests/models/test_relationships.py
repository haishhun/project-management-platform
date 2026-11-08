from app.models import Project, ProjectMember, User
from app.models.project_member import ProjectRole


def test_user_project_membership_relationships(session):
    user = User(
        first_name="Test",
        last_name="User",
        email="test@test.com",
        password_hash="original_hash",
    )

    project = Project(
        name="Test Project 1",
        description="Test Description 1",
    )

    membership = ProjectMember(
        user=user,
        project=project,
        role=ProjectRole.OWNER,
    )

    session.add_all([user, project, membership])
    session.flush()

    assert membership in user.project_memberships
    assert membership in project.memberships

    assert membership.user is user
    assert membership.project is project
