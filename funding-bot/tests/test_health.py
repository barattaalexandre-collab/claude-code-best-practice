from __future__ import annotations

import sqlite3

from health import from_log_and_db


def test_health_summary_from_log_and_db(tmp_path) -> None:
    log = tmp_path / "run.log"
    log.write_text(
        "Starting new collection cycle\n"
        "GET /x attempt 1/4 failed: ... retrying in 0.5s\n"
        "Cycle 1 had errors\n"
        "Starting new collection cycle\n",
        encoding="utf-8",
    )

    db = tmp_path / "d.db"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE snapshots (oi REAL, price REAL)")
        conn.execute("INSERT INTO snapshots VALUES (1, 100)")
        conn.execute("INSERT INTO snapshots VALUES (0, 100)")

    s = from_log_and_db(str(log), str(db))
    assert s.cycles == 2
    assert s.error_cycles == 1
    assert s.retries == 1
    assert s.snapshots == 2
    assert s.invalid_oi_or_price == 1
