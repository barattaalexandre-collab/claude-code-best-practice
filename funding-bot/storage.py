from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterator

from config import COOLDOWN_MINUTES, DB_PATH


@dataclass
class OpenPaperTrade:
    id: int
    symbol: str
    side: str
    entry_price: float
    entry_time: datetime
    tp_price: float
    sl_price: float


@dataclass
class PaperStats:
    trades: int
    win_rate: float
    avg_pnl_pct: float
    total_pnl_usd: float
    worst_trade: float
    best_trade: float


class Storage:
    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    funding REAL NOT NULL,
                    oi REAL NOT NULL,
                    price REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    type TEXT NOT NULL,
                    funding REAL NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS paper_trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    side TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    entry_time TEXT NOT NULL,
                    tp_price REAL NOT NULL,
                    sl_price REAL NOT NULL,
                    exit_price REAL,
                    exit_time TEXT,
                    exit_reason TEXT,
                    pnl_pct REAL,
                    pnl_usd REAL,
                    status TEXT NOT NULL DEFAULT 'OPEN'
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_signals_symbol ON signals(symbol)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_snapshots_symbol_ts ON snapshots(symbol, timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_paper_trades_symbol_status ON paper_trades(symbol, status)")

    def close(self) -> None:
        return

    def save_snapshot(self, symbol: str, funding: float, oi: float, price: float, timestamp: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO snapshots (symbol, funding, oi, price, timestamp) VALUES (?, ?, ?, ?, ?)",
                (symbol, funding, oi, price, timestamp),
            )

    def save_signal(self, symbol: str, signal_type: str, funding: float, timestamp: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO signals (symbol, type, funding, timestamp) VALUES (?, ?, ?, ?)",
                (symbol, signal_type, funding, timestamp),
            )

    def get_last_signal_time(self, symbol: str) -> datetime | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT timestamp FROM signals WHERE symbol = ? ORDER BY id DESC LIMIT 1",
                (symbol,),
            ).fetchone()
        if not row:
            return None
        return datetime.fromisoformat(row[0])

    def can_emit_signal(self, symbol: str, now: datetime) -> bool:
        last = self.get_last_signal_time(symbol)
        if last is None:
            return True
        return now - last >= timedelta(minutes=COOLDOWN_MINUTES)

    def save_paper_trade(self, symbol: str, side: str, entry_price: float, entry_time: str, tp_price: float, sl_price: float) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO paper_trades (symbol, side, entry_price, entry_time, tp_price, sl_price, status)
                VALUES (?, ?, ?, ?, ?, ?, 'OPEN')
                """,
                (symbol, side, entry_price, entry_time, tp_price, sl_price),
            )

    def get_open_paper_trades(self, symbol: str) -> list[OpenPaperTrade]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, symbol, side, entry_price, entry_time, tp_price, sl_price
                FROM paper_trades
                WHERE symbol = ? AND status = 'OPEN'
                ORDER BY id ASC
                """,
                (symbol,),
            ).fetchall()

        return [
            OpenPaperTrade(
                id=row[0],
                symbol=row[1],
                side=row[2],
                entry_price=float(row[3]),
                entry_time=datetime.fromisoformat(row[4]),
                tp_price=float(row[5]),
                sl_price=float(row[6]),
            )
            for row in rows
        ]

    def close_paper_trade(
        self,
        trade_id: int,
        exit_price: float,
        exit_time: str,
        exit_reason: str,
        pnl_pct: float,
        pnl_usd: float,
    ) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE paper_trades
                SET exit_price = ?, exit_time = ?, exit_reason = ?, pnl_pct = ?, pnl_usd = ?, status = 'CLOSED'
                WHERE id = ? AND status = 'OPEN'
                """,
                (exit_price, exit_time, exit_reason, pnl_pct, pnl_usd, trade_id),
            )

    def get_paper_stats(self) -> PaperStats:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT
                  COUNT(*) AS trades,
                  COALESCE(SUM(CASE WHEN pnl_pct > 0 THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT(*), 0), 0.0) AS win_rate,
                  COALESCE(AVG(pnl_pct), 0.0) AS avg_pnl_pct,
                  COALESCE(SUM(pnl_usd), 0.0) AS total_pnl_usd,
                  COALESCE(MIN(pnl_usd), 0.0) AS worst_trade,
                  COALESCE(MAX(pnl_usd), 0.0) AS best_trade
                FROM paper_trades
                WHERE status = 'CLOSED'
                """
            ).fetchone()

        return PaperStats(
            trades=int(row[0]),
            win_rate=float(row[1]),
            avg_pnl_pct=float(row[2]),
            total_pnl_usd=float(row[3]),
            worst_trade=float(row[4]),
            best_trade=float(row[5]),
        )


def utc_now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()
