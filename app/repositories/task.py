from collections.abc import Sequence
from datetime import date
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ResourceDoesNotExistException
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

    def update(
        self,
        task_id: UUID,
        *,
        title: str | None = None,
        description: str | None = None,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        assigned_to_id: UUID | None = None,
        due_date: date | None = None,
    ) -> Task:
        task = self.get_by_id(task_id=task_id)
        if task is None:
            raise ResourceDoesNotExistException("Task does not exist.")
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if assigned_to_id is not None:
            task.assigned_to_id = assigned_to_id
        if due_date is not None:
            task.due_date = due_date
        self.db.flush()

        return task

    def delete(self, task_id: UUID) -> None:
        task = self.get_by_id(task_id=task_id)
        if task is None:
            raise ResourceDoesNotExistException("Task does not exist.")

        self.db.delete(task)
        self.db.flush()
