# Publishing scrimba-mcp-unified to PyPI

## Package Status
✅ **READY FOR PUBLICATION**

- Package Name: `scrimba-mcp-unified`
- Version: 3.0.0
- Built Files:
  - `dist/scrimba_mcp_unified-3.0.0.tar.gz` 
  - `dist/scrimba_mcp_unified-3.0.0-py3-none-any.whl`

## Manual Publishing Steps

### 1. Create PyPI Account (if needed)
Visit https://pypi.org/account/register/

### 2. Generate API Token
1. Go to https://pypi.org/manage/account/
2. Scroll to "API tokens"
3. Click "Add API token"
4. Set scope to "Entire account" for first upload
5. Copy the token (starts with `pypi-`)

### 3. Configure PyPI Credentials

Create `~/.pypirc`:
```bash
cat > ~/.pypirc << 'EOF'
[pypi]
username = __token__
password = YOUR_TOKEN_HERE
EOF

chmod 600 ~/.pypirc
```

Or use environment variable:
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
```

### 4. Upload to PyPI

```bash
cd /home/rishabh/Desktop/dev/claude-code-mcp/scrimba-mcp-unified

# Upload to PyPI
twine upload dist/*
```

### 5. Verify Publication

After upload, check:
- https://pypi.org/project/scrimba-mcp-unified/

Test installation:
```bash
# Uninstall local version
pip uninstall -y scrimba-mcp-unified

# Install from PyPI
pip install scrimba-mcp-unified

# Test it works
scrimba-mcp-unified --test
```

## Alternative: TestPyPI First (Recommended)

### Upload to TestPyPI
```bash
# Upload to test repository
twine upload --repository testpypi dist/*
```

### Install from TestPyPI
```bash
pip install --index-url https://test.pypi.org/simple/ scrimba-mcp-unified
```

## After PyPI Publication

### Submit to MCP Registry

1. **Install MCP Publisher**:
```bash
# macOS
brew install mcp-publisher

# Or download from GitHub
https://github.com/modelcontextprotocol/publisher/releases
```

2. **Authenticate with GitHub**:
```bash
mcp-publisher auth github
```

3. **Publish to Registry**:
```bash
cd /home/rishabh/Desktop/dev/claude-code-mcp/scrimba-mcp-unified
mcp-publisher publish
```

This will submit the `server.json` configuration to the MCP registry.

### Configure in Claude Desktop

Once on PyPI, users can install via:

```json
{
  "mcpServers": {
    "scrimba-mcp-unified": {
      "command": "uvx",
      "args": ["scrimba-mcp-unified"]
    }
  }
}
```

Or with pip:
```json
{
  "mcpServers": {
    "scrimba-mcp-unified": {
      "command": "scrimba-mcp-unified"
    }
  }
}
```

## Current Package Contents

The package includes:
- **20+ Tools** for interactive programming education
- **Unified server** combining all agents
- **Visual learning** prompts and animations
- **Code visualization** tools
- **Real projects** and challenges

## Files Ready for Upload

```bash
$ ls -la dist/
-rw-rw-r--  1 rishabh rishabh 11930 Sep 24 19:47 scrimba_mcp_unified-3.0.0-py3-none-any.whl
-rw-rw-r--  1 rishabh rishabh 13698 Sep 24 19:47 scrimba_mcp_unified-3.0.0.tar.gz
```

Both distribution files are built and ready for upload.

## Quick Command Reference

```bash
# Build (already done)
python -m build

# Check package
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install scrimba-mcp-unified
scrimba-mcp-unified --test
```

---

**Status**: Package built and tested locally. Ready for PyPI publication once credentials are configured.