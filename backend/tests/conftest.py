"""Shared pytest configuration.

Adds the backend root and the generated proto stub directories to
``sys.path`` so service packages and stubs import cleanly when pytest
runs from the repo root or from ``backend/``.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

_GENERATED = _BACKEND_ROOT / "rpc" / "generated"
for sub in ("database_service", "proxy_service"):
    path = _GENERATED / sub
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

import pytest  # noqa: E402


@pytest.fixture
def temp_db_path(tmp_path):
    db_file = tmp_path / "test.db"
    os.environ["DATABASE_SERVICE_DB_PATH"] = str(db_file)
    yield str(db_file)
