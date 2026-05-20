from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractProxyAnalysesService(ABC):
    """Mid-tier contract.

    Returns proto messages because both inbound and outbound hops on this
    tier are gRPC. ``analyze`` is the public entry point — it runs the
    analyzer and persists the result in a single hop.
    """

    @abstractmethod
    def analyze(self, raw_logs: str):
        ...

    @abstractmethod
    def list_analyses(self) -> list:
        ...

    @abstractmethod
    def get_analysis(self, analysis_id: int):
        ...

    @abstractmethod
    def delete_analysis(self, analysis_id: int) -> bool:
        ...
