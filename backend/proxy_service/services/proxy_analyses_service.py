"""Forwards calls to the database service over gRPC.

The natural seam for caching, retry policies, fan-out or authentication.
"""

from __future__ import annotations

from google.protobuf import empty_pb2

import database_analyses_pb2 as db_pb

from proxy_service.interfaces.proxy_analyses_service import (
    AbstractProxyAnalysesService,
)


class ProxyAnalysesService(AbstractProxyAnalysesService):
    def __init__(self, database_client) -> None:
        self._db = database_client

    def list_analyses(self) -> list[db_pb.RpcLogAnalysis]:
        return list(self._db.ListAnalyses(empty_pb2.Empty()).analyses)

    def get_analysis(self, analysis_id: int) -> db_pb.RpcLogAnalysis:
        return self._db.GetAnalysis(db_pb.RpcAnalysisId(id=analysis_id))

    def save_analysis(
        self,
        raw_logs: str,
        summary: str,
        category: int,
        recommended_action: str,
    ) -> db_pb.RpcLogAnalysis:
        request = db_pb.RpcSaveAnalysisRequest(
            raw_logs=raw_logs,
            summary=summary,
            category=category,
            recommended_action=recommended_action,
        )
        return self._db.SaveAnalysis(request)

    def delete_analysis(self, analysis_id: int) -> bool:
        return self._db.DeleteAnalysis(db_pb.RpcAnalysisId(id=analysis_id)).deleted
