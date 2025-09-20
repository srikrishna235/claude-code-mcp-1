#!/usr/bin/env python3
"""
Teaching MCP Server - Interactive learning tool like Scrimba
Provides step-by-step tutorials and exercises
"""

from mcp.server.fastmcp import FastMCP
from typing import Optional, Dict, List
import json

mcp = FastMCP("teaching-tools")

# Tutorial content storage
TUTORIALS = {
    "python_basics": {
        "title": "Python Basics",
        "steps": [
            {
                "step": 1,
                "title": "Variables",
                "explanation": "Variables store data values. In Python, you create a variable by assigning a value.",
                "code": "name = 'Alice'\nage = 25\nprint(f'{name} is {age} years old')",
                "exercise": "Create variables for your name and favorite number, then print them.",
                "hint": "Use the same pattern: variable_name = value"
            },
            {
                "step": 2,
                "title": "Lists",
                "explanation": "Lists store multiple items in a single variable using square brackets [].",
                "code": "fruits = ['apple', 'banana', 'orange']\nprint(fruits[0])  # First item\nfruits.append('grape')",
                "exercise": "Create a list of 3 colors and add a fourth one.",
                "hint": "Use list.append() to add items"
            },
            {
                "step": 3,
                "title": "Functions",
                "explanation": "Functions are reusable blocks of code defined with 'def'.",
                "code": "def greet(name):\n    return f'Hello, {name}!'\n\nmessage = greet('World')\nprint(message)",
                "exercise": "Create a function that adds two numbers.",
                "hint": "def add(a, b): return ..."
            }
        ]
    },
    "javascript_dom": {
        "title": "JavaScript DOM Manipulation",
        "steps": [
            {
                "step": 1,
                "title": "Selecting Elements",
                "explanation": "Use querySelector to select HTML elements.",
                "code": "const button = document.querySelector('#myButton');\nconst divs = document.querySelectorAll('.box');",
                "exercise": "Select an element with class 'header'.",
                "hint": "document.querySelector('.className')"
            },
            {
                "step": 2,
                "title": "Event Listeners",
                "explanation": "Add interactivity with event listeners.",
                "code": "button.addEventListener('click', () => {\n    console.log('Button clicked!');\n});",
                "exercise": "Add a click handler that changes button text.",
                "hint": "Inside handler: event.target.textContent = 'New Text'"
            }
        ]
    },
    "react_hooks": {
        "title": "React Hooks",
        "steps": [
            {
                "step": 1,
                "title": "useState Hook",
                "explanation": "useState manages component state in functional components.",
                "code": "import { useState } from 'react';\n\nfunction Counter() {\n    const [count, setCount] = useState(0);\n    return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;\n}",
                "exercise": "Create a component with a text input using useState.",
                "hint": "const [text, setText] = useState('')"
            }
        ]
    }
}

# User progress tracking
user_progress: Dict[str, Dict] = {}

@mcp.tool()
async def list_tutorials() -> str:
    """
    List all available tutorials.
    
    Returns:
        List of tutorials with descriptions
    """
    result = "📚 Available Tutorials:\n\n"
    for key, tutorial in TUTORIALS.items():
        total_steps = len(tutorial["steps"])
        progress = user_progress.get(key, {}).get("completed_steps", 0)
        status = "✅ Completed" if progress == total_steps else f"📊 Progress: {progress}/{total_steps}"
        result += f"• {key}: {tutorial['title']} - {status}\n"
    return result

