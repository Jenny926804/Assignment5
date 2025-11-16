# map_servers/city_poi_server.py

import httpx
from fastmcp import FastMCP

mcp = FastMCP(name="city-poi-explorer")

BASE_URL = "https://nominatim.openstreetmap.org"
HEADERS = {
    "User-Agent": "city-poi-mcp/1.0 (jenni.hadad@gmail.com)",
}


async def _get_json(path: str, params: dict):
    async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
        resp = await client.get(f"{BASE_URL}{path}", params=params)
        resp.raise_for_status()
        return resp.json()


def _normalize_poi(item: dict) -> dict:
    """
    Normalize a Nominatim search result to a consistent POI structure.
    """
    return {
        "name": item.get("name") or item.get("display_name"),
        "lat": float(item["lat"]),
        "lon": float(item["lon"]),
        "type": item.get("type"),
        "category": item.get("category"),
        "display_name": item.get("display_name"),
    }


@mcp.tool()
async def search_poi(city: str, query: str, limit: int = 10):
    """
    Generic POI search within a city.

    Args:
        city: City name, e.g. "Paris".
        query: What to search for, e.g. "pharmacy", "pizza", "university".
        limit: Max number of results.
    """
    q = f"{query} in {city}"
    data = await _get_json(
        "/search",
        {
            "q": q,
            "format": "jsonv2",
            "limit": limit,
        },
    )
    pois = [_normalize_poi(item) for item in data]
    return {"city": city, "query": query, "results": pois}


@mcp.tool()
async def find_restaurants(city: str, cuisine: str | None = None, limit: int = 10):
    """
    Improved restaurant search with fallback strategies since OSM cuisine tags
    are often missing (especially in cities like Beirut).

    Strategy:
    1. Try: "{cuisine} restaurant in {city}"
    2. If empty → Try: "restaurant {cuisine} in {city}"
    3. If still empty → Generic: "restaurant in {city}"
    """

    queries = []

    # Step 1: Strict query
    if cuisine:
        queries.append(f"{cuisine} restaurant in {city}")

    # Step 2: Broader keyword search
        queries.append(f"restaurant {cuisine} in {city}")

    # Step 3: Fallback to generic restaurants
    queries.append(f"restaurant in {city}")

    for q in queries:
        data = await _get_json(
            "/search",
            {
                "q": q,
                "format": "jsonv2",
                "limit": limit,
            },
        )
        pois = [_normalize_poi(item) for item in data]
        if pois:  # Return first successful result
            return {"city": city, "cuisine": cuisine, "results": pois}

    # If absolutely nothing found (unlikely with fallback)
    return {"city": city, "cuisine": cuisine, "results": []}



@mcp.tool()
async def find_museums(city: str, limit: int = 10):
    """
    Find museums and cultural attractions in a city.

    Args:
        city: City name.
        limit: Max number of results.
    """
    q = f"museum in {city}"
    data = await _get_json(
        "/search",
        {
            "q": q,
            "format": "jsonv2",
            "limit": limit,
        },
    )
    pois = [_normalize_poi(item) for item in data]
    return {"city": city, "results": pois}


if __name__ == "__main__":
    # Run as an MCP stdio server
    mcp.run()
