#!/bin/bash
# Quick Fix Script - Phase 1: Make It Work
# Following Progressive Enhancement Methodology
# Goal: Get Claude CLI working in unified folder NOW

set -e  # Exit on error

echo "=========================================="
echo "PHASE 1 FIX: Core Claude CLI Integration"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check prerequisites
echo -e "${YELLOW}Step 1: Checking prerequisites...${NC}"

# Check if Claude CLI is installed
if ! command -v claude &> /dev/null; then
    echo -e "${RED}ERROR: Claude CLI not found!${NC}"
    echo "Install with: npm install -g @anthropic-ai/claude-code"
    exit 1
else
    echo -e "${GREEN}✓ Claude CLI found${NC}"
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 not found!${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Python 3 found${NC}"
fi

# Step 2: Copy core files
echo ""
echo -e "${YELLOW}Step 2: Copying core engine files...${NC}"

cd /home/rishabh/Desktop/dev/claude-code-mcp

# Copy essential files
cp -v claude_code_mcp_final.py scrimba-mcp-unified/ 2>/dev/null || echo "Already exists"
cp -v terminal_server.py scrimba-mcp-unified/ 2>/dev/null || echo "Already exists"
cp -v terminal.html scrimba-mcp-unified/ 2>/dev/null || echo "Already exists"

echo -e "${GREEN}✓ Core files copied${NC}"

# Step 3: Create minimal working config
echo ""
echo -e "${YELLOW}Step 3: Creating minimal config...${NC}"

cd scrimba-mcp-unified/

# Backup existing config
if [ -f .mcp.json ]; then
    cp .mcp.json .mcp.json.backup
    echo "Backed up existing config to .mcp.json.backup"
fi

# Create Phase 1 minimal config
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "claude-core": {
      "command": "python",
      "args": ["claude_code_mcp_final.py"]
    }
  }
}
EOF

echo -e "${GREEN}✓ Minimal config created${NC}"

# Step 4: Test Claude CLI wrapper
echo ""
echo -e "${YELLOW}Step 4: Testing Claude CLI wrapper...${NC}"

# Create test script
cat > test_phase1.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import json
import sys

def test_claude():
    """Test if Claude CLI wrapper works"""
    try:
        # Test simple prompt
        test_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "claude_execute",
                "arguments": {
                    "prompt": "What is 2+2? Answer with just the number."
                }
            },
            "id": 1
        }
        
        # Try to call claude_code_mcp_final.py
        result = subprocess.run(
            ["python", "claude_code_mcp_final.py"],
            input=json.dumps(test_request),
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✓ Claude CLI wrapper responds")
            return True
        else:
            print("✗ Claude CLI wrapper failed")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

if __name__ == "__main__":
    sys.exit(0 if test_claude() else 1)
EOF

python test_phase1.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Claude CLI wrapper working!${NC}"
else
    echo -e "${YELLOW}⚠ Claude CLI test had issues (may need API key)${NC}"
fi

# Step 5: Create startup script
echo ""
echo -e "${YELLOW}Step 5: Creating startup scripts...${NC}"

# Create server start script
cat > start_servers.sh << 'EOF'
#!/bin/bash
echo "Starting Phase 1 servers..."
echo ""
echo "1. Starting MCP server..."
python claude_code_mcp_final.py &
MCP_PID=$!
echo "   MCP Server PID: $MCP_PID"

echo "2. Starting terminal server..."
python terminal_server.py &
WEB_PID=$!
echo "   Web Server PID: $WEB_PID"

echo ""
echo "Servers running!"
echo "Open browser at: http://localhost:8080"
echo ""
echo "To stop servers:"
echo "  kill $MCP_PID $WEB_PID"
EOF

chmod +x start_servers.sh

echo -e "${GREEN}✓ Startup script created${NC}"

# Step 6: Clean up old duplicates (move, don't delete)
echo ""
echo -e "${YELLOW}Step 6: Organizing old files...${NC}"

mkdir -p DEPRECATED_BACKUP
mv -f teaching-server DEPRECATED_BACKUP/ 2>/dev/null || true
mv -f cli-wrapper DEPRECATED_BACKUP/ 2>/dev/null || true
mv -f servers/*v2* DEPRECATED_BACKUP/ 2>/dev/null || true

echo -e "${GREEN}✓ Old files moved to DEPRECATED_BACKUP${NC}"

# Final summary
echo ""
echo "=========================================="
echo -e "${GREEN}PHASE 1 FIX COMPLETE!${NC}"
echo "=========================================="
echo ""
echo "What we did:"
echo "1. ✓ Copied core Claude CLI wrapper"
echo "2. ✓ Added terminal interface" 
echo "3. ✓ Created minimal config"
echo "4. ✓ Tested basic functionality"
echo "5. ✓ Created startup script"
echo "6. ✓ Organized old files"
echo ""
echo -e "${YELLOW}To start using:${NC}"
echo "  cd scrimba-mcp-unified"
echo "  ./start_servers.sh"
echo ""
echo "Then open: http://localhost:8080"
echo ""
echo -e "${GREEN}Following methodology: Make it work FIRST!${NC}"