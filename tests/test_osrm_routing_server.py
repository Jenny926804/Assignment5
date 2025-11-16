import asyncio
from fastmcp import Client
from map_servers.osrm_routing_server import mcp


async def _run_route():
    print("Running route test...")

    async with Client(mcp) as client:
        res = await client.call_tool(
            "route",
            {
                "start_lat": 48.8584,
                "start_lon": 2.2945,
                "end_lat": 48.8606,
                "end_lon": 2.3376,
                "profile": "driving",
            },
        )

        print("Route Result:", res.data)

        assert "distance_m" in res.data
        assert "duration_s" in res.data


async def _run_nearest():
    print("Running nearest test...")

    async with Client(mcp) as client:
        res = await client.call_tool(
            "nearest_routable",
            {"lat": 48.8584, "lon": 2.2945, "profile": "driving"},
        )

        print("Nearest Result:", res.data)

        assert "snapped" in res.data


def test_route():
    asyncio.run(_run_route())


def test_nearest():
    asyncio.run(_run_nearest())


if __name__ == "__main__":
    test_route()
    test_nearest()
