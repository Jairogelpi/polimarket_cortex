import json
from typing import Any

from libs.polymarket_client.rest import PolymarketREST


def pretty_print_markets(data: Any) -> None:
    if isinstance(data, list):
        print(f"Mercados recibidos: {len(data)}")
        for idx, market in enumerate(data[:10], start=1):
            question = market.get("question")
            slug = market.get("slug")
            market_id = market.get("id")
            active = market.get("active")
            closed = market.get("closed")
            end_date = market.get("endDate")
            outcomes = market.get("outcomes")
            clob_token_ids = market.get("clobTokenIds")

            print("=" * 80)
            print(f"[{idx}] question     : {question}")
            print(f"[{idx}] slug         : {slug}")
            print(f"[{idx}] market_id    : {market_id}")
            print(f"[{idx}] active       : {active}")
            print(f"[{idx}] closed       : {closed}")
            print(f"[{idx}] endDate      : {end_date}")
            print(f"[{idx}] outcomes     : {outcomes}")
            print(f"[{idx}] clobTokenIds : {clob_token_ids}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))


def main() -> None:
    client = PolymarketREST()

    print("Consultando mercados abiertos...")
    data = client.list_markets(limit=20, closed=False)

    print("\nResumen:")
    pretty_print_markets(data)

    print("\n\nJSON completo truncado a 5000 caracteres:\n")
    raw = json.dumps(data, indent=2, ensure_ascii=False)
    print(raw[:5000])


if __name__ == "__main__":
    main()
