"""Entry point for the proxy service.

Run from ``backend/``::

    python -m proxy_service.main
"""

from __future__ import annotations

import signal
import sys
from concurrent import futures
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_GENERATED = _BACKEND_ROOT / "rpc" / "generated"
for sub in ("proxy_service", "database_service"):
    path = _GENERATED / sub
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import grpc  # noqa: E402

import proxy_tasks_pb2_grpc as proxy_pb_grpc  # noqa: E402

from proxy_service.config import settings  # noqa: E402
from proxy_service.container import build_container  # noqa: E402
from proxy_service.services.grpc.tasks_proxy_service import TasksProxyService  # noqa: E402


def serve() -> None:
    container = build_container()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    proxy_pb_grpc.add_RpcTasksProxyServiceServicer_to_server(
        TasksProxyService(container.proxy_tasks_service), server
    )

    address = f"{settings.host}:{settings.port}"
    server.add_insecure_port(address)

    def _stop(_signum, _frame):
        print(f"[{settings.service_name}] stopping…")
        server.stop(grace=2).wait()
        container.close()

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    print(f"[{settings.service_name}] gRPC listening on {address}")
    print(f"  upstream database service: {settings.database_service_address}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
