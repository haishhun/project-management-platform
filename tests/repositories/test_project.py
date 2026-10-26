from app.repositories import ProjectRepository


def test_create_project_and_get_by_id(session):
    repo = ProjectRepository(session)

    project = repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )

    result = repo.get_by_id(project.id)

    assert result is not None
    assert result.id == project.id
    assert result.name == "Test Project 1"
    assert result.description == "Test Description 1"


def test_create_and_get_all(session):
    repo = ProjectRepository(session)
    project1 = repo.create(name="Test Project 1", description="Test Description 1")
    project2 = repo.create(name="Test Project 2", description="Test Description 2")
    project3 = repo.create(name="Test Project 3", description="Test Description 3")
    projects = repo.get_all()
    assert len(projects) == 3
    assert [p.id for p in projects] == [
        project1.id,
        project2.id,
        project3.id,
    ]
    assert [p.name for p in projects] == [
        project1.name,
        project2.name,
        project3.name,
    ]
    assert [p.description for p in projects] == [
        project1.description,
        project2.description,
        project3.description,
    ]


def test_get_all_empty(session):
    repo = ProjectRepository(session)
    assert repo.get_all() == []


def test_update(session):
    repo = ProjectRepository(session)

    project = repo.create(name="Test Project 1", description="Test Description 1")

    repo.update(
        project_id=project.id,
        name="Updated Test Project 1",
        description="Updated Test Description 1",
    )

    updated_project = repo.get_by_id(project.id)

    assert updated_project is not None
    assert updated_project.name == "Updated Test Project 1"
    assert updated_project.description == "Updated Test Description 1"


def test_delete(session):
    repo = ProjectRepository(session)
    project = repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )
    repo.delete(project_id=project.id)
    assert repo.get_by_id(project_id=project.id) is None
