"""gRPC server-side implementation of RpcTasksProxyService."""

from __future__ import annotations

from google.protobuf import empty_pb2

import proxy_tasks_pb2 as proxy_pb
import proxy_tasks_pb2_grpc as proxy_pb_grpc

from proxy_service.interfaces.proxy_tasks_service import AbstractProxyTasksService
from proxy_service.mapping.tasks_mapping import database_to_proxy


class TasksProxyService(proxy_pb_grpc.RpcTasksProxyServiceServicer):
    def __init__(self, service: AbstractProxyTasksService) -> None:
        self._service = service

    def ListTasks(self, request: empty_pb2.Empty, context) -> proxy_pb.RpcTasksList:
        result = proxy_pb.RpcTasksList()
        result.tasks.extend(database_to_proxy(t) for t in self._service.list_tasks())
        return result

    def GetTask(self, request: proxy_pb.RpcTaskId, context) -> proxy_pb.RpcTask:
        return database_to_proxy(self._service.get_task(request.id))

    def CreateTask(
        self, request: proxy_pb.RpcCreateTaskRequest, context
    ) -> proxy_pb.RpcTask:
        description = request.description.value if request.HasField("description") else None
        return database_to_proxy(self._service.create_task(request.title, description))

    def UpdateTask(
        self, request: proxy_pb.RpcUpdateTaskRequest, context
    ) -> proxy_pb.RpcTask:
        title = request.title.value if request.HasField("title") else None
        description = request.description.value if request.HasField("description") else None
        mood_emoji = request.mood_emoji.value if request.HasField("mood_emoji") else None

        return database_to_proxy(
            self._service.update_task(
                task_id=request.id,
                title=title,
                description=description,
                status=request.status,
                mood_emoji=mood_emoji,
            )
        )

    def DeleteTask(self, request: proxy_pb.RpcTaskId, context) -> proxy_pb.RpcDeleteResult:
        return proxy_pb.RpcDeleteResult(deleted=self._service.delete_task(request.id))
