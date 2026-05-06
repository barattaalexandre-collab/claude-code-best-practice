from __future__ import annotations

import asyncio

import httpx
import pytest

import collector
from collector import BinancePublicClient
from main import next_consecutive_error_cycles


class _FakeResponse:
    def __init__(self, status_code: int, payload: dict[str, str] | None = None, retry_after: str | None = None) -> None:
        self.status_code = status_code
        self.headers = {}
        if retry_after is not None:
            self.headers["Retry-After"] = retry_after
        self._payload = payload or {"ok": "true"}
        self.request = httpx.Request("GET", "https://example.test/fapi")

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("boom", request=self.request, response=self)  # type: ignore[arg-type]

    def json(self) -> dict[str, str]:
        return self._payload


class _FakeAsyncClient:
    def __init__(self, outcomes: list[object]) -> None:
        self.outcomes = outcomes
        self.calls = 0

    async def get(self, endpoint: str, params: dict[str, str]) -> object:
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


@pytest.mark.parametrize("status", [400, 401, 403, 404])
def test_non_retryable_http_status_fails_fast(status: int) -> None:
    client = BinancePublicClient()
    fake = _FakeAsyncClient([_FakeResponse(status)])
    client._client = fake  # type: ignore[assignment]

    with pytest.raises(httpx.HTTPStatusError):
        asyncio.run(client._get("/x", {}))

    assert fake.calls == 1


def test_retryable_5xx_retries_until_success(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(collector.random, "uniform", lambda _start, _end: 0.0)

    client = BinancePublicClient()
    fake = _FakeAsyncClient([_FakeResponse(503), _FakeResponse(200, {"ok": "yes"})])
    client._client = fake  # type: ignore[assignment]

    result = asyncio.run(client._get("/x", {}))

    assert result == {"ok": "yes"}
    assert fake.calls == 2
    assert sleeps == [1.0]


def test_429_retry_after_is_honored_with_additive_jitter(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(collector.random, "uniform", lambda _start, _end: 0.25)

    client = BinancePublicClient()
    fake = _FakeAsyncClient([_FakeResponse(429, retry_after="2"), _FakeResponse(200, {"ok": "yes"})])
    client._client = fake  # type: ignore[assignment]

    result = asyncio.run(client._get("/x", {}))

    assert result == {"ok": "yes"}
    assert sleeps == [2.25]


def test_connect_timeout_retries_until_success(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    request = httpx.Request("GET", "https://example.test/fapi")
    monkeypatch.setattr(asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(collector.random, "uniform", lambda _start, _end: 0.0)

    client = BinancePublicClient()
    fake = _FakeAsyncClient([httpx.ConnectTimeout("timeout", request=request), _FakeResponse(200, {"ok": "yes"})])
    client._client = fake  # type: ignore[assignment]

    result = asyncio.run(client._get("/x", {}))

    assert result == {"ok": "yes"}
    assert fake.calls == 2
    assert sleeps == [1.0]


def test_circuit_breaker_counter_resets_after_healthy_cycle() -> None:
    assert next_consecutive_error_cycles(4, [False, True, True]) == 5
    assert next_consecutive_error_cycles(5, [True, True, True]) == 0


def test_circuit_breaker_counter_reaches_new_threshold() -> None:
    count = 0
    for _ in range(10):
        count = next_consecutive_error_cycles(count, [False, False])
    assert count == 10
