"""Composition root: outbound gRPC channel + the proxy service."""

from __future__ import annotations

import grpc

import database_tasks_pb2_grpc as db_pb_grpc

from proxy_service.config import settings
from proxy_service.interfaces.proxy_tasks_service import AbstractProxyTasksService
from proxy_service.services.proxy_tasks_service import ProxyTasksService


class Container:
    def __init__(self) -> None:
        self.database_channel = grpc.insecure_channel(settings.database_service_address)
        self.database_client = db_pb_grpc.RpcTasksDataServiceStub(self.database_channel)
        self.proxy_tasks_service: AbstractProxyTasksService = ProxyTasksService(
            self.database_client
        )

    def close(self) -> None:
        self.database_channel.close()


def build_container() -> Container:
    return Container()
