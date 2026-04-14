from sqlalchemy import text

from libs.storage.sqlite_store import engine


def main():
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM feature_snapshots"))
    print("feature_snapshots vaciada.")


if __name__ == "__main__":
    main()