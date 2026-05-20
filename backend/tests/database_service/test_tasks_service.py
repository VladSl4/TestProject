from database_service.models.vibe_status import VibeStatus
from database_service.repositories.database_context import DatabaseContext
from database_service.repositories.tasks_repository import TasksRepository
from database_service.services.tasks_service import TasksService


def _service(temp_db_path: str) -> TasksService:
    context = DatabaseContext(temp_db_path)
    context.initialize()
    return TasksService(TasksRepository(context))


def test_create_task_starts_in_pending(temp_db_path):
    service = _service(temp_db_path)
    task = service.create_task("Stretch", None)
    assert task.id is not None
    assert task.status == VibeStatus.PENDING
    assert task.mood_emoji is None


def test_update_to_groovy_preserves_other_fields(temp_db_path):
    service = _service(temp_db_path)
    task = service.create_task("Lift", "🏋️")
    updated = service.update_task(task.id, status=VibeStatus.GROOVY)
    assert updated.status == VibeStatus.GROOVY
    assert updated.title == "Lift"
    assert updated.description == "🏋️"


def test_delete_returns_false_for_missing(temp_db_path):
    service = _service(temp_db_path)
    assert service.delete_task(99999) is False
