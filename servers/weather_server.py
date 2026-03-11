from typing import List

from mcp.server import FastMCP

mcp = FastMCP("weather_server")

@mcp.tool()
async def get_weather(location: str) -> str:
    return "hot as hell"

if __name__ == "__main__":
    mcp.run("sse")