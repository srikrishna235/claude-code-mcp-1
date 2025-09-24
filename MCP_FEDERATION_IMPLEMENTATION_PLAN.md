# MCP Federation Implementation Plan

## 🎯 Goal: Build Full-Power MCP Teaching System

---

## PHASE 1: Foundation (Week 1)

### Logic Flow:
```
1. Create base infrastructure
2. Build single working MCP with resources + tools
3. Test with Claude Code
4. Iterate until stable
```

### Implementation Steps:

#### Step 1.1: Create Base MCP Class
**File:** `scrimba-mcp-unified/mcp_base/base_server.py`
```python
from mcp.server.fastmcp import FastMCP
from abc import ABC, abstractmethod
import asyncio
import json
import redis  # For inter-MCP communication

class BaseMCPServer(ABC):
    """Base class for all MCP servers in federation"""
    
    def __init__(self, name: str, port: int = None):
        self.mcp = FastMCP(name)
        self.name = name
        self.port = port
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.setup_tools()
        self.setup_resources()
        self.setup_prompts()
        
    @abstractmethod
    def setup_tools(self):
        """Each server defines its tools"""
        pass
        
    @abstractmethod
    def setup_resources(self):
        """Each server defines its resources"""
        pass
    
    def setup_prompts(self):
        """Optional prompt templates"""
        pass
    
    async def publish_event(self, event_type: str, data: dict):
        """Publish event to other MCPs"""
        message = json.dumps({
            "source": self.name,
            "type": event_type,
            "data": data
        })
        self.redis_client.publish('mcp_events', message)
    
    async def call_other_mcp(self, server_name: str, tool_name: str, args: dict):
        """Call tool on another MCP server"""
        request_id = f"{self.name}_{server_name}_{tool_name}_{asyncio.get_event_loop().time()}"
        
        # Publish request
        self.redis_client.publish(f'mcp_{server_name}_requests', json.dumps({
            "request_id": request_id,
            "tool": tool_name,
            "args": args
        }))
        
        # Wait for response
        response_key = f"response_{request_id}"
        for _ in range(100):  # 10 second timeout
            response = self.redis_client.get(response_key)
            if response:
                return json.loads(response)
            await asyncio.sleep(0.1)
        
        raise TimeoutError(f"No response from {server_name}")
```

#### Step 1.2: Create Content MCP with Resources
**File:** `scrimba-mcp-unified/mcp_servers/content_server.py`
```python
from mcp_base.base_server import BaseMCPServer
import json

class ContentMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__("content-server")
        self.lessons = self.load_lessons()
        
    def load_lessons(self):
        """Load lesson content from files"""
        return {
            "variables": {
                "title": "Variables - Storage Boxes",
                "levels": [
                    {"hook": "Story about organizing...", "code": "let x = 5;", "challenge": "Create 3 variables"},
                    # ... more levels
                ]
            },
            # ... more topics
        }
    
    def setup_tools(self):
        @self.mcp.tool()
        async def search_content(query: str) -> list:
            """Search for lessons matching query"""
            results = []
            for topic, content in self.lessons.items():
                if query.lower() in topic.lower() or query.lower() in str(content).lower():
                    results.append({"topic": topic, "title": content["title"]})
            return results
        
        @self.mcp.tool()
        async def get_lesson_structure(topic: str, level: int = 1) -> dict:
            """Get lesson structure for Claude to fill"""
            if topic not in self.lessons:
                return {"error": "Topic not found"}
            
            lesson = self.lessons[topic]["levels"][level - 1]
            
            # Publish event
            await self.publish_event("lesson_accessed", {"topic": topic, "level": level})
            
            return {
                "topic": topic,
                "level": level,
                "structure": {
                    "hook_template": lesson.get("hook", "Tell a 20-second story about {topic}"),
                    "code_scaffold": lesson.get("code", "// Write code for {topic}"),
                    "challenge_prompt": lesson.get("challenge", "Practice {topic}")
                },
                "metadata": {
                    "estimated_time": 300,  # 5 minutes
                    "prerequisites": lesson.get("prerequisites", []),
                    "next_topics": lesson.get("next", [])
                }
            }
    
    def setup_resources(self):
        @self.mcp.resource("lesson/{topic}/{level}")
        async def lesson_resource(uri: str) -> dict:
            """Provide lesson as resource"""
            parts = uri.split('/')
            topic = parts[1]
            level = int(parts[2]) if len(parts) > 2 else 1
            
            if topic in self.lessons:
                return {
                    "uri": uri,
                    "name": f"{topic} Level {level}",
                    "mimeType": "application/json",
                    "content": json.dumps(self.lessons[topic]["levels"][level - 1])
                }
            return {"error": "Not found"}
        
        @self.mcp.resource("curriculum")
        async def curriculum_resource(uri: str) -> dict:
            """Provide full curriculum structure"""
            return {
                "uri": uri,
                "name": "Full Curriculum",
                "mimeType": "application/json",
                "content": json.dumps({
                    "topics": list(self.lessons.keys()),
                    "total_lessons": sum(len(l["levels"]) for l in self.lessons.values())
                })
            }
```

