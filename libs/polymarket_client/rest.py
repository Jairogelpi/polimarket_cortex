import os
from typing import Any, Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

GAMMA_HOST = os.getenv("POLY_GAMMA_HOST", "https://gamma-api.polymarket.com")
DATA_HOST = os.getenv("POLY_DATA_HOST", "https://data-api.polymarket.com")
CLOB_HOST = os.getenv("POLY_CLOB_HOST", "https://clob.polymarket.com")


class PolymarketREST:
    def __init__(self, timeout: int = 20) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "openclaw-cortex-polymarket/0.1",
                "Accept": "application/json",
            }
        )

    def _get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    # ---------- Gamma API ----------
    def list_markets(self, limit: int = 20, closed: Optional[bool] = None) -> Any:
        params: Dict[str, Any] = {"limit": limit}
        if closed is not None:
            params["closed"] = str(closed).lower()
        return self._get(f"{GAMMA_HOST}/markets", params=params)

    def get_market_by_slug(self, slug: str) -> Any:
        return self._get(f"{GAMMA_HOST}/markets/slug/{slug}")

    def list_events(self, limit: int = 20, closed: Optional[bool] = None) -> Any:
        params: Dict[str, Any] = {"limit": limit}
        if closed is not None:
            params["closed"] = str(closed).lower()
        return self._get(f"{GAMMA_HOST}/events", params=params)

    # ---------- CLOB public ----------
    def get_orderbook(self, token_id: str) -> Any:
        return self._get(f"{CLOB_HOST}/book", params={"token_id": token_id})

    def get_midpoint(self, token_id: str) -> Any:
        return self._get(f"{CLOB_HOST}/midpoint", params={"token_id": token_id})

    def get_spread(self, token_id: str) -> Any:
        return self._get(f"{CLOB_HOST}/spread", params={"token_id": token_id})

    def get_market_price(self, token_id: str) -> Any:
        return self._get(f"{CLOB_HOST}/price", params={"token_id": token_id})

    def get_server_time(self) -> Any:
        return self._get(f"{CLOB_HOST}/time")

    # ---------- Data API public ----------
    def get_open_interest(self, market: str) -> Any:
        return self._get(f"{DATA_HOST}/open-interest", params={"market": market})
