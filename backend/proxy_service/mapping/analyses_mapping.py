"""Copies a database-tier RpcLogAnalysis into the proxy-tier namespace."""

import database_analyses_pb2 as db_pb
import proxy_analyses_pb2 as proxy_pb


def database_to_proxy(analysis: db_pb.RpcLogAnalysis) -> proxy_pb.RpcLogAnalysis:
    message = proxy_pb.RpcLogAnalysis(
        id=analysis.id,
        raw_logs=analysis.raw_logs,
        summary=analysis.summary,
        category=analysis.category,
        recommended_action=analysis.recommended_action,
    )
    if analysis.HasField("created_at"):
        message.created_at.CopyFrom(analysis.created_at)
    return message
