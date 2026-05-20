"""Translation between public REST DTOs and proxy-tier proto messages."""

from __future__ import annotations

from datetime import datetime, timezone

import proxy_tasks_pb2 as proxy_pb

from gateway.models.task_dtos import TaskResponse, VibeStatusDto


_PROTO_TO_DTO: dict[int, VibeStatusDto] = {
    proxy_pb.PENDING: VibeStatusDto.PENDING,
    proxy_pb.IN_PROGRESS: VibeStatusDto.IN_PROGRESS,
    proxy_pb.GROOVY: VibeStatusDto.GROOVY,
}

_DTO_TO_PROTO: dict[VibeStatusDto, int] = {v: k for k, v in _PROTO_TO_DTO.items()}


def status_dto_to_proto(status: VibeStatusDto) -> int:
    return _DTO_TO_PROTO[status]


def proto_task_to_response(task: proxy_pb.RpcTask) -> TaskResponse:
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description.value if task.HasField("description") else None,
        status=_PROTO_TO_DTO.get(task.status, VibeStatusDto.PENDING),
        mood_emoji=task.mood_emoji.value if task.HasField("mood_emoji") else None,
        created_at=(
            task.created_at.ToDatetime().replace(tzinfo=timezone.utc)
            if task.HasField("created_at")
            else datetime.now(timezone.utc)
        ),
    )
