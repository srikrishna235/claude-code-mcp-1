# Scrimba Teaching API - Complete Documentation

## 🚀 Overview

The Scrimba Teaching API brings revolutionary programming education to any application. Every response is dynamically generated using Claude's intelligence, ensuring unique, contextual, and engaging learning experiences.

**Key Features:**
- **100% Dynamic Content** - No hardcoded responses
- **Claude-Powered** - Full AI intelligence in every response
- **Scrimba Methodology** - 60-second rule, console.log everything
- **Context-Aware** - Maintains conversation history
- **Fallback Mode** - Works even without Claude CLI

## 🔧 Quick Start

### Installation

```bash
# Install dependencies
pip install fastapi uvicorn

# Start the server
python production_api.py
```

### Your First Request

```bash
# Test the API
curl http://localhost:8002/

# Teach a concept
curl -X POST http://localhost:8002/api/teach \
  -H "Content-Type: application/json" \
  -d '{"topic": "variables", "step": 1}'
```

## 📡 Base URL

```
http://localhost:8002
```

## 🔑 Authentication

Currently no authentication required. Add API keys for production:

```python
# Future implementation
headers = {
  "X-API-Key": "your-api-key"
}
```

## 📚 Endpoints

### Health Check

#### `GET /`

Check API status and Claude availability.

**Response:**
```json
{
  "status": "ready",
  "mode": "intelligent",
  "version": "4.0.0",
  "session_started": "2024-01-20T10:30:00",
  "challenges_completed": 5,
  "claude_available": true
}
```

---

### Teaching Endpoints

#### `POST /api/teach`

Teach a programming concept using Scrimba methodology.

**Request Body:**
```json
{
  "topic": "functions",
  "step": 1,
  "context": "Student has learned variables"
}
```

**Parameters:**
- `topic` (string, required): Programming concept to teach
- `step` (integer, 1-5): Difficulty level
- `context` (string, optional): Additional context

**Response:**
```json
{
  "success": true,
  "lesson": "🎮 20-SECOND STORY: Last week at Netflix...\n\nTYPE THIS NOW (60 seconds):\n```javascript\nfunction greet(name) {\n  console.log('Hello ' + name);\n}\ngreet('World');\n```\n\nSee it work instantly! Your challenge: Create another function!",
  "metadata": {
    "topic": "functions",
    "step": 1,
    "next_step": 2,
    "powered_by": "claude"
  }
}
```

---

#### `POST /api/challenge`

Generate a unique coding challenge.

**Request Body:**
```json
{
  "difficulty": "easy",
  "topic": "arrays"
}
```

**Parameters:**
- `difficulty` (string): "easy" | "medium" | "hard"
- `topic` (string, optional): Related topic

**Response:**
```json
{
  "success": true,
  "challenge": "⚡ CHALLENGE TIME! 60 SECONDS!\n\nThe Pizza Calculator 🍕\n\nYou have 17 developers, each wants 3 slices...\n\nCode:\n```javascript\nlet developers = 17;\nlet slicesPerDev = 3;\nconsole.log(/* your calculation */);\n```",
  "metadata": {
    "difficulty": "easy",
    "number": 12,
    "topic": "arrays"
  }
}
```

---

#### `POST /api/check`

Review code with intelligent feedback.

**Request Body:**
```json
{
  "code": "let x = 5;\nconsole.log(x);",
  "challenge": "Create a variable"
}
```

**Parameters:**
- `code` (string, required): Code to review
- `challenge` (string, optional): Challenge context

**Response:**
```json
{
  "success": true,
  "feedback": "🌟 FANTASTIC! You're using console.log()!\n\nI LOVE that you:\n✅ Declared a variable correctly\n✅ Used console.log to verify\n\nQuick tip: Try let myName = 'YourName' next!",
  "metadata": {
    "code_length": 28,
    "has_console_log": true,
    "lines": 2
  }
}
```

---

### Adaptive Learning

#### `POST /api/adaptive`

Handle any learning request intelligently.

**Request Body:**
```json
{
  "message": "How do I reverse an array?"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Great question! TYPE THIS NOW:\n\n```javascript\nlet fruits = ['apple', 'banana', 'orange'];\nconsole.log('Original:', fruits);\n\nlet reversed = fruits.reverse();\nconsole.log('Reversed:', reversed);\n```\n\nSee the magic? Try with numbers next!",
  "context_length": 8
}
```

---

#### `POST /api/continue`

Continue from previous lesson.

**Response:**
```json
{
  "success": true,
  "next_lesson": "Excellent! Now let's level up...\n\n[Next lesson content]",
  "lesson_count": 5
}
```

---

#### `POST /api/explain-error`

Turn errors into learning opportunities.

**Request Body:**
```json
{
  "error": "Uncaught TypeError: Cannot read property 'length' of undefined"
}
```

