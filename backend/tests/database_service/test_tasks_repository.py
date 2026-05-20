from database_service.models.vibe_status import VibeStatus
from database_service.models.vibe_task import VibeTask
from database_service.repositories.database_context import DatabaseContext
from database_service.repositories.tasks_repository import TasksRepository


def _make_task(title: str = "Buy oat milk") -> VibeTask:
    return VibeTask(
        id=None,
        title=title,
        description="for the vibes",
        status=VibeStatus.PENDING,
        mood_emoji=None,
    )


def _repo(temp_db_path: str) -> TasksRepository:
    context = DatabaseContext(temp_db_path)
    context.initialize()
    return TasksRepository(context)


def test_add_assigns_id_and_persists(temp_db_path):
    repo = _repo(temp_db_path)
    saved = repo.add(_make_task())
    assert saved.id is not None
    fetched = repo.get_by_id(saved.id)
    assert fetched is not None
    assert fetched.status == VibeStatus.PENDING


def test_update_changes_status_to_groovy(temp_db_path):
    repo = _repo(temp_db_path)
    saved = repo.add(_make_task())
    saved.status = VibeStatus.GROOVY
    saved.mood_emoji = "🚀"
    repo.update(saved)
    fetched = repo.get_by_id(saved.id)
    assert fetched.status == VibeStatus.GROOVY
    assert fetched.mood_emoji == "🚀"


def test_delete_returns_true_then_false(temp_db_path):
    repo = _repo(temp_db_path)
    saved = repo.add(_make_task())
    assert repo.delete(saved.id) is True
    assert repo.delete(saved.id) is False


def test_get_all_preserves_insertion_order(temp_db_path):
    repo = _repo(temp_db_path)
    first = repo.add(_make_task("first"))
    second = repo.add(_make_task("second"))
    assert [t.id for t in repo.get_all()] == [first.id, second.id]
