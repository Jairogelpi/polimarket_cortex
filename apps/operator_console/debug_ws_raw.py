import asyncio
import json

from libs.polymarket_client.ws_market import stream_market

TOKENS = [
    "62175071347174625226150315285313253447421342829125204348718351595219328818513",
    "78072873004240978963355420834937928453039445105472046717163863208590700950152",
]

MAX_SAMPLES = 20


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


async def on_message(raw_msg: str):
    try:
        data = json.loads(raw_msg)
        print(f"type={classify_message(data)}")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:5000])
        print("-" * 100)
    except Exception:
        print(raw_msg[:5000])


async def main():
    stats = {
        "received": 0,
        "json_ok": 0,
        "json_failed": 0,
        "empty_list": 0,
        "token_update": 0,
        "market_snapshot": 0,
        "control_or_other": 0,
    }
    samples = []

    async def counting_handler(raw_msg: str):
        stats["received"] += 1

        try:
            data = json.loads(raw_msg)
            stats["json_ok"] += 1
            msg_type = classify_message(data)
            stats[msg_type] = stats.get(msg_type, 0) + 1

            if len(samples) < MAX_SAMPLES:
                samples.append({"type": msg_type, "data": data})

            await on_message(raw_msg)
        except Exception:
            stats["json_failed"] += 1
            print(raw_msg[:5000])

        if stats["received"] >= MAX_SAMPLES:
            raise SystemExit(0)

    try:
        await stream_market(TOKENS, counting_handler)
    except SystemExit:
        pass
    finally:
        print("=== WS SUMMARY ===")
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        print("=== WS SAMPLES ===")
        print(json.dumps(samples, indent=2, ensure_ascii=False)[:12000])


if __name__ == "__main__":
    asyncio.run(main())