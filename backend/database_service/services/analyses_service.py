from __future__ import annotations

from database_service.interfaces.analyses_repository import AbstractAnalysesRepository
from database_service.interfaces.analyses_service import AbstractAnalysesService
from database_service.models.log_analysis import LogAnalysis
from database_service.models.log_category import LogCategory


class AnalysesService(AbstractAnalysesService):
    def __init__(self, repository: AbstractAnalysesRepository) -> None:
        self._repo = repository

    def list_analyses(self) -> list[LogAnalysis]:
        return self._repo.get_all()

    def get_analysis(self, analysis_id: int) -> LogAnalysis | None:
        return self._repo.get_by_id(analysis_id)

    def save_analysis(
        self,
        raw_logs: str,
        summary: str,
        category: LogCategory,
        recommended_action: str,
    ) -> LogAnalysis:
        return self._repo.add(
            LogAnalysis(
                id=None,
                raw_logs=raw_logs,
                summary=summary,
                category=category,
                recommended_action=recommended_action,
            )
        )

    def delete_analysis(self, analysis_id: int) -> bool:
        return self._repo.delete(analysis_id)