#### Step 1.3: Create State Management
**File:** `scrimba-mcp-unified/mcp_base/state_manager.py`
```python
import json
import os
from typing import Dict, Any

class StateManager:
    """Manages distributed state across MCP servers"""
    
    def __init__(self, state_dir: str = "/tmp/mcp_state"):
        self.state_dir = state_dir
        os.makedirs(state_dir, exist_ok=True)
        
    def get_student_state(self, student_id: str) -> Dict[str, Any]:
        """Get complete student state"""
        state_file = f"{self.state_dir}/{student_id}.json"
        if os.path.exists(state_file):
            with open(state_file, 'r') as f:
                return json.load(f)
        return {
            "id": student_id,
            "topics_completed": [],
            "current_topic": None,
            "current_level": 1,
            "interaction_count": 0,
            "learning_style": "unknown",
            "struggles": [],
            "strengths": []
        }
    
    def update_student_state(self, student_id: str, updates: Dict[str, Any]):
        """Update student state"""
        state = self.get_student_state(student_id)
        state.update(updates)
        state_file = f"{self.state_dir}/{student_id}.json"
        with open(state_file, 'w') as f:
            json.dump(state, f)
        return state
```

---

## PHASE 2: Orchestration (Week 2)

### Logic Flow:
```
1. Build orchestrator that coordinates other MCPs
2. Implement inter-MCP communication
3. Create routing logic
4. Test multi-server coordination
```

