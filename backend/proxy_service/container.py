from __future__ import annotations

import grpc

import database_analyses_pb2_grpc as db_pb_grpc

from proxy_service.config import settings
from proxy_service.interfaces.proxy_analyses_service import (
    AbstractProxyAnalysesService,
)
from proxy_service.services.proxy_analyses_service import ProxyAnalysesService


class Container:
    def __init__(self) -> None:
        self.database_channel = grpc.insecure_channel(settings.database_service_address)
        self.database_client = db_pb_grpc.RpcLogsAnalysisServiceStub(
            self.database_channel
        )
        self.analyses_service: AbstractProxyAnalysesService = ProxyAnalysesService(
            self.database_client
        )

    def close(self) -> None:
        self.database_channel.close()


def build_container() -> Container:
    return Container()
