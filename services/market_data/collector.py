import asyncio
import json
from datetime import datetime, timezone

from libs.polymarket_client.rest import PolymarketREST
from libs.polymarket_client.ws_market import stream_market
from libs.storage.sqlite_store import init_db, insert_snapshot
from services.market_data.parser import extract_token_ids, parse_market_message

MARKET_SLUG = "btc-updown-5m-1776181500"

TOKEN_MAP = {
    "62175071347174625226150315285313253447421342829125204348718351595219328818513": "UP",
    "78072873004240978963355420834937928453039445105472046717163863208590700950152": "DOWN",
}

rest_client = PolymarketREST()


stats = {
    "received": 0,
    "json_ok": 0,
    "json_failed": 0,
    "control_or_other": 0,
    "token_updates": 0,
    "market_snapshots": 0,
    "snapshots_written": 0,
}


def classify_message(data) -> str:
    if isinstance(data, list):
        if not data:
            return "empty_list"
        return "list"

    if isinstance(data, dict):
        if data.get("asset_id") or data.get("token_id") or data.get("clobTokenId"):
            return "token_update"
        if data.get("clobTokenIds") or data.get("markets"):
            return "market_snapshot"
        return "control_or_other"

    return type(data).__name__


async def seed_snapshot(token_id: str) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    try:
        side_label = TOKEN_MAP.get(token_id, "UNKNOWN")
        market = rest_client.get_market_by_slug(MARKET_SLUG)
        parsed = parse_market_message(market)

        insert_snapshot(
            ts=ts,
            market_slug=MARKET_SLUG,
            token_id=token_id,
            side_label=side_label,
            best_bid=parsed["best_bid"],
            best_ask=parsed["best_ask"],
            midpoint=parsed["midpoint"],
            spread=parsed["spread"],
            bid_size=parsed["bid_size"],
            ask_size=parsed["ask_size"],
            last_trade_price=safe_last_trade_price(token_id),
            last_trade_side=None,
            raw_json=json.dumps(market, ensure_ascii=False),
        )

        print(
            f"[bootstrap] {side_label:<5} "
            f"bid={parsed['best_bid']} ask={parsed['best_ask']} "
            f"mid={parsed['midpoint']} spr={parsed['spread']} "
            f"bid_sz={parsed['bid_size']} ask_sz={parsed['ask_size']}"
        )
    except Exception as exc:
        print(f"[bootstrap] Error for {token_id}: {exc}")


def safe_last_trade_price(token_id: str):
    try:
        value = rest_client.get_last_trade_price(token_id)
        if isinstance(value, dict):
            price = value.get("price")
            return float(price) if price is not None else None
        return None
    except Exception:
        return None


async def on_message(raw_msg: str):
    ts = datetime.now(timezone.utc).isoformat()
    stats["received"] += 1

    try:
        data = json.loads(raw_msg)
        stats["json_ok"] += 1
    except json.JSONDecodeError:
        stats["json_failed"] += 1
        print("Mensaje no JSON:", raw_msg[:300])
        return

    messages = data if isinstance(data, list) else [data]

    for item in messages:
        if not isinstance(item, dict):
            continue

        msg_type = classify_message(item)
        if msg_type == "control_or_other":
            stats["control_or_other"] += 1
        elif msg_type == "token_update":
            stats["token_updates"] += 1
        elif msg_type == "market_snapshot":
            stats["market_snapshots"] += 1

        parsed = parse_market_message(item)

        token_ids = [parsed["token_id"]] if parsed["token_id"] else extract_token_ids(item)
        if not token_ids:
            print("Control/otro mensaje:", json.dumps(item, ensure_ascii=False)[:300])
            continue

        for token_id in token_ids:
            side_label = TOKEN_MAP.get(token_id, "UNKNOWN")

            insert_snapshot(
                ts=ts,
                market_slug=MARKET_SLUG,
                token_id=token_id,
                side_label=side_label,
                best_bid=parsed["best_bid"],
                best_ask=parsed["best_ask"],
                midpoint=parsed["midpoint"],
                spread=parsed["spread"],
                bid_size=parsed["bid_size"],
                ask_size=parsed["ask_size"],
                last_trade_price=parsed["last_trade_price"],
                last_trade_side=parsed["last_trade_side"],
                raw_json=json.dumps(item, ensure_ascii=False),
            )
            stats["snapshots_written"] += 1

            print(
                f"[{ts}] {side_label:<5} "
                f"bid={parsed['best_bid']} ask={parsed['best_ask']} "
                f"mid={parsed['midpoint']} spr={parsed['spread']} "
                f"bid_sz={parsed['bid_size']} ask_sz={parsed['ask_size']} "
                f"last={parsed['last_trade_price']} side={parsed['last_trade_side']}"
            )

        if stats["received"] % 25 == 0:
            print("=== WS STATS ===")
            print(json.dumps(stats, indent=2, ensure_ascii=False))


async def main():
    init_db()
    for token_id in TOKEN_MAP:
        await seed_snapshot(token_id)
    asset_ids = list(TOKEN_MAP.keys())
    try:
        await stream_market(asset_ids, on_message)
    finally:
        print("=== FINAL WS STATS ===")
        print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())