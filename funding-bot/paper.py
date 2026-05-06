from __future__ import annotations

from datetime import datetime, timedelta
from typing import Literal

from config import MAX_HOLD_MINUTES, PAPER_FEE_PCT, PAPER_NOTIONAL_USD, SL_PCT, TP_PCT
from signals import Signal
from storage import OpenPaperTrade, Storage


CloseReason = Literal["TP", "SL", "TIMEOUT"]


def open_paper_trade(storage: Storage, signal: Signal, mark_price: float, now_iso: str) -> None:
    side = signal["type"]
    if side == "LONG":
        tp_price = mark_price * (1 + TP_PCT)
        sl_price = mark_price * (1 - SL_PCT)
    else:
        tp_price = mark_price * (1 - TP_PCT)
        sl_price = mark_price * (1 + SL_PCT)

    storage.save_paper_trade(
        symbol=signal["symbol"],
        side=side,
        entry_price=mark_price,
        entry_time=now_iso,
        tp_price=tp_price,
        sl_price=sl_price,
    )


def check_open_trades(storage: Storage, symbol: str, mark_price: float, now: datetime) -> None:
    open_trades = storage.get_open_paper_trades(symbol)
    for trade in open_trades:
        reason = _resolve_close_reason(trade, mark_price, now)
        if reason is None:
            continue
        close_paper_trade(storage, trade, mark_price, now.isoformat(), reason)


def _resolve_close_reason(trade: OpenPaperTrade, mark_price: float, now: datetime) -> CloseReason | None:
    if trade.side == "LONG":
        if mark_price >= trade.tp_price:
            return "TP"
        if mark_price <= trade.sl_price:
            return "SL"
    else:
        if mark_price <= trade.tp_price:
            return "TP"
        if mark_price >= trade.sl_price:
            return "SL"

    if now - trade.entry_time >= timedelta(minutes=MAX_HOLD_MINUTES):
        return "TIMEOUT"
    return None


def close_paper_trade(storage: Storage, trade: OpenPaperTrade, exit_price: float, exit_time: str, reason: CloseReason) -> None:
    gross_pnl_pct = ((exit_price - trade.entry_price) / trade.entry_price) if trade.side == "LONG" else ((trade.entry_price - exit_price) / trade.entry_price)
    net_pnl_pct = gross_pnl_pct - (2 * PAPER_FEE_PCT)
    pnl_usd = PAPER_NOTIONAL_USD * net_pnl_pct
    storage.close_paper_trade(trade.id, exit_price, exit_time, reason, net_pnl_pct, pnl_usd)
