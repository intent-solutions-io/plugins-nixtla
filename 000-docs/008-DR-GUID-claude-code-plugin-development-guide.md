# Claude Code Plugin Development Guide - Complete Marketplace Instructions

**Document Type:** Documentation & Reference
**Category:** DR (Documentation & Reference)
**Type:** GUID (Guide)
**Version:** 1.0.0
**Last Updated:** 2025-11-23
**Source Repository:** jeremylongshore/claude-code-plugins-plus

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Plugin Architecture Overview](#plugin-architecture-overview)
3. [Creating Your First Plugin](#creating-your-first-plugin)
4. [Slash Commands](#slash-commands)
5. [Agent Skills](#agent-skills)
6. [MCP (Model Context Protocol) Servers](#mcp-model-context-protocol-servers)
7. [Hooks](#hooks)
8. [Marketplace Integration](#marketplace-integration)
9. [Best Practices & Quality Standards](#best-practices--quality-standards)
10. [Publishing & Distribution](#publishing--distribution)
11. [Real-World Examples](#real-world-examples)

---

## Executive Summary

Claude Code plugins are lightweight packages that extend Claude's capabilities through four main extension points:
1. **Slash Commands** - Custom shortcuts for frequent operations
2. **Agent Skills** - Auto-activated capabilities based on conversation context
3. **MCP Servers** - External tool and data source connections
4. **Hooks** - Workflow customization at key points

This guide provides comprehensive instructions for developing, testing, and publishing Claude Code plugins to the marketplace, based on analysis of the production marketplace repository with 254+ plugins.

---

## Plugin Architecture Overview

### Plugin Structure

Every Claude Code plugin follows this directory structure:

```
your-plugin/
├── .claude-plugin/
│   └── plugin.json         # Plugin metadata (REQUIRED)
├── commands/               # Slash commands (optional)
│   └── command-name.md     # Command definition
├── skills/                 # Agent skills (optional)
│   └── skill-name/
│       └── SKILL.md        # Skill definition
├── agents/                 # Sub-agents (optional)
│   └── agent-name.md       # Agent definition
├── hooks/                  # Event hooks (optional)
│   └── hook-config.json    # Hook configuration
├── scripts/                # Supporting scripts (optional)
│   └── helper.sh          # Executable scripts
├── README.md              # Documentation (REQUIRED)
└── LICENSE                # License file (REQUIRED)
```

### Plugin Types

1. **AI Instruction Plugins** (Most common)
   - Markdown files with YAML frontmatter
   - Work through Claude's interpretation
   - No external code execution required
   - Example: Code formatters, analyzers

2. **MCP Server Plugins** (Advanced)
   - TypeScript/Node.js applications
   - Run as separate processes
   - Provide tools via Model Context Protocol
   - Example: Database connectors, API integrations

3. **Hybrid Plugins**
   - Combine multiple extension points
   - Most powerful and flexible
   - Example: DevOps automation suites

---

## Creating Your First Plugin

### Step 1: Create Plugin Structure

```bash
# Create plugin directory
mkdir -p my-awesome-plugin/.claude-plugin

# Create required metadata file
cat > my-awesome-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-awesome-plugin",
  "version": "1.0.0",
  "description": "A brief, clear description of what your plugin does",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "repository": "https://github.com/yourusername/my-awesome-plugin",
  "license": "MIT",
  "keywords": ["productivity", "automation", "development"]
}
EOF
```

### Step 2: Add Documentation

Create a comprehensive README.md:

```markdown
# My Awesome Plugin

## Overview
Brief description of what your plugin does and why it's useful.

## Installation
\`\`\`bash
/plugin marketplace add yourusername/plugin-repo
/plugin install my-awesome-plugin@your-marketplace
\`\`\`

## Features
- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Usage Examples
[Provide concrete examples of how to use your plugin]

## Configuration
[Any configuration options or environment variables]

## Contributing
[How others can contribute to your plugin]

## License
MIT License - see LICENSE file
```

### Step 3: Add License

```bash
# Create MIT License (most common)
cat > my-awesome-plugin/LICENSE << 'EOF'
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy...
[Include full MIT license text]
EOF
```

---

## Slash Commands

Slash commands provide custom shortcuts for frequent operations.

### Creating a Slash Command

Create `commands/my-command.md`:

```markdown
---
description: Brief description of what this command does
shortcut: mc
category: productivity
difficulty: beginner
estimated_time: 2 minutes
version: 1.0.0
model: sonnet
---

# My Command

Detailed description of what this command does and when to use it.

## When to Use

Use this command when:
- Specific scenario 1
- Specific scenario 2
- Specific scenario 3

## Process

### Step 1: [Action Name]
[Describe what happens]

### Step 2: [Action Name]
[Describe what happens]

## Examples

### Example 1: Basic Usage
\`\`\`bash
/my-command parameter1 parameter2
\`\`\`

**Result:** [Describe the outcome]

## Best Practices

✅ **DO:**
- Use clear, descriptive names
- Provide helpful feedback
- Handle errors gracefully

❌ **DON'T:**
- Perform destructive operations without confirmation
- Expose sensitive information
- Ignore user preferences

## Related Commands
- `/other-command` - Description
- `/another-command` - Description
```

### Command Metadata Fields

| Field | Required | Description |
|-------|----------|-------------|
| description | Yes | One-line description |
| shortcut | No | Short alias (1-3 chars) |
| category | No | Command category |
| difficulty | No | beginner/intermediate/advanced |
| estimated_time | No | Expected execution time |
| version | No | Command version |
| model | No | sonnet/haiku (never opus) |

---

## Agent Skills

Agent Skills are AI capabilities that activate automatically based on conversation context.

### Creating an Agent Skill

Skills follow the 2025 schema specification. Create `skills/performance-analyzer/SKILL.md`:

```markdown
---
name: performance-analyzer
description: |
  Automatically analyzes code performance issues when users mention
  slow execution, optimization, or performance problems.
  Activates on phrases like "this is slow", "optimize this",
  or "performance issues".
allowed-tools: Read, Grep, Bash, Glob
version: 1.0.0
---

## Overview

This skill automatically activates when performance issues are discussed.
It analyzes code for common performance bottlenecks, suggests optimizations,
and provides benchmarking strategies.

## How It Works

### Phase 1: Detection
1. Identifies performance-related files
2. Analyzes code patterns
3. Checks for common bottlenecks

### Phase 2: Analysis
1. Profiles critical paths
2. Identifies optimization opportunities
3. Estimates performance impact

### Phase 3: Recommendations
1. Provides specific optimization suggestions
2. Offers refactoring patterns
3. Suggests monitoring strategies

## When to Use This Skill

This skill activates when users:
- Mention "slow", "performance", or "optimization"
- Ask about bottlenecks or profiling
- Request benchmark comparisons
- Discuss scaling issues

## Examples

### Example 1: Database Query Optimization

**User says:** "My database queries are running slow"

**Skill activates and:**
1. Analyzes query patterns
2. Identifies N+1 queries
3. Suggests query optimization
4. Recommends indexing strategies

### Example 2: Algorithm Optimization

**User says:** "This sorting function takes forever"

**Skill activates and:**
1. Analyzes algorithm complexity
2. Suggests more efficient algorithms
3. Provides optimized implementation
4. Adds performance benchmarks

## Best Practices

- Use minimal tool permissions (read-only when possible)
- Provide actionable suggestions
- Include measurement strategies
- Consider trade-offs (readability vs performance)
```

### Skill Metadata Fields

| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Lowercase with hyphens, max 64 chars |
| description | Yes | Clear trigger phrases, max 1024 chars |
| allowed-tools | Yes | Comma-separated tool list |
| version | Yes | Semantic versioning |

### Tool Permission Categories

```yaml
# Read-only analysis
allowed-tools: Read, Grep, Glob, Bash

# Code modification
allowed-tools: Read, Write, Edit, Grep, Glob, Bash

# Web research
allowed-tools: Read, WebFetch, WebSearch, Grep

# Database operations
allowed-tools: Read, Write, Bash, Grep

# Testing
allowed-tools: Read, Bash, Grep, Glob
```

---

## MCP (Model Context Protocol) Servers

MCP servers are TypeScript/Node.js applications that provide tools and data sources.

### Creating an MCP Server

#### Step 1: Initialize Project

```bash
mkdir -p my-mcp-server
cd my-mcp-server

# Initialize package.json
npm init -y

# Install MCP SDK
npm install @modelcontextprotocol/sdk

# Install dev dependencies
npm install -D typescript @types/node tsx
```

#### Step 2: Configure TypeScript

Create `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

#### Step 3: Implement MCP Server

Create `src/index.ts`:

```typescript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

// Create server instance
const server = new Server(
  {
    name: 'my-mcp-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'analyze_data',
        description: 'Analyze data and return insights',
        inputSchema: {
          type: 'object',
          properties: {
            data: {
              type: 'string',
              description: 'Data to analyze',
            },
          },
          required: ['data'],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case 'analyze_data':
      // Implement your tool logic
      return {
        content: [
          {
            type: 'text',
            text: `Analysis complete for: ${args.data}`,
          },
        ],
      };

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

// Start server
const transport = new StdioServerTransport();
server.connect(transport);
```

#### Step 4: Add MCP Configuration

Create `.claude-plugin/mcp.json`:

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "node",
      "args": ["dist/index.js"],
      "env": {}
    }
  }
}
```

#### Step 5: Build Scripts

Update `package.json`:

```json
{
  "scripts": {
    "build": "tsc",
    "dev": "tsx src/index.ts",
    "test": "jest",
    "typecheck": "tsc --noEmit"
  }
}
```

---

## Hooks

Hooks allow customization at key workflow points.

### Available Hook Points

| Hook | Trigger | Use Cases |
|------|---------|-----------|
| PreToolUse | Before any tool execution | Validation, logging |
| PostToolUse | After tool execution | Cleanup, analysis |
| SessionStart | New Claude session | Setup, initialization |
| DirectoryChange | User changes directory | Context updates |
| FileModified | File is edited | Auto-formatting, linting |

### Creating Hooks

Create `hooks/config.json`:

```json
{
  "hooks": {
    "PostToolUse": {
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/post-tool.sh",
      "description": "Run after any tool use"
    },
    "FileModified": {
      "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
      "description": "Auto-format on file changes",
      "filePatterns": ["*.js", "*.ts", "*.jsx", "*.tsx"]
    }
  }
}
```

Create executable script `scripts/post-tool.sh`:

```bash
#!/bin/bash
# Make sure to chmod +x this file

# Access hook environment variables
TOOL_NAME="$1"
TOOL_RESULT="$2"

# Perform your hook logic
echo "Tool $TOOL_NAME completed"

# Log to a file if needed
echo "$(date): $TOOL_NAME executed" >> "${CLAUDE_PLUGIN_ROOT}/tool-log.txt"
```

---

## Marketplace Integration

### Creating a Plugin Marketplace

A marketplace is a Git repository with a catalog file.

#### Step 1: Create Marketplace Structure

```bash
mkdir my-marketplace
cd my-marketplace

# Create catalog directory
mkdir -p .claude-plugin

# Create marketplace catalog
cat > .claude-plugin/marketplace.json << 'EOF'
{
  "name": "my-marketplace",
  "displayName": "My Plugin Marketplace",
  "description": "Collection of my Claude Code plugins",
  "owner": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "plugins": []
}
EOF
```

#### Step 2: Add Plugins to Marketplace

Edit `.claude-plugin/marketplace.json`:

```json
{
  "plugins": [
    {
      "name": "my-awesome-plugin",
      "source": "./plugins/my-awesome-plugin",
      "description": "Does awesome things",
      "version": "1.0.0",
      "category": "productivity",
      "keywords": ["automation", "development"],
      "author": {
        "name": "Your Name",
        "email": "your.email@example.com"
      }
    }
  ]
}
```

#### Step 3: Extended Metadata (Optional)

For richer marketplace features, create `marketplace.extended.json`:

```json
{
  "metadata": {
    "version": "1.0.0",
    "totalPlugins": 1,
    "categories": ["productivity"],
    "lastUpdated": "2025-11-23"
  },
  "plugins": [
    {
      "name": "my-awesome-plugin",
      "source": "./plugins/my-awesome-plugin",
      "description": "Does awesome things",
      "version": "1.0.0",
      "category": "productivity",
      "keywords": ["automation", "development"],
      "author": {
        "name": "Your Name",
        "email": "your.email@example.com"
      },
      "featured": true,
      "mcpTools": 0,
      "components": {
        "commands": 3,
        "skills": 1,
        "agents": 0,
        "hooks": 2
      }
    }
  ]
}
```

Then sync to CLI-compatible format:

```bash
# Create sync script
cat > sync-marketplace.js << 'EOF'
const extended = require('./marketplace.extended.json');
const simplified = {
  name: extended.name || "my-marketplace",
  owner: extended.owner,
  plugins: extended.plugins.map(p => ({
    name: p.name,
    source: p.source,
    description: p.description,
    version: p.version,
    category: p.category,
    keywords: p.keywords,
    author: p.author
  }))
};

require('fs').writeFileSync(
  '.claude-plugin/marketplace.json',
  JSON.stringify(simplified, null, 2)
);
EOF

node sync-marketplace.js
```

---

## Best Practices & Quality Standards

### Plugin Quality Checklist

- [ ] **Clear Naming**: Use descriptive, lowercase-hyphenated names
- [ ] **Comprehensive README**: Include installation, usage, examples
- [ ] **Semantic Versioning**: Follow MAJOR.MINOR.PATCH format
- [ ] **Minimal Permissions**: Request only necessary tool access
- [ ] **Error Handling**: Gracefully handle failures
- [ ] **User Confirmation**: Require approval for destructive operations
- [ ] **Documentation**: Document all commands, skills, and configurations
- [ ] **License**: Include appropriate open-source license
- [ ] **Testing**: Test in isolated environment before publishing
- [ ] **Security**: Never hardcode secrets or credentials

### Skill Quality Standards

**Required Elements:**
1. Clear trigger phrases in description
2. Specific `allowed-tools` list
3. Version number
4. Overview section
5. How It Works section
6. When to Use section
7. At least 2 examples

**Quality Metrics:**
- Description: 100-500 characters with explicit triggers
- Content: 2000+ characters of documentation
- Examples: Minimum 2 real-world scenarios
- Tool permissions: Minimal necessary set

### Command Quality Standards

**Required Elements:**
1. YAML frontmatter with description
2. When to Use section
3. Process/Steps section
4. At least 2 examples
5. Error handling section
6. Best practices

**Quality Metrics:**
- Documentation: 1000+ characters
- Examples: Show input and output
- Error cases: Cover common failures

---

## Publishing & Distribution

### Publishing to GitHub

1. **Create Repository**
```bash
git init
git add .
git commit -m "Initial plugin release"
git remote add origin https://github.com/yourusername/my-plugin
git push -u origin main
```

2. **Tag Release**
```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

3. **Create GitHub Release**
   - Go to repository → Releases → Create new release
   - Choose tag v1.0.0
   - Add release notes
   - Publish release

### User Installation

Users install your plugin via:

```bash
# Add your marketplace (GitHub shorthand)
/plugin marketplace add yourusername/your-marketplace-repo

# Or direct URL
/plugin marketplace add https://github.com/yourusername/your-marketplace-repo

# Install specific plugin
/plugin install my-awesome-plugin@your-marketplace

# List installed plugins
/plugin list

# Remove plugin
/plugin uninstall my-awesome-plugin
```

### Testing Before Release

```bash
# Create test marketplace locally
mkdir -p ~/test-marketplace/.claude-plugin

# Point to local plugin
cat > ~/test-marketplace/.claude-plugin/marketplace.json << EOF
{
  "name": "test",
  "owner": {"name": "Test"},
  "plugins": [{
    "name": "my-plugin",
    "source": "/absolute/path/to/my-plugin"
  }]
}
EOF

# Add test marketplace
/plugin marketplace add ~/test-marketplace

# Install and test
/plugin install my-plugin@test

# Test commands
/my-command test

# Uninstall after testing
/plugin uninstall my-plugin
```

---

## Real-World Examples

### Example 1: DevOps Automation Plugin

Structure:
```
devops-automation/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── deploy.md          # Deployment command
│   ├── rollback.md        # Rollback command
│   └── status.md          # Status check
├── skills/
│   └── incident-responder/
│       └── SKILL.md       # Auto-responds to incidents
├── hooks/
│   └── config.json        # Post-deployment hooks
└── scripts/
    ├── health-check.sh    # Health monitoring
    └── notify-slack.sh    # Notifications
```

### Example 2: Code Quality Plugin

Structure:
```
code-quality/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── lint.md            # Run linters
│   └── format.md          # Format code
├── skills/
│   ├── code-reviewer/
│   │   └── SKILL.md       # Auto code review
│   └── test-generator/
│       └── SKILL.md       # Generate tests
└── hooks/
    └── config.json        # Pre-commit hooks
```

### Example 3: MCP Database Plugin

Structure:
```
database-connector/
├── .claude-plugin/
│   ├── plugin.json
│   └── mcp.json           # MCP configuration
├── src/
│   ├── index.ts           # MCP server
│   ├── database.ts        # Database logic
│   └── queries.ts         # Query builders
├── dist/                  # Compiled JS (gitignored)
├── package.json
└── tsconfig.json
```

---

## Troubleshooting

### Common Issues

1. **Plugin not loading**
   - Verify `plugin.json` syntax
   - Check file permissions (scripts must be executable)
   - Ensure required fields are present

2. **Skill not activating**
   - Include clear trigger phrases in description
   - Verify SKILL.md has correct frontmatter
   - Check allowed-tools are valid

3. **MCP server not starting**
   - Run `npm install` and `npm build`
   - Check Node.js version (20+ required)
   - Verify `mcp.json` configuration

4. **Marketplace not found**
   - Ensure `.claude-plugin/marketplace.json` exists
   - Verify JSON syntax is valid
   - Check repository is public (or accessible)

5. **Hook not executing**
   - Make scripts executable: `chmod +x script.sh`
   - Use `${CLAUDE_PLUGIN_ROOT}` for paths
   - Check hook configuration syntax

---

## Resources

### Official Documentation
- Claude Code Docs: https://docs.claude.com/en/docs/claude-code/
- Plugin Guide: https://docs.claude.com/en/docs/claude-code/plugins
- MCP Protocol: https://modelcontextprotocol.io/

### Example Repositories
- Official Marketplace: https://github.com/jeremylongshore/claude-code-plugins
- 254+ Production Plugins: https://github.com/jeremylongshore/claude-code-plugins-plus
- Anthropic Skills Spec: https://github.com/anthropics/skills

### Community
- Discord: https://discord.com/invite/anthropic
- GitHub Discussions: https://github.com/anthropics/claude-code/discussions

---

## Summary

Claude Code plugins provide a powerful way to extend Claude's capabilities through:

1. **Slash Commands** - Quick shortcuts for common tasks
2. **Agent Skills** - Context-aware auto-activation
3. **MCP Servers** - External tool integration
4. **Hooks** - Workflow customization

Success keys:
- Start simple with commands or skills
- Follow quality standards and best practices
- Test thoroughly before publishing
- Provide clear documentation
- Request minimal permissions
- Handle errors gracefully

The plugin ecosystem is rapidly growing with 250+ production plugins available. By following this guide, you can create high-quality plugins that provide real value to the Claude Code community.

---

**Document Version:** 1.0.0
**Last Updated:** 2025-11-23
**Based on:** claude-code-plugins-plus v1.4.0 (254 plugins)
**Marketplace:** https://github.com/jeremylongshore/claude-code-plugins