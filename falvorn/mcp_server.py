"""Optional MCP stdio server adapter. Requires: pip install 'mcp>=1.0,<2'."""
import os
from .sdk import FalvornClient

try:
    from mcp.server.fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("MCP extra not installed: pip install 'mcp>=1.0,<2'") from exc

mcp = FastMCP("falvorn-ai")

def client():
    return FalvornClient(os.getenv("FALVORN_BASE_URL", "http://127.0.0.1:8000"),
                          os.getenv("FALVORN_API_KEY", ""))

@mcp.tool()
def search_web(query: str) -> dict:
    """Search the live web with a configured SearXNG backend."""
    with client() as c:
        return c.search(query)

@mcp.tool()
def fetch_page(url: str) -> dict:
    """Extract clean page content from an HTTP(S) URL."""
    with client() as c:
        return c.fetch(url)

@mcp.tool()
def run_web_agent(url: str, goal: str) -> dict:
    """Start a safe, bounded browser-agent run. Returns a run ID to poll."""
    with client() as c:
        return c.start_agent(url, goal)

@mcp.tool()
def get_web_agent_run(run_id: str) -> dict:
    """Get task execution status, events and final answer."""
    with client() as c:
        return c.get_run(run_id)

@mcp.tool()
def check_webpage_change(url: str) -> dict:
    """Compare current page content against the previous stored check."""
    with client() as c:
        return c.monitor(url)

if __name__ == "__main__":
    mcp.run(transport="stdio")
