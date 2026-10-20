from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Project


class ProjectRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, name: str, description: str | None = None) -> Project:
        new_project = Project(name=name, description=description)
        self.db.add(new_project)
        self.db.flush()
        return new_project

    def get_by_id(self, project_id: UUID) -> Project | None:
        query = select(Project).where(Project.id == project_id)
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def get_all(self, limit: int = 50, offset: int = 0) -> Sequence[Project]:
        query = (
            select(Project)
            .order_by(Project.id)
            .limit(limit=limit)
            .offset(offset=offset)
        )
        result = self.db.execute(query)
        return result.scalars().all()
