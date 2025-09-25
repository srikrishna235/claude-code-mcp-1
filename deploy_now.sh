#!/bin/bash
# Quick & Secure Railway Deployment for Scrimba MCP

echo "🚀 Deploying Scrimba MCP to Railway..."

# Check for Railway CLI
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    curl -fsSL https://railway.app/install.sh | sh
fi

# Set token securely
echo "Enter your NEW Railway token (hidden):"
read -s RAILWAY_TOKEN
export RAILWAY_TOKEN

# Navigate to project
cd scrimba-mcp-unified

# Create Railway config
cat > railway.json << EOF
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python -m scrimba_mcp_unified"
  }
}
EOF

# Deploy
railway login --browserless
railway up --detach

echo "✅ Deployment started!"
echo "Check status at: https://railway.app/dashboard"
echo ""
echo "Once deployed, add to Claude Desktop:"
echo "URL: https://YOUR-APP.up.railway.app/mcp"