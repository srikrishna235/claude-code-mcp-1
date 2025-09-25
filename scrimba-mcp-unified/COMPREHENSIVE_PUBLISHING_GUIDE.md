# 🚀 Comprehensive MCP Publishing Guide

## Current Status
- **PyPI Package**: `scrimba-teaching-mcp` v3.0.1 ✅
- **MCP Registry**: `io.github.srikrishna235/scrimba-teaching-mcp` ✅
- **GitHub**: Skills03/claude-code-mcp

## 📦 Complete Publishing Workflow

### Step 1: Pre-Release Checklist
```bash
cd scrimba-mcp-unified

# Verify all tests pass
python test_unified_server.py
python test_mcp_servers.py

# Validate server.json
python validate_server_json.py

# Check package structure
tree scrimba_mcp_unified/
```

### Step 2: Version Management
```bash
# Update version in THREE places:
# 1. pyproject.toml -> version = "3.0.2"
# 2. server.json -> "version": "3.0.2" 
# 3. scrimba_mcp_unified/__init__.py -> __version__ = "3.0.2"

# Semantic versioning:
# MAJOR.MINOR.PATCH
# - MAJOR: Breaking changes
# - MINOR: New features (backward compatible)
# - PATCH: Bug fixes
```

### Step 3: Build & Publish to PyPI
```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Build the package
python -m build

# Check package integrity
twine check dist/*

# Upload to PyPI
twine upload dist/*
# Username: __token__
# Password: pypi-AgEIcHlwaS5vcmc... (your token)

# Verify installation
pip install --upgrade scrimba-teaching-mcp
scrimba-mcp-unified --test
```

### Step 4: Publish to MCP Registry
```bash
# Method 1: Using REST API (Recommended)
cat > publish_to_registry.sh << 'EOF'
#!/bin/bash
TOKEN="your-mcp-registry-token-here"

curl -X POST "https://registry.modelcontextprotocol.io/v0/publish" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d @server.json

echo "Published to MCP Registry!"
EOF

chmod +x publish_to_registry.sh
./publish_to_registry.sh
```

### Step 5: GitHub Release
```bash
# Commit all changes
git add .
git commit -m "Release v3.0.2: [Brief description]"
git push origin main

# Create GitHub release
git tag -a v3.0.2 -m "Release v3.0.2"
git push origin v3.0.2
```

## 🤖 Automated CI/CD Pipeline

### GitHub Actions Workflow
Create `.github/workflows/publish.yml`:

```yaml
name: Publish MCP Server

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
    
    - name: Wait for PyPI propagation
      run: sleep 60
    
    - name: Publish to MCP Registry
      env:
        MCP_TOKEN: ${{ secrets.MCP_REGISTRY_TOKEN }}
      run: |
        curl -X POST "https://registry.modelcontextprotocol.io/v0/publish" \
          -H "Content-Type: application/json" \
          -H "Authorization: Bearer $MCP_TOKEN" \
          -d @scrimba-mcp-unified/server.json
```

## 🔧 One-Command Publishing

Create `publish.sh`:

```bash
#!/bin/bash
set -e

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "Usage: ./publish.sh <version>"
    echo "Example: ./publish.sh 3.0.2"
    exit 1
fi

echo "📦 Publishing Scrimba MCP v$VERSION"

# Update version in all files
sed -i "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml
sed -i "s/\"version\": \".*\"/\"version\": \"$VERSION\"/" server.json
sed -i "s/__version__ = \".*\"/__version__ = \"$VERSION\"/" scrimba_mcp_unified/__init__.py

# Build and publish to PyPI
rm -rf dist/ build/
python -m build
twine upload dist/*

# Wait for propagation
echo "⏳ Waiting for PyPI propagation..."
sleep 60

# Publish to MCP Registry
curl -X POST "https://registry.modelcontextprotocol.io/v0/publish" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MCP_REGISTRY_TOKEN" \
  -d @server.json

# Git operations
git add .
git commit -m "Release v$VERSION"
git tag -a v$VERSION -m "Release v$VERSION"
git push origin main --tags

echo "✅ Successfully published v$VERSION!"
echo "PyPI: https://pypi.org/project/scrimba-teaching-mcp/$VERSION/"
echo "MCP Registry: Search for 'scrimba' in Claude Desktop"
```

## 📋 Environment Setup

### Required Tokens
```bash
# Save in ~/.bashrc or ~/.zshrc
export PYPI_API_TOKEN="pypi-AgEIcHlwaS5vcmc..."
export MCP_REGISTRY_TOKEN="mcp_pat_..."
```

### GitHub Secrets (for CI/CD)
1. Go to Settings → Secrets → Actions
2. Add:
   - `PYPI_API_TOKEN`: Your PyPI token
   - `MCP_REGISTRY_TOKEN`: Your MCP registry token

## 🔍 Verification Commands

```bash
# Check PyPI
pip index versions scrimba-teaching-mcp

# Test installation
pip install --upgrade scrimba-teaching-mcp
python -c "import scrimba_mcp_unified; print(scrimba_mcp_unified.__version__)"

# Check MCP Registry (via API)
curl "https://registry.modelcontextprotocol.io/v0/servers?search=scrimba"

# Test in Claude Desktop
# Add to config and restart Claude
{
  "mcpServers": {
    "scrimba": {
      "command": "uvx",
      "args": ["scrimba-teaching-mcp"]
    }
  }
}
```

## 📊 Publishing Decision Tree

```
Is this a bug fix?
├─ YES → Increment PATCH (3.0.1 → 3.0.2)
└─ NO → Is this a new feature?
    ├─ YES → Increment MINOR (3.0.2 → 3.1.0)
    └─ NO → Breaking change?
        └─ YES → Increment MAJOR (3.1.0 → 4.0.0)
```

## 🚨 Common Issues & Solutions

### Issue 1: PyPI Token Scope Error
**Error**: "Invalid token scope"
**Solution**: Token must be scoped to exact package name `scrimba-teaching-mcp`

### Issue 2: MCP Registry Field Error
**Error**: "registryType vs registry_type"
**Solution**: Use direct curl instead of mcp-publisher tool

### Issue 3: Version Mismatch
**Error**: "Version already exists"
**Solution**: Always increment version before publishing

### Issue 4: Import Errors After Publishing
**Error**: "Module not found"
**Solution**: Ensure `__init__.py` exists in all directories

## 📈 Success Metrics

After successful publishing:
- ✅ Package appears on https://pypi.org/project/scrimba-teaching-mcp/
- ✅ `pip install scrimba-teaching-mcp` works globally
- ✅ MCP Registry search returns your server
- ✅ Claude Desktop discovers and uses your server
- ✅ GitHub release is tagged and documented

## 🔗 Quick Links
- **PyPI Package**: https://pypi.org/project/scrimba-teaching-mcp/
- **GitHub Repo**: https://github.com/Skills03/claude-code-mcp
- **MCP Registry**: https://registry.modelcontextprotocol.io/
- **MCP Docs**: https://modelcontextprotocol.io/docs

---

**Last Updated**: 2025-09-25
**Current Version**: 3.0.1
**Maintainer**: Skills03/srikrishna235