#### Step 2.1: Create Orchestrator MCP
**File:** `scrimba-mcp-unified/mcp_servers/orchestrator_server.py`
```python
from mcp_base.base_server import BaseMCPServer
from mcp_base.state_manager import StateManager

class OrchestratorMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__("orchestrator")
        self.state_manager = StateManager()
        self.learning_graph = self.build_learning_graph()
        
    def build_learning_graph(self):
        """Build directed graph of learning dependencies"""
        return {
            "variables": ["functions", "arrays"],
            "functions": ["objects", "callbacks"],
            "arrays": ["loops", "array-methods"],
            "loops": ["recursion"],
            # ...
        }
    
    def setup_tools(self):
        @self.mcp.tool()
        async def start_learning_journey(student_id: str, goal: str = None) -> dict:
            """Initialize personalized learning journey"""
            
            # Get or create student state
            state = self.state_manager.get_student_state(student_id)
            
            # Determine starting point
            if not state["topics_completed"]:
                starting_topic = "variables"
            else:
                # Use learning graph to find next topic
                starting_topic = self.get_next_topic(state)
            
            # Get content structure from Content MCP
            content = await self.call_other_mcp(
                "content-server",
                "get_lesson_structure",
                {"topic": starting_topic, "level": state["current_level"]}
            )
            
            # Update state
            self.state_manager.update_student_state(student_id, {
                "current_topic": starting_topic,
                "session_start": asyncio.get_event_loop().time()
            })
            
            # Publish event
            await self.publish_event("journey_started", {
                "student_id": student_id,
                "topic": starting_topic
            })
            
            return {
                "student_id": student_id,
                "current_topic": starting_topic,
                "lesson_structure": content,
                "next_topics": self.learning_graph.get(starting_topic, []),
                "progress": {
                    "completed": len(state["topics_completed"]),
                    "total": len(self.learning_graph)
                }
            }
        
        @self.mcp.tool()
        async def adaptive_next_lesson(student_id: str, performance: dict) -> dict:
            """Adaptively select next lesson based on performance"""
            
            state = self.state_manager.get_student_state(student_id)
            
            # Analyze performance
            if performance.get("success_rate", 0) < 0.7:
                # Struggling - repeat with more explanation
                action = "repeat_with_support"
                next_level = state["current_level"]
            elif performance.get("success_rate", 1) > 0.9:
                # Mastered - skip ahead
                action = "advance_topic"
                next_topic = self.get_next_topic(state, skip_level=True)
            else:
                # Normal progression
                action = "next_level"
                next_level = state["current_level"] + 1
            
            # Get appropriate content
            if action == "advance_topic":
                content = await self.call_other_mcp(
                    "content-server",
                    "get_lesson_structure",
                    {"topic": next_topic, "level": 1}
                )
            else:
                content = await self.call_other_mcp(
                    "content-server",
                    "get_lesson_structure",
                    {"topic": state["current_topic"], "level": next_level}
                )
            
            return {
                "action": action,
                "reasoning": f"Based on {performance['success_rate']*100}% success rate",
                "next_content": content
            }
        
    def setup_prompts(self):
        @self.mcp.prompt("teach_with_context")
        async def contextual_teaching_prompt(student_id: str, topic: str) -> str:
            """Generate teaching prompt with full context"""
            
            state = self.state_manager.get_student_state(student_id)
            
            prompt = f"""
You are teaching {topic} to a student with this profile:
- Topics completed: {', '.join(state['topics_completed'])}
- Current level: {state['current_level']}
- Recent struggles: {', '.join(state['struggles'][-3:])}
- Learning style: {state['learning_style']}

Adapt your teaching to address their specific needs.
Use Scrimba methodology but personalize based on their history.
"""
            return prompt
```

#### Step 2.2: Create Execution MCP
**File:** `scrimba-mcp-unified/mcp_servers/execution_server.py`
```python
import subprocess
import tempfile
import asyncio
from mcp_base.base_server import BaseMCPServer

class ExecutionMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__("execution-server")
        self.sandboxes = {}
        
    def setup_tools(self):
        @self.mcp.tool()
        async def run_javascript(code: str, student_id: str = None) -> dict:
            """Execute JavaScript code in sandbox"""
            
            # Create temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            try:
                # Run with node
                process = await asyncio.create_subprocess_exec(
                    'node', temp_file,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=5.0
                )
                
                result = {
                    "output": stdout.decode() if stdout else "",
                    "errors": stderr.decode() if stderr else "",
                    "success": process.returncode == 0
                }
                
                # Publish execution event
                await self.publish_event("code_executed", {
                    "student_id": student_id,
                    "success": result["success"],
                    "code_length": len(code)
                })
                
                # Analyze for teaching opportunities
                if "console.log" not in code:
                    result["suggestions"] = ["Try adding console.log to see values!"]
                
                return result
                
            except asyncio.TimeoutError:
                return {"error": "Code execution timeout", "success": False}
            finally:
                os.unlink(temp_file)
        
        @self.mcp.tool()
        async def analyze_code(code: str) -> dict:
            """Analyze code for patterns and issues"""
            
            analysis = {
                "has_console_log": "console.log" in code,
                "line_count": len(code.split('\n')),
                "uses_let": "let " in code,
                "uses_const": "const " in code,
                "uses_var": "var " in code,
                "has_functions": "function" in code or "=>" in code,
                "has_loops": any(loop in code for loop in ["for", "while", "forEach"]),
                "complexity_score": self.calculate_complexity(code)
            }
            
            return analysis
```

---

## PHASE 3: Integration (Week 3)

### Logic Flow:
```
1. Create launcher that starts all MCPs
2. Build inter-MCP message bus
3. Integrate with Claude Code
4. Test full system
```

