import json
from pathlib import Path

FILE_PATH = Path("data/raw/ws/market_ws_raw.jsonl")


def main():
    if not FILE_PATH.exists():
        print("No existe el archivo raw todavía.")
        return

    with FILE_PATH.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            obj = json.loads(line)
            print("=" * 100)
            print(f"REGISTRO {idx} | ts={obj['ts']}")
            raw = obj["raw"]

            try:
                parsed = json.loads(raw)
                print(json.dumps(parsed, indent=2, ensure_ascii=False)[:8000])
            except Exception:
                print(raw[:8000])

            if idx >= 10:
                break


if __name__ == "__main__":
    main()