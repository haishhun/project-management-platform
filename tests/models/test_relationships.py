from app.models import Project, ProjectMember, Task, User
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


def test_user_task_relationships(session):
    creator = User(
        first_name="Test1",
        last_name="User1",
        email="test1@test.com",
        password_hash="original_hash1",
    )

    assignee = User(
        first_name="Test2",
        last_name="User2",
        email="test2@test.com",
        password_hash="original_hash2",
    )

    project = Project(name="Test Project")

    task = Task(
        title="Implement authentication",
        project=project,
        created_by=creator,
        assigned_to=assignee,
    )

    session.add_all([creator, assignee, project, task])
    session.flush()

    assert task in creator.created_tasks
    assert task in assignee.assigned_tasks

    assert task.created_by is creator
    assert task.assigned_to is assignee
