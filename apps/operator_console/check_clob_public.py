import json
import sys

from libs.polymarket_client.rest import PolymarketREST


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso:")
        print("python -m apps.operator_console.check_clob_public <token_id>")
        sys.exit(1)

    token_id = sys.argv[1]
    client = PolymarketREST()

    print("=== ORDERBOOK ===")
    try:
        book = client.get_orderbook(token_id)
        print(json.dumps(book, indent=2, ensure_ascii=False)[:4000])
    except Exception as e:
        print(f"Error orderbook: {e}")

    print("\n=== MIDPOINT ===")
    try:
        midpoint = client.get_midpoint(token_id)
        print(json.dumps(midpoint, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error midpoint: {e}")

    print("\n=== SPREAD ===")
    try:
        spread = client.get_spread(token_id)
        print(json.dumps(spread, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error spread: {e}")

    print("\n=== PRICE (BUY) ===")
    try:
        price = client.get_price(token_id, "BUY")
        print(json.dumps(price, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error price: {e}")

    print("\n=== LAST TRADE PRICE ===")
    try:
        last_trade_price = client.get_last_trade_price(token_id)
        print(json.dumps(last_trade_price, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error last trade price: {e}")

    print("\n=== SERVER TIME ===")
    try:
        server_time = client.get_server_time()
        print(json.dumps(server_time, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error server time: {e}")


if __name__ == "__main__":
    main()
