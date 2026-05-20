"""Translation between proxy-tier proto messages and public REST DTOs."""

from __future__ import annotations

from datetime import datetime, timezone

import proxy_analyses_pb2 as proxy_pb

from gateway.models.analysis_dtos import AnalysisHistoryItem, LogCategoryDto


_PROTO_TO_DTO: dict[int, LogCategoryDto] = {
    proxy_pb.INFO: LogCategoryDto.INFO,
    proxy_pb.WARNING: LogCategoryDto.WARNING,
    proxy_pb.ERROR: LogCategoryDto.ERROR,
}

_DTO_TO_PROTO: dict[LogCategoryDto, int] = {v: k for k, v in _PROTO_TO_DTO.items()}


def category_dto_to_proto(category: LogCategoryDto) -> int:
    return _DTO_TO_PROTO[category]


def category_proto_to_dto(value: int) -> LogCategoryDto:
    return _PROTO_TO_DTO.get(value, LogCategoryDto.INFO)


def proto_to_history_item(analysis: proxy_pb.RpcLogAnalysis) -> AnalysisHistoryItem:
    return AnalysisHistoryItem(
        id=analysis.id,
        raw_logs=analysis.raw_logs,
        summary=analysis.summary,
        category=category_proto_to_dto(analysis.category),
        recommended_action=analysis.recommended_action,
        created_at=(
            analysis.created_at.ToDatetime().replace(tzinfo=timezone.utc)
            if analysis.HasField("created_at")
            else datetime.now(timezone.utc)
        ),
    )
