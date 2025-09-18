#!/usr/bin/env python3
"""Serve the streaming terminal HTML"""

import http.server
import socketserver

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/terminal_streaming.html'
        return super().do_GET()

PORT = 8081
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Streaming Terminal Server running at http://127.0.0.1:{PORT}")
    httpd.serve_forever()