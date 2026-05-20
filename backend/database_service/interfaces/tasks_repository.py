from __future__ import annotations

from abc import ABC, abstractmethod

from database_service.models.vibe_task import VibeTask


class AbstractTasksRepository(ABC):
    """Persistence boundary for vibe tasks."""

    @abstractmethod
    def get_all(self) -> list[VibeTask]:
        ...

    @abstractmethod
    def get_by_id(self, task_id: int) -> VibeTask | None:
        ...

    @abstractmethod
    def add(self, task: VibeTask) -> VibeTask:
        ...

    @abstractmethod
    def update(self, task: VibeTask) -> VibeTask | None:
        ...

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        ...
