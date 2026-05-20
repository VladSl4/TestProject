"""Public REST endpoints for the VibeLog dashboard."""

from __future__ import annotations

import grpc
from fastapi import APIRouter, Depends, HTTPException, status
from google.protobuf import empty_pb2

import proxy_analyses_pb2 as proxy_pb

from gateway.dependencies import get_analyzer_service, get_proxy_client
from gateway.interfaces.analyzer_service import AbstractAnalyzerService
from gateway.mapping.analyses_mapping import (
    category_dto_to_proto,
    proto_to_history_item,
)
from gateway.models.analysis_dtos import (
    AnalysisHistoryItem,
    AnalysisInsight,
    AnalyzeRequest,
)

router = APIRouter(prefix="/api", tags=["analyses"])


@router.post("/analyze", response_model=AnalysisInsight)
def analyze(
    payload: AnalyzeRequest,
    analyzer: AbstractAnalyzerService = Depends(get_analyzer_service),
    proxy=Depends(get_proxy_client),
) -> AnalysisInsight:
    insight = analyzer.analyze(payload.raw_logs)

    # Persist the analysis through the proxy -> database pipeline.
    saved = proxy.SaveAnalysis(
        proxy_pb.RpcSaveAnalysisRequest(
            raw_logs=payload.raw_logs,
            summary=insight.summary,
            category=category_dto_to_proto(insight.category),
            recommended_action=insight.recommended_action,
        )
    )

    history_item = proto_to_history_item(saved)
    return AnalysisInsight(
        id=history_item.id,
        summary=history_item.summary,
        category=history_item.category,
        recommended_action=history_item.recommended_action,
        created_at=history_item.created_at,
    )


@router.get("/analyses", response_model=list[AnalysisHistoryItem])
def list_history(proxy=Depends(get_proxy_client)) -> list[AnalysisHistoryItem]:
    reply = proxy.ListAnalyses(empty_pb2.Empty())
    return [proto_to_history_item(item) for item in reply.analyses]


@router.delete("/analyses/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(analysis_id: int, proxy=Depends(get_proxy_client)) -> None:
    try:
        result = proxy.DeleteAnalysis(proxy_pb.RpcAnalysisId(id=analysis_id))
    except grpc.RpcError as err:
        if err.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Analysis not found") from err
        raise
    if not result.deleted:
        raise HTTPException(status_code=404, detail="Analysis not found")
