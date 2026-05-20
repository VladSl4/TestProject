from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    service_name: str = "database_service"
    host: str = os.getenv("DATABASE_SERVICE_HOST", "0.0.0.0")
    port: int = int(os.getenv("DATABASE_SERVICE_PORT", "5001"))
    db_path: str = os.getenv(
        "DATABASE_SERVICE_DB_PATH",
        str(Path(__file__).resolve().parent.parent / "vibelog.db"),
    )


settings = Settings()
