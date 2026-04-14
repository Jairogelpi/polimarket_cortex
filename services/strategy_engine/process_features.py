from sqlalchemy import text

from libs.cortex_core.kappa_scoring import score_snapshot
from libs.cortex_core.lambda_validation import classify_snapshot
from libs.cortex_core.phi_features import compute_features
from libs.storage.sqlite_store import engine, init_db, insert_feature_snapshot


def main():
    init_db()

    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, ts, market_slug, token_id, side_label,
                   best_bid, best_ask, bid_size, ask_size
            FROM market_snapshots
            ORDER BY id ASC
        """)).fetchall()

    processed = 0

    for row in rows:
        r = dict(row._mapping)

        features = compute_features(
            best_bid=r["best_bid"],
            best_ask=r["best_ask"],
            bid_size=r["bid_size"],
            ask_size=r["ask_size"],
        )

        score = score_snapshot(features)
        classification, reason = classify_snapshot(features, score)

        insert_feature_snapshot(
            market_snapshot_id=r["id"],
            ts=r["ts"],
            market_slug=r["market_slug"],
            token_id=r["token_id"],
            side_label=r["side_label"],
            spread=features["spread"],
            midpoint=features["midpoint"],
            imbalance=features["imbalance"],
            microprice=features["microprice"],
            pressure=features["pressure"],
            score=score,
            classification=classification,
            reason=reason,
        )
        processed += 1

    print(f"Procesados {processed} snapshots.")


if __name__ == "__main__":
    main()