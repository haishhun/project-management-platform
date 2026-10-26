from uuid import uuid4

import pytest

from app.core.exceptions import ResourceDoesNotExistException
from app.repositories import ProjectRepository


def test_create_project_without_description(session):
    repo = ProjectRepository(session)

    project = repo.create(name="Project Without Description")

    result = repo.get_by_id(project.id)

    assert result is not None
    assert result.name == "Project Without Description"
    assert result.description is None


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


def test_get_by_id_not_found(session):
    repo = ProjectRepository(session)

    assert repo.get_by_id(uuid4()) is None


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


def test_get_all_with_limit(session):
    repo = ProjectRepository(session)

    for i in range(5):
        repo.create(
            name=f"Project {i}",
            description=f"Description {i}",
        )

    projects = repo.get_all(limit=2)

    assert len(projects) == 2


def test_get_all_with_offset(session):
    repo = ProjectRepository(session)

    for i in range(5):
        repo.create(
            name=f"Project {i}",
            description=f"Description {i}",
        )

    all_projects = repo.get_all()
    projects = repo.get_all(offset=2)

    assert [p.id for p in projects] == [p.id for p in all_projects[2:]]


def test_get_all_with_limit_and_offset(session):
    repo = ProjectRepository(session)

    for i in range(5):
        repo.create(
            name=f"Project {i}",
            description=f"Description {i}",
        )

    all_projects = repo.get_all()
    projects = repo.get_all(limit=2, offset=1)

    assert [p.id for p in projects] == [p.id for p in all_projects[1:3]]


def test_get_all_with_offset_beyond_results(session):
    repo = ProjectRepository(session)

    repo.create(name="Only Project")

    assert repo.get_all(offset=100) == []


def test_get_all_with_zero_limit(session):
    repo = ProjectRepository(session)

    repo.create(name="Project 1")
    repo.create(name="Project 2")

    assert repo.get_all(limit=0) == []


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


def test_update_not_found(session):
    repo = ProjectRepository(session)

    with pytest.raises(ResourceDoesNotExistException, match="Project does not exist."):
        repo.update(
            project_id=uuid4(),
            name="Updated Project",
        )


def test_update_name_only(session):
    repo = ProjectRepository(session)

    project = repo.create(
        name="Original Name",
        description="Original Description",
    )

    repo.update(
        project_id=project.id,
        name="Updated Name",
    )
    result = repo.get_by_id(project.id)

    assert result is not None
    assert result.name == "Updated Name"
    assert result.description == "Original Description"


def test_update_description_only(session):
    repo = ProjectRepository(session)

    project = repo.create(
        name="Original Name",
        description="Original Description",
    )

    repo.update(
        project_id=project.id,
        description="Updated Description",
    )

    result = repo.get_by_id(project.id)

    assert result is not None
    assert result.name == "Original Name"
    assert result.description == "Updated Description"


def test_update_with_none_does_not_change_fields(session):
    repo = ProjectRepository(session)

    project = repo.create(
        name="Original Name",
        description="Original Description",
    )

    repo.update(
        project_id=project.id,
        name=None,
        description=None,
    )

    result = repo.get_by_id(project.id)

    assert result is not None
    assert result.name == "Original Name"
    assert result.description == "Original Description"


def test_delete(session):
    repo = ProjectRepository(session)
    project = repo.create(
        name="Test Project 1",
        description="Test Description 1",
    )
    repo.delete(project_id=project.id)
    assert repo.get_by_id(project_id=project.id) is None


def test_delete_not_found(session):
    repo = ProjectRepository(session)

    with pytest.raises(
        ResourceDoesNotExistException,
        match="Project does not exist.",
    ):
        repo.delete(project_id=uuid4())


def test_delete_does_not_delete_other_projects(session):
    repo = ProjectRepository(session)

    project1 = repo.create(name="Project 1")
    project2 = repo.create(name="Project 2")

    repo.delete(project_id=project1.id)

    assert repo.get_by_id(project1.id) is None

    remaining_project = repo.get_by_id(project2.id)

    assert remaining_project is not None
    assert remaining_project.name == "Project 2"