@mcp.tool()
async def start_tutorial(
    tutorial_name: str,
    step: Optional[int] = 1
) -> str:
    """
    Start or continue a tutorial.
    
    Args:
        tutorial_name: Name of the tutorial (e.g., "python_basics")
        step: Step number to start from (default: 1)
    
    Returns:
        Tutorial content for the specified step
    """
    if tutorial_name not in TUTORIALS:
        return f"❌ Tutorial '{tutorial_name}' not found. Use list_tutorials() to see available options."
    
    tutorial = TUTORIALS[tutorial_name]
    max_steps = len(tutorial["steps"])
    
    if step < 1 or step > max_steps:
        return f"❌ Invalid step. Tutorial has {max_steps} steps."
    
    step_data = tutorial["steps"][step - 1]
    
    # Track progress
    if tutorial_name not in user_progress:
        user_progress[tutorial_name] = {"completed_steps": 0, "current_step": step}
    else:
        user_progress[tutorial_name]["current_step"] = step
    
    result = f"""
📖 **{tutorial['title']}** - Step {step}/{max_steps}
{'='*50}

**{step_data['title']}**

📝 **Explanation:**
{step_data['explanation']}

💻 **Example Code:**
```
{step_data['code']}
```

🎯 **Exercise:**
{step_data['exercise']}

💡 Use get_hint('{tutorial_name}', {step}) if you need help
✅ Use check_solution('{tutorial_name}', {step}, 'your code here') to verify
➡️  Use next_step('{tutorial_name}') to continue
"""
    return result

@mcp.tool()
async def next_step(tutorial_name: str) -> str:
    """
    Move to the next step in a tutorial.
    
    Args:
        tutorial_name: Name of the current tutorial
    
    Returns:
        Next step content or completion message
    """
    if tutorial_name not in user_progress:
        return await start_tutorial(tutorial_name, 1)
    
    current = user_progress[tutorial_name].get("current_step", 0)
    max_steps = len(TUTORIALS[tutorial_name]["steps"])
    
    # Mark current step as completed
    user_progress[tutorial_name]["completed_steps"] = max(
        user_progress[tutorial_name].get("completed_steps", 0),
        current
    )
    
    if current >= max_steps:
        return f"🎉 Congratulations! You've completed the {TUTORIALS[tutorial_name]['title']} tutorial!"
    
    return await start_tutorial(tutorial_name, current + 1)

@mcp.tool()
async def get_hint(
    tutorial_name: str,
    step: int
) -> str:
    """
    Get a hint for a specific exercise.
    
    Args:
        tutorial_name: Name of the tutorial
        step: Step number
    
    Returns:
        Hint for the exercise
    """
    if tutorial_name not in TUTORIALS:
        return "❌ Tutorial not found"
    
    tutorial = TUTORIALS[tutorial_name]
    if step < 1 or step > len(tutorial["steps"]):
        return "❌ Invalid step number"
    
    hint = tutorial["steps"][step - 1]["hint"]
    return f"💡 **Hint:** {hint}"

@mcp.tool()
async def check_solution(
    tutorial_name: str,
    step: int,
    solution_code: str
) -> str:
    """
    Check if a solution is correct (basic validation).
    
    Args:
        tutorial_name: Name of the tutorial
        step: Step number
        solution_code: The user's solution code
    
    Returns:
        Feedback on the solution
    """
    if tutorial_name not in TUTORIALS:
        return "❌ Tutorial not found"
    
    # Simple keyword-based checking (in real implementation, would execute and test)
    checks = {
        "python_basics": {
            1: ["=", "print"],
            2: ["[", "]", "append"],
            3: ["def", "return"]
        },
        "javascript_dom": {
            1: ["querySelector", ".header"],
            2: ["addEventListener", "click"]
        },
        "react_hooks": {
            1: ["useState", "set"]
        }
    }
    
    if tutorial_name in checks and step <= len(checks[tutorial_name]):
        required_keywords = checks[tutorial_name][step]
        missing = [kw for kw in required_keywords if kw not in solution_code]
        
        if not missing:
            user_progress[tutorial_name]["completed_steps"] = max(
                user_progress[tutorial_name].get("completed_steps", 0),
                step
            )
            return "✅ Great job! Your solution looks correct. Use next_step() to continue."
        else:
            return f"❌ Not quite. Make sure your solution includes: {', '.join(missing)}"
    
    return "✅ Solution recorded. Use next_step() to continue."

