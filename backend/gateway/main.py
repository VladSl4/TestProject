"""Entry point for the gateway service.

Run from ``backend/``::

    python -m gateway.main
"""

from __future__ import annotations

import sys
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
_GENERATED = _BACKEND_ROOT / "rpc" / "generated" / "proxy_service"
if str(_GENERATED) not in sys.path:
    sys.path.insert(0, str(_GENERATED))

from fastapi import FastAPI  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402

from gateway.config import settings  # noqa: E402
from gateway.controllers.analyses_controller import router as analyses_router  # noqa: E402


def create_app() -> FastAPI:
    app = FastAPI(title="VibeLog – Gateway", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(analyses_router)

    @app.get("/health", tags=["health"])
    def health() -> dict:
        return {
            "status": "ok",
            "service": settings.service_name,
            "proxy_address": settings.proxy_service_address,
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "gateway.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )
