#!/usr/bin/env python3
"""
Scrimba Teaching MCP Server with Claude Integration
Actually calls Claude CLI for intelligent responses
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional
import subprocess
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("scrimba-teaching")

def call_claude(prompt: str) -> str:
    """
    Call Claude CLI with the given prompt
    Returns Claude's response or fallback
    """
    try:
        # Call Claude with proper syntax
        result = subprocess.run(
            [
                "claude",
                "-p", prompt,
                "--dangerously-skip-permissions",
                "--output-format", "text"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout:
            logger.info("Claude responded successfully")
            return result.stdout
        else:
            logger.warning(f"Claude error: {result.stderr}")
            return f"I'll help you learn! {prompt}"
            
    except subprocess.TimeoutExpired:
        logger.error("Claude timed out")
        return "Let me teach you step by step!"
    except Exception as e:
        logger.error(f"Error calling Claude: {e}")
        return "Let's start learning together!"

@mcp.tool()
async def teach_concept(topic: str, step: int = 1) -> str:
    """
    Teach a programming concept using Scrimba methodology with Claude
    
    Args:
        topic: The concept to teach (e.g., "variables", "functions")
        step: Complexity level (1-5)
    
    Returns:
        Scrimba-style lesson from Claude
    """
    
    prompt = f"""You are a Scrimba teacher. Teach {topic} in JavaScript.
    
This is level {step}/5 of progressive complexity.

Format your response EXACTLY like this:

**20-Second Story:**
[Brief personal story about the concept]

**Type THIS Now (60 seconds):**
```javascript
// Code they should type immediately
console.log("example");
```

**Your Challenge:**
[Specific task to try right now]

Keep it under 300 words. Be enthusiastic! Use emojis! 
Remember: Students should be coding within 60 seconds!"""
    
    response = call_claude(prompt)
    
    return response

@mcp.tool()
async def give_challenge(difficulty: str = "easy", topic: Optional[str] = None) -> str:
    """
    Create a coding challenge with Claude
    
    Args:
        difficulty: "easy", "medium", or "hard"
        topic: Optional specific topic for the challenge
    
    Returns:
        Timed coding challenge
    """
    
    time_limits = {"easy": 60, "medium": 120, "hard": 180}
    time = time_limits.get(difficulty, 60)
    
    topic_part = f"about {topic}" if topic else "for JavaScript beginners"
    
    prompt = f"""Create a {difficulty} coding challenge {topic_part}.
    
Time limit: {time} seconds

Format:
⚡ **{time}-SECOND CHALLENGE!**

Task:
[What they need to build]

```javascript
// Starter code
```

Remember: Make it urgent and exciting! They should start typing immediately!"""
    
    response = call_claude(prompt)
    
    return response

@mcp.tool()
async def check_code(code: str) -> str:
    """
    Review user's code with encouragement using Claude
    
    Args:
        code: The user's code to review
    
    Returns:
        Encouraging feedback from Claude
    """
    
    prompt = f"""You are an encouraging Scrimba teacher. Review this code:

```javascript
{code}
```

Give feedback following these rules:
1. ALWAYS be positive and encouraging
2. Point out what they did RIGHT first
3. If there are issues, phrase them as "let's try..." suggestions
4. Check if they used console.log (celebrate if they did!)
5. End with excitement for their next step

Keep it brief (under 150 words) and enthusiastic!"""
    
    response = call_claude(prompt)
    
    return response

@mcp.tool()
async def next_lesson() -> str:
    """
    Continue to the next lesson in the learning journey
    
    Returns:
        Next lesson suggestion from Claude
    """
    
    prompt = """Give the next mini-lesson in the Scrimba learning journey.
    
Pick a random next topic from: variables, functions, arrays, loops, objects.
Make it feel like a natural progression.

Use the same format:
- 20-second story
- Code to type NOW
- Challenge

Keep the 60-second urgency!"""
    
    response = call_claude(prompt)
    
    return response

@mcp.tool()
async def celebrate(achievement: str = "progress") -> str:
    """
    Celebrate user's achievement with Scrimba enthusiasm
    
    Args:
        achievement: What to celebrate
    
    Returns:
        Celebration message from Claude
    """
    
    prompt = f"""Celebrate this achievement in Scrimba style: {achievement}

Be SUPER enthusiastic! Use emojis! Make them feel amazing!
Keep it to 2-3 sentences. Reference how far they've come!"""
    
    response = call_claude(prompt)
    
    return response

@mcp.tool()
async def show_hint(level: int = 1) -> str:
    """
    Give progressive hints without revealing the answer
    
    Args:
        level: Hint level (1=subtle, 2=clearer, 3=almost there)
    
    Returns:
        Progressive hint from Claude
    """
    
    hint_descriptions = {
        1: "very subtle, just a gentle nudge",
        2: "clearer but still not giving it away",
        3: "almost revealing the answer but they still have to type it"
    }
    
    prompt = f"""Give a {hint_descriptions.get(level, 'helpful')} hint for a JavaScript problem.

Don't reveal the answer! Just guide them closer.
Use Scrimba's encouraging tone. Keep it brief!"""
    
    response = call_claude(prompt)
    
    return response

if __name__ == "__main__":
    import sys
    
    if "--http" in sys.argv:
        # HTTP mode for testing
        import asyncio
        import uvicorn
        from starlette.applications import Starlette
        from starlette.middleware.cors import CORSMiddleware
        
        async def run_http_server():
            """Run as HTTP server for testing"""
            app = Starlette()
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            # Mount MCP app
            mcp_app = mcp.streamable_http_app()
            app.mount("/", mcp_app)
            
            print("=" * 60)
            print("🚀 Scrimba Teaching MCP Server with Claude (HTTP Mode)")
            print("✅ Actually calls Claude CLI for responses")
            print("📍 Server: http://localhost:8007")
            print("=" * 60)
            print("Available tools:")
            print("  - teach_concept: Teach programming concepts")
            print("  - give_challenge: Create coding challenges")
            print("  - check_code: Review user code")
            print("  - next_lesson: Continue learning journey")
            print("  - celebrate: Celebrate achievements")
            print("  - show_hint: Give progressive hints")
            print("=" * 60)
            
            # Run with session manager
            async with mcp.session_manager.run():
                config = uvicorn.Config(app, host="127.0.0.1", port=8007, log_level="info")
                server = uvicorn.Server(config)
                await server.serve()
        
        asyncio.run(run_http_server())
    else:
        # STDIO mode for Claude Desktop integration
        print("=" * 60, file=sys.stderr)
        print("🚀 Scrimba Teaching MCP Server with Claude (STDIO Mode)", file=sys.stderr)
        print("✅ Actually calls Claude CLI for responses", file=sys.stderr)
        print("=" * 60, file=sys.stderr)
        
        # Run in stdio mode (default for Claude Desktop)
        mcp.run()  # This expects stdin/stdout communication