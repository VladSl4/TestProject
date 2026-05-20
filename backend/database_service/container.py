from __future__ import annotations

from database_service.config import settings
from database_service.interfaces.analyses_repository import AbstractAnalysesRepository
from database_service.interfaces.analyses_service import AbstractAnalysesService
from database_service.repositories.analyses_repository import AnalysesRepository
from database_service.repositories.database_context import DatabaseContext
from database_service.services.analyses_service import AnalysesService


class Container:
    def __init__(self) -> None:
        self.db_context: DatabaseContext = DatabaseContext(settings.db_path)
        self.analyses_repository: AbstractAnalysesRepository = AnalysesRepository(
            self.db_context
        )
        self.analyses_service: AbstractAnalysesService = AnalysesService(
            self.analyses_repository
        )


def build_container() -> Container:
    container = Container()
    container.db_context.initialize()
    return container
