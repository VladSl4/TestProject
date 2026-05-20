"""Generate Python gRPC stubs from .proto files.

Drops generated modules under ``backend/rpc/generated/<service>/``. Every
service adds the relevant subdirectory to ``sys.path`` at startup so the
stubs are importable by their flat module names
(``database_tasks_pb2``, ``proxy_tasks_pb2``, etc.).

Usage (from the repo root)::

    python backend/rpc/gen_protos.py
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

RPC_ROOT = Path(__file__).resolve().parent
PROTOS_ROOT = RPC_ROOT / "protos"
GENERATED_ROOT = RPC_ROOT / "generated"


def _ensure_init_files(directory: Path) -> None:
    init = directory / "__init__.py"
    if not init.exists():
        init.write_text("", encoding="utf-8")


def main() -> int:
    if GENERATED_ROOT.exists():
        shutil.rmtree(GENERATED_ROOT)
    GENERATED_ROOT.mkdir(parents=True, exist_ok=True)
    _ensure_init_files(GENERATED_ROOT)

    proto_files = list(PROTOS_ROOT.rglob("*.proto"))
    if not proto_files:
        print("No .proto files found under", PROTOS_ROOT)
        return 1

    for proto in proto_files:
        service_dir = proto.parent.name  # e.g. database_service
        out_dir = GENERATED_ROOT / service_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        _ensure_init_files(out_dir)

        # Scope --proto_path to the .proto's own folder so the generated
        # stubs use flat module names (database_tasks_pb2) rather than
        # package-prefixed imports that would collide with our service
        # packages of the same name.
        proto_dir_arg = proto.parent.as_posix()
        out_dir_arg = out_dir.as_posix()
        proto_name = proto.name

        cmd = [
            sys.executable,
            "-m",
            "grpc_tools.protoc",
            f"--proto_path={proto_dir_arg}",
            f"--python_out={out_dir_arg}",
            f"--grpc_python_out={out_dir_arg}",
            f"--pyi_out={out_dir_arg}",
            proto_name,
        ]
        print("-->", " ".join(cmd))
        result = subprocess.run(cmd, cwd=str(proto.parent))
        if result.returncode != 0:
            return result.returncode

    print(f"\nStubs generated under {GENERATED_ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
