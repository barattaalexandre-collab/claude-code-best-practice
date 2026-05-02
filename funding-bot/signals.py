from __future__ import annotations

from typing import Literal, TypedDict

from config import FUNDING_CONFIDENCE_SCALE, FUNDING_LONG_THRESHOLD, FUNDING_SHORT_THRESHOLD


class Signal(TypedDict):
    symbol: str
    type: Literal["LONG", "SHORT"]
    funding: float
    confidence: float


def _is_stable_or_rising(last_prices: list[float]) -> bool:
    if len(last_prices) < 3:
        return False
    p1, p2, p3 = last_prices[-3:]
    return p3 >= p2 * 0.998 and p2 >= p1 * 0.998


def _is_not_parabolic(last_prices: list[float]) -> bool:
    if len(last_prices) < 5:
        return False
    move = (last_prices[-1] - last_prices[0]) / last_prices[0]
    return move < 0.02


def generate_signal(symbol: str, funding: float, oi: float, prices: list[float]) -> Signal | None:
    if oi <= 0 or len(prices) < 5:
        return None

    confidence_base = min(1.0, abs(funding) / FUNDING_CONFIDENCE_SCALE)

    if funding < FUNDING_LONG_THRESHOLD and _is_stable_or_rising(prices):
        return {
            "symbol": symbol,
            "type": "LONG",
            "funding": funding,
            "confidence": round(0.6 + confidence_base * 0.4, 3),
        }

    if funding > FUNDING_SHORT_THRESHOLD and _is_not_parabolic(prices):
        return {
            "symbol": symbol,
            "type": "SHORT",
            "funding": funding,
            "confidence": round(0.6 + confidence_base * 0.4, 3),
        }

    return None
