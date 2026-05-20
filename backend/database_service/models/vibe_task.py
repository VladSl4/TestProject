from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from database_service.models.vibe_status import VibeStatus


@dataclass
class VibeTask:
    id: int | None
    title: str
    description: str | None
    status: VibeStatus
    mood_emoji: str | None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
