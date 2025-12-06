# Contributing to Claude Code Plugins for Nixtla

First off, thank you for considering contributing to Claude Code Plugins for Nixtla! It's people like you that help make these tools powerful and accessible for the entire time series community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Process](#development-process)
- [Plugin Contribution Guidelines](#plugin-contribution-guidelines)
- [Style Guides](#style-guides)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to jeremy@intentsolutions.io.

## Getting Started

### Prerequisites

- Python 3.9+ installed
- Git for version control
- Claude Code CLI (for testing plugins)
- Familiarity with Nixtla's ecosystem (TimeGPT, StatsForecast, etc.)

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/claude-code-plugins-nixtla.git
   cd claude-code-plugins-nixtla
   ```

2. **Set up development environment**
   ```bash
   ./scripts/setup-dev-environment.sh
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Run tests to verify setup**
   ```bash
   pytest
   ```

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, please include:

- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Environment details (OS, Python version, Claude Code version)
- Relevant logs or error messages
- Screenshots if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- A clear and descriptive title
- Detailed description of the proposed functionality
- Use cases and examples
- Why this enhancement would be useful to most users
- Possible implementation approach (optional)

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:

- `good first issue` - Simple issues perfect for beginners
- `help wanted` - Issues where we need community help
- `documentation` - Help improve our docs

### Pull Requests

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, commented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Follow the commit convention**
   ```bash
   git commit -m "feat(plugin-name): add new validation command"
   ```

   Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**
   - Use the PR template
   - Link related issues
   - Ensure all CI checks pass

## Development Process

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - Individual feature development
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates

### Testing Requirements

All contributions must include appropriate tests:

```python
# Example test structure
def test_timegpt_deployment():
    """Test TimeGPT deployment command."""
    result = deploy_timegpt(env="staging")
    assert result.status == "success"
    assert result.endpoint is not None
```

Run tests locally before submitting:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_timegpt_deployer.py

# Run with coverage
pytest --cov=plugins
```

### Code Review Process

All submissions require review before merging:

1. Automated CI checks must pass
2. At least one maintainer approval required
3. No merge conflicts with main branch
4. Documentation updated if needed
5. Tests provide adequate coverage

## Plugin Contribution Guidelines

### Plugin Structure

Every plugin must follow this structure:

```
plugins/your-plugin-name/
├── .claude-plugin/
│   └── plugin.json         # Plugin metadata
├── commands/                # User-invoked commands (optional)
│   ├── command1.md
│   └── command2.md
├── agents/                  # AI agents (optional)
│   └── agent.md
├── scripts/                 # Supporting scripts (optional)
│   └── helper.sh
├── tests/                   # Plugin-specific tests
│   └── test_plugin.py
├── README.md                # Plugin documentation
└── LICENSE                  # Plugin license (MIT preferred)
```

### Plugin Metadata (plugin.json)

```json
{
  "name": "your-plugin-name",
  "version": "1.0.0",
  "description": "Clear, concise description",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "repository": "https://github.com/yourusername/your-repo",
  "license": "MIT",
  "keywords": ["forecasting", "timeseries", "nixtla"],
  "requirements": {
    "claude-code": ">=1.0.0",
    "python": ">=3.9"
  }
}
```

### Command/Agent Format

Commands and agents use markdown with YAML frontmatter:

```markdown
---
name: deploy
description: Deploy TimeGPT model to cloud
model: sonnet
parameters:
  - name: env
    description: Target environment
    required: true
    type: string
    choices: [dev, staging, production]
---

# Deploy TimeGPT Model

Deploy the TimeGPT model to ${env} environment...
```

### Plugin Best Practices

1. **Single Responsibility**: Each plugin should do one thing well
2. **Clear Documentation**: Include examples and use cases
3. **Error Handling**: Gracefully handle errors with helpful messages
4. **Idempotency**: Commands should be safe to run multiple times
5. **Security**: Never hardcode credentials or sensitive data
6. **Performance**: Optimize for speed, especially for common operations
7. **Compatibility**: Test with multiple Nixtla library versions

## Style Guides

### Python Style Guide

We follow PEP 8 with these additions:

- Use type hints for function arguments and returns
- Maximum line length: 100 characters
- Use docstrings for all public functions
- Prefer f-strings over .format()

```python
def deploy_model(
    model_name: str,
    environment: str,
    config: Dict[str, Any]
) -> DeploymentResult:
    """
    Deploy a forecasting model to the specified environment.

    Args:
        model_name: Name of the model to deploy
        environment: Target environment (dev, staging, production)
        config: Deployment configuration dictionary

    Returns:
        DeploymentResult object containing status and metadata
    """
    # Implementation here
```

### Markdown Style Guide

- Use ATX-style headers (`#` not underlines)
- Include a table of contents for documents > 3 sections
- Use fenced code blocks with language specification
- Keep lines under 80 characters when possible
- Use reference-style links for repeated URLs

### Commit Message Guidelines

Format: `<type>(<scope>): <subject>`

Examples:
- `feat(timegpt-deployer): add multi-region support`
- `fix(validator): correct cross-validation logic`
- `docs(readme): update installation instructions`
- `test(pipeline): add integration tests`

## Community

### Getting Help

- **Documentation**: Start with our [documentation](./000-docs/)
- **Issues**: Search [existing issues](https://github.com/intent-solutions-io/plugins-nixtla/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/intent-solutions-io/plugins-nixtla/discussions)
- **Email**: Reach out to jeremy@intentsolutions.io

### Recognition

Contributors are recognized in:
- [CONTRIBUTORS.md](./CONTRIBUTORS.md) - All contributors
- Release notes - Per-version contributions
- Plugin documentation - Plugin authors

### Development Roadmap

See [ROADMAP.md](./ROADMAP.md) for upcoming features and priorities. Feel free to:
- Suggest new features
- Vote on existing proposals
- Volunteer to implement features

## License

By contributing, you agree that your contributions will be licensed under the MIT License.