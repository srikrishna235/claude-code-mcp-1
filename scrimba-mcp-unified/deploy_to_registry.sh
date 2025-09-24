#!/bin/bash
set -e

echo "=========================================="
echo "DEPLOYING SCRIMBA-MCP-UNIFIED TO REGISTRY"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Step 1: Check if package exists on PyPI
echo "Step 1: Checking PyPI availability..."
if pip index versions scrimba-mcp-unified 2>/dev/null | grep -q "scrimba-mcp-unified"; then
    print_warning "Package already exists on PyPI. Increment version if needed."
else
    print_status "Package name available on PyPI"
fi

# Step 2: Install twine
echo -e "\nStep 2: Installing twine..."
pip install --upgrade twine
print_status "Twine installed"

# Step 3: Clean and rebuild
echo -e "\nStep 3: Rebuilding package..."
rm -rf dist/ build/ *.egg-info
python -m build
print_status "Package built successfully"

# Step 4: Check package integrity
echo -e "\nStep 4: Checking package..."
twine check dist/*
print_status "Package validation passed"

# Step 5: Upload to PyPI
echo -e "\nStep 5: Publishing to PyPI..."
echo "Please make sure you have PyPI credentials configured:"
echo "  - Username: __token__"
echo "  - Password: Your PyPI API token"
echo ""
read -p "Do you want to proceed with PyPI upload? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    twine upload dist/*
    print_status "Published to PyPI successfully!"
else
    print_warning "PyPI upload skipped"
    exit 0
fi

# Step 6: Wait for PyPI propagation
echo -e "\nStep 6: Waiting for PyPI propagation..."
echo "Waiting 30 seconds for package to be available..."
sleep 30

# Step 7: Verify installation from PyPI
echo -e "\nStep 7: Verifying PyPI installation..."
pip uninstall -y scrimba-mcp-unified 2>/dev/null || true
pip install scrimba-mcp-unified
if scrimba-mcp-unified --test > /dev/null 2>&1; then
    print_status "Package installed and working from PyPI"
else
    print_error "Package installation verification failed"
    exit 1
fi

# Step 8: Submit to MCP Registry
echo -e "\nStep 8: Submitting to MCP Registry..."
echo "The package is now on PyPI. To submit to MCP registry:"
echo ""
echo "1. Install MCP publisher:"
echo "   brew install mcp-publisher (or download from GitHub)"
echo ""
echo "2. Authenticate with GitHub:"
echo "   mcp-publisher auth github"
echo ""
echo "3. Validate server.json:"
echo "   mcp-publisher validate"
echo ""
echo "4. Publish to MCP registry:"
echo "   mcp-publisher publish"
echo ""
echo "Or use the REST API:"
echo "   POST https://registry.modelcontextprotocol.io/v0/servers"
echo "   with server.json content"

print_status "Deployment script complete!"

# Step 9: Create verification script
cat > verify_deployment.py << 'EOF'
#!/usr/bin/env python3
"""Verify deployment to PyPI and MCP registry"""
import subprocess
import json
import sys

def check_pypi():
    """Check if package is on PyPI"""
    try:
        result = subprocess.run(
            ["pip", "index", "versions", "scrimba-mcp-unified"],
            capture_output=True,
            text=True
        )
        if "scrimba-mcp-unified" in result.stdout:
            print("✓ Package found on PyPI")
            return True
        else:
            print("✗ Package not found on PyPI")
            return False
    except:
        print("✗ Could not check PyPI")
        return False

def check_mcp_registry():
    """Check if server is in MCP registry"""
    try:
        import requests
        response = requests.get(
            "https://registry.modelcontextprotocol.io/v0/servers/io.github.Skills03/scrimba-mcp-unified"
        )
        if response.status_code == 200:
            print("✓ Server found in MCP registry")
            return True
        else:
            print("✗ Server not in MCP registry yet")
            return False
    except:
        print("⚠ Install 'requests' to check MCP registry")
        return False

def main():
    print("=" * 50)
    print("DEPLOYMENT VERIFICATION")
    print("=" * 50)
    
    pypi_ok = check_pypi()
    mcp_ok = check_mcp_registry()
    
    if pypi_ok:
        print("\nPyPI deployment: SUCCESS ✓")
    else:
        print("\nPyPI deployment: PENDING ...")
    
    if mcp_ok:
        print("MCP registry: SUCCESS ✓")
    else:
        print("MCP registry: PENDING ...")
    
    print("=" * 50)
    
    return 0 if (pypi_ok and mcp_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x verify_deployment.py
print_status "Created verify_deployment.py - run it to check deployment status"

echo -e "\n=========================================="
echo "DEPLOYMENT PROCESS COMPLETE"
echo "=========================================="