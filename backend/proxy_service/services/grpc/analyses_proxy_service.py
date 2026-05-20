"""gRPC server-side implementation of RpcLogsProxyService."""

from __future__ import annotations

from google.protobuf import empty_pb2

import proxy_analyses_pb2 as proxy_pb
import proxy_analyses_pb2_grpc as proxy_pb_grpc

from proxy_service.interfaces.proxy_analyses_service import (
    AbstractProxyAnalysesService,
)
from proxy_service.mapping.analyses_mapping import database_to_proxy


class AnalysesProxyService(proxy_pb_grpc.RpcLogsProxyServiceServicer):
    def __init__(self, service: AbstractProxyAnalysesService) -> None:
        self._service = service

    def Analyze(
        self, request: proxy_pb.RpcAnalyzeRequest, context
    ) -> proxy_pb.RpcLogAnalysis:
        return database_to_proxy(self._service.analyze(request.raw_logs))

    def ListAnalyses(self, request: empty_pb2.Empty, context) -> proxy_pb.RpcAnalysesList:
        reply = proxy_pb.RpcAnalysesList()
        reply.analyses.extend(
            database_to_proxy(a) for a in self._service.list_analyses()
        )
        return reply

    def GetAnalysis(self, request: proxy_pb.RpcAnalysisId, context) -> proxy_pb.RpcLogAnalysis:
        return database_to_proxy(self._service.get_analysis(request.id))

    def DeleteAnalysis(
        self, request: proxy_pb.RpcAnalysisId, context
    ) -> proxy_pb.RpcDeleteResult:
        return proxy_pb.RpcDeleteResult(
            deleted=self._service.delete_analysis(request.id)
        )
