#!/usr/bin/env python3
"""
CORS Proxy for MCP Server
Adds proper CORS support for browser access
"""

from flask import Flask, request, jsonify, Response
import requests
import json

app = Flask(__name__)

# MCP server backend
MCP_BACKEND = "http://127.0.0.1:8000/mcp"

@app.route('/mcp', methods=['OPTIONS', 'POST', 'GET'])
def proxy():
    # Handle preflight
    if request.method == 'OPTIONS':
        response = Response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Accept, Mcp-Session-Id'
        response.headers['Access-Control-Expose-Headers'] = 'Mcp-Session-Id, mcp-session-id'
        return response, 200
    
    # Proxy actual requests
    try:
        # Forward headers
        headers = {
            'Content-Type': request.headers.get('Content-Type', 'application/json'),
            'Accept': request.headers.get('Accept', 'application/json, text/event-stream')
        }
        
        # Include session ID if present
        session_id = request.headers.get('Mcp-Session-Id')
        if session_id:
            headers['Mcp-Session-Id'] = session_id
        
        # Forward the request
        if request.method == 'POST':
            backend_response = requests.post(
                MCP_BACKEND,
                headers=headers,
                data=request.data,
                stream=True
            )
        else:
            backend_response = requests.get(
                MCP_BACKEND,
                headers=headers,
                stream=True
            )
        
        # Create response
        def generate():
            for chunk in backend_response.iter_content(chunk_size=1024):
                if chunk:
                    yield chunk
        
        response = Response(
            generate(),
            status=backend_response.status_code,
            headers=dict(backend_response.headers)
        )
        
        # Add CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Expose-Headers'] = 'Mcp-Session-Id, mcp-session-id'
        
        return response
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("CORS Proxy for MCP Server")
    print("=========================")
    print("Proxying: http://127.0.0.1:8000/mcp")
    print("Listening on: http://127.0.0.1:8001/mcp")
    print("")
    print("Update terminal.html to use port 8001")
    
    app.run(host='127.0.0.1', port=8001, debug=False)