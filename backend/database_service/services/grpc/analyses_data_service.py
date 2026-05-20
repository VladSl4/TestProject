"""gRPC server-side implementation of RpcLogsAnalysisService."""

from __future__ import annotations

import grpc
from google.protobuf import empty_pb2

import database_analyses_pb2 as pb
import database_analyses_pb2_grpc as pb_grpc

from database_service.interfaces.analyses_service import AbstractAnalysesService
from database_service.mapping.analyses_mapping import (
    analysis_to_proto,
    category_from_proto,
)


class AnalysesDataService(pb_grpc.RpcLogsAnalysisServiceServicer):
    def __init__(self, analyses_service: AbstractAnalysesService) -> None:
        self._service = analyses_service

    def ListAnalyses(self, request: empty_pb2.Empty, context) -> "pb.RpcAnalysesList":
        reply = pb.RpcAnalysesList()
        reply.analyses.extend(
            analysis_to_proto(a) for a in self._service.list_analyses()
        )
        return reply

    def GetAnalysis(self, request: "pb.RpcAnalysisId", context) -> "pb.RpcLogAnalysis":
        analysis = self._service.get_analysis(request.id)
        if analysis is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Analysis {request.id} not found")
        return analysis_to_proto(analysis)

    def SaveAnalysis(
        self, request: "pb.RpcSaveAnalysisRequest", context
    ) -> "pb.RpcLogAnalysis":
        saved = self._service.save_analysis(
            raw_logs=request.raw_logs,
            summary=request.summary,
            category=category_from_proto(request.category),
            recommended_action=request.recommended_action,
        )
        return analysis_to_proto(saved)

    def DeleteAnalysis(self, request: "pb.RpcAnalysisId", context) -> "pb.RpcDeleteResult":
        return pb.RpcDeleteResult(deleted=self._service.delete_analysis(request.id))
