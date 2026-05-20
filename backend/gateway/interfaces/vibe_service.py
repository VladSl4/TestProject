from __future__ import annotations

from abc import ABC, abstractmethod

from gateway.models.task_dtos import VibeCheckResponse


class AbstractVibeService(ABC):
    @abstractmethod
    def vibe_check(self, task_id: int) -> VibeCheckResponse | None:
        ...
