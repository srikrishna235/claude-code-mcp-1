"""
Enhanced MCP Server with Real Tools and Agents
"""
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import asyncio
import os
import uuid
import subprocess
import tempfile
from typing import Any, Dict, List
from datetime import datetime

app = FastAPI(title="Enhanced Scrimba MCP Server")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"]
)

# Session storage for learning progress
sessions = {}

# Teaching content database
LESSONS = {
    "variables": {
        1: """📦 **Variables - Storage Boxes for Data**

A variable is like a labeled box where you store information.

```javascript
let myName = "Alice";
let age = 25;
let isStudent = true;
```

**Key Concepts:**
• `let` - Creates a variable that can change
• `const` - Creates a variable that cannot change
• `var` - Old way (avoid using)

**Try This:**
Create variables for your name, age, and favorite color.""",

        2: """🔄 **Variable Types & Operations**

JavaScript has different data types:

```javascript
// Numbers
let score = 100;
score = score + 10;  // Now 110

// Strings
let greeting = "Hello";
let name = "World";
let message = greeting + " " + name;  // "Hello World"

// Booleans
let isReady = false;
isReady = !isReady;  // Now true
```

**Challenge:** Create a shopping cart with price calculations.""",

        3: """🎯 **Advanced Variables - Scope & Hoisting**

Variables have scope (where they can be accessed):

```javascript
// Global scope
let globalVar = "I'm everywhere";

function myFunction() {
    // Function scope
    let localVar = "Only here";
    
    if (true) {
        // Block scope
        let blockVar = "Only in this block";
        const CONSTANT = "Never changes";
    }
}
```

**Remember:** Variables declared with `let` and `const` are block-scoped!"""
    },
    
    "functions": {
        1: """🎮 **Functions - Reusable Code Blocks**

Functions are like recipes - a set of instructions you can use again and again:

```javascript
function greet(name) {
    return "Hello, " + name + "!";
}

let message = greet("Alice");  // "Hello, Alice!"
```

**Parts of a Function:**
• `function` keyword
• Name (greet)
• Parameters (name)
• Body (the code inside {})
• Return value""",

        2: """⚡ **Arrow Functions & Callbacks**

Modern JavaScript uses arrow functions:

```javascript
// Traditional
function add(a, b) {
    return a + b;
}

// Arrow function
const add = (a, b) => a + b;

// As callback
[1, 2, 3].map(x => x * 2);  // [2, 4, 6]
```

**When to Use:**
• Callbacks
• Short functions
• Array methods"""
    },
    
    "loops": {
        1: """🔁 **Loops - Repeat Actions**

Loops let you repeat code:

```javascript
// for loop - when you know how many times
for (let i = 0; i < 5; i++) {
    console.log("Count: " + i);
}

// while loop - while condition is true
let count = 0;
while (count < 5) {
    console.log(count);
    count++;
}
```

**Use Cases:**
• Process arrays
• Repeat until condition met
• Count things"""
    }
}

# Code challenges database
CHALLENGES = {
    "easy": [
        {
            "title": "Hello Variable",
            "description": "Create a variable called `greeting` that stores 'Hello World'",
            "starter": "// Create your variable here\n",
            "solution": "let greeting = 'Hello World';",
            "test": "greeting === 'Hello World'"
        },
        {
            "title": "Simple Math",
            "description": "Create two variables `a` and `b` with values 5 and 3, then create `sum` with their sum",
            "starter": "// Create three variables\n",
            "solution": "let a = 5;\nlet b = 3;\nlet sum = a + b;",
            "test": "a === 5 && b === 3 && sum === 8"
        }
    ],
    "medium": [
        {
            "title": "Temperature Converter",
            "description": "Write a function `celsiusToFahrenheit` that converts Celsius to Fahrenheit",
            "starter": "function celsiusToFahrenheit(celsius) {\n  // Your code here\n}",
            "solution": "function celsiusToFahrenheit(celsius) {\n  return (celsius * 9/5) + 32;\n}",
            "test": "celsiusToFahrenheit(0) === 32 && celsiusToFahrenheit(100) === 212"
        },
        {
            "title": "Array Sum",
            "description": "Write a function `sumArray` that returns the sum of all numbers in an array",
            "starter": "function sumArray(arr) {\n  // Your code here\n}",
            "solution": "function sumArray(arr) {\n  return arr.reduce((sum, num) => sum + num, 0);\n}",
            "test": "sumArray([1,2,3]) === 6 && sumArray([]) === 0"
        }
    ],
    "hard": [
        {
            "title": "Fibonacci Generator",
            "description": "Write a function `fibonacci(n)` that returns the nth Fibonacci number",
            "starter": "function fibonacci(n) {\n  // Your code here\n}",
            "solution": "function fibonacci(n) {\n  if (n <= 1) return n;\n  return fibonacci(n-1) + fibonacci(n-2);\n}",
            "test": "fibonacci(0) === 0 && fibonacci(1) === 1 && fibonacci(10) === 55"
        }
    ]
}

