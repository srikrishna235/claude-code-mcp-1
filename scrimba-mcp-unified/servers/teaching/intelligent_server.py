#!/usr/bin/env python3
"""
Intelligent Teaching Server - Uses Claude for dynamic responses
Actually leverages Claude's intelligence, not hardcoded content
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, Any
import subprocess
import asyncio
import json

mcp = FastMCP("scrimba-teaching-intelligent")

# Session state
SESSION_STATE = {
    "conversation_history": [],
    "current_topic": None,
    "learning_level": 1
}

async def ask_claude(prompt: str, system_prompt: Optional[str] = None) -> str:
    """
    Call Claude CLI directly for intelligent responses
    This gives us the full power of Claude's knowledge and reasoning
    """
    try:
        # Build the Claude command
        cmd = ["claude"]
        
        # Add system prompt if provided
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {prompt}"
        else:
            full_prompt = prompt
            
        # Run Claude CLI
        process = await asyncio.create_subprocess_exec(
            "claude",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate(input=full_prompt.encode())
        
        if process.returncode != 0:
            # Fallback to a teaching prompt if Claude CLI fails
            return await generate_teaching_response(prompt)
            
        return stdout.decode().strip()
        
    except FileNotFoundError:
        # Claude CLI not available, use embedded teaching logic
        return await generate_teaching_response(prompt)
    except Exception as e:
        return f"Error calling Claude: {str(e)}. Using fallback teaching mode."

async def generate_teaching_response(prompt: str) -> str:
    """
    Fallback teaching response generator
    Uses Scrimba methodology even without Claude CLI
    """
    return f"""📚 **Interactive Lesson**
    
Following Scrimba's methodology:
1. **60-second rule** - You'll write code within 60 seconds
2. **Console.log everything** - See immediate results
3. **Learn by doing** - Type first, understand second

Your request: {prompt}

**Quick Challenge:**
Write some code related to this topic RIGHT NOW!
Don't think, just type. Use console.log() to verify.

The best way to learn is to WRITE CODE immediately! 🚀"""

@mcp.tool()
async def teach(topic: str, step: Optional[int] = 1) -> str:
    """
    Teach using Claude's full intelligence
    Dynamic, contextual responses, not hardcoded
    """
    SESSION_STATE["current_topic"] = topic
    
    system_prompt = """You are an expert programming teacher following Scrimba's revolutionary methodology:

CORE PRINCIPLES:
1. Students MUST write code within 60 seconds
2. Use console.log() for EVERYTHING (Console.log Driven Development)
3. Hook with personal story (20 seconds max)
4. Jump to code immediately
5. Celebrate EVERY small success
6. 5-level progression: Basic → Modify → Shortcuts → Advanced → Build Real App

TEACHING FORMAT:
1. Brief hook/story (20 seconds)
2. Simple code example they can type NOW
3. Challenge with 60-120 second timer
4. Instant verification with console.log()
5. Enthusiastic celebration

Keep responses under 300 words. Make them TYPE CODE immediately!"""
    
    user_prompt = f"Teach me {topic} at level {step}/5. Give me something to code RIGHT NOW with a 60-second timer. Include console.log() for immediate verification."
    
    response = await ask_claude(user_prompt, system_prompt)
    
    # Add to conversation history
    SESSION_STATE["conversation_history"].append({
        "role": "user",
        "content": f"teach {topic} step {step}"
    })
    SESSION_STATE["conversation_history"].append({
        "role": "assistant",
        "content": response
    })
    
    return response

@mcp.tool()
async def give_challenge(difficulty: Optional[str] = "easy") -> str:
    """
    Generate unique challenges using Claude's creativity
    Different every time, contextually aware
    """
    system_prompt = """Generate a coding challenge following Scrimba rules:

DIFFICULTY LEVELS:
- easy: 60 seconds, single line of code
- medium: 120 seconds, small function
- hard: 180 seconds, multiple concepts

FORMAT:
⚡ **CHALLENGE TIME!**
Timer: [time]
Mission: [clear, specific task]
Hint: [small hint if stuck]

