from sqlalchemy import text

from libs.storage.sqlite_store import engine


def main():
    with engine.begin() as conn:
        rows = conn.execute(
            text(
                """
            SELECT id, ts, market_slug, side_label, best_bid, best_ask, midpoint, spread
            FROM market_snapshots
            ORDER BY id DESC
            LIMIT 20
        """
            )
        ).fetchall()

    for row in rows:
        print(dict(row._mapping))


if __name__ == "__main__":
    main()