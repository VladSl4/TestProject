"""Entry point for the database service.

Run from the ``backend/`` directory::

    python -m database_service.main
"""

from __future__ import annotations

import signal
import sys
from concurrent import futures
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_GENERATED = _BACKEND_ROOT / "rpc" / "generated" / "database_service"
if str(_GENERATED) not in sys.path:
    sys.path.insert(0, str(_GENERATED))

import grpc  # noqa: E402

import database_tasks_pb2_grpc as pb_grpc  # noqa: E402

from database_service.config import settings  # noqa: E402
from database_service.container import build_container  # noqa: E402
from database_service.services.grpc.tasks_data_service import TasksDataService  # noqa: E402


def serve() -> None:
    container = build_container()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_RpcTasksDataServiceServicer_to_server(
        TasksDataService(container.tasks_service), server
    )

    address = f"{settings.host}:{settings.port}"
    server.add_insecure_port(address)

    def _stop(_signum, _frame):
        print(f"[{settings.service_name}] stopping…")
        server.stop(grace=2).wait()

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    print(f"[{settings.service_name}] gRPC listening on {address}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
