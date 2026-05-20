"""Public REST endpoints for the VibeLog dashboard.

Pure HTTP-to-gRPC bridge: every endpoint forwards to proxy_service and
returns the mapped response. All analysis logic lives in proxy_service.
"""

from __future__ import annotations

import grpc
from fastapi import APIRouter, Depends, HTTPException, status
from google.protobuf import empty_pb2

import proxy_analyses_pb2 as proxy_pb

from gateway.dependencies import get_proxy_client
from gateway.mapping.analyses_mapping import proto_to_history_item
from gateway.models.analysis_dtos import (
    AnalysisHistoryItem,
    AnalysisInsight,
    AnalyzeRequest,
)

router = APIRouter(prefix="/api", tags=["analyses"])


@router.post("/analyze", response_model=AnalysisInsight)
def analyze(
    payload: AnalyzeRequest,
    proxy=Depends(get_proxy_client),
) -> AnalysisInsight:
    saved = proxy.Analyze(proxy_pb.RpcAnalyzeRequest(raw_logs=payload.raw_logs))
    item = proto_to_history_item(saved)
    return AnalysisInsight(
        id=item.id,
        summary=item.summary,
        category=item.category,
        recommended_action=item.recommended_action,
        created_at=item.created_at,
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
