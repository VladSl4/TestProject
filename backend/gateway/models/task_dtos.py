"""Pydantic DTOs for the public REST API."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class VibeStatusDto(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "InProgress"
    GROOVY = "Groovy"


class CreateTaskRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)


class UpdateTaskRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    status: VibeStatusDto | None = None
    mood_emoji: str | None = Field(default=None, max_length=8)


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: VibeStatusDto
    mood_emoji: str | None
    created_at: datetime


class VibeCheckResponse(BaseModel):
    task_id: int
    mood_emoji: str
    vibe_message: str
