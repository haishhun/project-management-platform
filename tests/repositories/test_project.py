from app.repositories import ProjectRepository


def test_create_project_and_get_by_id(session):
    repo = ProjectRepository(session)
    project = repo.create(name="Test Project 1", description="Test Description 1")
    assert repo.get_by_id(project.id).name == "Test Project 1"
    assert repo.get_by_id(project.id).description == "Test Description 1"


def test_create_and_get_all(session):
    repo = ProjectRepository(session)
    project1 = repo.create(name="Test Project 1", description="Test Description 1")
    project2 = repo.create(name="Test Project 2", description="Test Description 2")
    project3 = repo.create(name="Test Project 3", description="Test Description 3")
    assert repo.get_all()[0].name == project1.name
    assert repo.get_all()[0].description == project1.description
    assert repo.get_all()[1].name == project2.name
    assert repo.get_all()[1].description == project2.description
    assert repo.get_all()[2].name == project3.name
    assert repo.get_all()[2].description == project3.description


def test_get_all_empty(session):
    repo = ProjectRepository(session)
    assert repo.get_all() == []
