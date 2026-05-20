from __future__ import annotations

from abc import ABC, abstractmethod

from database_service.models.log_analysis import LogAnalysis
from database_service.models.log_category import LogCategory


class AbstractAnalysesService(ABC):
    @abstractmethod
    def list_analyses(self) -> list[LogAnalysis]:
        ...

    @abstractmethod
    def get_analysis(self, analysis_id: int) -> LogAnalysis | None:
        ...

    @abstractmethod
    def save_analysis(
        self,
        raw_logs: str,
        summary: str,
        category: LogCategory,
        recommended_action: str,
    ) -> LogAnalysis:
        ...

    @abstractmethod
    def delete_analysis(self, analysis_id: int) -> bool:
        ...
