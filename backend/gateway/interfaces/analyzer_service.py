from __future__ import annotations

from abc import ABC, abstractmethod

from gateway.models.analysis_dtos import AnalysisInsight


class AbstractAnalyzerService(ABC):
    """Turns raw log text into a structured insight."""

    @abstractmethod
    def analyze(self, raw_logs: str) -> AnalysisInsight:
        ...
