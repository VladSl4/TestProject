"""Translation between domain LogAnalysis and proto RpcLogAnalysis."""

from __future__ import annotations

from datetime import timezone

from google.protobuf.timestamp_pb2 import Timestamp

import database_analyses_pb2 as pb

from database_service.models.log_analysis import LogAnalysis
from database_service.models.log_category import LogCategory


def _datetime_to_timestamp(value) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(value.astimezone(timezone.utc).replace(tzinfo=None))
    return ts


def analysis_to_proto(analysis: LogAnalysis) -> "pb.RpcLogAnalysis":
    return pb.RpcLogAnalysis(
        id=analysis.id or 0,
        raw_logs=analysis.raw_logs,
        summary=analysis.summary,
        category=int(analysis.category),
        recommended_action=analysis.recommended_action,
        created_at=_datetime_to_timestamp(analysis.created_at),
    )


def category_from_proto(value: int) -> LogCategory:
    return LogCategory(value)
