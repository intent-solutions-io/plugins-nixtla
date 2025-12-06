# Claude Code Marketplace Setup Guide

**Created**: 2025-11-23
**Version**: 1.0.0
**Status**: Active

## Overview

This document describes the Claude Code marketplace structure implemented for the Nixtla plugins repository, enabling easy installation and distribution of plugins through the official Claude Code CLI.

## Marketplace Structure

### Repository Layout

```
nixtla/
├── .claude-plugin/
│   └── marketplace.json          # Marketplace manifest
├── plugins/
│   └── nixtla-search-to-slack/
│       ├── .claude-plugin/
│       │   └── plugin.json       # Plugin manifest
│       ├── src/                  # Plugin source code
│       ├── config/               # Configuration files
│       ├── tests/                # Test suite
│       ├── README.md             # Plugin documentation
│       └── requirements.txt      # Python dependencies
├── scripts/
│   └── validate-marketplace.sh   # Validation script
└── README.md                     # Repository documentation
```

## Files Created

### 1. Marketplace Manifest (`/.claude-plugin/marketplace.json`)

**Purpose**: Defines the marketplace metadata and lists all available plugins.

**Key Fields**:
- `name`: "nixtla-plugins" (marketplace identifier)
- `owner`: Contact information for marketplace maintainer
- `metadata.version`: "0.2.0" (synced with repository VERSION file)
- `metadata.pluginRoot`: "./plugins" (base path for plugin sources)
- `plugins[]`: Array of plugin entries

**Plugin Entry Schema**:
```json
{
  "name": "nixtla-search-to-slack",
  "source": "./nixtla-search-to-slack",
  "description": "Brief description",
  "version": "0.2.0",
  "author": { "name": "...", "email": "..." },
  "keywords": [...],
  "category": "productivity",
  "license": "MIT",
  "strict": false
}
```

**Note**: `strict: false` means the plugin.json is optional - marketplace entry serves as complete manifest if plugin.json is missing.

### 2. Plugin Manifest (`/plugins/nixtla-search-to-slack/.claude-plugin/plugin.json`)

**Purpose**: Detailed plugin metadata, configuration, and capabilities.

**Key Sections**:

1. **Basic Metadata**:
   - Name, version, description
   - Author, license, homepage
   - Repository information

2. **Keywords & Classification**:
   - Keywords for discoverability
   - Category and tags
   - Maturity level ("mvp")
   - Stability ("experimental")

3. **Dependencies**:
   - Python version requirement (>=3.8)
   - Required packages (python-dotenv, pyyaml, requests, slack-sdk)
   - Alternative LLM providers (openai OR anthropic)

4. **Configuration**:
   - Required environment variables (SLACK_BOT_TOKEN, SERP_API_KEY, GITHUB_TOKEN)
   - Optional variables (AI provider keys, channel settings)

5. **Features**:
   - List of capabilities with status (all "stable")
   - Web Search, GitHub Search, AI Curation, Slack Publishing, Deduplication

6. **Support Information**:
   - Email, phone contact
   - Documentation links
   - Issues and discussions URLs

7. **Disclaimers**:
   - Not affiliated with Nixtla
   - Construction kit, not production service
   - No SLA or guarantees
   - User responsibility for costs and compliance

## Installation Methods

### Method 1: Marketplace Installation (Recommended)

```bash
# Add the marketplace
claude marketplace add https://github.com/intent-solutions-io/plugins-nixtla.git

# Install specific plugin
claude plugin install nixtla-search-to-slack

# List available plugins
claude marketplace list nixtla-plugins
```

### Method 2: Direct Git Installation

```bash
# Install directly from repository
claude plugin install github:intent-solutions-io/plugins-nixtla/plugins/nixtla-search-to-slack
```

### Method 3: Local Development Installation

```bash
# Clone repository
git clone https://github.com/intent-solutions-io/plugins-nixtla.git
cd claude-code-plugins-nixtla

# Install in development mode
claude plugin install --dev ./plugins/nixtla-search-to-slack
```

## Validation

### Automated Validation

Run the validation script to check marketplace structure:

```bash
./scripts/validate-marketplace.sh
```

**Checks Performed**:
1. marketplace.json existence and syntax
2. Required fields (name, owner, plugins)
3. Plugin entries validation
4. Plugin.json existence (if strict mode enabled)
5. Plugin directory existence

**Exit Codes**:
- 0: Validation passed
- 1: Validation failed with errors

### Manual Validation

```bash
# Validate JSON syntax
jq empty .claude-plugin/marketplace.json
jq empty plugins/nixtla-search-to-slack/.claude-plugin/plugin.json

# Check required fields
jq '.name, .owner, .plugins' .claude-plugin/marketplace.json

# List all plugins
jq '.plugins[].name' .claude-plugin/marketplace.json
```

## Version Management

