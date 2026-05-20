from __future__ import annotations

from database_service.interfaces.tasks_repository import AbstractTasksRepository
from database_service.interfaces.tasks_service import AbstractTasksService
from database_service.models.vibe_status import VibeStatus
from database_service.models.vibe_task import VibeTask


class TasksService(AbstractTasksService):
    def __init__(self, repository: AbstractTasksRepository) -> None:
        self._repo = repository

    def list_tasks(self) -> list[VibeTask]:
        return self._repo.get_all()

    def get_task(self, task_id: int) -> VibeTask | None:
        return self._repo.get_by_id(task_id)

    def create_task(self, title: str, description: str | None) -> VibeTask:
        return self._repo.add(
            VibeTask(
                id=None,
                title=title,
                description=description,
                status=VibeStatus.PENDING,
                mood_emoji=None,
            )
        )

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: VibeStatus | None = None,
        mood_emoji: str | None = None,
    ) -> VibeTask | None:
        existing = self._repo.get_by_id(task_id)
        if existing is None:
            return None
        if title is not None:
            existing.title = title
        if description is not None:
            existing.description = description
        if status is not None and status != VibeStatus.UNSPECIFIED:
            existing.status = status
        if mood_emoji is not None:
            existing.mood_emoji = mood_emoji
        return self._repo.update(existing)

    def delete_task(self, task_id: int) -> bool:
        return self._repo.delete(task_id)
