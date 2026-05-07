from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass

from config import DB_PATH, SYMBOLS


@dataclass
class HealthSummary:
    cycles: int
    error_cycles: int
    retries: int
    count_429_418: int
    snapshots: int
    expected_snapshots: int
    invalid_oi_or_price: int


def from_log_and_db(log_path: str, db_path: str) -> HealthSummary:
    cycles = error_cycles = retries = count_429_418 = 0
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if "Starting new collection cycle" in line:
                cycles += 1
            if "had errors" in line:
                error_cycles += 1
            if "retrying in" in line:
                retries += 1
            if " 429 " in line or " 418 " in line:
                count_429_418 += 1

    with sqlite3.connect(db_path) as conn:
        snapshots = int(conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0])
        invalid = int(conn.execute("SELECT COUNT(*) FROM snapshots WHERE oi <= 0 OR price <= 0").fetchone()[0])

    expected = cycles * len(SYMBOLS)
    return HealthSummary(cycles, error_cycles, retries, count_429_418, snapshots, expected, invalid)


def main() -> None:
    parser = argparse.ArgumentParser(description="Health summary")
    parser.add_argument("--log-path", default="run_long.log")
    parser.add_argument("--db-path", default=DB_PATH)
    args = parser.parse_args()

    s = from_log_and_db(args.log_path, args.db_path)
    print(f"cycles={s.cycles}")
    print(f"error_cycles={s.error_cycles}")
    print(f"retries={s.retries}")
    print(f"count_429_418={s.count_429_418}")
    print(f"snapshots={s.snapshots}/{s.expected_snapshots}")
    print(f"invalid_oi_or_price={s.invalid_oi_or_price}")


if __name__ == "__main__":
    main()
