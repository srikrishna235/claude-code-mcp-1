"""
MCPDeploy - Deploy MCP servers to the internet in < 10 lines
"""

# ============================================
# EXAMPLE 1: Deploy existing MCP server (3 lines)
# ============================================
from mcpdeploy import deploy_mcp

# That's it! Your local MCP server is now on Cloudflare
deploy_mcp("./weather_server.py", "cloudflare")


# ============================================
# EXAMPLE 2: Deploy with decorator (5 lines)
# ============================================
from mcpdeploy import mcp_deploy
from mcp import McpServer

@mcp_deploy("vercel")  # Auto-deploys when defined
class MyServer(McpServer):
    async def get_weather(self, city: str):
        return f"Weather in {city}: Sunny, 72°F"


# ============================================
# EXAMPLE 3: Deploy your existing Scrimba server (3 lines)
# ============================================
from mcpdeploy import MCPDeploy

server = MCPDeploy("../scrimba-mcp-unified/scrimba_mcp_unified/__main__.py")
server.deploy("railway")  # Deployed to Railway!


# ============================================
# EXAMPLE 4: One-liner deployment
# ============================================
MCPDeploy("my_server.py").deploy("render")


# ============================================
# EXAMPLE 5: Deploy with auth (4 lines)
# ============================================
from mcpdeploy import deploy_mcp
import os

os.environ["MCP_API_KEY"] = "secret-key-123"
deploy_mcp("./agent.py", "cloudflare", auth="key")


# ============================================
# EXAMPLE 6: Deploy FastMCP server (6 lines)
# ============================================
from fastmcp import FastMCP
from mcpdeploy import deploy_mcp

mcp = FastMCP("My Tools")
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

deploy_mcp(mcp, "vercel")


# ============================================
# EXAMPLE 7: Ultra-minimal (2 lines!)
# ============================================
from mcpdeploy import MCPDeploy
MCPDeploy("server.py").deploy()  # Local by default


# ============================================
# EXAMPLE 8: Production deployment (7 lines)
# ============================================
from mcpdeploy import MCPDeploy

deployer = MCPDeploy(
    server_path="production_server.py",
    port=8080,
    auth="oauth"
)
deployer.deploy("cloudflare", 
    domain="mcp.mycompany.com",
    env="production")


# ============================================
# EXAMPLE 9: Deploy multiple servers (9 lines)
# ============================================
from mcpdeploy import deploy_mcp

servers = [
    ("weather_mcp.py", "cloudflare"),
    ("database_mcp.py", "vercel"),
    ("ai_agent_mcp.py", "railway"),
]

for server, provider in servers:
    deploy_mcp(server, provider)
print("✅ All MCP servers deployed!")


# ============================================
# EXAMPLE 10: The ULTIMATE one-liner
# ============================================
__import__('mcpdeploy').MCPDeploy("s.py").deploy("cloudflare")