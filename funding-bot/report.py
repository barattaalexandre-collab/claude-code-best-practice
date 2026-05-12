from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from datetime import datetime

from config import DB_PATH


@dataclass
class ExtendedStats:
    trades: int
    win_rate: float
    avg_pnl_pct: float
    total_pnl_usd: float
    worst_trade: float
    best_trade: float
    profit_factor: float
    expectancy_pct: float
    avg_time_minutes: float


def _parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _build_where(since: str | None, until: str | None) -> tuple[str, list[str]]:
    clauses = ["status = 'CLOSED'"]
    params: list[str] = []
    if since:
        clauses.append("entry_time >= ?")
        params.append(since)
    if until:
        clauses.append("entry_time < ?")
        params.append(until)
    return " AND ".join(clauses), params


def load_extended_stats(db_path: str, since: str | None = None, until: str | None = None) -> ExtendedStats:
    where, params = _build_where(since, until)
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            f"""
            SELECT
              COUNT(*),
              COALESCE(SUM(CASE WHEN pnl_pct > 0 THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT(*), 0), 0.0),
              COALESCE(AVG(pnl_pct), 0.0),
              COALESCE(SUM(pnl_usd), 0.0),
              COALESCE(MIN(pnl_usd), 0.0),
              COALESCE(MAX(pnl_usd), 0.0),
              COALESCE(SUM(CASE WHEN pnl_usd > 0 THEN pnl_usd ELSE 0 END), 0.0),
              COALESCE(ABS(SUM(CASE WHEN pnl_usd < 0 THEN pnl_usd ELSE 0 END)), 0.0),
              COALESCE(AVG(CASE WHEN pnl_pct > 0 THEN pnl_pct END), 0.0),
              COALESCE(AVG(CASE WHEN pnl_pct <= 0 THEN ABS(pnl_pct) END), 0.0)
            FROM paper_trades
            WHERE {where}
            """,
            params,
        ).fetchone()

        durations = conn.execute(
            f"SELECT entry_time, exit_time FROM paper_trades WHERE {where} AND exit_time IS NOT NULL",
            params,
        ).fetchall()

    trades = int(row[0])
    gross_wins = float(row[6])
    gross_losses = float(row[7])
    avg_win = float(row[8])
    avg_loss = float(row[9])
    win_rate = float(row[1])
    expectancy = (win_rate * avg_win) - ((1 - win_rate) * avg_loss)
    profit_factor = (gross_wins / gross_losses) if gross_losses > 0 else (float("inf") if gross_wins > 0 else 0.0)

    avg_time_minutes = 0.0
    if durations:
        total = 0.0
        for entry, exit_ in durations:
            total += (_parse_iso(exit_) - _parse_iso(entry)).total_seconds() / 60.0
        avg_time_minutes = total / len(durations)

    return ExtendedStats(
        trades=trades,
        win_rate=win_rate,
        avg_pnl_pct=float(row[2]),
        total_pnl_usd=float(row[3]),
        worst_trade=float(row[4]),
        best_trade=float(row[5]),
        profit_factor=profit_factor,
        expectancy_pct=expectancy,
        avg_time_minutes=avg_time_minutes,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Paper trading KPI report")
    parser.add_argument("--db-path", default=DB_PATH)
    parser.add_argument("--since", default=None, help="ISO date lower bound on entry_time")
    parser.add_argument("--until", default=None, help="ISO date upper bound on entry_time")
    args = parser.parse_args()

    stats = load_extended_stats(args.db_path, since=args.since, until=args.until)
    print("paper_trades CLOSED stats")
    print(f"trades: {stats.trades}")
    print(f"win_rate: {stats.win_rate:.2%}")
    print(f"avg_pnl_pct: {stats.avg_pnl_pct:.4%}")
    print(f"total_pnl_usd: {stats.total_pnl_usd:.2f}")
    print(f"worst_trade: {stats.worst_trade:.2f}")
    print(f"best_trade: {stats.best_trade:.2f}")
    print(f"profit_factor: {stats.profit_factor:.3f}")
    print(f"expectancy_pct: {stats.expectancy_pct:.4%}")
    print(f"avg_time_minutes: {stats.avg_time_minutes:.2f}")


if __name__ == "__main__":
    main()
