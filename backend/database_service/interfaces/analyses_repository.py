from __future__ import annotations

from abc import ABC, abstractmethod

from database_service.models.log_analysis import LogAnalysis


class AbstractAnalysesRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[LogAnalysis]:
        ...

    @abstractmethod
    def get_by_id(self, analysis_id: int) -> LogAnalysis | None:
        ...

    @abstractmethod
    def add(self, analysis: LogAnalysis) -> LogAnalysis:
        ...

    @abstractmethod
    def delete(self, analysis_id: int) -> bool:
        ...
