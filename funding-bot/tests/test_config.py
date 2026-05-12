from __future__ import annotations

from config import FUNDING_LONG_THRESHOLD, FUNDING_SHORT_THRESHOLD


def test_research_thresholds_are_point_0002() -> None:
    assert FUNDING_LONG_THRESHOLD == -0.0002
    assert FUNDING_SHORT_THRESHOLD == 0.0002


def test_research_thresholds_are_symmetric() -> None:
    assert abs(FUNDING_LONG_THRESHOLD) == FUNDING_SHORT_THRESHOLD


def test_long_threshold_is_negative_and_short_threshold_is_positive() -> None:
    assert FUNDING_LONG_THRESHOLD < 0
    assert FUNDING_SHORT_THRESHOLD > 0
