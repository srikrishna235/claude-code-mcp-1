#!/bin/bash
# Start Claude Code MCP server with CORS proxy for browser access

echo "Starting Claude Code Terminal with CORS support..."
echo "================================================="

# Kill any existing processes on ports
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:8001 | xargs kill -9 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null

sleep 1

echo "1. Starting MCP server on port 8001 (internal)..."
python claude_code_mcp_final.py --port 8001 &
MCP_PID=$!

sleep 2

echo "2. Starting CORS proxy on port 8000 (public)..."
python cors_proxy.py --port 8000 --mcp-port 8001 &
PROXY_PID=$!

sleep 2

echo "3. Starting Terminal server on port 8080..."
python terminal_server.py --port 8080 &
TERMINAL_PID=$!

sleep 2

echo ""
echo "Services started successfully!"
echo "=============================="
echo "MCP Server:   http://127.0.0.1:8001/mcp (PID: $MCP_PID) - Internal"
echo "CORS Proxy:   http://127.0.0.1:8000/mcp (PID: $PROXY_PID) - For browser"
echo "Terminal UI:  http://127.0.0.1:8080 (PID: $TERMINAL_PID)"
echo ""
echo "Open your browser at: http://127.0.0.1:8080"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C to kill all processes
trap "echo 'Stopping services...'; kill $MCP_PID $PROXY_PID $TERMINAL_PID 2>/dev/null; exit" INT

# Wait for processes
wait