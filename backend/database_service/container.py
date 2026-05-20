"""Composition root: builds the dependency graph for the service."""

from __future__ import annotations

from database_service.config import settings
from database_service.interfaces.tasks_repository import AbstractTasksRepository
from database_service.interfaces.tasks_service import AbstractTasksService
from database_service.repositories.database_context import DatabaseContext
from database_service.repositories.tasks_repository import TasksRepository
from database_service.services.tasks_service import TasksService


class Container:
    def __init__(self) -> None:
        self.db_context: DatabaseContext = DatabaseContext(settings.db_path)
        self.tasks_repository: AbstractTasksRepository = TasksRepository(self.db_context)
        self.tasks_service: AbstractTasksService = TasksService(self.tasks_repository)


def build_container() -> Container:
    container = Container()
    container.db_context.initialize()
    return container
