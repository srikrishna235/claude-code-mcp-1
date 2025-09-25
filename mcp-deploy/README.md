# 🚀 MCPDeploy - Deploy MCP to Internet in < 10 Lines

**Problem**: MCP servers are powerful but complex to deploy remotely. You need HTTP/SSE transport, OAuth, state management, cloud configs...

**Solution**: MCPDeploy - A wrapper that makes MCP deployment trivial.

## Install

```bash
pip install mcpdeploy
```

## Deploy in 3 Lines

```python
from mcpdeploy import deploy_mcp

# Your local MCP server → Internet
deploy_mcp("./my_server.py", "cloudflare")
```

**That's it.** Your MCP server is now live at `https://your-project.workers.dev/mcp`

## Why MCPDeploy?

### Before (50+ lines, multiple files)
- Configure HTTP/SSE transport
- Implement OAuth flow
- Write Cloudflare worker config
- Handle session management
- Deploy manually

### After (3 lines)
```python
from mcpdeploy import MCPDeploy
server = MCPDeploy("server.py")
server.deploy("cloudflare")
```

## Features

✅ **Any MCP → HTTP**: Converts stdio MCP to HTTP/SSE automatically  
✅ **Multi-Cloud**: Cloudflare, Vercel, Railway, Render  
✅ **Auth Built-in**: API keys, OAuth, or none  
✅ **State Persistence**: Handles stateful servers  
✅ **Zero Config**: Smart defaults, override when needed  

## Examples

### Deploy Existing Server
```python
deploy_mcp("./weather_mcp.py", "vercel")
```

### Deploy with Decorator
```python
@mcp_deploy("cloudflare")
class MyMCP:
    def get_data(self): 
        return "data"
```

### Deploy with Auth
```python
deploy_mcp("agent.py", "railway", auth="oauth")
```

### One-Liner
```python
MCPDeploy("s.py").deploy()
```

## Supported Providers

| Provider | Deploy Time | Free Tier | Command |
|----------|------------|-----------|---------|
| Cloudflare | ~30s | 100k req/day | `deploy("cloudflare")` |
| Vercel | ~45s | Unlimited | `deploy("vercel")` |
| Railway | ~60s | $5 credit | `deploy("railway")` |
| Render | ~2min | 750 hrs/mo | `deploy("render")` |
| Local | Instant | Unlimited | `deploy("local")` |

## How It Works

1. **Wraps your MCP server** with FastAPI HTTP endpoints
2. **Auto-generates configs** for your chosen platform
3. **Deploys with one command** using platform CLIs
4. **Returns live URL** ready for Claude

## Advanced Usage

### Custom Configuration
```python
deployer = MCPDeploy(
    server_path="prod_server.py",
    port=8080,
    auth="oauth"
)
deployer.deploy("cloudflare", 
    domain="api.company.com",
    workers_config={...})
```

### Multiple Servers
```python
servers = ["db.py", "ai.py", "tools.py"]
for s in servers:
    deploy_mcp(s, "vercel")
```

### From Existing Instance
```python
from fastmcp import FastMCP

mcp = FastMCP("Tools")
@mcp.tool()
def calculate(x: int) -> int:
    return x * 2

MCPDeploy.from_mcp(mcp).deploy("cloudflare")
```

## Architecture

```
Your MCP Server (stdio)
        ↓
   MCPDeploy Wrapper
        ↓
  HTTP/SSE Transport
        ↓
   Cloud Provider
        ↓
  Claude Can Access!
```

## The Magic

MCPDeploy handles:
- **Transport bridging** (stdio → HTTP/SSE)
- **Protocol translation** (MCP ↔ HTTP)
- **Authentication** (API keys, OAuth)
- **State management** (sessions, persistence)
- **Platform configs** (wrangler.toml, vercel.json, etc.)
- **Deployment automation** (CLI commands)

All in < 200 lines of code.

## Quick Start

1. Have an MCP server
2. Install: `pip install mcpdeploy`
3. Deploy: `deploy_mcp("server.py", "cloudflare")`
4. Share URL with Claude users

## FAQ

**Q: Does it work with any MCP server?**  
A: Yes, stdio-based or HTTP-based.

**Q: Do I need cloud accounts?**  
A: Yes, free tiers work fine.

**Q: Can I customize the deployment?**  
A: Yes, full control via kwargs.

**Q: Is it production ready?**  
A: It's a wrapper - your MCP server's stability matters.

## License

MIT - Deploy freely!

---

**Made MCP deployment boring.** 🎉