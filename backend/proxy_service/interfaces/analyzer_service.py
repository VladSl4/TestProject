from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisInsight:
    """Result of one analyzer run — domain object inside proxy_service."""

    summary: str
    category: int  # matches the proto LogCategory enum tag
    recommended_action: str


class AbstractAnalyzerService(ABC):
    """Turns raw log text into a structured insight."""

    @abstractmethod
    def analyze(self, raw_logs: str) -> AnalysisInsight:
        ...
