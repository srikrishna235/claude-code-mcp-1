#!/bin/bash
echo "Starting Phase 1 servers..."
echo ""
echo "2. Starting terminal server..."
python terminal_server.py &
WEB_PID=$!
echo "   Web Server PID: $WEB_PID"

echo ""
echo "Server running!"
echo "Open browser at: http://localhost:8080"
echo ""
echo "To stop server:"
echo "  kill $WEB_PID"
