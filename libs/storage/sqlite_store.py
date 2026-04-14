import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "sqlite:///data/trading.db")
engine = create_engine(DB_URL, future=True)


def init_db() -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS market_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            market_slug TEXT,
            token_id TEXT NOT NULL,
            side_label TEXT,
            best_bid REAL,
            best_ask REAL,
            midpoint REAL,
            spread REAL,
            bid_size REAL,
            ask_size REAL,
            last_trade_price REAL,
            last_trade_side TEXT,
            raw_json TEXT NOT NULL
        )
        """
            )
        )
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS feature_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_snapshot_id INTEGER NOT NULL,
            ts TEXT NOT NULL,
            market_slug TEXT,
            token_id TEXT NOT NULL,
            side_label TEXT,
            spread REAL,
            midpoint REAL,
            imbalance REAL,
            microprice REAL,
            pressure TEXT,
            score REAL,
            classification TEXT,
            reason TEXT
        )
        """
            )
        )


def insert_snapshot(
    ts: str,
    market_slug: str,
    token_id: str,
    side_label: str,
    best_bid,
    best_ask,
    midpoint,
    spread,
    bid_size,
    ask_size,
    last_trade_price,
    last_trade_side,
    raw_json: str,
) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
            INSERT INTO market_snapshots (
                ts, market_slug, token_id, side_label,
                best_bid, best_ask, midpoint, spread,
                bid_size, ask_size,
                last_trade_price, last_trade_side,
                raw_json
            )
            VALUES (
                :ts, :market_slug, :token_id, :side_label,
                :best_bid, :best_ask, :midpoint, :spread,
                :bid_size, :ask_size,
                :last_trade_price, :last_trade_side,
                :raw_json
            )
        """
            ),
            {
                "ts": ts,
                "market_slug": market_slug,
                "token_id": token_id,
                "side_label": side_label,
                "best_bid": best_bid,
                "best_ask": best_ask,
                "midpoint": midpoint,
                "spread": spread,
                "bid_size": bid_size,
                "ask_size": ask_size,
                "last_trade_price": last_trade_price,
                "last_trade_side": last_trade_side,
                "raw_json": raw_json,
            },
        )


def insert_feature_snapshot(
    market_snapshot_id: int,
    ts: str,
    market_slug: str,
    token_id: str,
    side_label: str,
    spread,
    midpoint,
    imbalance,
    microprice,
    pressure: str,
    score,
    classification: str,
    reason: str,
) -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
            INSERT INTO feature_snapshots (
                market_snapshot_id, ts, market_slug, token_id, side_label,
                spread, midpoint, imbalance, microprice, pressure,
                score, classification, reason
            )
            VALUES (
                :market_snapshot_id, :ts, :market_slug, :token_id, :side_label,
                :spread, :midpoint, :imbalance, :microprice, :pressure,
                :score, :classification, :reason
            )
        """
            ),
            {
                "market_snapshot_id": market_snapshot_id,
                "ts": ts,
                "market_slug": market_slug,
                "token_id": token_id,
                "side_label": side_label,
                "spread": spread,
                "midpoint": midpoint,
                "imbalance": imbalance,
                "microprice": microprice,
                "pressure": pressure,
                "score": score,
                "classification": classification,
                "reason": reason,
            },
        )