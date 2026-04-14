from sqlalchemy import text

from libs.storage.sqlite_store import engine


def main():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT side_label,
                   COUNT(*) AS total,
                   SUM(CASE WHEN bid_size IS NOT NULL THEN 1 ELSE 0 END) AS bid_size_ok,
                   SUM(CASE WHEN ask_size IS NOT NULL THEN 1 ELSE 0 END) AS ask_size_ok
            FROM market_snapshots
            GROUP BY side_label
        """)).fetchall()

    for row in rows:
        r = dict(row._mapping)
        print(r)


if __name__ == "__main__":
    main()