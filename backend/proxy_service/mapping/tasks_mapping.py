"""Copies a database-tier RpcTask into the proxy-tier RpcTask namespace."""

import database_tasks_pb2 as db_pb
import proxy_tasks_pb2 as proxy_pb


def database_to_proxy(task: db_pb.RpcTask) -> proxy_pb.RpcTask:
    message = proxy_pb.RpcTask(
        id=task.id,
        title=task.title,
        status=task.status,
    )
    if task.HasField("description"):
        message.description.CopyFrom(task.description)
    if task.HasField("mood_emoji"):
        message.mood_emoji.CopyFrom(task.mood_emoji)
    if task.HasField("created_at"):
        message.created_at.CopyFrom(task.created_at)
    return message
