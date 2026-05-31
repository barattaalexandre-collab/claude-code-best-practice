from __future__ import annotations

import asyncio
import logging
import random
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any

import httpx

from config import (
    API_BASE_URL,
    BACKOFF_BASE_SECONDS,
    BACKOFF_JITTER_SECONDS,
    BACKOFF_MAX_SECONDS,
    HTTP_CONNECT_TIMEOUT_SECONDS,
    HTTP_POOL_TIMEOUT_SECONDS,
    HTTP_READ_TIMEOUT_SECONDS,
    HTTP_WRITE_TIMEOUT_SECONDS,
    MAX_RETRIES,
)

logger = logging.getLogger(__name__)

RETRYABLE_HTTP_STATUSES: set[int] = {418, 429, 500, 502, 503, 504}


def _parse_retry_after_seconds(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            retry_at = parsedate_to_datetime(value)
        except (TypeError, ValueError):
            return None
        return max(0.0, (retry_at - datetime.now(tz=timezone.utc)).total_seconds())


def _is_retryable_http_error(exc: httpx.HTTPStatusError) -> bool:
    return exc.response.status_code in RETRYABLE_HTTP_STATUSES


class BinancePublicClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=API_BASE_URL,
            timeout=httpx.Timeout(
                connect=HTTP_CONNECT_TIMEOUT_SECONDS,
                read=HTTP_READ_TIMEOUT_SECONDS,
                write=HTTP_WRITE_TIMEOUT_SECONDS,
                pool=HTTP_POOL_TIMEOUT_SECONDS,
            ),
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
        )

    async def __aenter__(self) -> "BinancePublicClient":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.close()

    async def close(self) -> None:
        await self._client.aclose()

    def _sleep_seconds(self, attempt: int, exc: Exception) -> float:
        retry_after = None
        if isinstance(exc, httpx.HTTPStatusError):
            retry_after = _parse_retry_after_seconds(exc.response.headers.get("Retry-After"))

        raw_backoff = min(BACKOFF_MAX_SECONDS, BACKOFF_BASE_SECONDS * (2 ** (attempt - 1)))
        base_sleep = retry_after if retry_after is not None else raw_backoff
        return base_sleep + random.uniform(0.0, BACKOFF_JITTER_SECONDS)

    async def _get(self, endpoint: str, params: dict[str, str]) -> dict[str, Any] | list[Any]:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await self._client.get(endpoint, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                if not _is_retryable_http_error(exc):
                    logger.error(
                        "GET %s failed with non-retryable HTTP status %d on attempt %d/%d",
                        endpoint,
                        status,
                        attempt,
                        MAX_RETRIES,
                    )
                    raise
                if attempt == MAX_RETRIES:
                    logger.error(
                        "GET %s exhausted retries after HTTP status %d on attempt %d/%d",
                        endpoint,
                        status,
                        attempt,
                        MAX_RETRIES,
                    )
                    raise
                sleep_s = self._sleep_seconds(attempt, exc)
                logger.warning(
                    "GET %s attempt %d/%d failed with retryable HTTP status %d; retrying in %.2fs",
                    endpoint,
                    attempt,
                    MAX_RETRIES,
                    status,
                    sleep_s,
                )
                await asyncio.sleep(sleep_s)
            except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.PoolTimeout, httpx.WriteTimeout, httpx.NetworkError) as exc:
                if attempt == MAX_RETRIES:
                    logger.error(
                        "GET %s exhausted retries after %s on attempt %d/%d: %s",
                        endpoint,
                        exc.__class__.__name__,
                        attempt,
                        MAX_RETRIES,
                        exc,
                    )
                    raise
                sleep_s = self._sleep_seconds(attempt, exc)
                logger.warning(
                    "GET %s attempt %d/%d failed with %s; retrying in %.2fs: %s",
                    endpoint,
                    attempt,
                    MAX_RETRIES,
                    exc.__class__.__name__,
                    sleep_s,
                    exc,
                )
                await asyncio.sleep(sleep_s)
        raise RuntimeError("Unreachable retry loop")

    async def get_funding_and_price(self, symbol: str) -> tuple[float, float]:
        data = await self._get("/fapi/v1/premiumIndex", {"symbol": symbol})
        if not isinstance(data, dict):
            raise ValueError(f"Unexpected premiumIndex payload for {symbol}: {type(data)}")
        return float(data["lastFundingRate"]), float(data["markPrice"])

    async def get_open_interest(self, symbol: str) -> float:
        data = await self._get("/fapi/v1/openInterest", {"symbol": symbol})
        if not isinstance(data, dict):
            raise ValueError(f"Unexpected openInterest payload for {symbol}: {type(data)}")
        return float(data["openInterest"])

    async def get_recent_klines(self, symbol: str, limit: int = 5) -> list[float]:
        data = await self._get("/fapi/v1/klines", {"symbol": symbol, "interval": "1m", "limit": str(limit)})
        if not isinstance(data, list):
            raise ValueError(f"Unexpected klines payload for {symbol}: {type(data)}")
        closes: list[float] = []
        for candle in data:
            if not isinstance(candle, list) or len(candle) < 5:
                raise ValueError(f"Unexpected kline item format for {symbol}: {candle}")
            closes.append(float(candle[4]))
        return closes