@mcp.tool()
async def create_exercise(
    topic: str,
    difficulty: Optional[str] = "beginner"
) -> str:
    """
    Generate a coding exercise on a specific topic.
    
    Args:
        topic: Programming topic (e.g., "loops", "arrays", "functions")
        difficulty: Level - "beginner", "intermediate", "advanced"
    
    Returns:
        A coding exercise with instructions
    """
    exercises = {
        "loops": {
            "beginner": {
                "task": "Write a loop that prints numbers 1 to 10",
                "hint": "Use a for loop with range(1, 11)",
                "solution": "for i in range(1, 11):\n    print(i)"
            },
            "intermediate": {
                "task": "Create a loop that finds all prime numbers between 1 and 50",
                "hint": "Use nested loops to check divisibility",
                "solution": "for n in range(2, 51):\n    is_prime = True\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0:\n            is_prime = False\n            break\n    if is_prime:\n        print(n)"
            }
        },
        "arrays": {
            "beginner": {
                "task": "Create an array of 5 fruits and print the third one",
                "hint": "Remember arrays are 0-indexed",
                "solution": "fruits = ['apple', 'banana', 'orange', 'grape', 'melon']\nprint(fruits[2])"
            }
        },
        "functions": {
            "beginner": {
                "task": "Write a function that returns the square of a number",
                "hint": "def square(x): return ...",
                "solution": "def square(x):\n    return x * x"
            }
        }
    }
    
    if topic not in exercises:
        return f"📝 Create your own {topic} exercise:\n1. Define the problem clearly\n2. Break it into steps\n3. Write test cases\n4. Implement solution\n5. Test and refine"
    
    if difficulty not in exercises[topic]:
        difficulty = "beginner"
    
    exercise = exercises[topic][difficulty]
    return f"""
🎯 **Exercise: {topic.title()} ({difficulty})**

**Task:** {exercise['task']}

**Requirements:**
- Write clean, readable code
- Test with different inputs
- Add comments if needed

💡 Need help? The hint is: {exercise['hint']}

Submit your solution with check_solution() when ready!
"""

@mcp.tool()
async def explain_concept(
    concept: str,
    language: Optional[str] = "python"
) -> str:
    """
    Explain a programming concept with examples.
    
    Args:
        concept: The concept to explain (e.g., "recursion", "closures")
        language: Programming language for examples
    
    Returns:
        Detailed explanation with code examples
    """
    explanations = {
        "recursion": """
**Recursion** is when a function calls itself to solve a problem by breaking it into smaller pieces.

**Key Components:**
1. **Base Case:** Stops the recursion
2. **Recursive Case:** Function calls itself with modified input

**Example - Factorial:**
```python
def factorial(n):
    # Base case
    if n <= 1:
        return 1
    # Recursive case
    return n * factorial(n - 1)

# factorial(5) = 5 * 4 * 3 * 2 * 1 = 120
```

**When to use:** Problems that can be broken into similar subproblems (trees, nested structures)
""",
        "closures": """
**Closures** are functions that remember variables from their outer scope even after that scope has finished.

**Example:**
```python
def make_multiplier(x):
    def multiplier(y):
        return x * y  # 'x' is remembered
    return multiplier

times_two = make_multiplier(2)
print(times_two(5))  # Output: 10
```

**Use cases:** Creating function factories, maintaining state, callbacks
"""
    }
    
    if concept in explanations:
        return explanations[concept]
    
    return f"""
📚 **{concept.title()}**

This is a concept you should explore by:
1. Understanding the basic definition
2. Looking at simple examples
3. Building your own examples
4. Identifying use cases
5. Practice with exercises

Try: create_exercise('{concept}') for practice!
"""

if __name__ == "__main__":
    import sys
    
    if "--http" in sys.argv:
        # HTTP mode for testing
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
                print("Teaching MCP Server (HTTP Mode)")
                print("================================")
                print("Starting on http://localhost:8004")
                print("\nAvailable tools:")
                print("  - list_tutorials: See all tutorials")
                print("  - start_tutorial: Begin learning")
                print("  - next_step: Continue tutorial")
                print("  - get_hint: Get help")
                print("  - check_solution: Verify your code")
                print("  - create_exercise: Get practice problems")
                print("  - explain_concept: Learn concepts")
                
                config = uvicorn.Config(app, host="127.0.0.1", port=8004, log_level="info")
                server = uvicorn.Server(config)
                await server.serve()
        
        asyncio.run(run_server())
    else:
        # STDIO mode for Claude Code
        mcp.run()