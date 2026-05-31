from __future__ import annotations

import sqlite3

from report import load_extended_stats


def test_extended_stats_metrics(tmp_path) -> None:
    db = tmp_path / "t.db"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE paper_trades (status TEXT, pnl_pct REAL, pnl_usd REAL, entry_time TEXT, exit_time TEXT)")
        conn.execute("INSERT INTO paper_trades VALUES ('CLOSED', 0.01, 10, '2026-01-01T00:00:00+00:00', '2026-01-01T01:00:00+00:00')")
        conn.execute("INSERT INTO paper_trades VALUES ('CLOSED', -0.005, -5, '2026-01-01T00:00:00+00:00', '2026-01-01T00:30:00+00:00')")

    s = load_extended_stats(str(db))
    assert s.trades == 2
    assert s.profit_factor == 2.0
    assert s.avg_time_minutes == 45.0
