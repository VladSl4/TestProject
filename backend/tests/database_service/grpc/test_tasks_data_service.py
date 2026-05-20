"""In-process gRPC servicer tests for RpcTasksDataService."""

from __future__ import annotations

import pytest

try:
    import database_tasks_pb2 as pb
except ModuleNotFoundError:
    pytest.skip(
        "Generated proto stubs missing — run `python backend/rpc/gen_protos.py`",
        allow_module_level=True,
    )

from google.protobuf import empty_pb2

from database_service.repositories.database_context import DatabaseContext
from database_service.repositories.tasks_repository import TasksRepository
from database_service.services.grpc.tasks_data_service import TasksDataService
from database_service.services.tasks_service import TasksService


def _servicer(temp_db_path: str) -> TasksDataService:
    context = DatabaseContext(temp_db_path)
    context.initialize()
    return TasksDataService(TasksService(TasksRepository(context)))


class _StubContext:
    """Minimal stand-in for grpc.ServicerContext."""

    def abort(self, code, details):  # pragma: no cover — only on error paths
        raise RuntimeError(f"aborted: {code} {details}")


def test_create_task_via_grpc_servicer(temp_db_path):
    servicer = _servicer(temp_db_path)
    result = servicer.CreateTask(
        pb.RpcCreateTaskRequest(title="Vibe with the team"),
        _StubContext(),
    )
    assert result.id > 0
    assert result.title == "Vibe with the team"
    assert result.status == pb.PENDING
    assert not result.HasField("mood_emoji")


def test_list_after_create_via_grpc_servicer(temp_db_path):
    servicer = _servicer(temp_db_path)
    servicer.CreateTask(pb.RpcCreateTaskRequest(title="first"), _StubContext())
    servicer.CreateTask(pb.RpcCreateTaskRequest(title="second"), _StubContext())

    reply = servicer.ListTasks(empty_pb2.Empty(), _StubContext())
    assert [t.title for t in reply.tasks] == ["first", "second"]
