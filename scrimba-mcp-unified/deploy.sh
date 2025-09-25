#!/bin/bash

# Deploy Scrimba MCP to Railway

echo "🚀 Deploying Scrimba MCP to Railway..."

# Set environment variables
export RAILWAY_TOKEN=f9553690-34bb-4cfc-b1b2-6b4c1d0ab525
export MCP_API_KEY=scrimba-teaching-secure-key-2024

# Create or link project (non-interactive)
railway projects create scrimba-mcp --json > project.json 2>/dev/null || true

# Link to the project
PROJECT_ID=$(railway projects list --json | python3 -c "import json, sys; data = json.load(sys.stdin); print(next((p['id'] for p in data if p['name'] == 'scrimba-mcp'), ''))")

if [ -z "$PROJECT_ID" ]; then
    echo "Creating new project..."
    PROJECT_ID=$(railway projects create scrimba-mcp --json | python3 -c "import json, sys; print(json.load(sys.stdin)['id'])")
fi

# Deploy
echo "Deploying to project: $PROJECT_ID"
railway up --service scrimba-mcp --environment production

echo "✅ Deployment complete!"
echo "Check your app at: https://railway.app/dashboard"