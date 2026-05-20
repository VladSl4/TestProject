from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    service_name: str = "gateway"
    host: str = os.getenv("GATEWAY_HOST", "0.0.0.0")
    port: int = int(os.getenv("GATEWAY_PORT", "8000"))
    proxy_service_address: str = os.getenv(
        "PROXY_SERVICE_ADDRESS", "127.0.0.1:5002"
    )
    cors_origins: list[str] = field(
        default_factory=lambda: os.getenv(
            "GATEWAY_CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        ).split(",")
    )


settings = Settings()
