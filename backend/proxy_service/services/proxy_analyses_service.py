"""Mid-tier business service.

`analyze` is the public entry point: it asks the analyzer for an insight
and persists the resulting record through the database service. The
remaining methods are thin pass-throughs to the database tier.
"""

from __future__ import annotations

from google.protobuf import empty_pb2

import database_analyses_pb2 as db_pb

from proxy_service.interfaces.analyzer_service import AbstractAnalyzerService
from proxy_service.interfaces.proxy_analyses_service import (
    AbstractProxyAnalysesService,
)


class ProxyAnalysesService(AbstractProxyAnalysesService):
    def __init__(
        self,
        database_client,
        analyzer: AbstractAnalyzerService,
    ) -> None:
        self._db = database_client
        self._analyzer = analyzer

    def analyze(self, raw_logs: str) -> db_pb.RpcLogAnalysis:
        insight = self._analyzer.analyze(raw_logs)
        request = db_pb.RpcSaveAnalysisRequest(
            raw_logs=raw_logs,
            summary=insight.summary,
            category=insight.category,
            recommended_action=insight.recommended_action,
        )
        return self._db.SaveAnalysis(request)

    def list_analyses(self) -> list[db_pb.RpcLogAnalysis]:
        return list(self._db.ListAnalyses(empty_pb2.Empty()).analyses)

    def get_analysis(self, analysis_id: int) -> db_pb.RpcLogAnalysis:
        return self._db.GetAnalysis(db_pb.RpcAnalysisId(id=analysis_id))

    def delete_analysis(self, analysis_id: int) -> bool:
        return self._db.DeleteAnalysis(db_pb.RpcAnalysisId(id=analysis_id)).deleted
