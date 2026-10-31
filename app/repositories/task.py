from collections.abc import Sequence
from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task, TaskPriority, TaskStatus


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        project_id: UUID,
        title: str,
        created_by_id: UUID,
        status: TaskStatus = TaskStatus.TODO,
        priority: TaskPriority = TaskPriority.MEDIUM,
        description: str | None = None,
        assigned_to_id: UUID | None = None,
        due_date: date | None = None,
    ) -> Task:
        new_task = Task(
            project_id=project_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            created_by_id=created_by_id,
            assigned_to_id=assigned_to_id,
            due_date=due_date,
        )
        self.db.add(new_task)
        self.db.flush()

        return new_task

    def get_by_id(self, task_id: UUID) -> Task | None:
        query = select(Task).where(Task.id == task_id)
        result = self.db.execute(query)
        return result.scalar_one_or_none()

    def get_all_by_project(self, project_id: UUID) -> Sequence[Task]:
        query = (
            select(Task)
            .where(Task.project_id == project_id)
            .order_by(Task.created_at.asc(), Task.id.asc())
        )
        result = self.db.execute(query)
        return result.scalars().all()
