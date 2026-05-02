from __future__ import annotations

import argparse
import asyncio
import logging
import random
import signal
from datetime import datetime, timezone

from collector import BinancePublicClient
from config import (
    INTERVAL_JITTER_SECONDS,
    INTERVAL_SECONDS,
    MAX_CONSECUTIVE_ERRORS,
    MAX_CONCURRENT_REQUESTS,
    PAPER_FEE_PCT,
    SYMBOLS,
    TP_PCT,
)
from notifier import notify_signal
from paper import check_open_trades, open_paper_trade
from signals import generate_signal
from storage import Storage, utc_now_iso

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

def validate_runtime_config() -> None:
    round_trip_fee_pct = 2 * PAPER_FEE_PCT
    if TP_PCT <= round_trip_fee_pct:
        logger.warning(
            "TP_PCT=%.4f is <= round-trip fees=%.4f; TP wins can still be net negative.",
            TP_PCT,
            round_trip_fee_pct,
        )


async def process_symbol(symbol: str, client: BinancePublicClient, storage: Storage, sem: asyncio.Semaphore) -> bool:
    async with sem:
        try:
            funding, mark_price = await client.get_funding_and_price(symbol)
            oi = await client.get_open_interest(symbol)
            prices = await client.get_recent_klines(symbol, limit=6)
            closed_prices = prices[:-1]

            now_iso = utc_now_iso()
            now_dt = datetime.fromisoformat(now_iso)
            storage.save_snapshot(symbol, funding, oi, mark_price, now_iso)
            check_open_trades(storage, symbol, mark_price, now_dt)

            signal_obj = generate_signal(symbol, funding, oi, closed_prices)
            if signal_obj is None:
                return True

            if not storage.can_emit_signal(symbol, now_dt):
                logger.info("Cooldown active for %s; skipping signal.", symbol)
                return True

            storage.save_signal(symbol, signal_obj["type"], signal_obj["funding"], now_iso)
            open_paper_trade(storage, signal_obj, mark_price, now_iso)
            notify_signal(signal_obj)
            return True

        except Exception as exc:
            logger.exception("Failed processing %s: %s", symbol, exc)
            return False


async def run(max_cycles: int | None = None) -> None:
    validate_runtime_config()
    storage = Storage()
    sem = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    stop_event = asyncio.Event()

    def _request_stop() -> None:
        logger.info("Shutdown signal received. Stopping after current cycle.")
        stop_event.set()

    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _request_stop)
        except NotImplementedError:
            pass

    cycles_run = 0
    consecutive_error_cycles = 0
    try:
        async with BinancePublicClient() as client:
            while not stop_event.is_set():
                logger.info("Starting new collection cycle for %d symbols", len(SYMBOLS))
                results = await asyncio.gather(*(process_symbol(symbol, client, storage, sem) for symbol in SYMBOLS))
                cycles_run += 1

                if all(results):
                    consecutive_error_cycles = 0
                else:
                    consecutive_error_cycles += 1
                    logger.warning(
                        "Cycle %d had errors (%d/%d consecutive error cycles).",
                        cycles_run,
                        consecutive_error_cycles,
                        MAX_CONSECUTIVE_ERRORS,
                    )
                    if consecutive_error_cycles >= MAX_CONSECUTIVE_ERRORS:
                        logger.error("Circuit breaker triggered after %d consecutive error cycles.", MAX_CONSECUTIVE_ERRORS)
                        break

                if max_cycles is not None and cycles_run >= max_cycles:
                    logger.info("Reached max_cycles=%d; exiting.", max_cycles)
                    break
                if stop_event.is_set():
                    break

                jitter = random.uniform(-INTERVAL_JITTER_SECONDS, INTERVAL_JITTER_SECONDS)
                sleep_seconds = max(0.0, INTERVAL_SECONDS + jitter)
                logger.debug("Sleeping %.2fs before next cycle.", sleep_seconds)
                try:
                    await asyncio.wait_for(stop_event.wait(), timeout=sleep_seconds)
                except asyncio.TimeoutError:
                    pass
    finally:
        storage.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Funding-rate signal bot")
    parser.add_argument("--max-cycles", type=int, default=None, help="Run a finite number of cycles then exit")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run(max_cycles=args.max_cycles))
