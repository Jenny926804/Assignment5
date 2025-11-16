import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import asyncio
from fastmcp import Client
from map_servers.city_poi_server import mcp


async def _run_search_poi():
    print("Running POI search test...")
    async with Client(mcp) as client:
        res = await client.call_tool(
            "search_poi",
            {"city": "Beirut", "query": "pharmacy", "limit": 3},
        )

        print("Search POI Result:", res.data)

        assert "results" in res.data
        assert isinstance(res.data["results"], list)


async def _run_find_restaurants():
    print("Running restaurant search test...")
    async with Client(mcp) as client:
        res = await client.call_tool(
            "find_restaurants",
            {"city": "Rome", "cuisine": "pizza", "limit": 3},
        )

        print("Find Restaurants Result:", res.data)

        assert "results" in res.data


def test_search_poi():
    asyncio.run(_run_search_poi())


def test_find_restaurants():
    asyncio.run(_run_find_restaurants())


if __name__ == "__main__":
    test_search_poi()
    test_find_restaurants()
