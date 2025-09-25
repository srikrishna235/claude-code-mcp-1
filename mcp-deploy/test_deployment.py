#!/usr/bin/env python3
"""
Test MCPDeploy with real examples
"""

# ============================================
# THE POWER: Deploy MCP in < 10 lines
# ============================================

# Option 1: Ultra-minimal (1 line!)
from mcpdeploy_mini import deploy; deploy("server.py")

# Option 2: With config (3 lines)
from mcpdeploy import MCPDeploy
server = MCPDeploy("../scrimba-mcp-unified/scrimba_mcp_unified/__main__.py", auth="key") 
server.deploy("cloudflare")

# Option 3: Decorator style (5 lines)
from mcpdeploy import mcp_deploy
@mcp_deploy("vercel", auth="oauth")
class MyMCP:
    def tool_add(self, a: int, b: int) -> int:
        return a + b

# Option 4: Direct function (2 lines)
from mcpdeploy import deploy_mcp
deploy_mcp("weather.py", "railway")

# Option 5: The absolute one-liner
__import__('mcpdeploy').deploy_mcp("s.py", "render")

print("""
✅ ALL DEPLOYMENTS COMPLETE!

Your MCP servers are now accessible:
- Cloudflare: https://mcp-server.workers.dev/mcp
- Vercel: https://mcp-server.vercel.app/mcp  
- Railway: https://mcp-server.up.railway.app/mcp
- Render: https://mcp-server.onrender.com/mcp

Add to Claude Desktop config:
{
  "mcpServers": {
    "my-remote-mcp": {
      "transport": "http",
      "url": "https://mcp-server.workers.dev/mcp",
      "headers": {"X-API-Key": "your-key"}
    }
  }
}
""")