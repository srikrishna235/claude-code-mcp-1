#!/bin/bash

# Add scrimba-unified MCP to Claude config
# Uses local directory version, not PyPI

echo "Adding scrimba-unified to Claude config..."

# Update Claude config to use local version
jq '.mcpServers."scrimba-unified" = {
  "command": "python",
  "args": ["-m", "scrimba_mcp_unified"],
  "cwd": "/home/rishabh/Desktop/dev/claude-code-mcp/scrimba-mcp-unified"
}' /home/rishabh/.claude.json > /tmp/claude_updated.json && mv /tmp/claude_updated.json /home/rishabh/.claude.json

echo "✅ Added scrimba-unified to Claude config"
echo ""
echo "⚠️  IMPORTANT: Restart Claude Desktop to see the new MCP server"
echo ""
echo "The server will appear as 'scrimba-unified' in your MCP servers list"