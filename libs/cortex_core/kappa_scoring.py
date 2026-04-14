def score_snapshot(features: dict) -> float:
    spread = features.get("spread")
    imbalance = features.get("imbalance")
    microprice = features.get("microprice")
    midpoint = features.get("midpoint")

    if spread is None or midpoint is None:
        return -999.0

    score = 0.0

    score += spread * 1000.0

    if imbalance is not None:
        score += abs(imbalance) * 5.0

    if microprice is not None:
        score += abs(microprice - midpoint) * 1000.0

    return score