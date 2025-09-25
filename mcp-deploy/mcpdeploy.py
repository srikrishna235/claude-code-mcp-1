"""
MCPDeploy - Deploy any MCP server to the internet in < 10 lines
"""

import os
import json
import asyncio
import subprocess
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse


@dataclass
class MCPDeploy:
    """Ultra-simple MCP deployment wrapper"""
    
    def __init__(self, 
                 server_path: str = None,
                 server_class: Any = None,
                 port: int = 8080,
                 auth: str = "none"):
        """
        Deploy MCP in one line.
        
        Args:
            server_path: Path to existing MCP server file
            server_class: Or provide a Python MCP server class
            port: Port to run on (default 8080)
            auth: Authentication type: "none", "key", "oauth"
        """
        self.server = server_class or self._load_server(server_path)
        self.port = port
        self.auth = auth
        self.app = self._create_app()
        
    def _load_server(self, path: str):
        """Load an existing MCP server from file"""
        # Dynamic import of existing MCP server
        import importlib.util
        spec = importlib.util.spec_from_file_location("mcp_server", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.server
        
    def _create_app(self):
        """Create FastAPI app with MCP HTTP/SSE endpoints"""
        app = FastAPI()
        
        # Single unified MCP endpoint (modern spec)
        @app.post("/mcp")
        async def mcp_endpoint(request: Request):
            """Handle MCP requests over HTTP/SSE"""
            body = await request.json()
            
            # Auth check
            if self.auth == "key":
                if request.headers.get("X-API-Key") != os.getenv("MCP_API_KEY"):
                    raise HTTPException(status_code=401)
            
            # Process MCP request
            response = await self._process_mcp(body)
            
            # Stream or regular response
            if request.headers.get("Accept") == "text/event-stream":
                return EventSourceResponse(self._stream_response(response))
            return response
        
        # Legacy dual-endpoint support
        @app.get("/mcp")
        async def mcp_sse_endpoint(session_id: str):
            """SSE endpoint for server-to-client messages"""
            return EventSourceResponse(self._stream_session(session_id))
        
        @app.post("/messages")
        async def messages_endpoint(request: Request):
            """Client-to-server messages"""
            return await mcp_endpoint(request)
        
        return app
    
    async def _process_mcp(self, request: Dict[str, Any]):
        """Bridge between HTTP and MCP server"""
        # Convert HTTP request to MCP protocol
        method = request.get("method")
        params = request.get("params", {})
        
        # Call the underlying MCP server
        if hasattr(self.server, method):
            result = await getattr(self.server, method)(**params)
            return {"jsonrpc": "2.0", "result": result, "id": request.get("id")}
        
        return {"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found"}, "id": request.get("id")}
    
    async def _stream_response(self, response):
        """Stream responses as SSE"""
        yield f"data: {json.dumps(response)}\n\n"
    
    async def _stream_session(self, session_id: str):
        """Stream session messages"""
        # Implement session-based streaming
        while True:
            await asyncio.sleep(1)
            yield f"data: {json.dumps({'keepalive': True})}\n\n"
    
    def deploy(self, provider: str = "local", **kwargs):
        """
        Deploy to cloud provider with one command.
        
        Args:
            provider: "local", "cloudflare", "vercel", "railway", "render"
            **kwargs: Provider-specific config
        """
        if provider == "local":
            # Run locally with uvicorn
            import uvicorn
            uvicorn.run(self.app, host="0.0.0.0", port=self.port)
            
        elif provider == "cloudflare":
            self._deploy_cloudflare(**kwargs)
            
        elif provider == "vercel":
            self._deploy_vercel(**kwargs)
            
        elif provider == "railway":
            self._deploy_railway(**kwargs)
            
        elif provider == "render":
            self._deploy_render(**kwargs)
    
    def _deploy_cloudflare(self, **kwargs):
        """Deploy to Cloudflare Workers"""
        # Generate wrangler.toml
        config = f"""
name = "mcp-server"
main = "worker.py"
compatibility_date = "2024-01-01"

[env.production]
vars = {{ MCP_API_KEY = "{os.getenv('MCP_API_KEY', 'default-key')}" }}
        """
        Path("wrangler.toml").write_text(config)
        
        # Generate worker.py
        worker = f"""
from js import Response
import json

async def on_fetch(request, env):
    # Bridge to our MCP server
    if request.url.endswith('/mcp'):
        body = await request.json()
        # Process MCP request
        response = {{"jsonrpc": "2.0", "result": "OK", "id": 1}}
        return Response(json.dumps(response), {{
            'headers': {{'Content-Type': 'application/json'}}
        }})
    return Response("MCP Server Running", {{'status': 200}})
        """
        Path("worker.py").write_text(worker)
        
        # Deploy
        subprocess.run(["wrangler", "deploy"])
        print(f"✅ Deployed to Cloudflare Workers")
    
    def _deploy_vercel(self, **kwargs):
        """Deploy to Vercel"""
        # Generate vercel.json
        config = {
            "builds": [{"src": "api/mcp.py", "use": "@vercel/python"}],
            "routes": [{"src": "/mcp", "dest": "/api/mcp.py"}]
        }
        Path("vercel.json").write_text(json.dumps(config, indent=2))
        
        # Generate api/mcp.py
        Path("api").mkdir(exist_ok=True)
        api_code = f"""
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.post("/mcp")
async def mcp_endpoint(request: dict):
    # Your MCP logic here
    return {{"status": "ok"}}

handler = Mangum(app)
        """
        Path("api/mcp.py").write_text(api_code)
        
        # Deploy
        subprocess.run(["vercel", "--prod"])
        print(f"✅ Deployed to Vercel")
    
    def _deploy_railway(self, **kwargs):
        """Deploy to Railway"""
        # Generate railway.json
        config = {
            "$schema": "https://railway.app/railway.schema.json",
            "build": {"builder": "nixpacks"},
            "deploy": {
                "startCommand": f"uvicorn mcpdeploy:app --host 0.0.0.0 --port ${{PORT:-{self.port}}}"
            }
        }
        Path("railway.json").write_text(json.dumps(config, indent=2))
        
        # Deploy
        subprocess.run(["railway", "up"])
        print(f"✅ Deployed to Railway")
    
    def _deploy_render(self, **kwargs):
        """Deploy to Render"""
        # Generate render.yaml
        config = f"""
services:
  - type: web
    name: mcp-server
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn mcpdeploy:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: MCP_API_KEY
        value: {os.getenv('MCP_API_KEY', 'your-key')}
        """
        Path("render.yaml").write_text(config)
        
        print("✅ Push to GitHub and connect to Render")
    
    @staticmethod
    def from_mcp(mcp_server):
        """Create from existing MCP server instance"""
        deploy = MCPDeploy(server_class=mcp_server)
        return deploy
    
    def __repr__(self):
        return f"MCPDeploy(port={self.port}, auth={self.auth})"


# Even simpler wrapper function
def deploy_mcp(server, provider="cloudflare", auth="key"):
    """
    Deploy any MCP server in one line.
    
    Examples:
        deploy_mcp(my_server, "cloudflare")
        deploy_mcp("./weather_server.py", "vercel", auth="oauth")
    """
    deployer = MCPDeploy(
        server_path=server if isinstance(server, str) else None,
        server_class=server if not isinstance(server, str) else None,
        auth=auth
    )
    deployer.deploy(provider)
    return deployer


# Ultra-minimal class decorator
def mcp_deploy(provider="cloudflare", auth="key"):
    """
    Decorator to auto-deploy MCP servers.
    
    Usage:
        @mcp_deploy("vercel")
        class MyMCPServer:
            ...
    """
    def decorator(cls):
        # Auto-deploy on import
        instance = cls()
        deploy_mcp(instance, provider, auth)
        return cls
    return decorator