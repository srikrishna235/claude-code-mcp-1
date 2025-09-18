#!/bin/bash
# Start both Claude Code MCP server and Terminal interface

echo "Starting Claude Code Terminal..."
echo "================================"

# Kill any existing processes on ports
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:8080 | xargs kill -9 2>/dev/null

sleep 1

echo "1. Starting MCP server on port 8000..."
python claude_code_mcp_final.py &
MCP_PID=$!

sleep 2

echo "2. Starting Terminal server on port 8080..."
python terminal_server.py --port 8080 &
TERMINAL_PID=$!

sleep 2

echo ""
echo "Services started successfully!"
echo "==============================="
echo "MCP Server: http://127.0.0.1:8000/mcp (PID: $MCP_PID)"
echo "Terminal:   http://127.0.0.1:8080 (PID: $TERMINAL_PID)"
echo ""
echo "Open your browser at: http://127.0.0.1:8080"
echo ""
echo "Press Ctrl+C to stop all services"

# Trap Ctrl+C to kill both processes
trap "echo 'Stopping services...'; kill $MCP_PID $TERMINAL_PID; exit" INT

# Wait for processes
wait