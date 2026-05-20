"""gRPC server-side implementation of RpcTasksDataService."""

from __future__ import annotations

import grpc
from google.protobuf import empty_pb2

import database_tasks_pb2 as pb
import database_tasks_pb2_grpc as pb_grpc

from database_service.interfaces.tasks_service import AbstractTasksService
from database_service.mapping.tasks_mapping import status_from_proto, task_to_proto


class TasksDataService(pb_grpc.RpcTasksDataServiceServicer):
    def __init__(self, tasks_service: AbstractTasksService) -> None:
        self._service = tasks_service

    def ListTasks(self, request: empty_pb2.Empty, context) -> "pb.RpcTasksList":
        result = pb.RpcTasksList()
        result.tasks.extend(task_to_proto(t) for t in self._service.list_tasks())
        return result

    def GetTask(self, request: "pb.RpcTaskId", context) -> "pb.RpcTask":
        task = self._service.get_task(request.id)
        if task is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Task {request.id} not found")
        return task_to_proto(task)

    def CreateTask(self, request: "pb.RpcCreateTaskRequest", context) -> "pb.RpcTask":
        description = request.description.value if request.HasField("description") else None
        created = self._service.create_task(request.title, description)
        return task_to_proto(created)

    def UpdateTask(self, request: "pb.RpcUpdateTaskRequest", context) -> "pb.RpcTask":
        title = request.title.value if request.HasField("title") else None
        description = request.description.value if request.HasField("description") else None
        mood_emoji = request.mood_emoji.value if request.HasField("mood_emoji") else None

        updated = self._service.update_task(
            task_id=request.id,
            title=title,
            description=description,
            status=status_from_proto(request.status),
            mood_emoji=mood_emoji,
        )
        if updated is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Task {request.id} not found")
        return task_to_proto(updated)

    def DeleteTask(self, request: "pb.RpcTaskId", context) -> "pb.RpcDeleteResult":
        return pb.RpcDeleteResult(deleted=self._service.delete_task(request.id))
