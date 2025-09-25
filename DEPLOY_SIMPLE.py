#!/usr/bin/env python3
"""
SIMPLEST Railway Deployment - Run this one file!
"""

import subprocess
import os
import json
from pathlib import Path
from getpass import getpass

def deploy():
    """One-command deployment to Railway"""
    
    print("🚀 Scrimba MCP → Railway Deployment\n")
    
    # Get token securely
    token = getpass("Paste your NEW Railway token (hidden): ")
    os.environ["RAILWAY_TOKEN"] = token
    
    # Prepare for deployment
    print("\n📦 Preparing deployment...")
    
    # Create deployment package
    deploy_dir = Path("scrimba-mcp-unified")
    
    # Add Railway config
    config = {
        "build": {"builder": "NIXPACKS"},
        "deploy": {
            "startCommand": "uvicorn scrimba_mcp_unified.__main__:app --host 0.0.0.0 --port $PORT",
            "region": "us-west1",
            "healthcheckPath": "/health"
        }
    }
    
    (deploy_dir / "railway.json").write_text(json.dumps(config, indent=2))
    
    # Create simple HTTP wrapper
    wrapper = '''
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import your existing MCP server
from scrimba_mcp_unified import scrimba_agent

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/mcp")
async def mcp_endpoint(request: dict):
    """Bridge to MCP tools"""
    prompt = request.get("prompt", "")
    mode = request.get("mode", "auto")
    result = await scrimba_agent(prompt=prompt, mode=mode)
    return JSONResponse({"result": result})

# Make it importable
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
'''
    
    (deploy_dir / "app.py").write_text(wrapper)
    
    # Update requirements
    reqs = """
fastmcp>=0.5.0
fastapi>=0.100.0
uvicorn>=0.23.0
sse-starlette>=1.6.0
httpx>=0.24.0
mcp>=1.0.0
anthropic>=0.39.0
"""
    (deploy_dir / "requirements.txt").write_text(reqs)
    
    # Deploy
    print("\n🚂 Deploying to Railway...")
    os.chdir(deploy_dir)
    
    try:
        # Login and deploy
        subprocess.run(["railway", "login", "--browserless"], check=True)
        result = subprocess.run(["railway", "up", "--detach"], 
                              capture_output=True, text=True, check=True)
        
        print("\n✅ SUCCESS! Deployment started!")
        print("\n📋 Next steps:")
        print("1. Go to https://railway.app/dashboard")
        print("2. Click on your deployment to get the URL")
        print("3. Add to Claude Desktop config:")
        print("""
{
  "mcpServers": {
    "scrimba-teaching": {
      "transport": "http",
      "url": "https://YOUR-APP.up.railway.app/mcp"
    }
  }
}
        """)
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error: {e}")
        print("Make sure Railway CLI is installed:")
        print("curl -fsSL https://railway.app/install.sh | sh")
    
    except FileNotFoundError:
        print("\n❌ Railway CLI not found!")
        print("Installing...")
        os.system("curl -fsSL https://railway.app/install.sh | sh")
        print("\n✅ Installed! Run this script again.")

if __name__ == "__main__":
    deploy()