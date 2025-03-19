import dotenv
import os
import httpx
from mcp.server.fastmcp import FastMCP
from typing import Any


dotenv.load_dotenv()
mcp = FastMCP("crewai_enterprise_server")

CREWAI_ENTERPRISE_SERVER_URL = os.getenv("MCP_CREWAI_ENTERPRISE_SERVER_URL")
CREWAI_ENTERPRISE_BEARER_TOKEN = os.getenv("MCP_CREWAI_ENTERPRISE_BEARER_TOKEN")


@mcp.tool()
async def kickoff_crew(inputs: dict[str, Any]) -> dict[str, Any]:
    """Start a new crew task

    Args:
        inputs: Dictionary containing the query and other input parameters

    Returns:
        Dictionary containing the crew task response. The response will contain the crew id which needs to be returned to check the status of the crew.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{CREWAI_ENTERPRISE_SERVER_URL}/kickoff",
            headers={
                "Authorization": f"Bearer {CREWAI_ENTERPRISE_BEARER_TOKEN}",
                "Content-Type": "application/json",
            },
            json={"inputs": inputs},
        )
        response_json = response.json()
        return response_json


@mcp.tool()
async def get_crew_status(crew_id: str) -> dict[str, Any]:
    """Get the status of a crew task

    Args:
        crew_id: The ID of the crew task to check

    Returns:
        Dictionary containing the crew task status
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{CREWAI_ENTERPRISE_SERVER_URL}/status/{crew_id}",
            headers={
                "Authorization": f"Bearer {CREWAI_ENTERPRISE_BEARER_TOKEN}",
                "Content-Type": "application/json",
            },
        )
        return response.json()


if __name__ == "__main__":
    import mcp

    mcp.run()
