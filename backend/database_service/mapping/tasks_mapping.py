"""Translation between domain VibeTask and proto RpcTask messages."""

from __future__ import annotations

from datetime import timezone

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.wrappers_pb2 import StringValue

import database_tasks_pb2 as pb

from database_service.models.vibe_status import VibeStatus
from database_service.models.vibe_task import VibeTask


def _datetime_to_timestamp(value) -> Timestamp:
    ts = Timestamp()
    ts.FromDatetime(value.astimezone(timezone.utc).replace(tzinfo=None))
    return ts


def task_to_proto(task: VibeTask) -> "pb.RpcTask":
    message = pb.RpcTask(
        id=task.id or 0,
        title=task.title,
        status=int(task.status),
        created_at=_datetime_to_timestamp(task.created_at),
    )
    if task.description is not None:
        message.description.CopyFrom(StringValue(value=task.description))
    if task.mood_emoji is not None:
        message.mood_emoji.CopyFrom(StringValue(value=task.mood_emoji))
    return message


def status_from_proto(value: int) -> VibeStatus:
    return VibeStatus(value)
