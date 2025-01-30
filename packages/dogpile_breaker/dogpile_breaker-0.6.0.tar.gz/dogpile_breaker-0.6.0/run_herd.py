import asyncio
import math
import random

import httpx


async def get_(client: httpx.AsyncClient) -> httpx.Response:
    sleep_param = round(random.random() * (4 - 0.1) + 0.1, 1)
    return await client.get(f"http://127.0.0.1:8000/sleep?sleep_for={sleep_param}")


async def main():
    async with httpx.AsyncClient() as client:
        tasks = [get_(client) for _ in range(100)]
        result = await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
