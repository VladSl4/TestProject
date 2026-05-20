from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from gateway.dependencies import get_vibe_service
from gateway.interfaces.vibe_service import AbstractVibeService
from gateway.models.task_dtos import VibeCheckResponse

router = APIRouter(prefix="/api/tasks", tags=["vibe"])


@router.post("/{task_id}/vibe-check", response_model=VibeCheckResponse)
def vibe_check(
    task_id: int, service: AbstractVibeService = Depends(get_vibe_service)
) -> VibeCheckResponse:
    result = service.vibe_check(task_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return result
