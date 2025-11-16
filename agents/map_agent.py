# agents/map_agent.py

import asyncio
import shutil

from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServerStdio


async def main() -> None:
    if not shutil.which("python"):
        raise RuntimeError("Python executable not found on PATH")

    # Server 1: City POI Explorer (Nominatim)
    poi_server = MCPServerStdio(
        name="City POI Explorer",
        params={
            "command": "python",
            "args": ["-m", "map_servers.city_poi_server"],
        },
    )

    # Server 2: OSRM Routing
    osrm_server = MCPServerStdio(
        name="OSRM Routing Server",
        params={
            "command": "python",
            "args": ["-m", "map_servers.osrm_routing_server"],
        },
    )

    async with poi_server as poi, osrm_server as osrm:
        trace_id = gen_trace_id()
        print(f"Trace URL: https://platform.openai.com/traces/{trace_id}\n")

        with trace(workflow_name="Map Suite Demo", trace_id=trace_id):
            agent = Agent(
                name="CityMapAssistant",
                instructions=(
                    "You are a city mapping assistant. "
                    "Use the City POI Explorer tools to search for restaurants, "
                    "museums, and other POIs, and use the OSRM Routing tools to "
                    "compute routes, distances, and travel times between places. "
                    "When a user asks a mapping-related question, decide which "
                    "server's tools to call and summarize the results clearly."
                ),
                mcp_servers=[poi, osrm],
            )

            # Continuous loop for multiple questions
            while True:
                user_prompt = input("Ask a mapping question (or type exit): ")

                if user_prompt.lower().strip() in ["exit", "quit", "q"]:
                    print("Goodbye!")
                    break

                result = await Runner.run(starting_agent=agent, input=user_prompt)

                print("\n=== Final Answer ===\n")
                print(result.final_output)
                print("\n----------------------------------------\n")


if __name__ == "__main__":
    asyncio.run(main())
