"""Picks a random mood emoji + caption and writes it back to the task."""

from __future__ import annotations

import random

import grpc
from google.protobuf.wrappers_pb2 import StringValue

import proxy_tasks_pb2 as proxy_pb

from gateway.interfaces.vibe_service import AbstractVibeService
from gateway.models.task_dtos import VibeCheckResponse


_MOODS: list[tuple[str, str]] = [
    ("🚀", "Rocket fuel detected — ship it."),
    ("🔥", "Spicy energy. Approach with sunglasses."),
    ("🌊", "Flow-state vibes. Catch the wave."),
    ("🌈", "Wholesome rainbow grooves."),
    ("✨", "Sparkly and full of potential."),
    ("🎯", "Laser focus. The target trembles."),
    ("🧘", "Zen mode. Inhale, deploy, exhale."),
    ("🥁", "Drumroll please — momentum building."),
    ("☕", "Caffeine-dependent vibes."),
    ("🐢", "Slow and steady. Still groovy."),
]


class VibeService(AbstractVibeService):
    def __init__(self, proxy_client) -> None:
        self._proxy = proxy_client

    def vibe_check(self, task_id: int) -> VibeCheckResponse | None:
        try:
            self._proxy.GetTask(proxy_pb.RpcTaskId(id=task_id))
        except grpc.RpcError as err:
            if err.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise

        emoji, message = random.choice(_MOODS)

        patch = proxy_pb.RpcUpdateTaskRequest(id=task_id)
        patch.mood_emoji.CopyFrom(StringValue(value=emoji))
        self._proxy.UpdateTask(patch)

        return VibeCheckResponse(task_id=task_id, mood_emoji=emoji, vibe_message=message)
