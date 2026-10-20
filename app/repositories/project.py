from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Project


class ProjectRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, name: str) -> Project:
        new_project = Project(name=name)
        self.db.add(new_project)
        self.db.flush()
        return new_project

    def get_by_id(self, project_id: UUID) -> Project | None:
        query = select(Project).where(Project.id == project_id)
        result = self.db.execute(query)
        return result.scalar_one_or_none()
