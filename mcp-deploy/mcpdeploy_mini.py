"""
MCPDeploy Mini - The absolute minimum code to deploy MCP
"""
import subprocess as sp, json, os
from pathlib import Path as P

def deploy(server, cloud="cloudflare"):
    """Deploy any MCP server in ONE line: deploy('server.py')"""
    if cloud == "cloudflare":
        P("w.toml").write_text(f'name="mcp"\nmain="w.py"')
        P("w.py").write_text(f'from js import Response\nexec(open("{server}").read())')
        sp.run(["wrangler", "deploy"])
    elif cloud == "vercel":
        P("vercel.json").write_text('{"builds":[{"src":"*.py","use":"@vercel/python"}]}')
        sp.run(["vercel", "--prod"])
    elif cloud == "railway":
        sp.run(["railway", "up"])
    return f"✅ Deployed to {cloud}"

# ONE-LINER: deploy('my_server.py')
# That's it. Your MCP is on the internet.