from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from database_service.models.log_category import LogCategory


@dataclass
class LogAnalysis:
    id: int | None
    raw_logs: str
    summary: str
    category: LogCategory
    recommended_action: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
