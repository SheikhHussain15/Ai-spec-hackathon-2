"""
MCP Server Runner with stdio transport.

This module initializes and runs the MCP server with proper database connection handling.
Designed for stateless, serverless-compatible deployment.
"""

import asyncio
from mcp.server import stdio_server
from src.mcp_server import mcp_server
from src.mcp_server.tools import register_all_tools


async def main():
    """Run the MCP server with stdio transport."""
    # Register all tools before starting server
    register_all_tools(mcp_server)
    
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
