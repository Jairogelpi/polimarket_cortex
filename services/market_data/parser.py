from typing import Any


def safe_float(value):
    try:
        if value is None:
            return None
        return float(value)
    except Exception:
        return None


def extract_price_size(level: Any):
    """
    Soporta varios formatos posibles:
    {"price": "...", "size": "..."}
    {"price": "...", "quantity": "..."}
    ["0.10", "50"]
    """
    if isinstance(level, dict):
        price = safe_float(level.get("price") or level.get("p") or level.get("px"))
        size = safe_float(level.get("size") or level.get("quantity") or level.get("qty") or level.get("s"))
        return price, size

    if isinstance(level, (list, tuple)) and len(level) >= 2:
        return safe_float(level[0]), safe_float(level[1])

    return None, None


def pick_first_price_and_size(levels):
    if not levels or not isinstance(levels, list):
        return None, None

    return extract_price_size(levels[0])


def extract_token_ids(data: dict[str, Any]) -> list[str]:
    token_ids = []

    direct_token_id = (
        data.get("asset_id")
        or data.get("assetId")
        or data.get("token_id")
        or data.get("tokenId")
        or data.get("market")
        or data.get("condition_id")
        or data.get("clobTokenId")
        or data.get("clob_token_id")
        or ""
    )
    if direct_token_id:
        token_ids.append(str(direct_token_id))

    clob_token_ids = data.get("clobTokenIds") or data.get("clob_token_ids")
    if isinstance(clob_token_ids, list):
        for token_id in clob_token_ids:
            if token_id:
                token_ids.append(str(token_id))

    markets = data.get("markets")
    if isinstance(markets, list):
        for market in markets:
            if isinstance(market, dict):
                token_ids.extend(extract_token_ids(market))

    seen = set()
    unique_token_ids = []
    for token_id in token_ids:
        if token_id not in seen:
            seen.add(token_id)
            unique_token_ids.append(token_id)

    return unique_token_ids


def _resolve_book_source(data: dict[str, Any]) -> dict[str, Any]:
    for key in ("data", "market", "book", "orderbook"):
        candidate = data.get(key)
        if isinstance(candidate, dict):
            return candidate
    return data


def parse_market_message(data: dict[str, Any]) -> dict[str, Any]:
    source = _resolve_book_source(data)

    token_id = (
        source.get("asset_id")
        or source.get("assetId")
        or source.get("token_id")
        or source.get("tokenId")
        or source.get("market")
        or source.get("condition_id")
        or ""
    )

    bids = source.get("bids") or source.get("buy") or source.get("buy_orders") or []
    asks = source.get("asks") or source.get("sell") or source.get("sell_orders") or []

    best_bid, bid_size = pick_first_price_and_size(bids)
    best_ask, ask_size = pick_first_price_and_size(asks)

    midpoint = None
    spread = None
    if best_bid is not None and best_ask is not None:
        spread = best_ask - best_bid
        midpoint = (best_bid + best_ask) / 2.0

    last_trade_price = safe_float(
        source.get("last_trade_price")
        or source.get("lastPrice")
        or source.get("price")
        or source.get("p")
    )

    last_trade_side = (
        source.get("side")
        or source.get("last_trade_side")
        or source.get("taker_side")
        or source.get("trade_side")
    )

    return {
        "token_id": str(token_id),
        "best_bid": best_bid,
        "best_ask": best_ask,
        "midpoint": midpoint,
        "spread": spread,
        "bid_size": bid_size,
        "ask_size": ask_size,
        "last_trade_price": last_trade_price,
        "last_trade_side": last_trade_side,
    }