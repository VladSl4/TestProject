from __future__ import annotations

from datetime import datetime

from database_service.interfaces.analyses_repository import AbstractAnalysesRepository
from database_service.models.log_analysis import LogAnalysis
from database_service.models.log_category import LogCategory
from database_service.repositories.database_context import DatabaseContext


class AnalysesRepository(AbstractAnalysesRepository):
    def __init__(self, db_context: DatabaseContext) -> None:
        self._db = db_context

    @staticmethod
    def _row_to_analysis(row) -> LogAnalysis:
        return LogAnalysis(
            id=row["id"],
            raw_logs=row["raw_logs"],
            summary=row["summary"],
            category=LogCategory(row["category"]),
            recommended_action=row["recommended_action"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def get_all(self) -> list[LogAnalysis]:
        with self._db.connection() as conn:
            rows = conn.execute(
                "SELECT id, raw_logs, summary, category, recommended_action, created_at "
                "FROM analyses ORDER BY id DESC"
            ).fetchall()
            return [self._row_to_analysis(r) for r in rows]

    def get_by_id(self, analysis_id: int) -> LogAnalysis | None:
        with self._db.connection() as conn:
            row = conn.execute(
                "SELECT id, raw_logs, summary, category, recommended_action, created_at "
                "FROM analyses WHERE id = ?",
                (analysis_id,),
            ).fetchone()
            return self._row_to_analysis(row) if row else None

    def add(self, analysis: LogAnalysis) -> LogAnalysis:
        with self._db.connection() as conn:
            cur = conn.execute(
                "INSERT INTO analyses (raw_logs, summary, category, recommended_action, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    analysis.raw_logs,
                    analysis.summary,
                    int(analysis.category),
                    analysis.recommended_action,
                    analysis.created_at.isoformat(),
                ),
            )
            conn.commit()
            analysis.id = cur.lastrowid
            return analysis

    def delete(self, analysis_id: int) -> bool:
        with self._db.connection() as conn:
            cur = conn.execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
            conn.commit()
            return cur.rowcount > 0
