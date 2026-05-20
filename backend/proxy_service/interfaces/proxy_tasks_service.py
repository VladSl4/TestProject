from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractProxyTasksService(ABC):
    """Mid-tier contract. Returns proto messages because both the inbound and
    outbound hops on this tier are gRPC."""

    @abstractmethod
    def list_tasks(self) -> list:
        ...

    @abstractmethod
    def get_task(self, task_id: int):
        ...

    @abstractmethod
    def create_task(self, title: str, description: str | None):
        ...

    @abstractmethod
    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: int | None = None,
        mood_emoji: str | None = None,
    ):
        ...

    @abstractmethod
    def delete_task(self, task_id: int) -> bool:
        ...
