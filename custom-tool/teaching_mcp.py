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
    },
    "variables_comprehensive": {
        "title": "Variables in Programming - Complete Guide",
        "steps": [
            {
                "step": 1,
                "title": "What are Variables? - The Container Analogy",
                "explanation": "🗂️ Think of variables as **labeled storage boxes** or containers that store values. Just like you might have a box labeled 'Books' that contains actual books, a variable has a name and contains data. In programming, we use variables to store information that we want to use later. The name acts as a label so we can find and use the stored value whenever we need it.\n\n📦 **Visual Metaphor**: Imagine your computer's memory as a giant warehouse with thousands of storage boxes. Each box (variable) has:\n- A **label** (the variable name) written on the outside\n- **contents** (the value) stored inside\n- A specific **location** (memory address) in the warehouse\n\nWhen you create a variable, you're essentially:\n1. 🏷️ Getting a new box and writing a label on it\n2. 📥 Putting something valuable inside\n3. 📍 Placing it in a memorable location in your warehouse",
                "code": "// Variables are like labeled containers in a storage warehouse\n\n// 📦 Create three storage boxes with labels and contents\nlet studentName = 'Alice';        // Box labeled 'studentName' containing 'Alice'\nlet studentAge = 20;              // Box labeled 'studentAge' containing the number 20\nlet isStudent = true;             // Box labeled 'isStudent' containing true/false flag\n\n// 🔍 Look inside the boxes (retrieve values)\nconsole.log('What\\'s in the studentName box?', studentName);\nconsole.log('What\\'s in the studentAge box?', studentAge);\nconsole.log('What\\'s in the isStudent box?', isStudent);\n\n// 🔤 Combine values from multiple boxes\nconsole.log(`${studentName} is ${studentAge} years old`);\n\n// 🔄 Change what's in the box (reassignment)\nstudentAge = 21;                  // Take out 20, put in 21\nconsole.log(`Happy birthday! Now ${studentName} is ${studentAge} years old`);\n\n// 📊 Check what type of content each box holds\nconsole.log('studentName box contains:', typeof studentName, 'type data');\nconsole.log('studentAge box contains:', typeof studentAge, 'type data');\nconsole.log('isStudent box contains:', typeof isStudent, 'type data');",
                "exercise": "🎯 **Your Turn!** Create your own storage warehouse:\n1. Create three variables: one for your favorite color (string), one for your age (number), and one for whether you like pizza (boolean)\n2. Print a sentence using all three variables\n3. Use console.log to check the type of each variable\n4. Change one of the values and print the sentence again\n\n💡 **Real-world analogy**: Think of organizing your bedroom - you might have a box for 'Clothes', another for 'Books', and another for 'Electronics'. Each has a clear label and specific contents!",
                "hint": "Use let variableName = value; and template literals with ${variableName} for printing. Try: let favoriteColor = 'blue'; console.log(typeof favoriteColor);",
                "visual_prompt": "Create a bright, colorful warehouse illustration showing three labeled storage boxes on shelves. Box 1 labeled 'studentName' contains a glowing 'Alice' text, Box 2 labeled 'studentAge' contains the number '20' with sparkles, Box 3 labeled 'isStudent' contains a glowing 'true' with checkmark. Include a friendly warehouse worker character pointing at the boxes. Add arrows showing the process: 'Create' → 'Store' → 'Retrieve'. Style: educational infographic, bright colors (blue, orange, green), clean and beginner-friendly, Scrimba-inspired."
            },
            {
                "step": 2,
                "title": "Why Do We Need Variables? - The Power of Reusability",
                "explanation": "Variables make our code reusable, readable, and maintainable. Instead of repeating the same value multiple times, we store it once and use it everywhere. This means if we need to change the value, we only change it in one place. Variables also make our code self-documenting - a variable named 'taxRate' is much clearer than seeing 0.08 scattered throughout code.",
                "code": "// Without variables - hard to maintain and unclear\nconsole.log('Tax on $100: $' + (100 * 0.08));\nconsole.log('Tax on $200: $' + (200 * 0.08));\nconsole.log('Tax on $300: $' + (300 * 0.08));\n// What if tax rate changes? We'd have to update every 0.08!\n\n// With variables - clear, maintainable, reusable\nlet taxRate = 0.08;\nlet product1Price = 100;\nlet product2Price = 200;\nlet product3Price = 300;\n\nconsole.log(`Tax on $${product1Price}: $${product1Price * taxRate}`);\nconsole.log(`Tax on $${product2Price}: $${product2Price * taxRate}`);\nconsole.log(`Tax on $${product3Price}: $${product3Price * taxRate}`);\n// To change tax rate, just change one line: taxRate = 0.09;",
                "exercise": "Create a program that calculates the area of three different rectangles. Use variables for length, width, and store the formula (length * width) in a way that's reusable.",
                "hint": "Create variables for each rectangle's dimensions, then calculate and display the areas using clear variable names"
            },
            {
                "step": 3,
                "title": "Variable Declaration and Initialization",
                "explanation": "Declaration means creating a variable (giving it a name), while initialization means giving it its first value. In JavaScript, we can declare and initialize in one step, or separately. Different keywords (let, const, var) have different behaviors.",
                "code": "// Declaration and initialization in one step\nlet userName = 'John';           // Declare and initialize\nconst PI = 3.14159;             // Declare and initialize a constant\n\n// Declaration without initialization (undefined)\nlet userAge;                    // Declared but not initialized\nconsole.log(userAge);           // undefined\n\n// Later initialization\nuserAge = 25;                   // Now it has a value\nconsole.log(userAge);           // 25\n\n// Multiple declarations\nlet firstName = 'Jane', lastName = 'Doe', age = 30;\n\n// Reassignment (changing the value)\nuserName = 'Jane';              // userName now contains 'Jane' instead of 'John'\n// PI = 3.14;                   // Error! Can't reassign const variables",
                "exercise": "Declare a variable without initializing it, then assign it a value. Also create a constant for your birth year and try to change it (observe what happens).",
                "hint": "Use let for variables you want to change, const for values that stay the same"
            },
            {
                "step": 4,
                "title": "Variable Naming Rules and Conventions",
                "explanation": "Good variable names make code readable and maintainable. JavaScript has strict rules about what characters you can use, and the programming community has conventions that make code easier to understand. Use camelCase for variables, start with letters (not numbers), and choose descriptive names.",
                "code": "// GOOD variable names (following conventions)\nlet firstName = 'Alice';         // camelCase for multi-word names\nlet userAge = 25;               // descriptive and clear\nlet isLoggedIn = false;         // boolean variables often start with 'is', 'has', 'can'\nlet MAX_RETRY_ATTEMPTS = 3;     // constants in UPPER_SNAKE_CASE\nlet shoppingCartItems = [];     // clear what it contains\n\n// BAD variable names (but technically valid)\nlet a = 'Alice';                // too short, not descriptive\nlet user_age = 25;              // snake_case (valid but not JavaScript convention)\nlet IsLoggedIn = false;         // PascalCase (reserved for classes/constructors)\nlet shopping_cart_items = [];   // inconsistent with JavaScript style\n\n// INVALID variable names (will cause errors)\n// let 2users = 10;             // can't start with number\n// let user-name = 'Bob';       // hyphens not allowed\n// let let = 'keyword';         // can't use reserved words\n// let user name = 'Bob';       // spaces not allowed",
                "exercise": "Create variables for a simple user profile with good naming conventions: first name, last name, email address, age, and whether they have verified their email.",
                "hint": "Use camelCase, make names descriptive, and use 'is' prefix for boolean values"
            },
            {
                "step": 5,
                "title": "Data Types - What Variables Can Hold",
                "explanation": "Variables can store different types of data. The main primitive types in JavaScript are numbers, strings, booleans, null, and undefined. There are also complex types like arrays (lists) and objects (collections of key-value pairs). JavaScript is dynamically typed, meaning the same variable can hold different types of data at different times.",
                "code": "// Primitive Data Types\nlet age = 25;                    // Number (integer)\nlet height = 5.9;               // Number (decimal/float)\nlet name = 'Alice';             // String (text)\nlet isStudent = true;           // Boolean (true/false)\nlet middleName = null;          // Null (intentionally empty)\nlet phoneNumber;                // Undefined (declared but not assigned)\n\n// Complex Data Types\nlet hobbies = ['reading', 'swimming', 'coding'];  // Array (list of items)\nlet person = {                  // Object (collection of properties)\n    firstName: 'Alice',\n    lastName: 'Johnson',\n    age: 25,\n    isStudent: true\n};\n\n// Checking types\nconsole.log(typeof age);        // 'number'\nconsole.log(typeof name);       // 'string'\nconsole.log(typeof isStudent);  // 'boolean'\nconsole.log(typeof hobbies);    // 'object' (arrays are objects in JS)\nconsole.log(typeof person);     // 'object'\n\n// Dynamic typing - same variable, different types\nlet dynamicVar = 42;            // starts as number\nconsole.log(typeof dynamicVar); // 'number'\ndynamicVar = 'Hello';           // now it's a string\nconsole.log(typeof dynamicVar); // 'string'",
                "exercise": "Create variables of each data type: number, string, boolean, array with 3 items, and an object with at least 3 properties. Use typeof to check each one.",
                "hint": "Remember: arrays use [], objects use {}, and typeof operator shows the data type"
            },
            {
                "step": 6,
                "title": "Variable Scope - Global vs Local",
                "explanation": "Scope determines where in your code a variable can be accessed. Global variables can be used anywhere in your program, while local variables can only be used within the function or block where they're declared. Think of scope like rooms in a house - you can access things in your current room and shared areas (global), but not things locked in other rooms (other functions' local scope).",
                "code": "// Global scope - accessible everywhere\nlet globalMessage = 'I am global!';\nconst GLOBAL_CONSTANT = 'Available everywhere';\n\nfunction demonstrateScope() {\n    // Local scope - only accessible within this function\n    let localMessage = 'I am local to this function';\n    \n    console.log(globalMessage);    // ✅ Can access global variables\n    console.log(localMessage);     // ✅ Can access local variables\n    \n    if (true) {\n        // Block scope - only accessible within this block\n        let blockMessage = 'I am local to this block';\n        console.log(globalMessage);  // ✅ Can access global\n        console.log(localMessage);   // ✅ Can access function scope\n        console.log(blockMessage);   // ✅ Can access block scope\n    }\n    \n    // console.log(blockMessage);  // ❌ Error! Can't access block scope here\n}\n\ndemstrateScope();\nconsole.log(globalMessage);      // ✅ Can access global\n// console.log(localMessage);    // ❌ Error! Can't access function scope\n// console.log(blockMessage);    // ❌ Error! Can't access block scope\n\n// Scope shadowing - local variable 'hides' global one with same name\nlet message = 'Global message';\n\nfunction shadowExample() {\n    let message = 'Local message';  // This 'shadows' the global message\n    console.log(message);           // Prints 'Local message'\n}\n\nshadowExample();\nconsole.log(message);               // Prints 'Global message'",
                "exercise": "Create a global variable, then write a function that has a local variable with the same name. Also create a variable inside an if block and try to access it outside the block.",
                "hint": "Use let for proper block scoping, and remember that variables declared inside {} are only accessible within those braces"
            },
            {
                "step": 7,
                "title": "Constants vs Variables - const vs let vs var",
                "explanation": "JavaScript has three ways to declare variables: const (can't be reassigned), let (can be reassigned, block-scoped), and var (can be reassigned, function-scoped). Modern JavaScript prefers const for values that don't change and let for values that do change. Avoid var due to its confusing scoping behavior.",
                "code": "// const - cannot be reassigned, must be initialized\nconst PI = 3.14159;             // ✅ Good for values that don't change\nconst users = ['Alice', 'Bob'];  // ✅ Array itself can't be reassigned...\nusers.push('Charlie');          // ✅ ...but we can modify its contents\nconsole.log(users);             // ['Alice', 'Bob', 'Charlie']\n// PI = 3.14;                   // ❌ Error! Cannot reassign const\n// const name;                  // ❌ Error! Must initialize const\n\n// let - can be reassigned, block-scoped\nlet counter = 0;                // ✅ Good for values that change\ncounter = 1;                    // ✅ Can reassign\ncounter++;                      // ✅ Can modify\n\nif (true) {\n    let blockVar = 'block';\n}\n// console.log(blockVar);       // ❌ Error! let is block-scoped\n\n// var - can be reassigned, function-scoped (avoid in modern JS)\nvar oldStyle = 'avoid this';    // ⚠️  Works but not recommended\nif (true) {\n    var leaks = 'I leak out';   // ⚠️  var ignores block scope\n}\nconsole.log(leaks);             // 'I leak out' - var leaked out of the block!\n\n// Best practices\nconst userName = 'Alice';       // Use const when value won't change\nlet userScore = 0;              // Use let when value will change\n// var anything;                // Don't use var in modern JavaScript\n\n// Hoisting behavior (advanced concept)\nconsole.log(hoistedVar);        // undefined (not an error, but confusing)\nvar hoistedVar = 'I am hoisted';\n\n// console.log(notHoisted);     // ❌ Error! let/const are not hoisted\n// let notHoisted = 'Better behavior';",
                "exercise": "Create examples using const, let, and var. Try to reassign each one and observe the differences. Also try accessing a let variable before declaring it.",
                "hint": "Use const for unchanging values, let for changing values, and see how var behaves differently with scope"
            },
            {
                "step": 8,
                "title": "Common Mistakes and Best Practices",
                "explanation": "Avoid common pitfalls like using var, creating accidental globals, poor naming, and not understanding scope. Follow best practices: use const by default, let when you need to reassign, meaningful names, and be aware of scope. These habits will make your code more reliable and easier to maintain.",
                "code": "// ❌ COMMON MISTAKES\n\n// 1. Accidental global variables (forgetting let/const)\nfunction badFunction() {\n    accidentalGlobal = 'Oops!';  // Creates global variable!\n}\n\n// 2. Using var instead of let/const\nfor (var i = 0; i < 3; i++) {\n    setTimeout(() => console.log('var:', i), 100);  // Prints 3, 3, 3\n}\n\n// 3. Poor variable names\nlet d = new Date();              // What does 'd' represent?\nlet temp = userData.name;        // 'temp' doesn't describe the content\nlet flag = user.isActive;        // 'flag' is too generic\n\n// 4. Not understanding const with objects\nconst user = { name: 'Alice' };\nuser = { name: 'Bob' };          // ❌ Error! Can't reassign\n\n// ✅ BEST PRACTICES\n\n// 1. Use proper declarations\nfunction goodFunction() {\n    const localVariable = 'Safe!';\n    return localVariable;\n}\n\n// 2. Use let for proper scoping\nfor (let i = 0; i < 3; i++) {\n    setTimeout(() => console.log('let:', i), 200);  // Prints 0, 1, 2\n}\n\n// 3. Meaningful variable names\nconst currentDate = new Date();\nconst userName = userData.name;\nconst isUserActive = user.isActive;\n\n// 4. Understand const with objects/arrays\nconst userProfile = { name: 'Alice' };\nuserProfile.name = 'Bob';        // ✅ Can modify properties\nuserProfile.age = 25;            // ✅ Can add properties\n\n// 5. Use const by default, let when needed\nconst API_URL = 'https://api.example.com';  // Won't change\nconst users = [];                            // Array won't be reassigned\nlet currentUserIndex = 0;                   // Will change\n\n// 6. Initialize variables when possible\nlet userInput = '';              // Better than let userInput;\nconst defaultSettings = {        // Clear initialization\n    theme: 'light',\n    language: 'en'\n};\n\n// 7. Group related variable declarations\nconst CONFIG = {\n    maxRetries: 3,\n    timeout: 5000,\n    baseUrl: 'https://api.example.com'\n};\n\nlet gameState = {\n    score: 0,\n    level: 1,\n    lives: 3\n};",
                "exercise": "Fix this code by applying best practices: var x = 5; var y; function test() { z = 10; var a = x + y + z; return a; } Improve variable names, declarations, and scope handling.",
                "hint": "Use const/let instead of var, give variables meaningful names, avoid global variables, and initialize properly"
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
        },
        "variables_comprehensive": {
            1: ["let", "=", "console.log"],
            2: ["let", "*", "console.log"],
            3: ["let", "const", "="],
            4: ["let", "camelCase"],
            5: ["let", "const", "typeof"],
            6: ["let", "function", "console.log"],
            7: ["const", "let", "var"],
            8: ["const", "let"]
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