#### Step 3.1: Create Federation Launcher
**File:** `scrimba-mcp-unified/launch_federation.py`
```python
#!/usr/bin/env python3
"""Launch all MCP servers in federation"""

import subprocess
import time
import sys
import signal
import redis

class MCPFederationLauncher:
    def __init__(self):
        self.processes = {}
        self.redis_client = redis.Redis(host='localhost', port=6379)
        
    def start_redis(self):
        """Ensure Redis is running for inter-MCP communication"""
        try:
            self.redis_client.ping()
            print("✓ Redis already running")
        except:
            print("Starting Redis...")
            self.processes['redis'] = subprocess.Popen(['redis-server'])
            time.sleep(2)
    
    def start_mcp_server(self, name: str, script: str):
        """Start an MCP server"""
        print(f"Starting {name}...")
        process = subprocess.Popen(
            [sys.executable, script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.processes[name] = process
        time.sleep(1)
        
        # Check if running
        if process.poll() is None:
            print(f"✓ {name} started (PID: {process.pid})")
        else:
            stdout, stderr = process.communicate()
            print(f"✗ {name} failed to start")
            print(f"Error: {stderr.decode()}")
            
    def start_all(self):
        """Start entire federation"""
        print("=" * 60)
        print("Starting MCP Federation")
        print("=" * 60)
        
        # Start Redis
        self.start_redis()
        
        # Start MCP servers in order
        servers = [
            ("Content MCP", "mcp_servers/content_server.py"),
            ("Execution MCP", "mcp_servers/execution_server.py"),
            ("Progress MCP", "mcp_servers/progress_server.py"),
            ("Orchestrator MCP", "mcp_servers/orchestrator_server.py")
        ]
        
        for name, script in servers:
            self.start_mcp_server(name, script)
        
        print("\n" + "=" * 60)
        print("Federation Running!")
        print("=" * 60)
        print("\nTo use with Claude:")
        print("  claude mcp add teaching-os python launch_federation.py")
        print("\nPress Ctrl+C to stop all servers")
        
        # Wait for interrupt
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()
    
    def shutdown(self):
        """Stop all servers"""
        print("\nShutting down federation...")
        for name, process in self.processes.items():
            process.terminate()
            process.wait(timeout=5)
            print(f"✓ {name} stopped")

if __name__ == "__main__":
    launcher = MCPFederationLauncher()
    launcher.start_all()
```

#### Step 3.2: Create Unified Interface
**File:** `scrimba-mcp-unified/mcp_servers/unified_interface.py`
```python
"""Unified interface that Claude sees"""

from mcp.server.fastmcp import FastMCP
import redis
import json

mcp = FastMCP("teaching-os")
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

@mcp.tool()
async def teach(topic: str, student_id: str = None) -> dict:
    """Single entry point for teaching - routes to federation"""
    
    # This is what Claude calls
    # Behind scenes, entire federation activates
    
    # Route to orchestrator
    request = {
        "tool": "start_learning_journey",
        "args": {"student_id": student_id or "default", "goal": topic}
    }
    
    redis_client.publish('mcp_orchestrator_requests', json.dumps(request))
    
    # Wait for orchestrated response
    # ... (response handling)
    
    return {
        "instructions": "Use the returned structure to generate a lesson",
        "structure": orchestrated_response
    }

@mcp.resource("student/{id}/progress")
async def student_progress(uri: str) -> dict:
    """Unified view of student progress from all MCPs"""
    # Aggregates data from all servers
    pass

if __name__ == "__main__":
    # This is what Claude actually connects to
    mcp.run()
```

---

## EXECUTION FLOW

### 1. System Startup
```bash
# Start the federation
cd scrimba-mcp-unified
python launch_federation.py

# In another terminal, register with Claude
claude mcp add teaching-os python mcp_servers/unified_interface.py
```

