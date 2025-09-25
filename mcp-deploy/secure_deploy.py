#!/usr/bin/env python3
"""
SECURE Railway deployment for MCP - Never expose tokens!
"""

import os
import subprocess
import json
from pathlib import Path

def secure_deploy_to_railway():
    """Deploy to Railway using environment variable for token"""
    
    # STEP 1: Check for token in environment (never hardcode!)
    token = os.environ.get("RAILWAY_TOKEN")
    if not token:
        print("""
        ❌ RAILWAY_TOKEN not found!
        
        To deploy securely:
        1. Get new token from https://railway.app/account/tokens
        2. Set it as environment variable:
           
           export RAILWAY_TOKEN="your-token-here"
           
        3. Run this script again
        
        NEVER put tokens in code or share them!
        """)
        return False
    
    # STEP 2: Create Railway configuration
    railway_config = {
        "build": {
            "builder": "NIXPACKS",
            "buildCommand": "pip install -r requirements.txt"
        },
        "deploy": {
            "startCommand": "python -m scrimba_mcp_unified",
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 3
        },
        "services": [{
            "name": "scrimba-mcp-server",
            "source": {
                "repo": "."
            }
        }]
    }
    
    Path("railway.json").write_text(json.dumps(railway_config, indent=2))
    
    # STEP 3: Create Nixpacks config for Python
    nixpacks_config = """
[phases.setup]
nixPkgs = ["python311", "gcc"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[start]
cmd = "uvicorn scrimba_mcp_unified:app --host 0.0.0.0 --port $PORT"
    """
    Path("nixpacks.toml").write_text(nixpacks_config)
    
    # STEP 4: Create requirements for deployment
    requirements = """
fastmcp>=0.5.0
fastapi>=0.100.0
uvicorn>=0.23.0
sse-starlette>=1.6.0
httpx>=0.24.0
python-multipart>=0.0.6
mcp>=1.0.0
    """
    Path("requirements.txt").write_text(requirements)
    
    # STEP 5: Deploy using Railway CLI (token from env)
    try:
        # Railway CLI will use RAILWAY_TOKEN from environment
        result = subprocess.run(
            ["railway", "up", "--service", "scrimba-mcp-server"],
            capture_output=True,
            text=True,
            check=True
        )
        
        print("✅ Deployment initiated successfully!")
        print("\nNext steps:")
        print("1. Check deployment at: https://railway.app/dashboard")
        print("2. Get your URL from Railway dashboard")
        print("3. Add to Claude config:")
        print("""
{
  "mcpServers": {
    "scrimba-remote": {
      "transport": "http",
      "url": "https://YOUR-APP.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer YOUR-MCP-API-KEY"
      }
    }
  }
}
        """)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Deployment failed: {e.stderr}")
        return False
    except FileNotFoundError:
        print("""
        ❌ Railway CLI not found!
        
        Install it first:
        - Mac/Linux: curl -fsSL https://railway.app/install.sh | sh
        - Windows: npm install -g @railway/cli
        """)
        return False

if __name__ == "__main__":
    # Check for token in .env file as backup
    if os.path.exists(".env"):
        from dotenv import load_dotenv
        load_dotenv()
    
    secure_deploy_to_railway()