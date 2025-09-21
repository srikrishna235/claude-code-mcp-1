# Scrimba Teaching MCP - Quick Reference

## Live URLs
- **MCP Registry:** `io.github.Skills03/scrimba-teaching`
- **PyPI:** https://pypi.org/project/scrimba-teaching-mcp/
- **Server ID:** `db943fb5-a144-442c-8cc3-d76be306b58b`

## Install & Run
```bash
pip install scrimba-teaching-mcp
python -m scrimba_teaching_mcp
```

## Publish New Version
```bash
# 1. Update version in pyproject.toml
# 2. Build & upload to PyPI
python -m build
twine upload dist/scrimba_teaching_mcp-NEW_VERSION*

# 3. Publish to MCP Registry
./publish-to-registry.sh NEW_VERSION
```

## Manual Registry Publication (if script fails)
```bash
TOKEN=$(cat ~/.mcp_publisher_token | jq -r .token)
curl -X POST "https://registry.modelcontextprotocol.io/v0/publish" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "io.github.Skills03/scrimba-teaching",
    "description": "Interactive programming teacher using Scrimba methodology for 10x retention",
    "version": "VERSION_HERE",
    "packages": [{
      "registryType": "pypi",
      "identifier": "scrimba-teaching-mcp",
      "version": "VERSION_HERE",
      "transport": {"type": "stdio"}
    }]
  }'
```

## Re-authenticate
```bash
mcp-publisher login github
# Follow device code flow
```

## Verify Publication
```bash
curl -s "https://registry.modelcontextprotocol.io/v0/servers?search=scrimba" | jq .
```