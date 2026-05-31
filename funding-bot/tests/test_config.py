from __future__ import annotations

from config import (
    ENABLE_LONG_SIGNALS,
    ENABLE_SHORT_SIGNALS,
    FUNDING_LONG_THRESHOLD,
    FUNDING_SHORT_THRESHOLD,
    SYMBOLS,
)


def test_symbols_count_is_eighteen() -> None:
    assert len(SYMBOLS) == 18


def test_bchusdt_is_removed_from_watchlist() -> None:
    assert "BCHUSDT" not in SYMBOLS


def test_atomusdt_is_removed_from_watchlist() -> None:
    assert "ATOMUSDT" not in SYMBOLS


def test_research_thresholds_are_point_0002() -> None:
    assert FUNDING_LONG_THRESHOLD == -0.0002
    assert FUNDING_SHORT_THRESHOLD == 0.0002


def test_research_thresholds_are_symmetric() -> None:
    assert abs(FUNDING_LONG_THRESHOLD) == FUNDING_SHORT_THRESHOLD


def test_long_threshold_is_negative_and_short_threshold_is_positive() -> None:
    assert FUNDING_LONG_THRESHOLD < 0
    assert FUNDING_SHORT_THRESHOLD > 0


def test_signal_direction_flags_default_to_long_disabled_short_enabled() -> None:
    assert ENABLE_LONG_SIGNALS is False
    assert ENABLE_SHORT_SIGNALS is True
