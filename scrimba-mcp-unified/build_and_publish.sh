#!/bin/bash

echo "========================================="
echo "Scrimba Teaching MCP - Build & Publish"
echo "========================================="
echo

# Step 1: Clean previous builds
echo "Step 1: Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info/

# Step 2: Install build tools if needed
echo "Step 2: Checking build tools..."
pip install --upgrade pip build twine

# Step 3: Build the package
echo "Step 3: Building package..."
python -m build

# Step 4: Check the package
echo "Step 4: Checking package with twine..."
python -m twine check dist/*

echo
echo "========================================="
echo "Build complete! Files in dist/:"
ls -la dist/
echo

echo "To upload to PyPI:"
echo "1. Create account at https://pypi.org"
echo "2. Get API token from https://pypi.org/manage/account/token/"
echo "3. Run: python -m twine upload dist/*"
echo "   Username: __token__"
echo "   Password: [your-api-token]"
echo
echo "Or for test PyPI first:"
echo "python -m twine upload --repository testpypi dist/*"