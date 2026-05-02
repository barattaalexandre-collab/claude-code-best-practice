from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from config import API_BASE_URL, BACKOFF_BASE_SECONDS, MAX_RETRIES, REQUEST_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)


class BinancePublicClient:
    def __init__(self) -> None:
        self._client = httpx.AsyncClient(
            base_url=API_BASE_URL,
            timeout=httpx.Timeout(REQUEST_TIMEOUT_SECONDS),
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
        )

    async def __aenter__(self) -> "BinancePublicClient":
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.close()

    async def close(self) -> None:
        await self._client.aclose()

    async def _get(self, endpoint: str, params: dict[str, str]) -> dict[str, Any] | list[Any]:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await self._client.get(endpoint, params=params)
                response.raise_for_status()
                return response.json()
            except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as exc:
                if attempt == MAX_RETRIES:
                    logger.error("GET %s failed after %d attempts: %s", endpoint, attempt, exc)
                    raise
                sleep_s = BACKOFF_BASE_SECONDS * (2 ** (attempt - 1))
                logger.warning(
                    "GET %s attempt %d/%d failed: %s; retrying in %.2fs",
                    endpoint,
                    attempt,
                    MAX_RETRIES,
                    exc,
                    sleep_s,
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
