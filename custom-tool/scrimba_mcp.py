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

# Progress tracking
USER_PROGRESS = {
    "concepts_learned": [],
    "challenges_completed": 0,
    "current_level": "beginner"
}

@mcp.tool()
async def show_hint(
    level: Optional[int] = 1
) -> str:
    """
    Give progressive hints without revealing the full answer.
    
    Args:
        level: Hint level (1=subtle, 2=clearer, 3=almost there)
    
    Returns:
        Progressive hint based on level
    """
    if not CURRENT_LESSON["topic"]:
        # Give generic hints for challenges
        hints = {
            1: "💡 Remember: Variables start with 'let' or 'const'...",
            2: "💡 Try: let variableName = value",
            3: "💡 Almost there! Example: let count = 0"
        }
    else:
        # Context-aware hints based on current lesson
        topic = CURRENT_LESSON["topic"]
        if topic == "variables":
            hints = {
                1: "💡 Variables are like labeled boxes...",
                2: "💡 Use 'let' to create a new variable",
                3: "💡 Pattern: let name = 'value'"
            }
        elif topic == "loops":
            hints = {
                1: "💡 Loops repeat code multiple times...",
                2: "💡 'for' loops: for(let i = 0; i < max; i++)",
                3: "💡 Try: for(let i = 0; i < 3; i++) { console.log(i) }"
            }
        else:
            hints = {
                1: "💡 Think about what you're trying to store or do...",
                2: "💡 Break it down into smaller steps",
                3: "💡 Start with the simplest version"
            }
    
    hint = hints.get(level, hints[1])
    
    return f"""{hint}

{"Need more help? Ask for level 2 or 3 hint!" if level < 3 else "Give it your best shot! You've got this!"}

Remember: It's totally okay to need hints - everyone does at first!"""

@mcp.tool()
async def track_progress() -> str:
    """
    Show user's learning progress with checkmarks.
    
    Returns:
        Progress summary with achievements
    """
    # Update progress based on activities
    if CURRENT_LESSON["topic"] and CURRENT_LESSON["topic"] not in USER_PROGRESS["concepts_learned"]:
        USER_PROGRESS["concepts_learned"].append(CURRENT_LESSON["topic"])
    
    # Build progress report
    report = "📊 **YOUR CODING JOURNEY**\n"
    report += "=" * 40 + "\n\n"
    
    # Concepts learned
    report += "**Concepts Mastered:**\n"
    concepts = {
        "variables": "✓ Variables - Store data",
        "loops": "✓ Loops - Repeat code",
        "functions": "✓ Functions - Reusable code",
        "arrays": "✓ Arrays - Lists of items",
        "objects": "✓ Objects - Complex data"
    }
    
    for concept in USER_PROGRESS["concepts_learned"]:
        if concept in concepts:
            report += f"{concepts[concept]}\n"
    
    if not USER_PROGRESS["concepts_learned"]:
        report += "Start your first lesson to begin!\n"
    
    report += f"\n**Challenges Completed:** {USER_PROGRESS['challenges_completed']}\n"
    report += f"**Current Level:** {USER_PROGRESS['current_level'].title()}\n\n"
    
    # Motivational message
    if USER_PROGRESS["challenges_completed"] > 5:
        report += "🔥 You're on FIRE! Your skills are becoming dangerous!\n"
    elif USER_PROGRESS["challenges_completed"] > 2:
        report += "💪 You're making great progress! Keep coding!\n"
    else:
        report += "🚀 Your journey has just begun. Exciting times ahead!\n"
    
    report += "\nRemember: The only way to learn to code is to write a lot of code!"
    
    return report

@mcp.tool()
async def start_project(
    project_name: Optional[str] = "passenger_counter"
) -> str:
    """
    Start a real project with step-by-step guidance.
    
    Args:
        project_name: "passenger_counter", "blackjack", or "chrome_extension"
    
    Returns:
        Project setup and first steps
    """
    projects = {
        "passenger_counter": {
            "story": "When I was 19, I had to count people entering the subway. SO boring!",
            "goal": "Build an app to count passengers",
            "steps": [
                "1. Create variable: let count = 0",
                "2. Create function: increment()",  
                "3. Add button in HTML",
                "4. Connect button to function",
                "5. Display count on page"
            ],
            "starter": """let count = 0

function increment() {
    // Add 1 to count
    // Update the display
}

// Your turn! Fill in the function"""
        },
        "blackjack": {
            "story": "I won 100 euros playing Blackjack in Prague!",
            "goal": "Build a Blackjack game",
            "steps": [
                "1. Create variables for cards",
                "2. Calculate sum function",
                "3. Check for Blackjack",
                "4. Draw new card function",
                "5. Determine winner"
            ],
            "starter": """let firstCard = 11
let secondCard = 10
let sum = firstCard + secondCard

// Create a function to check if you have Blackjack!"""
        }
    }
    
    project = projects.get(project_name, projects["passenger_counter"])
    
    return f"""🎯 **PROJECT TIME: {project_name.upper().replace('_', ' ')}**

**Story:** {project['story']}
Let's solve this with code!

**Goal:** {project['goal']}

**Steps:**
{chr(10).join(project['steps'])}

**Starter Code:**
```javascript
{project['starter']}
```

🚀 **YOUR MISSION:** Complete step 1 right now!
This is a REAL project that solves an actual problem!

Go ahead and code! When stuck, ask for hints!"""

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