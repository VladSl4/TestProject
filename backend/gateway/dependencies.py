"""FastAPI dependency providers (singletons for gRPC channel + services)."""

from __future__ import annotations

from functools import lru_cache

import grpc

import proxy_tasks_pb2_grpc as proxy_pb_grpc

from gateway.config import settings
from gateway.interfaces.vibe_service import AbstractVibeService
from gateway.services.vibe_service import VibeService


@lru_cache(maxsize=1)
def _proxy_channel():
    return grpc.insecure_channel(settings.proxy_service_address)


@lru_cache(maxsize=1)
def get_proxy_client():
    return proxy_pb_grpc.RpcTasksProxyServiceStub(_proxy_channel())


@lru_cache(maxsize=1)
def get_vibe_service() -> AbstractVibeService:
    return VibeService(get_proxy_client())
