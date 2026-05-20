"""Public REST endpoints for vibe tasks."""

from __future__ import annotations

import grpc
from fastapi import APIRouter, Depends, HTTPException, status
from google.protobuf import empty_pb2
from google.protobuf.wrappers_pb2 import StringValue

import proxy_tasks_pb2 as proxy_pb

from gateway.dependencies import get_proxy_client
from gateway.mapping.tasks_mapping import proto_task_to_response, status_dto_to_proto
from gateway.models.task_dtos import CreateTaskRequest, TaskResponse, UpdateTaskRequest

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(proxy=Depends(get_proxy_client)) -> list[TaskResponse]:
    reply = proxy.ListTasks(empty_pb2.Empty())
    return [proto_task_to_response(t) for t in reply.tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, proxy=Depends(get_proxy_client)) -> TaskResponse:
    try:
        task = proxy.GetTask(proxy_pb.RpcTaskId(id=task_id))
    except grpc.RpcError as err:
        if err.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Task not found") from err
        raise
    return proto_task_to_response(task)


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: CreateTaskRequest, proxy=Depends(get_proxy_client)
) -> TaskResponse:
    request = proxy_pb.RpcCreateTaskRequest(title=payload.title)
    if payload.description is not None:
        request.description.CopyFrom(StringValue(value=payload.description))
    return proto_task_to_response(proxy.CreateTask(request))


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, payload: UpdateTaskRequest, proxy=Depends(get_proxy_client)
) -> TaskResponse:
    request = proxy_pb.RpcUpdateTaskRequest(id=task_id)
    if payload.title is not None:
        request.title.CopyFrom(StringValue(value=payload.title))
    if payload.description is not None:
        request.description.CopyFrom(StringValue(value=payload.description))
    if payload.status is not None:
        request.status = status_dto_to_proto(payload.status)
    if payload.mood_emoji is not None:
        request.mood_emoji.CopyFrom(StringValue(value=payload.mood_emoji))
    try:
        updated = proxy.UpdateTask(request)
    except grpc.RpcError as err:
        if err.code() == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="Task not found") from err
        raise
    return proto_task_to_response(updated)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, proxy=Depends(get_proxy_client)) -> None:
    result = proxy.DeleteTask(proxy_pb.RpcTaskId(id=task_id))
    if not result.deleted:
        raise HTTPException(status_code=404, detail="Task not found")
