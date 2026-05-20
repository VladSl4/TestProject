from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    service_name: str = "proxy_service"
    host: str = os.getenv("PROXY_SERVICE_HOST", "0.0.0.0")
    port: int = int(os.getenv("PROXY_SERVICE_PORT", "5002"))
    database_service_address: str = os.getenv(
        "DATABASE_SERVICE_ADDRESS", "127.0.0.1:5001"
    )
    # AI simulation delay (seconds). Override to 0 in tests.
    analyzer_latency_seconds: float = float(
        os.getenv("PROXY_ANALYZER_LATENCY_SECONDS", "1.0")
    )


settings = Settings()
