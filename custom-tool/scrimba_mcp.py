#!/usr/bin/env python3
"""
Scrimba-style Teaching MCP Server
Step-by-step interactive learning
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional

mcp = FastMCP("scrimba-tools")

# Simple lesson storage
CURRENT_LESSON = {
    "topic": None,
    "step": 0,
    "total_steps": 0
}

LESSONS = {
    "variables": {
        "title": "Understanding Variables",
        "steps": [
            {
                "explanation": "Variables are containers for storing data. Think of them as labeled boxes.",
                "code": "name = 'Alice'\nage = 25",
                "output": "# name now contains 'Alice'\n# age now contains 25"
            },
            {
                "explanation": "You can change what's inside a variable anytime.",
                "code": "age = 26  # Birthday!\nprint(f'{name} is now {age}')",
                "output": "Alice is now 26"
            },
            {
                "explanation": "Variables can hold different types: numbers, text, lists, etc.",
                "code": "count = 42          # integer\nprice = 19.99       # float\nis_ready = True     # boolean",
                "output": "# Three different data types stored"
            }
        ]
    },
    "loops": {
        "title": "Mastering Loops",
        "steps": [
            {
                "explanation": "Loops repeat code. A 'for' loop runs a specific number of times.",
                "code": "for i in range(3):\n    print(f'Count: {i}')",
                "output": "Count: 0\nCount: 1\nCount: 2"
            },
            {
                "explanation": "While loops continue until a condition becomes false.",
                "code": "counter = 0\nwhile counter < 3:\n    print(f'Counter: {counter}')\n    counter += 1",
                "output": "Counter: 0\nCounter: 1\nCounter: 2"
            }
        ]
    }
}

@mcp.tool()
async def show_lesson(
    topic: str,
    step: Optional[int] = 1
) -> str:
    """
    Display a specific lesson step with code and explanation.
    
    Args:
        topic: Lesson topic (e.g., "variables", "loops")
        step: Step number (default: 1)
    
    Returns:
        Formatted lesson content
    """
    if topic not in LESSONS:
        return f"❌ Unknown topic: {topic}\nAvailable: {', '.join(LESSONS.keys())}"
    
    lesson = LESSONS[topic]
    max_steps = len(lesson["steps"])
    
    if step < 1 or step > max_steps:
        return f"❌ Invalid step. {topic} has {max_steps} steps."
    
    # Update current lesson tracking
    CURRENT_LESSON["topic"] = topic
    CURRENT_LESSON["step"] = step
    CURRENT_LESSON["total_steps"] = max_steps
    
    step_data = lesson["steps"][step - 1]
    
    result = f"""📚 **{lesson['title']}** - Step {step}/{max_steps}
{'='*40}

**Concept:**
{step_data['explanation']}

**Code:**
```python
{step_data['code']}
```

**Result:**
```
{step_data['output']}
```

💡 Type 'next' to continue or 'previous' to go back."""
    
    return result

@mcp.tool()
async def next() -> str:
    """
    Move to the next step in the current lesson.
    
    Returns:
        Next lesson step or completion message
    """
    if not CURRENT_LESSON["topic"]:
        return "❌ No active lesson. Use show_lesson() to start."
    
    topic = CURRENT_LESSON["topic"]
    current_step = CURRENT_LESSON["step"]
    total_steps = CURRENT_LESSON["total_steps"]
    
    if current_step >= total_steps:
        return f"✅ You've completed '{topic}'! Start another lesson with show_lesson()."
    
    return await show_lesson(topic, current_step + 1)

@mcp.tool()
async def previous() -> str:
    """
    Go back to the previous step.
    
    Returns:
        Previous lesson step
    """
    if not CURRENT_LESSON["topic"]:
        return "❌ No active lesson. Use show_lesson() to start."
    
    topic = CURRENT_LESSON["topic"]
    current_step = CURRENT_LESSON["step"]
    
    if current_step <= 1:
        return "❌ Already at the first step."
    
    return await show_lesson(topic, current_step - 1)

if __name__ == "__main__":
    import sys
    
    if "--http" in sys.argv:
        import asyncio
        import uvicorn
        from starlette.applications import Starlette
        from starlette.middleware.cors import CORSMiddleware
        
        async def run_server():
            app = Starlette()
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            mcp_app = mcp.streamable_http_app()
            app.mount("/", mcp_app)
            
            async with mcp.session_manager.run():
                print("Scrimba Teaching MCP Server")
                print("============================")
                print("Tools: show_lesson, next, previous")
                
                config = uvicorn.Config(app, host="127.0.0.1", port=8006, log_level="info")
                server = uvicorn.Server(config)
                await server.serve()
        
        asyncio.run(run_server())
    else:
        mcp.run()