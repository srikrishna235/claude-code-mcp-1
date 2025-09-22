# Deployment Guide - Scrimba Teaching API

## 🚀 Quick Deploy Options

### Option 1: Railway (Recommended - 3 minutes)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up

# Your API is live at: https://your-app.railway.app
```

### Option 2: Render

1. Push to GitHub
2. Connect on [render.com](https://render.com)
3. Deploy as Web Service
4. Environment: Python 3
5. Start Command: `python production_api.py`

### Option 3: Heroku

```bash
# Create Procfile
echo "web: python production_api.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

## 🐳 Docker Deployment

### Build & Run

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY production_api.py .

# Expose port
EXPOSE 8002

# Run
CMD ["python", "production_api.py"]
```

### Docker Commands

```bash
# Build
docker build -t scrimba-api .

# Run locally
docker run -p 8002:8002 scrimba-api

# Push to Docker Hub
docker tag scrimba-api yourusername/scrimba-api
docker push yourusername/scrimba-api
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8002:8002"
    environment:
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
    restart: unless-stopped
```

## ☁️ Cloud Deployment

### AWS EC2

```bash
# 1. Launch EC2 instance (Ubuntu)
# 2. SSH into instance
ssh -i your-key.pem ubuntu@your-instance-ip

# 3. Setup
sudo apt update
sudo apt install python3-pip nginx
pip3 install fastapi uvicorn

# 4. Clone and run
git clone your-repo
cd your-repo/api-bridge
python3 production_api.py
```

### Google Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT-ID/scrimba-api

# Deploy
gcloud run deploy --image gcr.io/PROJECT-ID/scrimba-api --platform managed
```

### Azure Container Instances

```bash
# Create container
az container create \
  --resource-group myResourceGroup \
  --name scrimba-api \
  --image yourusername/scrimba-api \
  --dns-name-label scrimba-api \
  --ports 8002
```

## 🔧 Production Configuration

### Environment Variables

```bash
# .env file
API_PORT=8002
LOG_LEVEL=INFO
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
MAX_REQUESTS_PER_MINUTE=60
CLAUDE_TIMEOUT=30
FALLBACK_MODE=auto
```

### Load in Python

```python
import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv('API_PORT', 8002))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
```

## 🔒 Security Setup

### HTTPS with Nginx

```nginx
# /etc/nginx/sites-available/scrimba-api
server {
    listen 80;
    server_name api.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name api.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8002;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL Certificate

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d api.yourdomain.com
```

## 🎯 Production Checklist

### Pre-Deployment

- [ ] **Dependencies**
  ```txt
  # requirements.txt
  fastapi==0.104.1
  uvicorn==0.24.0
  pydantic==2.5.0
  python-dotenv==1.0.0
  ```

- [ ] **Error Handling**
  - Fallback responses ready
  - Graceful Claude failures
  - Rate limiting configured

- [ ] **Security**
  - CORS configured
  - HTTPS enabled
  - API keys (if needed)
  - Input validation

### Deployment

- [ ] **Server Setup**
  ```bash
  # System service (systemd)
  sudo nano /etc/systemd/system/scrimba-api.service
  ```
  
  ```ini
  [Unit]
  Description=Scrimba Teaching API
  After=network.target

  [Service]
  Type=simple
  User=ubuntu
  WorkingDirectory=/home/ubuntu/scrimba-api
  Environment=PATH=/home/ubuntu/.local/bin:/usr/bin
  ExecStart=/usr/bin/python3 production_api.py
  Restart=on-failure

  [Install]
  WantedBy=multi-user.target
  ```

- [ ] **Start Service**
  ```bash
  sudo systemctl enable scrimba-api
  sudo systemctl start scrimba-api
  sudo systemctl status scrimba-api
  ```

### Post-Deployment

- [ ] **Monitoring**
  ```bash
  # Health check
  curl https://api.yourdomain.com/
  
  # Test endpoints
  curl -X POST https://api.yourdomain.com/api/teach \
    -H "Content-Type: application/json" \
    -d '{"topic": "variables"}'
  ```

- [ ] **Logging**
  ```bash
  # View logs
  sudo journalctl -u scrimba-api -f
  
  # Log rotation
  sudo nano /etc/logrotate.d/scrimba-api
  ```

## 📊 Monitoring & Scaling

### Basic Monitoring

```python
# Add to production_api.py
from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
```

### Auto-Scaling (Docker Swarm)

```bash
# Initialize swarm
docker swarm init

# Create service
docker service create \
  --name scrimba-api \
  --replicas 3 \
  --publish published=8002,target=8002 \
  yourusername/scrimba-api

# Scale
docker service scale scrimba-api=5
```

### Load Balancing (HAProxy)

```
# haproxy.cfg
frontend api_front
    bind *:80
    default_backend api_back

backend api_back
    balance roundrobin
    server api1 localhost:8002 check
    server api2 localhost:8003 check
    server api3 localhost:8004 check
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Railway
      run: |
        npm install -g @railway/cli
        railway up
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## 🆘 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find process
lsof -i :8002
# Kill process
kill -9 PID
```

**Module Not Found**
```bash
pip install -r requirements.txt
```

**Claude Not Working**
```bash
# Check Claude CLI
which claude
# Test directly
echo "test" | claude
```

**CORS Errors**
```python
# Update production_api.py
allow_origins=["https://your-frontend.com"]
```

## 📈 Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_cached_response(prompt_hash):
    return await ask_claude(prompt)
```

### Database (Optional)

```python
# Store common responses
import sqlite3

conn = sqlite3.connect('responses.db')
# Cache frequent queries
```

### CDN for Static Assets

Use Cloudflare or AWS CloudFront for global distribution.

## 🎯 Ready to Deploy!

Your API is production-ready with:
- ✅ Intelligent Claude responses
- ✅ Fallback for reliability
- ✅ Session management
- ✅ Error handling
- ✅ Documentation
- ✅ Monitoring ready

**Deploy now and bring Scrimba's magic to the world!** 🚀