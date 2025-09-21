#!/bin/bash
# Script to publish Scrimba Teaching MCP to the registry
# Bypasses mcp-publisher bug with registryType conversion

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Publishing Scrimba Teaching MCP to Registry${NC}"

# Check if token file exists
if [ ! -f ~/.mcp_publisher_token ]; then
    echo -e "${RED}Error: Token file not found at ~/.mcp_publisher_token${NC}"
    echo "Please run: mcp-publisher login github"
    exit 1
fi

# Extract token
TOKEN=$(cat ~/.mcp_publisher_token | jq -r .token)

if [ -z "$TOKEN" ] || [ "$TOKEN" = "null" ]; then
    echo -e "${RED}Error: Could not extract token${NC}"
    exit 1
fi

# Get version from argument or default
VERSION=${1:-"1.0.1"}
echo -e "${GREEN}Publishing version: $VERSION${NC}"

# Make the publication request
RESPONSE=$(curl -s -X POST "https://registry.modelcontextprotocol.io/v0/publish" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"name\": \"io.github.Skills03/scrimba-teaching\",
    \"description\": \"Interactive programming teacher using Scrimba methodology for 10x retention\",
    \"version\": \"$VERSION\",
    \"packages\": [{
      \"registryType\": \"pypi\",
      \"identifier\": \"scrimba-teaching-mcp\",
      \"version\": \"$VERSION\",
      \"transport\": {
        \"type\": \"stdio\"
      }
    }]
  }")

# Check if response contains error
if echo "$RESPONSE" | jq -e '.errors' > /dev/null 2>&1; then
    echo -e "${RED}Error publishing:${NC}"
    echo "$RESPONSE" | jq .
    exit 1
elif echo "$RESPONSE" | jq -e '._meta' > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Successfully published!${NC}"
    echo "$RESPONSE" | jq '{
        name: .name,
        version: .version,
        serverId: ._meta."io.modelcontextprotocol.registry/official".serverId,
        versionId: ._meta."io.modelcontextprotocol.registry/official".versionId,
        publishedAt: ._meta."io.modelcontextprotocol.registry/official".publishedAt
    }'
    
    echo -e "\n${GREEN}Verify at:${NC}"
    echo "https://registry.modelcontextprotocol.io/v0/servers?search=scrimba"
else
    echo -e "${YELLOW}Unexpected response:${NC}"
    echo "$RESPONSE" | jq .
fi