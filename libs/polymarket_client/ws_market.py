import json
import asyncio

import websockets

WS_URL = "wss://ws-subscriptions-clob.polymarket.com/ws/market"


async def stream_market(asset_ids: list[str], on_message):
    payload = {
        "type": "market",
        "assets_ids": asset_ids,
        "initial_dump": True,
    }

    async with websockets.connect(
        WS_URL,
        ping_interval=20,
        ping_timeout=20,
        close_timeout=10,
        max_size=2**20,
    ) as ws:
        await ws.send(json.dumps(payload))
        print(f"Suscrito a market WS con assets_ids={asset_ids}")

        async def ping_loop() -> None:
            while True:
                await asyncio.sleep(50)
                await ws.send("PING")

        ping_task = asyncio.create_task(ping_loop())

        try:
            while True:
                raw_msg = await ws.recv()
                await on_message(raw_msg)
        finally:
            ping_task.cancel()