#!/usr/bin/env python3
"""
Phase 2: Claude CLI Agent Integration
Adds intelligent agent routing for complex requests
"""

import subprocess
import json
import asyncio
from typing import Dict, Any, Optional

class ClaudeAgentBridge:
    """Manages Claude CLI with agent system for complex tasks"""
    
    def __init__(self):
        self.claude_available = self._check_claude_cli()
        
    def _check_claude_cli(self) -> bool:
        """Check if Claude CLI is available"""
        try:
            result = subprocess.run(
                ['claude', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
            
    async def call_agent(self, prompt: str, agent: str = "agent-orchestrator") -> Dict:
        """Call Claude CLI with agent for complex tasks"""
        if not self.claude_available:
            return {
                "error": "Claude CLI not available",
                "fallback": "Use direct MCP tools instead"
            }
            
        try:
            # Build Claude CLI command
            cmd = [
                'claude',
                '--agent', agent,
                '--json',  # Request JSON output
                prompt
            ]
            
            # Run Claude CLI
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                return {
                    "error": f"Claude CLI error: {stderr.decode()}",
                    "fallback": "Use direct MCP tools"
                }
                
            # Parse response
            response = stdout.decode()
            
            # Try to extract JSON if present
            if '{' in response:
                try:
                    json_start = response.index('{')
                    json_str = response[json_start:]
                    return json.loads(json_str)
                except:
                    pass
                    
            return {"content": response}
            
        except asyncio.TimeoutError:
            return {"error": "Claude CLI timeout", "fallback": "Use direct MCP"}
        except Exception as e:
            return {"error": str(e), "fallback": "Use direct MCP"}
            
    def should_use_agent(self, request: str) -> bool:
        """Determine if request needs agent intelligence"""
        
        # Complex patterns that need agents
        complex_patterns = [
            "build",
            "create app",
            "debug",
            "explain why",
            "help me understand",
            "step by step",
            "with examples",
            "and show",
            "visual"
        ]
        
        # Simple patterns for direct MCP
        simple_patterns = [
            "teach",
            "challenge",
            "check code",
            "next",
            "progress"
        ]
        
        request_lower = request.lower()
        
        # Check for simple patterns first (faster)
        for pattern in simple_patterns:
            if pattern in request_lower and len(request.split()) < 5:
                return False
                
        # Check for complex patterns
        for pattern in complex_patterns:
            if pattern in request_lower:
                return True
                
        # Default to simple if short
        return len(request.split()) > 10

# Phase 3: Will add agent response caching
# Phase 4: Will add agent pool management
# Phase 5: Will add custom agent definitions