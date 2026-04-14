from sqlalchemy import text

from libs.storage.sqlite_store import engine


def main():
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT classification, COUNT(*) AS total
            FROM feature_snapshots
            GROUP BY classification
            ORDER BY total DESC
        """)).fetchall()

    print("Resumen de clasificaciones:")
    for row in rows:
        r = dict(row._mapping)
        print(f'{r["classification"]}: {r["total"]}')


if __name__ == "__main__":
    main()