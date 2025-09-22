#!/usr/bin/env python3
"""
Phase 1: Basic MCP Bridge - Following Progressive Enhancement
Simple subprocess management for MCP server communication
"""

import subprocess
import json
import threading
import queue
import uuid
from typing import Optional, Dict, Any

class MCPBridge:
    """Manages MCP server subprocess and stdio communication"""
    
    def __init__(self):
        self.process = None
        self.request_queue = {}
        self.response_queue = queue.Queue()
        self.reader_thread = None
        
    def start(self):
        """Phase 1: Start MCP server subprocess"""
        if self.process:
            return
            
        # Start MCP server
        self.process = subprocess.Popen(
            ['python', '-m', 'scrimba_teaching_mcp'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Start reader thread
        self.reader_thread = threading.Thread(target=self._read_output)
        self.reader_thread.daemon = True
        self.reader_thread.start()
        
        # Initialize connection
        self._initialize_mcp()
        
    def _initialize_mcp(self):
        """Send initialization handshake"""
        init_msg = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "api-bridge",
                    "version": "1.0.0"
                }
            }
        }
        response = self._send_request(init_msg)
        return response
        
    def _read_output(self):
        """Read MCP server output continuously"""
        while self.process and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                if line:
                    # Parse JSON-RPC response
                    try:
                        msg = json.loads(line)
                        if 'id' in msg and msg['id'] in self.request_queue:
                            # Match response to request
                            self.request_queue[msg['id']].put(msg)
                    except json.JSONDecodeError:
                        continue
            except Exception as e:
                print(f"Reader error: {e}")
                break
                
    def _send_request(self, message: Dict) -> Dict:
        """Send request and wait for response"""
        msg_id = message.get('id', str(uuid.uuid4()))
        message['id'] = msg_id
        
        # Create response queue for this request
        response_queue = queue.Queue()
        self.request_queue[msg_id] = response_queue
        
        # Send request
        self.process.stdin.write(json.dumps(message) + '\n')
        self.process.stdin.flush()
        
        # Wait for response (timeout 30s)
        try:
            response = response_queue.get(timeout=30)
            del self.request_queue[msg_id]
            return response
        except queue.Empty:
            del self.request_queue[msg_id]
            raise TimeoutError("MCP server timeout")
            
    def call_tool(self, tool_name: str, arguments: Dict = None) -> Any:
        """Phase 1: Call MCP tool directly"""
        if not self.process:
            self.start()
            
        request = {
            "jsonrpc": "2.0",
            "id": str(uuid.uuid4()),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }
        
        response = self._send_request(request)
        
        if 'error' in response:
            raise Exception(f"MCP error: {response['error']}")
            
        return response.get('result', {}).get('content', [])
        
    def stop(self):
        """Clean shutdown"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None

# Phase 2: Will add connection pooling
# Phase 3: Will add Claude CLI integration  
# Phase 4: Will add caching layer
# Phase 5: Will add metrics