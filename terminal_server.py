#!/usr/bin/env python3
"""
Simple HTTP server to host the Claude Code Terminal interface
Serves the HTML file and handles CORS for MCP server communication
"""

import http.server
import socketserver
import os
import sys
from urllib.parse import urlparse

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        """Serve files with proper MIME types"""
        # Default to terminal.html for root path
        if self.path == '/':
            self.path = '/terminal.html'
        
        return super().do_GET()

def run_server(port=8080):
    """Run the terminal server"""
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    Handler = CORSHTTPRequestHandler
    
    print(f"Claude Code Terminal Server")
    print(f"=" * 40)
    print(f"Serving at: http://127.0.0.1:{port}")
    print(f"")
    print(f"Steps to use:")
    print(f"1. Make sure MCP server is running:")
    print(f"   python claude_code_mcp_final.py")
    print(f"")
    print(f"2. Open browser at:")
    print(f"   http://127.0.0.1:{port}")
    print(f"")
    print(f"Press Ctrl+C to stop")
    print(f"-" * 40)
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            sys.exit(0)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Code Terminal Server")
    parser.add_argument("--port", type=int, default=8080, help="Port to serve on")
    args = parser.parse_args()
    
    run_server(args.port)