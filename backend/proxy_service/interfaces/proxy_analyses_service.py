from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractProxyAnalysesService(ABC):
    """Mid-tier contract. Returns proto messages because both inbound and
    outbound hops on this tier are gRPC."""

    @abstractmethod
    def list_analyses(self) -> list:
        ...

    @abstractmethod
    def get_analysis(self, analysis_id: int):
        ...

    @abstractmethod
    def save_analysis(
        self,
        raw_logs: str,
        summary: str,
        category: int,
        recommended_action: str,
    ):
        ...

    @abstractmethod
    def delete_analysis(self, analysis_id: int) -> bool:
        ...
