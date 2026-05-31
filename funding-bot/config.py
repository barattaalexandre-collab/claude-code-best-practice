from __future__ import annotations

SYMBOLS: list[str] = [
    # Majors
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    # Large-cap alts; BCHUSDT intentionally excluded after concentrated stop-loss share in paper trading.
    "DOGEUSDT",
    "ADAUSDT",
    "AVAXUSDT",
    "LINKUSDT",
    "DOTUSDT",
    "TRXUSDT",
    "LTCUSDT",
    # L1/L2
    "SUIUSDT",
    "NEARUSDT",
    "APTUSDT",
    "ARBUSDT",
    "OPUSDT",
    # Extras; ATOMUSDT intentionally excluded after repeated post-BCH stop losses.
    "TIAUSDT",
]

# Research threshold after live funding-rate observations showed ±0.0003 was still too strict; re-evaluate after 24-48h.
FUNDING_LONG_THRESHOLD: float = -0.0002
FUNDING_SHORT_THRESHOLD: float = 0.0002
FUNDING_CONFIDENCE_SCALE: float = 0.002
ENABLE_LONG_SIGNALS: bool = False
ENABLE_SHORT_SIGNALS: bool = True

INTERVAL_SECONDS: int = 60
INTERVAL_JITTER_SECONDS: float = 5.0
COOLDOWN_MINUTES: int = 30
MAX_CONSECUTIVE_ERRORS: int = 10

PAPER_NOTIONAL_USD: float = 1000.0
TP_PCT: float = 0.015
SL_PCT: float = 0.01
MAX_HOLD_MINUTES: int = 480
PAPER_FEE_PCT: float = 0.0005

API_BASE_URL: str = "https://fapi.binance.com"

HTTP_CONNECT_TIMEOUT_SECONDS: float = 5.0
HTTP_READ_TIMEOUT_SECONDS: float = 10.0
HTTP_WRITE_TIMEOUT_SECONDS: float = 5.0
HTTP_POOL_TIMEOUT_SECONDS: float = 5.0
REQUEST_TIMEOUT_SECONDS: float = HTTP_READ_TIMEOUT_SECONDS
MAX_RETRIES: int = 6
BACKOFF_BASE_SECONDS: float = 1.0
BACKOFF_MAX_SECONDS: float = 30.0
BACKOFF_JITTER_SECONDS: float = 0.25
MAX_CONCURRENT_REQUESTS: int = 5
DB_PATH: str = "funding_bot.db"
