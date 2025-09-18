#!/usr/bin/env python3
"""
Async CORS Proxy for MCP Server with SSE Streaming Support
Forwards Server-Sent Events without buffering
"""

from aiohttp import web, ClientSession
import aiohttp
import asyncio

# MCP server backend
MCP_BACKEND = "http://127.0.0.1:8000/mcp"

async def proxy_handler(request):
    """Handle proxy requests with proper SSE streaming"""
    
    # CORS preflight handling
    if request.method == 'OPTIONS':
        return web.Response(
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Expose-Headers': 'Mcp-Session-Id, mcp-session-id',
            }
        )
    
    # Prepare headers for backend request
    headers = {}
    for key, value in request.headers.items():
        # Skip host header, keep others
        if key.lower() not in ['host', 'content-length']:
            headers[key] = value
    
    async with ClientSession() as session:
        # Read request body if POST
        body = None
        if request.method == 'POST':
            body = await request.read()
        
        # Make request to backend
        async with session.request(
            method=request.method,
            url=MCP_BACKEND,
            headers=headers,
            data=body,
            timeout=aiohttp.ClientTimeout(total=300)  # 5 min timeout
        ) as backend_response:
            
            # Check if this is an SSE stream
            is_sse = 'text/event-stream' in backend_response.headers.get('content-type', '')
            
            if is_sse:
                # Stream SSE response
                response = web.StreamResponse(
                    status=backend_response.status,
                    headers={
                        'Content-Type': 'text/event-stream',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'X-Accel-Buffering': 'no',  # Disable nginx buffering
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Credentials': 'true',
                        'Access-Control-Expose-Headers': 'Mcp-Session-Id, mcp-session-id',
                    }
                )
                
                # Copy session ID header if present
                if 'mcp-session-id' in backend_response.headers:
                    response.headers['mcp-session-id'] = backend_response.headers['mcp-session-id']
                
                await response.prepare(request)
                
                # Stream chunks without buffering
                async for chunk in backend_response.content.iter_any():
                    await response.write(chunk)
                    # Force flush after each chunk for real-time updates
                    await response.drain()
                
                await response.write_eof()
                return response
                
            else:
                # Non-streaming response
                body = await backend_response.read()
                
                # Build response headers with CORS
                response_headers = dict(backend_response.headers)
                response_headers['Access-Control-Allow-Origin'] = '*'
                response_headers['Access-Control-Allow-Credentials'] = 'true'
                response_headers['Access-Control-Expose-Headers'] = 'Mcp-Session-Id, mcp-session-id'
                
                return web.Response(
                    body=body,
                    status=backend_response.status,
                    headers=response_headers
                )

async def init_app():
    """Initialize the aiohttp application"""
    app = web.Application()
    
    # Add routes - catch all paths
    app.router.add_route('*', '/{path:.*}', proxy_handler)
    
    return app

if __name__ == '__main__':
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Async CORS Proxy for MCP Server")
    parser.add_argument("--port", type=int, default=8001, help="Proxy port")
    parser.add_argument("--mcp-port", type=int, default=8000, help="MCP server port")
    
    args = parser.parse_args()
    
    # Update backend URL if custom port
    if args.mcp_port != 8000:
        MCP_BACKEND = f"http://127.0.0.1:{args.mcp_port}/mcp"
    
    print(f"Async CORS Proxy for MCP Server (SSE Streaming)", file=sys.stderr)
    print(f"===============================================", file=sys.stderr)
    print(f"Proxy listening on: http://127.0.0.1:{args.port}/mcp", file=sys.stderr)
    print(f"Forwarding to MCP: {MCP_BACKEND}", file=sys.stderr)
    print(f"Features: Real-time SSE streaming without buffering", file=sys.stderr)
    print(f"", file=sys.stderr)
    
    # Run the server
    app = asyncio.run(init_app())
    web.run_app(app, host='127.0.0.1', port=args.port, print=None)