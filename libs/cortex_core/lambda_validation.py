def classify_snapshot(features: dict, score: float) -> tuple[str, str]:
    spread = features.get("spread")
    imbalance = features.get("imbalance")
    pressure = features.get("pressure")

    if spread is None:
        return "NO_TRADE", "missing_spread"

    if spread < 0.005:
        return "NO_TRADE", "spread_too_tight"

    if score < 3:
        return "WATCH", "weak_setup"

    if imbalance is not None and abs(imbalance) >= 0.20 and pressure in ("UP", "DOWN"):
        return "INTERESTING", "book_pressure_setup"

    return "WATCH", "moderate_setup"