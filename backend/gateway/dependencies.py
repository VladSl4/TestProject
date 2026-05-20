"""FastAPI dependency providers (singletons for gRPC channel + services)."""

from __future__ import annotations

from functools import lru_cache

import grpc

import proxy_analyses_pb2_grpc as proxy_pb_grpc

from gateway.config import settings
from gateway.interfaces.analyzer_service import AbstractAnalyzerService
from gateway.services.analyzer_service import AnalyzerService


@lru_cache(maxsize=1)
def _proxy_channel():
    return grpc.insecure_channel(settings.proxy_service_address)


@lru_cache(maxsize=1)
def get_proxy_client():
    return proxy_pb_grpc.RpcLogsProxyServiceStub(_proxy_channel())


@lru_cache(maxsize=1)
def get_analyzer_service() -> AbstractAnalyzerService:
    return AnalyzerService(latency_seconds=settings.analyzer_latency_seconds)
