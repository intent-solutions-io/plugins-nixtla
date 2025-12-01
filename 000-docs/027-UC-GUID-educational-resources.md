# Educational Resources for Claude Code Plugin Development

**Learn from the Main Claude Code Plugins Marketplace**

This document links to educational resources from the [Claude Code Plugins Marketplace](https://github.com/jeremylongshore/claude-code-plugins), the comprehensive learning hub for plugin development with 254 production plugins and extensive documentation.

---

## Quick Links to Essential Resources

### Core Documentation
- **[Main Marketplace Repository](https://github.com/jeremylongshore/claude-code-plugins)** - 254 plugins, 185 Agent Skills, complete learning infrastructure
- **[Live Marketplace Website](https://claudecodeplugins.io/)** - Browse all plugins with descriptions
- **[Contributing Guide](https://github.com/jeremylongshore/claude-code-plugins/blob/main/CONTRIBUTING.md)** - Complete 396-line guide to plugin submission
- **[Security Policy](https://github.com/jeremylongshore/claude-code-plugins/blob/main/SECURITY.md)** - 407-line comprehensive security framework

### Learning Paths

The main marketplace offers three structured learning paths:

1. **[Quick Start Path](https://github.com/jeremylongshore/claude-code-plugins/blob/main/README.md#quick-start-15-minutes)** (15 minutes)
   - Install and use your first plugin
   - Basic CLI commands
   - Understanding plugin structure

2. **[Plugin Creator Path](https://github.com/jeremylongshore/claude-code-plugins/blob/main/000-docs/067-UC-GUID-plugin-creator-path.md)** (3 hours)
   - Build your first complete plugin from scratch
   - Covers: anatomy, templates, slash commands, hooks, agents
   - Testing and publishing workflow

3. **[Advanced Developer Path](https://github.com/jeremylongshore/claude-code-plugins/blob/main/000-docs/068-UC-GUID-advanced-developer-path.md)** (1 day)
   - Create production MCP servers
   - TypeScript/Node.js development
   - Tool design and deployment

---

## Agent Skills Development

### 2025 Schema Documentation
- **[Skills Schema 2025 Specification](https://github.com/jeremylongshore/claude-code-plugins/blob/main/SKILLS_SCHEMA_2025.md)** - Official schema with `allowed-tools` and versioning
- **[Skill Activation Guide](https://github.com/jeremylongshore/claude-code-plugins/blob/main/SKILL_ACTIVATION_GUIDE.md)** - How skills activate with trigger phrases
- **[Skills Automation Documentation](https://github.com/jeremylongshore/claude-code-plugins/blob/main/scripts/SKILLS_AUTOMATION.md)** - Automated generation with Vertex AI

### Agent Skills Best Practices

**Tool Permission Categories:**
```yaml
# Read-only analysis
allowed-tools: Read, Grep, Glob, Bash

# Code editing
allowed-tools: Read, Write, Edit, Grep, Glob, Bash

# Web research
allowed-tools: Read, WebFetch, WebSearch, Grep

# Database operations
allowed-tools: Read, Write, Bash, Grep

# Testing
allowed-tools: Read, Bash, Grep, Glob
```

**Trigger Phrase Examples for Nixtla:**
- "analyze forecast accuracy"
- "compare model performance"
- "generate TimeGPT pipeline"
- "benchmark forecasting models"
- "create forecast service"

---

## Plugin Templates & Examples

### Official Templates
- **[Minimal Plugin Template](https://github.com/jeremylongshore/claude-code-plugins/tree/main/templates/minimal-plugin)** - Bare minimum structure
- **[Command Plugin Template](https://github.com/jeremylongshore/claude-code-plugins/tree/main/templates/command-plugin)** - With slash commands
- **[Agent Plugin Template](https://github.com/jeremylongshore/claude-code-plugins/tree/main/templates/agent-plugin)** - With AI agent
- **[Full Plugin Template](https://github.com/jeremylongshore/claude-code-plugins/tree/main/templates/full-plugin)** - All features combined

### Working Examples
- **[Hello World Plugin](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/examples/hello-world)** - Basic slash command
- **[Security Agent Plugin](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/examples/security-agent)** - Specialized agent
- **[Formatter Plugin](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/examples/formatter)** - Hook-based automation

---

## Category-Specific Learning

### AI/ML Plugin Development
Browse 34 production AI/ML plugins for patterns:
- **[AI/ML Plugins Directory](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/ai-ml)** - ML engineering, model training, pipelines
- Examples: ml-engineer, ai-engineer, prompt-engineer, mlops-engineer
- Common patterns: model deployment, pipeline orchestration, experiment tracking

### API Development Plugins
27 API development plugins showing best practices:
- **[API Development Directory](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/api-development)** - REST, GraphQL, validation
- Examples: api-documenter, graphql-architect, backend-architect
- Patterns: OpenAPI generation, SDK creation, endpoint design

### Database Plugins
27 database plugins for data management patterns:
- **[Database Plugins Directory](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/database)** - SQL, NoSQL, migrations
- Examples: sql-pro, database-optimizer, data-engineer
- Patterns: query optimization, migration scripts, schema design

### Performance Optimization
25 performance plugins showing profiling patterns:
- **[Performance Directory](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/performance)** - Monitoring, profiling, optimization
- Examples: performance-engineer, database-optimizer, network-engineer
- Patterns: bottleneck detection, caching strategies, load testing

---

## Advanced Topics

### MCP Server Development

The marketplace includes 6 production MCP servers:
- **[MCP Plugins Directory](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/mcp)** - TypeScript/Node.js servers
- **[Project Health Auditor](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/mcp/project-health-auditor)** - 4 MCP tools
- **[Domain Memory Agent](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/mcp/domain-memory-agent)** - 6 MCP tools
- **[Workflow Orchestrator](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/mcp/workflow-orchestrator)** - 4 MCP tools

### Google ADK Integration

Production ADK patterns with Vertex AI:
- **[ADK Orchestrator Plugin](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/community/jeremy-adk-orchestrator)** - Complete LlmAgent implementation
- **[ADK Samples Directory](https://github.com/jeremylongshore/claude-code-plugins/tree/main/adk-samples)** - Python, Go, Java examples
- **[ADK Architecture Patterns](https://github.com/jeremylongshore/claude-code-plugins/blob/main/000-docs/090-AT-ADEC-adk-plugin-architecture-patterns.md)** - Migration guide

### Plugin Packs

Bundled plugin collections:
- **[DevOps Pack](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/packages/devops-automation-pack)** - 10 DevOps plugins
- **[Security Pack](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/packages/security-testing-pack)** - 8 security plugins
- **[Fullstack Pack](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/packages/fullstack-starter-pack)** - 12 fullstack plugins
- **[AI/ML Pack](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/packages/ai-ml-toolkit)** - 6 AI/ML plugins

---

## Documentation Standards

### Filing System Standard

The marketplace uses a sophisticated documentation filing system:

**Format:** `NNN-CC-ABCD-description.md`

**Category Codes:**
- **PP** - Product & Planning
- **AT** - Architecture & Technical
- **DC** - Development & Code
- **TQ** - Testing & Quality
- **OD** - Operations & Deployment
- **LS** - Logs & Status
- **RA** - Reports & Analysis
- **MC** - Meetings & Communication
- **PM** - Project Management
- **DR** - Documentation & Reference
- **UC** - User & Customer
- **AA** - After Action & Review

**[Complete Filing System Standard](https://github.com/jeremylongshore/claude-code-plugins/blob/main/000-docs/000-DR-REFF-filing-system-standard-v2.md)**

### Documentation Examples

Browse 111 indexed documents:
- **[Complete Documentation Index](https://github.com/jeremylongshore/claude-code-plugins/tree/main/000-docs)** - All project documentation
- Architecture decisions, user guides, audit reports
- Release notes, task documentation, memos

---

## Security Best Practices

### Security Resources
- **[Security Policy](https://github.com/jeremylongshore/claude-code-plugins/blob/main/SECURITY.md)** - Complete security framework
- **[User Security Guide](https://github.com/jeremylongshore/claude-code-plugins/blob/main/USER_SECURITY_GUIDE.md)** - Safe plugin evaluation
- **[Production Safety Guide](https://github.com/jeremylongshore/claude-code-plugins/blob/main/scripts/PRODUCTION_SAFETY_GUIDE.md)** - Deployment guidelines

### Security Checklist for Nixtla Plugins

Before releasing any Nixtla plugin:
1. No hardcoded API keys or secrets
2. Use environment variables for credentials
3. Validate all user inputs
4. Use `${CLAUDE_PLUGIN_ROOT}` for paths
5. Request minimal permissions
6. Test in isolated environment
7. Document all external API calls
8. Include security warnings in README

---

## CI/CD & Automation

### GitHub Actions Workflows

Study production workflows:
- **[Validation Pipeline](https://github.com/jeremylongshore/claude-code-plugins/blob/main/.github/workflows/validate-plugins.yml)** - Complete plugin validation
- **[Skill Generator](https://github.com/jeremylongshore/claude-code-plugins/blob/main/.github/workflows/daily-skill-generator.yml)** - Automated skills creation
- **[Marketplace Deployment](https://github.com/jeremylongshore/claude-code-plugins/blob/main/.github/workflows/deploy-marketplace.yml)** - Website deployment
- **[Security Audit](https://github.com/jeremylongshore/claude-code-plugins/blob/main/.github/workflows/security-audit.yml)** - CodeQL analysis

### Validation Scripts

Production validation tools:
- **[Validate All Plugins](https://github.com/jeremylongshore/claude-code-plugins/blob/main/scripts/validate-all-plugins.sh)** - Complete validation
- **[Validate Skills Schema](https://github.com/jeremylongshore/claude-code-plugins/blob/main/scripts/validate-skills-schema.py)** - 2025 compliance
- **[Sync Marketplace](https://github.com/jeremylongshore/claude-code-plugins/blob/main/scripts/sync-marketplace.cjs)** - Catalog synchronization

---

## Community Resources

### Engagement Channels
- **[GitHub Discussions](https://github.com/jeremylongshore/claude-code-plugins/discussions)** - Q&A, ideas, show & tell
- **[Discord Community](https://discord.com/invite/6PPFFzqPDZ)** - #claude-code channel
- **[Issue Templates](https://github.com/jeremylongshore/claude-code-plugins/tree/main/.github/ISSUE_TEMPLATE)** - Bug reports, features

### Contribution Process
- **[Pull Request Template](https://github.com/jeremylongshore/claude-code-plugins/blob/main/.github/PULL_REQUEST_TEMPLATE.md)** - PR guidelines
- **[Code of Conduct](https://github.com/jeremylongshore/claude-code-plugins/blob/main/CODE_OF_CONDUCT.md)** - Community standards
- **[Contributing Guide](https://github.com/jeremylongshore/claude-code-plugins/blob/main/CONTRIBUTING.md)** - Complete process

---

## Specific Resources for Nixtla Plugin Types

### TimeGPT Pipeline Builder Resources

Study these similar plugins:
- **[ML Engineer Plugin](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/ai-ml/ml-engineer)** - ML pipeline patterns
- **[Data Engineer Plugin](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/database/data-engineer)** - ETL patterns
- **[MLOps Engineer Plugin](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/ai-ml/mlops-engineer)** - Deployment patterns

### Benchmark Harness Resources

Learn from testing plugins:
- **[Performance Engineer](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/performance/performance-engineer)** - Benchmarking patterns
- **[Test Automator](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/testing/test-automator)** - Test framework patterns
- **[Quant Analyst](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/finance/quant-analyst)** - Statistical analysis

### FastAPI Service Resources

Study API development plugins:
- **[FastAPI Pro](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/api-development/fastapi-pro)** - FastAPI patterns
- **[Backend Architect](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/api-development/backend-architect)** - Service design
- **[API Documenter](https://github.com/jeremylongshore/claude-code-plugins/tree/main/plugins/api-development/api-documenter)** - OpenAPI generation

---

## Version Management & Releases

### Release Process Documentation
- **[Release Workflow](https://github.com/jeremylongshore/claude-code-plugins/blob/main/.github/workflows/release.yml)** - Automation
- **[Changelog Format](https://github.com/jeremylongshore/claude-code-plugins/blob/main/CHANGELOG.md)** - 148KB+ of release history
- **[Version Management](https://github.com/jeremylongshore/claude-code-plugins#version-management)** - Three-location updates

### Current Statistics (as of v1.4.0)
- 254 total plugins
- 185 Agent Skills (100% 2025 compliant)
- 6 MCP servers with 21 tools
- 111 documentation files
- 8 CI/CD workflows
- 4 plugin templates
- 3 working examples

---

## Quick Reference Commands

### Installation
```bash
# Add the main marketplace
/plugin marketplace add jeremylongshore/claude-code-plugins

# Install specific plugins
/plugin install ml-engineer@claude-code-plugins-plus
/plugin install fastapi-pro@claude-code-plugins-plus
/plugin install performance-engineer@claude-code-plugins-plus
```

### Local Testing
```bash
# Clone and explore
git clone https://github.com/jeremylongshore/claude-code-plugins.git
cd claude-code-plugins

# Validate plugins
./scripts/validate-all-plugins.sh

# Test installation
./scripts/test-installation.sh
```

---

## Support & Questions

### Direct Support
- **Main Repository Issues**: [Create an issue](https://github.com/jeremylongshore/claude-code-plugins/issues)
- **Discord Community**: [Join #claude-code](https://discord.com/invite/6PPFFzqPDZ)
- **Email**: jeremy@intentsolutions.io

### Official Documentation
- **Claude Code Docs**: https://docs.claude.com/en/docs/claude-code/
- **Plugin Guide**: https://docs.claude.com/en/docs/claude-code/plugins
- **Plugin Reference**: https://docs.claude.com/en/docs/claude-code/plugins-reference

---

**Last Updated**: November 23, 2025

**Note**: The main Claude Code Plugins marketplace is continuously evolving. Check the [repository](https://github.com/jeremylongshore/claude-code-plugins) for the latest updates, new plugins, and improved documentation.