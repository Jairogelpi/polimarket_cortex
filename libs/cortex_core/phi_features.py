from typing import Optional


def compute_features(
    best_bid: Optional[float],
    best_ask: Optional[float],
    bid_size: Optional[float],
    ask_size: Optional[float],
) -> dict:
    spread = None
    midpoint = None
    imbalance = None
    microprice = None
    pressure = "UNKNOWN"

    if best_bid is not None and best_ask is not None:
        spread = best_ask - best_bid
        midpoint = (best_bid + best_ask) / 2.0

    if (
        bid_size is not None and ask_size is not None
        and (bid_size + ask_size) > 0
    ):
        imbalance = (bid_size - ask_size) / (bid_size + ask_size)

        if best_bid is not None and best_ask is not None:
            microprice = (
                (best_ask * bid_size) + (best_bid * ask_size)
            ) / (bid_size + ask_size)

    if microprice is not None and midpoint is not None:
        if microprice > midpoint:
            pressure = "UP"
        elif microprice < midpoint:
            pressure = "DOWN"
        else:
            pressure = "FLAT"

    return {
        "spread": spread,
        "midpoint": midpoint,
        "imbalance": imbalance,
        "microprice": microprice,
        "pressure": pressure,
    }