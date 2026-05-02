from __future__ import annotations

from storage import Storage


def main() -> None:
    storage = Storage()
    stats = storage.get_paper_stats()
    print("paper_trades CLOSED stats")
    print(f"trades: {stats.trades}")
    print(f"win_rate: {stats.win_rate:.2%}")
    print(f"avg_pnl_pct: {stats.avg_pnl_pct:.4%}")
    print(f"total_pnl_usd: {stats.total_pnl_usd:.2f}")
    print(f"worst_trade: {stats.worst_trade:.2f}")
    print(f"best_trade: {stats.best_trade:.2f}")


if __name__ == "__main__":
    main()