**Response:**
```json
{
  "success": true,
  "explanation": "🎉 THIS ERROR IS AMAZING!\n\nIt means you're trying to use .length on something that doesn't exist yet!\n\nFIX:\n```javascript\nlet myArray = []; // Define it first!\nconsole.log(myArray.length); // Now it works!\n```",
  "error_type": "learning_opportunity"
}
```

---

### Session Management

#### `GET /api/session`

Get current session information.

**Response:**
```json
{
  "current_topic": "functions",
  "challenges_completed": 7,
  "conversation_length": 14,
  "session_started": "2024-01-20T10:30:00",
  "student_level": "beginner"
}
```

---

#### `POST /api/reset`

Reset session for fresh start.

**Response:**
```json
{
  "success": true,
  "message": "Fresh start! Ready for new adventures in coding! 🚀"
}
```

## 🎯 Response Format

All successful responses follow this structure:

```json
{
  "success": true,
  "data": "...",
  "metadata": {
    // Context-specific metadata
  }
}
```

## ⚠️ Error Handling

### Error Response Format

```json
{
  "error": "Error description",
  "fallback": true,
  "message": "User-friendly message"
}
```

### Common Status Codes

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Endpoint not found
- `503` - Claude temporarily unavailable (fallback mode active)

## 🔄 Rate Limiting

Currently no rate limiting. For production:

```python
# Recommended limits
- 60 requests/minute per IP
- 1000 requests/hour per API key
```

## 🌐 CORS

CORS is enabled for all origins. Configure for production:

```python
allow_origins=["https://yourdomain.com"]
```

## 💡 Usage Examples

### JavaScript/React

```javascript
// Teaching
const teachResponse = await fetch('http://localhost:8002/api/teach', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    topic: 'arrays',
    step: 1
  })
});
const lesson = await teachResponse.json();
console.log(lesson.lesson);

// Getting a challenge
const challengeResponse = await fetch('http://localhost:8002/api/challenge', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    difficulty: 'easy'
  })
});
const challenge = await challengeResponse.json();
```

### Python

```python
import requests

# Teach endpoint
response = requests.post(
    'http://localhost:8002/api/teach',
    json={'topic': 'loops', 'step': 2}
)
lesson = response.json()

# Check code
response = requests.post(
    'http://localhost:8002/api/check',
    json={'code': 'for(let i=0; i<5; i++) { console.log(i); }'}
)
feedback = response.json()
```

### cURL

```bash
# Teach
curl -X POST http://localhost:8002/api/teach \
  -H "Content-Type: application/json" \
  -d '{"topic": "objects", "step": 1}'

# Challenge
curl -X POST http://localhost:8002/api/challenge \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "medium"}'

# Continue learning
curl -X POST http://localhost:8002/api/continue
```

## 🏗️ Architecture

```
Client Request
     ↓
FastAPI Server
     ↓
Claude Integration
     ↓
Intelligent Response
     ↓
Client
```

### Components:

1. **FastAPI Server** - Handles HTTP requests
2. **Claude Integration** - Generates intelligent responses
3. **Session Manager** - Tracks conversation context
4. **Fallback System** - Ensures availability

## 🚀 Deployment

### Local Development

```bash
python production_api.py
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install fastapi uvicorn

EXPOSE 8002
CMD ["python", "production_api.py"]
```

### Environment Variables

```bash
export CLAUDE_API_KEY=your-key  # Future implementation
export API_PORT=8002
export LOG_LEVEL=INFO
```

### Production Checklist

- [ ] Configure CORS for your domain
- [ ] Add authentication/API keys
- [ ] Set up rate limiting
- [ ] Configure HTTPS
- [ ] Add monitoring/logging
- [ ] Set up error tracking
- [ ] Configure backup/fallback

## 📊 Monitoring

### Health Check

```bash
# Simple health check
curl http://localhost:8002/

# Detailed health with Claude status
curl http://localhost:8002/api/session
```

### Logging

Logs include:
- Request/response times
- Claude availability
- Error rates
- Session metrics

## 🔍 Troubleshooting

### Claude Not Available

**Symptom:** Responses contain "fallback mode"

**Solution:**
```bash
# Check Claude CLI
which claude

# Install if missing
# Follow Claude CLI installation guide
```

### Slow Responses

**Symptom:** Requests take >5 seconds

**Solution:**
- Check Claude CLI performance
- Reduce conversation history size
- Use fallback mode for faster responses

### CORS Errors

**Symptom:** Browser blocks requests

**Solution:**
```python
# Update CORS configuration
allow_origins=["http://localhost:3000", "https://yourdomain.com"]
```

## 📈 Best Practices

1. **Always include context** - Better responses with context
2. **Use appropriate difficulty** - Match student level
3. **Reset sessions periodically** - Keep context fresh
4. **Monitor Claude availability** - Have fallback ready
5. **Cache common requests** - Reduce API calls

## 🤝 Support

- **Documentation**: This file
- **Interactive Docs**: http://localhost:8002/docs
- **Alternative Docs**: http://localhost:8002/redoc
- **GitHub**: [Your repository]
- **Issues**: [GitHub Issues]

## 📝 License

MIT License - Use freely in your projects

---

**Built with ❤️ using Scrimba's revolutionary teaching methodology**

*Every response is unique, intelligent, and designed to get students coding in 60 seconds!*