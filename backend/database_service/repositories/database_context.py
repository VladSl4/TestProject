"""SQLite connection factory and schema initializer."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager


class DatabaseContext:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def initialize(self) -> None:
        with self.connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS analyses (
                    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                    raw_logs           TEXT    NOT NULL,
                    summary            TEXT    NOT NULL,
                    category           INTEGER NOT NULL,
                    recommended_action TEXT    NOT NULL,
                    created_at         TEXT    NOT NULL
                )
                """
            )
            conn.commit()

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
