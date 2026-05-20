from __future__ import annotations

from abc import ABC, abstractmethod

from database_service.models.vibe_status import VibeStatus
from database_service.models.vibe_task import VibeTask


class AbstractTasksService(ABC):
    """Business operations on vibe tasks."""

    @abstractmethod
    def list_tasks(self) -> list[VibeTask]:
        ...

    @abstractmethod
    def get_task(self, task_id: int) -> VibeTask | None:
        ...

    @abstractmethod
    def create_task(self, title: str, description: str | None) -> VibeTask:
        ...

    @abstractmethod
    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: VibeStatus | None = None,
        mood_emoji: str | None = None,
    ) -> VibeTask | None:
        ...

    @abstractmethod
    def delete_task(self, task_id: int) -> bool:
        ...
