from __future__ import annotations

import grpc

import database_analyses_pb2_grpc as db_pb_grpc

from proxy_service.config import settings
from proxy_service.interfaces.analyzer_service import AbstractAnalyzerService
from proxy_service.interfaces.proxy_analyses_service import (
    AbstractProxyAnalysesService,
)
from proxy_service.services.analyzer_service import AnalyzerService
from proxy_service.services.proxy_analyses_service import ProxyAnalysesService


class Container:
    def __init__(self) -> None:
        self.database_channel = grpc.insecure_channel(settings.database_service_address)
        self.database_client = db_pb_grpc.RpcLogsAnalysisServiceStub(
            self.database_channel
        )
        self.analyzer: AbstractAnalyzerService = AnalyzerService(
            latency_seconds=settings.analyzer_latency_seconds
        )
        self.analyses_service: AbstractProxyAnalysesService = ProxyAnalysesService(
            database_client=self.database_client,
            analyzer=self.analyzer,
        )

    def close(self) -> None:
        self.database_channel.close()


def build_container() -> Container:
    return Container()
