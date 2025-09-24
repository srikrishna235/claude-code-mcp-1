"""
Scrimba MCP Unified - Complete interactive programming education platform
Includes teaching, visual learning, code visualization, and project components
"""

__version__ = "3.0.0"
__author__ = "Scrimba Teaching System"
__description__ = "Unified MCP server for interactive programming education with Scrimba's methodology"

# Export main server functionality
from .server import main, mcp

__all__ = ["main", "mcp"]