from sqlalchemy import text

from libs.storage.sqlite_store import engine


def main():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT id, ts, side_label, spread, midpoint, imbalance, microprice,
                   pressure, score, classification, reason
            FROM feature_snapshots
            ORDER BY id DESC
            LIMIT 50
        """)).fetchall()

    rows = list(reversed(rows))

    for row in rows:
        r = dict(row._mapping)
        print(
            f'{r["id"]:>5} | {r["ts"]} | {r["side_label"]:<5} | '
            f'spread={r["spread"]} mid={r["midpoint"]} '
            f'imb={r["imbalance"]} micro={r["microprice"]} '
            f'pressure={r["pressure"]:<7} score={r["score"]:.3f} | '
            f'{r["classification"]} ({r["reason"]})'
        )


if __name__ == "__main__":
    main()