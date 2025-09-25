#!/usr/bin/env python3
"""
Deploy your Scrimba MCP server to the internet in 3 lines!
"""

from mcpdeploy import deploy_mcp

# Deploy your existing Scrimba teaching server to Cloudflare
deploy_mcp("../scrimba-mcp-unified/scrimba_mcp_unified/__main__.py", "cloudflare", auth="key")

# That's it! Your server is now available at:
# https://scrimba-mcp.workers.dev/mcp

# Users can now add this to their Claude desktop config:
# {
#   "mcpServers": {
#     "scrimba-remote": {
#       "transport": "http",
#       "url": "https://scrimba-mcp.workers.dev/mcp",
#       "headers": {
#         "X-API-Key": "your-api-key"
#       }
#     }
#   }
# }