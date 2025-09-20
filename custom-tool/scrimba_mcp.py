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

@mcp.tool()
async def give_challenge(
    difficulty: Optional[str] = "easy"
) -> str:
    """
    Give a coding challenge to practice immediately.
    
    Args:
        difficulty: "easy" (1 min), "medium" (2 min), or "hard" (3 min)
    
    Returns:
        Challenge instructions with specific tasks
    """
    challenges = {
        "easy": [
            {
                "task": "Create two variables:\n- firstName with your first name\n- lastName with your last name",
                "time": "1 minute",
                "hint": "let firstName = 'Your Name'"
            },
            {
                "task": "Create a variable called age and set it to your age.\nThen create doubleAge that's twice your age.",
                "time": "1 minute", 
                "hint": "let age = 25; let doubleAge = age * 2"
            }
        ],
        "medium": [
            {
                "task": "Write a function called greet that:\n1. Takes a name parameter\n2. Returns 'Hello ' + name\n3. Test it with console.log",
                "time": "2 minutes",
                "hint": "function greet(name) { return ... }"
            },
            {
                "task": "Create an array of 3 favorite foods.\nThen add a 4th item using push().",
                "time": "2 minutes",
                "hint": "let foods = ['pizza', ...]; foods.push('...')"
            }
        ],
        "hard": [
            {
                "task": "Build a counter:\n1. Variable count starting at 0\n2. Function increment() that adds 1\n3. Function save() that stores count in an array\n4. Test all functions",
                "time": "3 minutes",
                "hint": "let count = 0; let saves = []; function increment() { count += 1 }"
            }
        ]
    }
    
    level_challenges = challenges.get(difficulty, challenges["easy"])
    import random
    challenge = random.choice(level_challenges)
    
    return f"""🎯 **CHALLENGE TIME!** ({difficulty.upper()})

**Your mission ({challenge['time']}):**
{challenge['task']}

**Go ahead and do this RIGHT NOW!**
Pause and try it yourself first.

When done, I'll check your solution!
Need help? Ask for a hint!

Remember: The first time feels weird, but it becomes second nature! 💪"""

@mcp.tool()
async def check_code(
    code: str
) -> str:
    """
    Check user's code solution with encouraging Scrimba-style feedback.
    
    Args:
        code: The user's code solution
    
    Returns:
        Encouraging feedback with specific praise
    """
    # Basic checks for common patterns
    feedback = []
    
    # Check for variables
    if "let " in code or "const " in code or "var " in code:
        feedback.append("✓ Great job creating variables!")
    
    # Check for functions
    if "function" in code or "=>" in code:
        feedback.append("✓ Awesome function work!")
    
    # Check for console.log
    if "console.log" in code:
        feedback.append("✓ YES! Console.log is your best friend!")
    
    # Check for arrays
    if "[" in code and "]" in code:
        feedback.append("✓ Nice array skills!")
    
    # Check for common mistakes
    warnings = []
    if "=" in code and not "==" in code and not "let" in code and not "const" in code:
        warnings.append("💡 Oops! Super common mistake - did you forget 'let' or 'const'?")
    
    if "functoin" in code:
        warnings.append("💡 Tiny typo: 'functoin' should be 'function' - happens to everyone!")
    
    # Build response
    response = "🎉 **GREAT JOB!** You just wrote real code!\n\n"
    
    if feedback:
        response += "What you did well:\n"
        response += "\n".join(feedback) + "\n\n"
    
    if warnings:
        response += "Quick fixes:\n"
        response += "\n".join(warnings) + "\n\n"
        response += "But that's totally okay - making mistakes is how we learn!\n\n"
    
    response += "**You're officially programming!** 🚀\n"
    response += "Your JavaScript journey is really taking off!\n\n"
    response += "Ready for another challenge? Just ask!"
    
    return response

@mcp.tool()
async def celebrate(
    achievement: Optional[str] = "progress"
) -> str:
    """
    Celebrate user's achievement with Scrimba-style enthusiasm.
    
    Args:
        achievement: What to celebrate (e.g., "first_variable", "completed_lesson", "fixed_bug")
    
    Returns:
        Enthusiastic celebration message
    """
    celebrations = {
        "first_variable": "🎉 HUGE moment! You just created your FIRST variable! You're no longer like everyone else - you're a PROGRAMMER!",
        "first_function": "🚀 This is MASSIVE! You just wrote a function! You can now create reusable code blocks!",
        "completed_lesson": "💪 You CRUSHED it! Give yourself a pat on the back - that's a HUGE accomplishment!",
        "fixed_bug": "🔧 YES! You just debugged code! That's what real developers do every day!",
        "progress": "🌟 You're doing AMAZING! Your skills are becoming dangerous!",
        "project": "🏆 INCREDIBLE! You built something REAL! This solves actual problems!"
    }
    
    message = celebrations.get(achievement, celebrations["progress"])
    
    return f"""{message}

Remember: The only way to learn how to code is to write a lot of code!
And you're doing EXACTLY that!

Keep going, buddy! 💪"""

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