from __future__ import annotations

SYMBOLS: list[str] = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
]

FUNDING_LONG_THRESHOLD: float = -0.0005
FUNDING_SHORT_THRESHOLD: float = 0.0005
FUNDING_CONFIDENCE_SCALE: float = 0.002

INTERVAL_SECONDS: int = 60
INTERVAL_JITTER_SECONDS: float = 5.0
COOLDOWN_MINUTES: int = 30
MAX_CONSECUTIVE_ERRORS: int = 5

PAPER_NOTIONAL_USD: float = 1000.0
TP_PCT: float = 0.015
SL_PCT: float = 0.01
MAX_HOLD_MINUTES: int = 480
PAPER_FEE_PCT: float = 0.0005

API_BASE_URL: str = "https://fapi.binance.com"

REQUEST_TIMEOUT_SECONDS: float = 8.0
MAX_RETRIES: int = 4
BACKOFF_BASE_SECONDS: float = 0.5
MAX_CONCURRENT_REQUESTS: int = 5
DB_PATH: str = "funding_bot.db"
