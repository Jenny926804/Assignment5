# map_servers/osrm_routing_server.py

import httpx
from fastmcp import FastMCP

mcp = FastMCP(name="osrm-routing")

OSRM_BASE = "https://router.project-osrm.org"  # OSRM public demo server


async def _osrm_get(path: str, params: dict) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(f"{OSRM_BASE}{path}", params=params)
        resp.raise_for_status()
        return resp.json()


@mcp.tool()
async def route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float,
    profile: str = "driving",
):
    """
    Compute a route between two coordinates using OSRM.

    Returns distance (meters), duration (seconds), and GeoJSON geometry.
    """
    coords = f"{start_lon},{start_lat};{end_lon},{end_lat}"
    data = await _osrm_get(
        f"/route/v1/{profile}/{coords}",
        {"overview": "full", "geometries": "geojson"},
    )
    route0 = data["routes"][0]
    return {
        "profile": profile,
        "distance_m": route0["distance"],
        "duration_s": route0["duration"],
        "geometry": route0["geometry"],  # GeoJSON LineString
    }


@mcp.tool()
async def distance_matrix(
    lats: list[float],
    lons: list[float],
    profile: str = "driving",
):
    """
    Build a travel-time and distance matrix for a list of locations.

    Args:
        lats, lons: Lists of equal length with coordinates.
        profile: "driving", "cycling", or "walking" (if supported).
    """
    if len(lats) != len(lons):
        raise ValueError("lats and lons must have the same length")

    coords = ";".join(f"{lon},{lat}" for lat, lon in zip(lats, lons))
    data = await _osrm_get(
        f"/table/v1/{profile}/{coords}",
        {"annotations": "duration,distance"},
    )
    return {
        "profile": profile,
        "durations": data.get("durations"),
        "distances": data.get("distances"),
    }


@mcp.tool()
async def nearest_routable(lat: float, lon: float, profile: str = "driving"):
    """
    Snap a coordinate to the nearest routable point on the OSRM network.

    Useful when the original coordinate is off-road or noisy.
    """
    coord = f"{lon},{lat}"
    data = await _osrm_get(
        f"/nearest/v1/{profile}/{coord}",
        {"number": 1},
    )
    wp = data["waypoints"][0]
    snapped_lat, snapped_lon = wp["location"][1], wp["location"][0]
    return {
        "input": {"lat": lat, "lon": lon},
        "snapped": {"lat": snapped_lat, "lon": snapped_lon},
        "name": wp.get("name"),
        "distance_m": wp.get("distance"),
    }


if __name__ == "__main__":
    # Run as an MCP stdio server
    mcp.run()
