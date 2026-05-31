from __future__ import annotations

import signals


def test_generate_signal_returns_none_when_long_disabled(monkeypatch):
    monkeypatch.setattr(signals, "ENABLE_LONG_SIGNALS", False)
    monkeypatch.setattr(signals, "ENABLE_SHORT_SIGNALS", True)

    result = signals.generate_signal(
        symbol="TESTUSDT",
        funding=-0.001,
        oi=1.0,
        prices=[100.0, 100.1, 100.2, 100.3, 100.4],
    )

    assert result is None


def test_generate_signal_returns_short_when_short_enabled(monkeypatch):
    monkeypatch.setattr(signals, "ENABLE_LONG_SIGNALS", False)
    monkeypatch.setattr(signals, "ENABLE_SHORT_SIGNALS", True)

    result = signals.generate_signal(
        symbol="TESTUSDT",
        funding=0.001,
        oi=1.0,
        prices=[100.0, 100.5, 100.7, 100.9, 101.0],
    )

    assert result is not None
    assert result["type"] == "SHORT"
