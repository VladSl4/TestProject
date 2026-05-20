from __future__ import annotations

from datetime import datetime

from database_service.interfaces.tasks_repository import AbstractTasksRepository
from database_service.models.vibe_status import VibeStatus
from database_service.models.vibe_task import VibeTask
from database_service.repositories.database_context import DatabaseContext


class TasksRepository(AbstractTasksRepository):
    def __init__(self, db_context: DatabaseContext) -> None:
        self._db = db_context

    @staticmethod
    def _row_to_task(row) -> VibeTask:
        return VibeTask(
            id=row["id"],
            title=row["title"],
            description=row["description"],
            status=VibeStatus(row["status"]),
            mood_emoji=row["mood_emoji"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )

    def get_all(self) -> list[VibeTask]:
        with self._db.connection() as conn:
            rows = conn.execute(
                "SELECT id, title, description, status, mood_emoji, created_at "
                "FROM tasks ORDER BY id ASC"
            ).fetchall()
            return [self._row_to_task(r) for r in rows]

    def get_by_id(self, task_id: int) -> VibeTask | None:
        with self._db.connection() as conn:
            row = conn.execute(
                "SELECT id, title, description, status, mood_emoji, created_at "
                "FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()
            return self._row_to_task(row) if row else None

    def add(self, task: VibeTask) -> VibeTask:
        with self._db.connection() as conn:
            cur = conn.execute(
                "INSERT INTO tasks (title, description, status, mood_emoji, created_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    task.title,
                    task.description,
                    int(task.status),
                    task.mood_emoji,
                    task.created_at.isoformat(),
                ),
            )
            conn.commit()
            task.id = cur.lastrowid
            return task

    def update(self, task: VibeTask) -> VibeTask | None:
        if task.id is None:
            return None
        with self._db.connection() as conn:
            cur = conn.execute(
                "UPDATE tasks SET title = ?, description = ?, status = ?, mood_emoji = ? "
                "WHERE id = ?",
                (
                    task.title,
                    task.description,
                    int(task.status),
                    task.mood_emoji,
                    task.id,
                ),
            )
            conn.commit()
            if cur.rowcount == 0:
                return None
            return task

    def delete(self, task_id: int) -> bool:
        with self._db.connection() as conn:
            cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cur.rowcount > 0