### 2. Runtime Flow
```
Claude: "Teach variables"
    ↓
Unified Interface receives request
    ↓
Publishes to Orchestrator via Redis
    ↓
Orchestrator:
    - Checks student state
    - Queries Content MCP for structure
    - Notifies Progress MCP
    - Returns coordinated response
    ↓
Content MCP:
    - Provides lesson structure
    - Publishes "content_accessed" event
    ↓
Execution MCP (when code submitted):
    - Runs code in sandbox
    - Analyzes patterns
    - Publishes results
    ↓
Progress MCP:
    - Records all interactions
    - Updates student model
    - Predicts next best action
    ↓
Response flows back to Claude
    ↓
Claude generates personalized lesson using structure
```

### 3. Inter-MCP Communication
```python
# Any MCP can call another's tools
result = await self.call_other_mcp("execution-server", "run_javascript", {
    "code": student_code,
    "student_id": student_id
})

# Any MCP can publish events
await self.publish_event("lesson_completed", {
    "topic": "variables",
    "student_id": student_id,
    "success_rate": 0.85
})

# Any MCP can subscribe to events
async def on_lesson_completed(event):
    # Update progress tracking
    pass
```

---

## INTEGRATION WITH EXISTING CODE

### 1. Keep What Works
- `production_api_session.py` - Still useful for web interface
- `scrimba-learning-app.html` - Can call federation via API
- `.claude/agents/` - Can coexist with MCP

### 2. Migration Path
```
Phase 1: Single MCP with resources (Week 1)
    ↓
Phase 2: Add orchestrator + one more MCP (Week 2)
    ↓
Phase 3: Full federation (Week 3)
    ↓
Phase 4: Production optimization (Week 4)
```

### 3. Testing Strategy
```python
# Test each MCP individually
python mcp_servers/content_server.py --test

# Test inter-MCP communication
python tests/test_federation.py

# Test with Claude
claude -p "Use teaching-os to teach me loops"

# Load test
python tests/load_test_federation.py
```

---

## KEY INSIGHT

The real power isn't in one MCP doing everything - it's in **specialized MCPs working together**, each handling what it does best:

- **Content MCP**: Manages curriculum
- **Execution MCP**: Runs code safely
- **Progress MCP**: Tracks learning
- **Orchestrator MCP**: Coordinates everything

This architecture scales infinitely - add more specialized MCPs as needed!


> give logic , flow of logic and flow of execution on how to implement this in our codebase think 
  harder

✻ Thinking…

  The user wants a concrete implementation plan for this full-power MCP architecture in their 
  existing codebase. Let me think about the logical steps, dependencies, and execution flow to 
  actually build this.

  Current state:
  - They have a scrimba-mcp-unified folder
  - They have working API server (production_api_session.py)
  - They have MCP servers but they timeout when calling Claude
  - They have agents in .claude/agents/
  - They understand MCP basics

  Need to think about:
  1. What can actually be implemented given MCP protocol limits
  2. Logical build order (dependencies)
  3. Flow of execution
  4. How to integrate with existing codebase
  5. Practical steps not just theory

  Let me create a systematic implementation plan.

● Update Todos
  ⎿  ☐ Create implementation plan for MCP federation
     ☐ Design base MCP server class
     ☐ Build orchestrator MCP
     ☐ Implement content MCP with resources
     ☐ Create execution MCP
     ☐ Build inter-MCP communication
     ☐ Test federation

✻ Thinking…

  The user wants concrete implementation steps. Let me break this down into:
  1. Logic flow (what needs to happen)
  2. Dependency chain (what depends on what)
  3. Execution flow (how to build it step by step)
  4. Integration with existing code

  I need to be practical and show how to actually build this in their codebase.

● Write(~/Desktop/dev/claude-code-mcp/MCP_FEDERATION_IMPLEMENTATION_PLAN.md)
  ⎿  Wrote 699 lines to ../MCP_FEDERATION_IMPLEMENTATION_PLAN.md
     # MCP Federation Implementation Plan
     ## 🎯 Goal: Build Full-Power MCP Teaching System
     ---
     ## PHASE 1: Foundation (Week 1)
     ### Logic Flow:
     ```
     … +689 lines (ctrl+r to expand)

· Computing… (esc to interrupt)

╭───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ >                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
  ? for shortcuts                                                                    ◯ IDE disconnected
                                        Context low (0% remaining) · Run /compact to compact & continue

