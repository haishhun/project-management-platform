from datetime import UTC, date, datetime
from uuid import uuid4

from app.models.task import TaskPriority, TaskStatus
from app.repositories import ProjectRepository, TaskRepository, UserRepository


def test_create_task(session):
    task_repo = TaskRepository(session)
    project_repo = ProjectRepository(session)
    user_repo = UserRepository(session)
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
    task = task_repo.create(
        project_id=project.id,
        title="Test Task 1",
        created_by_id=user.id,
        description="Test Description 1",
        assigned_to_id=user.id,
        due_date=date(2027, 11, 1),
    )
    assert task.id is not None
    assert task.project_id == project.id
    assert task.title == "Test Task 1"
    assert task.created_by_id == user.id
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert task.description == "Test Description 1"
    assert task.assigned_to_id == user.id
    assert task.due_date == date(2027, 11, 1)


def test_create_task_with_defaults(session):
    task_repo = TaskRepository(session)
    project_repo = ProjectRepository(session)
    user_repo = UserRepository(session)
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
    task = task_repo.create(
        project_id=project.id,
        title="Test Task 1",
        created_by_id=user.id,
    )
    assert task.id is not None
    assert task.status == TaskStatus.TODO
    assert task.priority == TaskPriority.MEDIUM
    assert task.description is None
    assert task.assigned_to_id is None
    assert task.due_date is None


def test_get_by_id(session):
    task_repo = TaskRepository(session)
    project_repo = ProjectRepository(session)
    user_repo = UserRepository(session)
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
    task = task_repo.create(
        project_id=project.id,
        title="Test Task 1",
        created_by_id=user.id,
    )
    search_result = task_repo.get_by_id(task_id=task.id)

    assert search_result is not None
    assert search_result.id == task.id
    assert search_result.project_id == project.id
    assert search_result.title == task.title
    assert search_result.created_by_id == user.id


def test_get_by_id_not_found(session):
    task_repo = TaskRepository(session)

    search_result = task_repo.get_by_id(uuid4())
    assert search_result is None


def test_all_by_project(session):
    task_repo = TaskRepository(session)
    project_repo = ProjectRepository(session)
    user_repo = UserRepository(session)
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
    task1 = task_repo.create(
        project_id=project.id,
        title="Test Task 1",
        created_by_id=user.id,
    )
    task2 = task_repo.create(
        project_id=project.id,
        title="Test Task 2",
        created_by_id=user.id,
    )
    task1.created_at = datetime(2027, 11, 1, tzinfo=UTC)
    task2.created_at = datetime(2028, 11, 1, tzinfo=UTC)

    session.flush()

    all_tasks = task_repo.get_all_by_project(project_id=project.id)

    assert len(all_tasks) == 2
    assert all_tasks[0].title == "Test Task 1"
    assert all_tasks[1].title == "Test Task 2"


def test_all_by_project_empty(session):
    task_repo = TaskRepository(session)
    project_repo = ProjectRepository(session)
    project = project_repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )
    all_tasks = task_repo.get_all_by_project(project_id=project.id)

    assert all_tasks == []
