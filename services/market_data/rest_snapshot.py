import json
from datetime import datetime, timezone

from libs.polymarket_client.rest import PolymarketREST
from libs.storage.sqlite_store import insert_snapshot, init_db


TOKEN_MAP = {
    "62175071347174625226150315285313253447421342829125204348718351595219328818513": "UP",
    "78072873004240978963355420834937928453039445105472046717163863208590700950152": "DOWN",
}

MARKET_SLUG = "btc-updown-5m-1776181500"


def safe_float(value):
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def main():
    init_db()
    client = PolymarketREST()

    for token_id, side_label in TOKEN_MAP.items():
        try:
            book = client.get_orderbook(token_id)
        except Exception as exc:
            print(f"{side_label} | no orderbook disponible: {exc}")
            continue

        bids = book.get("bids", [])
        asks = book.get("asks", [])

        best_bid = safe_float(bids[0].get("price")) if bids else None
        bid_size = safe_float(bids[0].get("size")) if bids else None

        best_ask = safe_float(asks[0].get("price")) if asks else None
        ask_size = safe_float(asks[0].get("size")) if asks else None

        midpoint = None
        spread = None
        if best_bid is not None and best_ask is not None:
            midpoint = (best_bid + best_ask) / 2.0
            spread = best_ask - best_bid

        ts = datetime.now(timezone.utc).isoformat()

        insert_snapshot(
            ts=ts,
            market_slug=MARKET_SLUG,
            token_id=token_id,
            side_label=side_label,
            best_bid=best_bid,
            best_ask=best_ask,
            midpoint=midpoint,
            spread=spread,
            bid_size=bid_size,
            ask_size=ask_size,
            last_trade_price=None,
            last_trade_side=None,
            raw_json=json.dumps(book, ensure_ascii=False),
        )

        print(
            f"{side_label} | bid={best_bid} ask={best_ask} "
            f"bid_size={bid_size} ask_size={ask_size} "
            f"mid={midpoint} spread={spread}"
        )


if __name__ == "__main__":
    main()