### Synchronization Strategy

All version numbers should stay synchronized:

1. `/VERSION` file: `0.2.0`
2. `/.claude-plugin/marketplace.json` → `metadata.version`: `"0.2.0"`
3. `/plugins/*/plugin.json` → `version`: `"0.2.0"`
4. `/CHANGELOG.md` → Latest entry: `v0.2.0`

### Version Bump Checklist

When releasing a new version:

- [ ] Update `/VERSION` file
- [ ] Update `marketplace.json` → `metadata.version`
- [ ] Update each `plugin.json` → `version`
- [ ] Update `CHANGELOG.md` with release notes
- [ ] Update `README.md` badges and status
- [ ] Tag git commit: `git tag v0.2.0`
- [ ] Push tags: `git push --tags`

## Adding New Plugins

### Step 1: Create Plugin Structure

```bash
mkdir -p plugins/new-plugin/.claude-plugin
mkdir -p plugins/new-plugin/{src,tests,config}
touch plugins/new-plugin/.claude-plugin/plugin.json
touch plugins/new-plugin/README.md
touch plugins/new-plugin/requirements.txt
```

### Step 2: Create plugin.json

Copy template from `nixtla-search-to-slack/.claude-plugin/plugin.json` and customize:
- Update name, description, version
- Adjust keywords and category
- Update dependencies
- Define configuration requirements
- List features

### Step 3: Add to Marketplace

Edit `.claude-plugin/marketplace.json` and add plugin entry:

```json
{
  "plugins": [
    {
      "name": "new-plugin",
      "source": "./new-plugin",
      "description": "Brief description",
      "version": "0.1.0",
      "author": { "name": "...", "email": "..." },
      "keywords": [...],
      "category": "...",
      "license": "MIT",
      "strict": false
    }
  ]
}
```

### Step 4: Validate

```bash
./scripts/validate-marketplace.sh
```

### Step 5: Document

- Update main `README.md` to list new plugin
- Create plugin-specific `README.md` with setup instructions
- Add to `CHANGELOG.md`

## Troubleshooting

### Common Issues

**Issue**: Validation fails with "plugin.json not found"

**Solutions**:
- Set `strict: false` in marketplace.json (plugin.json becomes optional)
- Create plugin.json file following schema
- Verify plugin source path is correct

**Issue**: JSON syntax errors

**Solutions**:
- Use `jq` to validate: `jq empty file.json`
- Check for trailing commas (invalid in JSON)
- Verify all quotes are double quotes, not single

**Issue**: Plugin not appearing in marketplace list

**Solutions**:
- Verify plugin entry in marketplace.json plugins array
- Check plugin source path matches actual directory
- Run validation script to identify issues
- Ensure git repository is committed and pushed

### Debug Commands

```bash
# Pretty-print marketplace.json
jq '.' .claude-plugin/marketplace.json

# List all plugins with versions
jq '.plugins[] | {name, version}' .claude-plugin/marketplace.json

# Check plugin source paths
jq '.plugins[].source' .claude-plugin/marketplace.json

# Verify plugin.json exists for all plugins
for plugin in $(jq -r '.plugins[].source' .claude-plugin/marketplace.json); do
  echo "Checking: $plugin"
  ls -la "plugins/$plugin/.claude-plugin/plugin.json"
done
```

## Future Enhancements

### Planned Improvements

1. **Automated Version Sync**:
   - Script to update all version fields simultaneously
   - CI/CD validation before merging PRs

2. **Plugin Discovery**:
   - Automated plugin.json generation from README
   - Extract metadata from source code annotations

3. **Marketplace Publishing**:
   - Submit to official Claude Code marketplace
   - Automated publishing workflow

4. **Multi-Plugin Support**:
   - Add TimeGPT Pipeline Builder plugin
   - Add Bench Harness Generator plugin
   - Add Service Template Builder plugin

5. **Testing Infrastructure**:
   - Integration tests for marketplace installation
   - End-to-end plugin activation tests
   - Compatibility matrix testing

## References

### Official Documentation

- [Claude Code Plugin Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Plugin Development Guide](https://code.claude.com/docs/en/plugins)
- [JSON Schema Specification](https://json-schema.org/)

### Repository Files

- `/README.md` - Main repository documentation
- `/ARCHITECTURE.md` - Plugin architecture details
- `/CONTRIBUTING.md` - Contribution guidelines
- `/000-docs/002-AT-ARCH-plugin-architecture.md` - Technical architecture

### External Tools

- [jq](https://stedolan.github.io/jq/) - JSON processor
- [JSON Lint](https://jsonlint.com/) - Online JSON validator
- [JSON Schema Validator](https://www.jsonschemavalidator.net/)

---

**Last Updated**: 2025-11-23
**Maintainer**: Jeremy Longshore (jeremy@intentsolutions.io)
**Status**: Production Ready
