from __future__ import annotations

import logging

from signals import Signal

logger = logging.getLogger(__name__)


def notify_signal(signal: Signal) -> None:
    logger.info(
        "🚨 SIGNAL %-5s | %-10s | funding=%+.6f | confidence=%.3f",
        signal["type"],
        signal["symbol"],
        signal["funding"],
        signal["confidence"],
    )
