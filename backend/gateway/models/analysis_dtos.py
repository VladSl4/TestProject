"""Pydantic DTOs for the public REST API."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class LogCategoryDto(str, Enum):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"


class AnalyzeRequest(BaseModel):
    raw_logs: str = Field(..., min_length=1, max_length=200_000)


class AnalysisInsight(BaseModel):
    """Result of a single analyzer run (also persisted as history)."""

    id: int | None = None
    summary: str
    category: LogCategoryDto
    recommended_action: str
    created_at: datetime | None = None


class AnalysisHistoryItem(BaseModel):
    id: int
    raw_logs: str
    summary: str
    category: LogCategoryDto
    recommended_action: str
    created_at: datetime