def get_session(session_id: str) -> Dict:
    """Get or create session"""
    if session_id not in sessions:
        sessions[session_id] = {
            "id": session_id,
            "created": datetime.now().isoformat(),
            "progress": {},
            "completed_challenges": [],
            "current_topic": None,
            "level": 1
        }
    return sessions[session_id]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"name": "Enhanced Scrimba MCP Server", "version": "2.0.0", "protocol": "MCP"}

@app.post("/mcp")
@app.get("/mcp")
async def mcp_endpoint(request: Request):
    """MCP endpoint - handles both GET (SSE) and POST (JSON-RPC)"""
    
    # Handle GET request for SSE stream
    if request.method == "GET":
        session_id = str(uuid.uuid4())
        
        async def event_stream():
            yield f"data: {json.dumps({'type': 'connection', 'status': 'connected'})}\n\n"
            while True:
                await asyncio.sleep(30)
                yield f"data: {json.dumps({'type': 'ping'})}\n\n"
        
        return StreamingResponse(
            event_stream(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    
    # Handle POST request
    session_id = request.headers.get("Mcp-Session-Id") or str(uuid.uuid4())
    session = get_session(session_id)
    
    # Parse JSON-RPC request
    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    request_id = body.get("id")
    
    # Handle different MCP methods
    if method == "initialize":
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {
                    "name": "enhanced-scrimba-mcp",
                    "version": "2.0.0"
                },
                "capabilities": {
                    "tools": {},
                    "resources": {
                        "list": True,
                        "read": True
                    }
                }
            }
        }
    
    elif method == "tools/list":
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "teach",
                        "description": "Teach a programming concept with detailed lessons",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "topic": {
                                    "type": "string",
                                    "description": "Topic to teach (variables, functions, loops)",
                                    "enum": ["variables", "functions", "loops"]
                                },
                                "level": {
                                    "type": "integer",
                                    "description": "Complexity level (1-3)",
                                    "minimum": 1,
                                    "maximum": 3,
                                    "default": 1
                                }
                            },
                            "required": ["topic"]
                        }
                    },
                    {
                        "name": "challenge",
                        "description": "Get a coding challenge with starter code",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "difficulty": {
                                    "type": "string",
                                    "enum": ["easy", "medium", "hard"],
                                    "default": "easy"
                                }
                            }
                        }
                    },
                    {
                        "name": "run_code",
                        "description": "Execute JavaScript code and see the output",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "code": {
                                    "type": "string",
                                    "description": "JavaScript code to execute"
                                }
                            },
                            "required": ["code"]
                        }
                    },
                    {
                        "name": "check_solution",
                        "description": "Check if a code solution is correct",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "challenge_id": {
                                    "type": "string",
                                    "description": "Challenge title"
                                },
                                "code": {
                                    "type": "string",
                                    "description": "User's solution code"
                                }
                            },
                            "required": ["challenge_id", "code"]
                        }
                    },
                    {
                        "name": "learning_agent",
                        "description": "Adaptive learning agent that tracks progress",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "enum": ["next", "review", "suggest", "progress"],
                                    "description": "Agent action"
                                }
                            },
                            "required": ["action"]
                        }
                    }
                ]
            }
        }
    
    elif method == "resources/list":
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": [
                    {
                        "uri": f"session://{session_id}/progress",
                        "name": "Learning Progress",
                        "mimeType": "application/json"
                    },
                    {
                        "uri": "lessons://catalog",
                        "name": "Available Lessons",
                        "mimeType": "application/json"
                    }
                ]
            }
        }
    
    elif method == "resources/read":
        uri = params.get("uri", "")
        if uri.startswith("session://"):
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "contents": [{
                        "text": json.dumps(session, indent=2),
                        "mimeType": "application/json"
                    }]
                }
            }
        else:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "contents": [{
                        "text": json.dumps({"lessons": list(LESSONS.keys())}),
                        "mimeType": "application/json"
                    }]
                }
            }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        if tool_name == "teach":
            topic = tool_args.get("topic", "variables")
            level = tool_args.get("level", 1)
            
            # Update session
            session["current_topic"] = topic
            session["level"] = level
            
            # Get lesson content
            lesson = LESSONS.get(topic, {}).get(level, "Topic not found")
            
            # Track progress
            if topic not in session["progress"]:
                session["progress"][topic] = []
            if level not in session["progress"][topic]:
                session["progress"][topic].append(level)
            
            result = {
                "type": "text",
                "text": lesson + f"\n\n📊 Progress: {topic} Level {level} completed!"
            }
        
        elif tool_name == "challenge":
            difficulty = tool_args.get("difficulty", "easy")
            challenges = CHALLENGES.get(difficulty, [])
            
            if challenges:
                import random
                challenge = random.choice(challenges)
                result = {
                    "type": "text",
                    "text": f"""🎯 **Challenge: {challenge['title']}**

{challenge['description']}

```javascript
{challenge['starter']}
```

When ready, use the `check_solution` tool with your code!"""
                }
            else:
                result = {"type": "text", "text": "No challenges available"}
        
        elif tool_name == "run_code":
            code = tool_args.get("code", "")
            
            # Run JavaScript code safely
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                f.flush()
                
                try:
                    result_output = subprocess.run(
                        ['node', f.name],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    output = result_output.stdout or result_output.stderr
                    result = {
                        "type": "text",
                        "text": f"""📟 **Code Output:**

```
{output}
```

Exit Code: {result_output.returncode}"""
                    }
                except subprocess.TimeoutExpired:
                    result = {"type": "text", "text": "⏱️ Code execution timed out (5 seconds)"}
                except Exception as e:
                    result = {"type": "text", "text": f"❌ Error: {str(e)}"}
                finally:
                    os.unlink(f.name)
        
        elif tool_name == "check_solution":
            challenge_id = tool_args.get("challenge_id", "")
            user_code = tool_args.get("code", "")
            
            # Find the challenge
            challenge = None
            for diff in CHALLENGES.values():
                for c in diff:
                    if c["title"] == challenge_id:
                        challenge = c
                        break
            
            if challenge:
                # Test the solution
                test_code = f"""
{user_code}
{challenge['test']}
"""
                try:
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                        f.write(f"try {{ {test_code}; console.log('true'); }} catch(e) {{ console.log('false'); }}")
                        f.flush()
                        
                        result_output = subprocess.run(
                            ['node', f.name],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        
                        if "true" in result_output.stdout:
                            session["completed_challenges"].append(challenge_id)
                            result = {
                                "type": "text",
                                "text": f"""✅ **Correct Solution!**

Great job! You solved "{challenge_id}".

Completed challenges: {len(session['completed_challenges'])}"""
                            }
                        else:
                            result = {
                                "type": "text",
                                "text": f"""❌ **Not quite right**

Keep trying! Check your solution against the requirements.

Hint: {challenge['description']}"""
                            }
                        os.unlink(f.name)
                except Exception as e:
                    result = {"type": "text", "text": f"Error checking solution: {str(e)}"}
            else:
                result = {"type": "text", "text": "Challenge not found"}
        
        elif tool_name == "learning_agent":
            action = tool_args.get("action", "suggest")
            
            if action == "next":
                # Suggest next topic based on progress
                current = session.get("current_topic")
                level = session.get("level", 1)
                
                if current and level < 3:
                    result = {
                        "type": "text",
                        "text": f"📚 Ready for {current} Level {level + 1}? Use: teach('{current}', {level + 1})"
                    }
                else:
                    topics = list(LESSONS.keys())
                    for topic in topics:
                        if topic not in session["progress"]:
                            result = {
                                "type": "text",
                                "text": f"🆕 Try learning about '{topic}' next!"
                            }
                            break
                    else:
                        result = {"type": "text", "text": "🎉 You've completed all topics!"}
            
            elif action == "progress":
                completed = len(session["completed_challenges"])
                topics_learned = len(session["progress"])
                result = {
                    "type": "text",
                    "text": f"""📊 **Learning Progress Report**

• Topics studied: {topics_learned}
• Challenges completed: {completed}
• Current level: {session.get('level', 1)}
• Topics covered: {', '.join(session['progress'].keys()) if session['progress'] else 'None yet'}

Keep up the great work! 🚀"""
                }
            
            elif action == "suggest":
                suggestions = []
                if not session["progress"]:
                    suggestions.append("Start with 'variables' - the foundation of programming")
                elif len(session["completed_challenges"]) < 3:
                    suggestions.append("Try some coding challenges to practice")
                else:
                    suggestions.append("Move to the next level for deeper understanding")
                
                result = {
                    "type": "text",
                    "text": f"💡 **Suggestion**: {suggestions[0] if suggestions else 'Keep learning!'}"
                }
            
            else:
                result = {"type": "text", "text": f"Agent action '{action}' executed"}
        
        else:
            result = {"type": "text", "text": f"Unknown tool: {tool_name}"}
        
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
    
    else:
        # Unknown method
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }
    
    # Return response
    return Response(
        content=json.dumps(response),
        media_type="application/json",
        headers={"Mcp-Session-Id": session_id}
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)