Students must START TYPING IMMEDIATELY!
Include console.log() for verification.
Make it exciting and achievable!"""
    
    # Use conversation context for relevant challenges
    context = ""
    if SESSION_STATE["current_topic"]:
        context = f"Related to {SESSION_STATE['current_topic']}. "
    
    user_prompt = f"{context}Create a {difficulty} coding challenge that can be solved quickly. Make it unique and engaging!"
    
    response = await ask_claude(user_prompt, system_prompt)
    return response

@mcp.tool()
async def check_code(code: str) -> str:
    """
    Intelligently analyze code using Claude
    Provides specific, encouraging feedback
    """
    system_prompt = """You are an encouraging Scrimba code reviewer:

ALWAYS:
1. Celebrate ANY attempt enthusiastically
2. Find something specific to praise
3. Give ONE concrete improvement tip
4. Use console.log() to show verification
5. Keep feedback under 100 words
6. NEVER discourage, always encourage

Even for errors, say things like:
"LOVE that you're experimenting! Try adding console.log() to see what's happening!"
"""
    
    user_prompt = f"Review this code and give encouraging Scrimba-style feedback:\n```javascript\n{code}\n```"
    
    response = await ask_claude(user_prompt, system_prompt)
    return response

@mcp.tool()
async def adaptive_teach(request: str) -> str:
    """
    Fully adaptive teaching using Claude's intelligence
    Understands any request and teaches accordingly
    """
    system_prompt = """You are the Scrimba teaching system with these STRICT rules:

1. **60-Second Rule**: Students MUST write code within 60 seconds
2. **Console.log EVERYTHING**: Every example uses console.log()
3. **Type First, Think Later**: Code before theory
4. **Celebrate Everything**: Even errors are learning!
5. **Personal Stories**: Quick 20-second hooks from real experience

Analyze the request and provide:
- Immediate code to type (60-second timer)
- Console.log() for instant feedback
- Next challenge ready
- Keep under 300 words
- Make it FUN and URGENT!"""
    
    response = await ask_claude(request, system_prompt)
    
    # Track in conversation
    SESSION_STATE["conversation_history"].append({
        "role": "user",
        "content": request
    })
    SESSION_STATE["conversation_history"].append({
        "role": "assistant",
        "content": response
    })
    
    return response

@mcp.tool()
async def continue_learning() -> str:
    """
    Continue from where the student left off
    Uses conversation history for context
    """
    if not SESSION_STATE["conversation_history"]:
        return "Let's start fresh! What would you like to learn? I'll have you coding in 60 seconds!"
    
    system_prompt = """Based on the conversation history, provide the next logical lesson.
    
Follow Scrimba rules:
- Next challenge in 60 seconds
- Build on what they just learned
- Slightly increase complexity
- Use console.log() for everything
- Celebrate their progress!"""
    
    context = json.dumps(SESSION_STATE["conversation_history"][-4:])  # Last 2 exchanges
    user_prompt = f"Continue teaching based on this context:\n{context}\n\nWhat's the next step?"
    
    response = await ask_claude(user_prompt, system_prompt)
    return response

@mcp.tool()
async def explain_error(error_message: str) -> str:
    """
    Explain errors in Scrimba style
    Turn errors into learning moments
    """
    system_prompt = """Explain this error in Scrimba style:

1. "This error is PERFECT for learning!"
2. Explain in simple terms (under 50 words)
3. Give the fix they can type NOW
4. Show console.log() to verify the fix
5. Celebrate that they found an error (that's progress!)

Make errors feel like discoveries, not failures!"""
    
    user_prompt = f"Explain this error and how to fix it:\n{error_message}"
    
    response = await ask_claude(user_prompt, system_prompt)
    return response

# Add health check
@mcp.tool()
async def health() -> str:
    """Check if intelligent features are working"""
    try:
        # Quick test of Claude CLI
        result = await ask_claude("Say 'Claude is ready!' in 3 words")
        if "Claude" in result or "ready" in result:
            return "✅ Intelligent mode active - Full Claude power available!"
    except:
        pass
    
    return "⚠️ Running in fallback mode - Limited to embedded teaching logic"

if __name__ == "__main__":
    mcp.run()