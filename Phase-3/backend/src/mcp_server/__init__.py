"""
MCP Server Module for Phase-3 AI-Powered Todo Chatbot.

This module exposes stateless task management tools via the Model Context Protocol (MCP).
All tools are invoked by AI agents and execute against Neon PostgreSQL database.
"""

from mcp.server import Server

# MCP server instance
mcp_server = Server("phase-3-task-tools")

__all__ = ["mcp_server", "Server"]
