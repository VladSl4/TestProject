"""Forwards calls to the database service over gRPC.

The natural seam for caching, retry policies, fan-out or authentication.
"""

from __future__ import annotations

from google.protobuf import empty_pb2
from google.protobuf.wrappers_pb2 import StringValue

import database_tasks_pb2 as db_pb

from proxy_service.interfaces.proxy_tasks_service import AbstractProxyTasksService


class ProxyTasksService(AbstractProxyTasksService):
    def __init__(self, database_client) -> None:
        # ``database_client`` is an RpcTasksDataServiceStub instance.
        self._db = database_client

    def list_tasks(self) -> list[db_pb.RpcTask]:
        return list(self._db.ListTasks(empty_pb2.Empty()).tasks)

    def get_task(self, task_id: int) -> db_pb.RpcTask:
        return self._db.GetTask(db_pb.RpcTaskId(id=task_id))

    def create_task(self, title: str, description: str | None) -> db_pb.RpcTask:
        request = db_pb.RpcCreateTaskRequest(title=title)
        if description is not None:
            request.description.CopyFrom(StringValue(value=description))
        return self._db.CreateTask(request)

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
        status: int | None = None,
        mood_emoji: str | None = None,
    ) -> db_pb.RpcTask:
        request = db_pb.RpcUpdateTaskRequest(id=task_id, status=status or 0)
        if title is not None:
            request.title.CopyFrom(StringValue(value=title))
        if description is not None:
            request.description.CopyFrom(StringValue(value=description))
        if mood_emoji is not None:
            request.mood_emoji.CopyFrom(StringValue(value=mood_emoji))
        return self._db.UpdateTask(request)

    def delete_task(self, task_id: int) -> bool:
        return self._db.DeleteTask(db_pb.RpcTaskId(id=task_id)).deleted
