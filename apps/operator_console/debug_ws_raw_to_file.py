import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path

from libs.polymarket_client.ws_market import stream_market

TOKENS = [
    "62175071347174625226150315285313253447421342829125204348718351595219328818513",
    "78072873004240978963355420834937928453039445105472046717163863208590700950152",
]

OUT_DIR = Path("data/raw/ws")
OUT_DIR.mkdir(parents=True, exist_ok=True)

FILE_PATH = OUT_DIR / "market_ws_raw.jsonl"
MAX_MESSAGES = 100
counter = 0


async def on_message(raw_msg: str):
    global counter
    ts = datetime.now(timezone.utc).isoformat()

    with FILE_PATH.open("a", encoding="utf-8") as f:
        record = {
            "ts": ts,
            "raw": raw_msg,
        }
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    counter += 1
    print(f"[{counter}] mensaje guardado")

    if counter >= MAX_MESSAGES:
        raise SystemExit("Límite alcanzado")


async def main():
    try:
        await stream_market(TOKENS, on_message)
    except SystemExit as exc:
        print(str(exc))


if __name__ == "__main__":
    asyncio.run(main())