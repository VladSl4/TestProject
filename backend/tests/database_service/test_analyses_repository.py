from database_service.models.log_analysis import LogAnalysis
from database_service.models.log_category import LogCategory
from database_service.repositories.analyses_repository import AnalysesRepository
from database_service.repositories.database_context import DatabaseContext


def _repo(temp_db_path: str) -> AnalysesRepository:
    context = DatabaseContext(temp_db_path)
    context.initialize()
    return AnalysesRepository(context)


def _make_analysis(summary: str = "all clear") -> LogAnalysis:
    return LogAnalysis(
        id=None,
        raw_logs="INFO ok",
        summary=summary,
        category=LogCategory.INFO,
        recommended_action="keep monitoring",
    )


def test_add_assigns_id_and_persists(temp_db_path):
    repo = _repo(temp_db_path)
    saved = repo.add(_make_analysis())
    assert saved.id is not None
    fetched = repo.get_by_id(saved.id)
    assert fetched is not None
    assert fetched.category == LogCategory.INFO
    assert fetched.summary == "all clear"


def test_get_all_returns_newest_first(temp_db_path):
    repo = _repo(temp_db_path)
    first = repo.add(_make_analysis("first"))
    second = repo.add(_make_analysis("second"))
    rows = repo.get_all()
    assert [r.id for r in rows] == [second.id, first.id]


def test_delete_returns_true_then_false(temp_db_path):
    repo = _repo(temp_db_path)
    saved = repo.add(_make_analysis())
    assert repo.delete(saved.id) is True
    assert repo.delete(saved.id) is False
