import json
import sys

from libs.polymarket_client.rest import PolymarketREST


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso:")
        print("python -m apps.operator_console.get_market_by_slug <slug>")
        sys.exit(1)

    slug = sys.argv[1]
    client = PolymarketREST()
    data = client.get_market_by_slug(slug)
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
