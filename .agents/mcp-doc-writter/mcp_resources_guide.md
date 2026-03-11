# MCP Resources Guide: Building a Mini Pokédex

This guide walks through creating an MCP server that exposes Data Resources using the Model Context Protocol (MCP) and Python's `fastmcp` framework, based on our `main.py` Mini Pokédex example.

## 1. Core Concepts: MCP Resources

In MCP, **Resources** allow a server to expose read-only data to the client. They are analogous to `GET` endpoints in a REST API. Resources are identified by custom URIs (e.g., `poke://starters`).

There are two primary ways to define resources in FastMCP:
- **Static Resources**: Fixed URIs (e.g., `poke://starters`)
- **Dynamic Resources**: URIs with parameters (e.g., `poke://pokemon/{id}`)

## 2. Code Breakdown (`main.py`)

### The FastMCP Instance
```python
from fastmcp import FastMCP
app = FastMCP(name="mini.pokedex-lite")
```
This initializes our MCP server.

### Static Resources (Async)
```python
@app.resource("poke://starters")
async def list_starters() -> str:
    """list all starter pokemon available in this demo"""
    # ... logic returning JSON string
```
The `@app.resource` decorator binds a Python function to a specific URI. We use `async def` and asynchronous operations (like `httpx.AsyncClient` elsewhere) to ensure our server handles requests without blocking, which is a best practice for I/O bound tasks.

### Dynamic Resources (Async)
```python
@app.resource("poke://pokemon/{pokemon_id_or_name}")
async def get_pokemon(pokemon_id_or_name: str) -> str:
    """Get detailed Pokémon information by ID or name."""
    # ... async HTTP request to PokeAPI ...
```
Dynamic resources use path parameters enclosed in braces `{}`. FastMCP automatically parses the URI and passes the parameter `pokemon_id_or_name` to the function. This allows a single endpoint to handle infinite distinct resources!

### Running the Server
```python
if __name__ == "__main__":
    app.run(transport="stdio")
```
For local integration with desktop clients, we use the `stdio` transport. The client and server communicate via standard input/output.

---

## 3. Configuring the MCP Server in Antigravity (Local)

To use this server locally within Antigravity, you need to add it to your MCP configuration file (typically `mcp.json` or `claude_desktop_config.json`).

Here is how you would map the server configuration:

```json
{
  "mcpServers": {
    "pokemon": {
      "command": "python",
      "args": [
        "/absolute/path/to/code/udemy/mcp-crash-course/main.py"
      ],
      "env": {}
    }
  }
}
```

*Note: If your script uses a virtual environment, the `command` should be the absolute path to the Python executable within that virtual environment (e.g., `/path/to/venv/bin/python`). If you're running this from WSL and your UI is on Windows, you might need to structure the command to invoke `wsl.exe`.*

---

## 4. Next Steps: Cloud Deployment and Remote Access

Currently, we are exposing this server locally using `stdio`. What if we want others to access it over the internet?

### Transitioning to SSE (Server-Sent Events)

When deploying to the cloud, `stdio` is no longer viable for remote clients. Instead, MCP uses **SSE (Server-Sent Events)** for HTTP-based communication. 

To convert the script for cloud usage, you change the transport layer:
```python
if __name__ == "__main__":
    # Change transport from "stdio" to "sse"
    app.run(transport="sse", host="0.0.0.0", port=8000)
```

### Cloud Deployment Strategy

1. **Host the App**: Deploy your Python application to a cloud provider like Render, Heroku, AWS ECS, or DigitalOcean App Platform.
2. **Expose the Port**: Ensure port 8000 is exposed to the public internet securely (HTTPS is strongly recommended).
3. **Client Configuration**: Users would configure their MCP clients to connect to your service via an SSE URL instead of a local command.

```json
{
  "mcpServers": {
    "remote-pokemon": {
      "url": "https://your-cloud-app.com/sse",
      "type": "sse"
    }
  }
}
```
*Note: FastMCP handles setting up the SSE and HTTP POST endpoints automatically when `transport="sse"` is used.*

### Sharing with Others
Once hosted via SSE, you can provide the SSE URL to any team member. They simply add the configuration block to their own Antigravity/Claude Desktop JSON, and they immediately gain access to your custom `poke://` resources from within their AI client!
