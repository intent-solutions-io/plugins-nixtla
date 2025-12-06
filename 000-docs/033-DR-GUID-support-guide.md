# Support

## Getting Help with Claude Code Plugins for Nixtla

Thank you for using Claude Code Plugins for Nixtla! We're here to help you get the most out of these tools. This document provides information on how to get support, report issues, and connect with the community.

## Direct Support Channels

### Priority Support for Nixtla
- **Slack**: Dedicated channel at Intent Solutions IO workspace
- **Email**: jeremy@intentsolutions.io
- **Cell**: 251.213.1115
- **Response Time**: Same day for all inquiries

## Documentation Resources

### Primary Documentation

- [README.md](./README.md) - Overview and quick start guide
- [Plugin Documentation](./000-docs/) - Detailed technical documentation
- [Architecture Guide](./ARCHITECTURE.md) - System design and integration patterns
- [Contributing Guide](./CONTRIBUTING.md) - How to contribute and develop plugins

### Nixtla Ecosystem Documentation

- [TimeGPT Documentation](https://docs.nixtla.io/) - Official TimeGPT docs
- [StatsForecast](https://nixtla.github.io/statsforecast/) - Statistical models documentation
- [MLForecast](https://nixtla.github.io/mlforecast/) - ML forecasting documentation
- [NeuralForecast](https://nixtla.github.io/neuralforecast/) - Neural network models
- [HierarchicalForecast](https://nixtla.github.io/hierarchicalforecast/) - Hierarchical methods

## Additional Support Options

### Support Options

| Issue Type | Where to Go |
|------------|-------------|
| Bug Report | [GitHub Issues](https://github.com/intent-solutions-io/plugins-nixtla/issues/new?template=bug_report.yml) |
| Feature Request | [GitHub Issues](https://github.com/intent-solutions-io/plugins-nixtla/issues/new?template=feature_request.yml) |
| Security Issue | security@intentsolutions.io |
| General Question | [GitHub Discussions](https://github.com/intent-solutions-io/plugins-nixtla/discussions/new?category=q-a) |
| Plugin Proposal | [GitHub Issues](https://github.com/intent-solutions-io/plugins-nixtla/issues/new?template=plugin_proposal.yml) |
| Direct Support | jeremy@intentsolutions.io / 251.213.1115 |

**Note**: All support requests are handled as quickly as possible. Direct contact via Slack, email, or cell gets immediate attention.

### Provide Necessary Information

When seeking support, please provide:

#### For Bug Reports:
```markdown
**Environment:**
- OS: [e.g., Ubuntu 22.04, macOS 14.0, Windows 11]
- Python version: [e.g., 3.11.5]
- Claude Code version: [e.g., 1.0.0]
- Plugin version: [e.g., timegpt-deployer v1.2.0]

**Steps to Reproduce:**
1. Run command X
2. See error Y

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Error Messages:**
```
[Paste full error message here]
```

**Additional Context:**
[Any other relevant information]
```

#### For Feature Requests:
```markdown
**Problem Statement:**
[What problem does this solve?]

**Proposed Solution:**
[How would you like it to work?]

**Alternatives Considered:**
[What other approaches have you tried?]

**Use Case:**
[Specific example of how you'd use this]
```

## Community Support

### GitHub Discussions

Join our community discussions for:
- Q&A with other users
- Sharing tips and best practices
- Plugin ideas and feedback
- General time series forecasting topics

[Join Discussions →](https://github.com/intent-solutions-io/plugins-nixtla/discussions)

### Contributing

Interested in contributing? We welcome:
- Bug fixes
- New plugins
- Documentation improvements
- Example code
- Test coverage

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## Professional Support

### Professional Support

For enterprise or professional support needs:

**Email**: jeremy@intentsolutions.io

**Services Available:**
- Custom plugin development
- Integration assistance
- Training and workshops
- Architecture consulting
- Priority support plans

**Response Times:**
- Critical issues: Same day
- High priority: 24 hours
- Normal priority: 48 hours
- Low priority: 1 week

### Support Hours

- **Regular Support**: Monday-Friday, 9 AM - 6 PM EST
- **Emergency Support**: Available for critical production issues
- **Holiday Schedule**: Limited support on US holidays

## Frequently Asked Questions

### Installation Issues

**Q: Plugin installation fails with "not found" error**
```bash
# Solution: Ensure marketplace is added first
/plugin marketplace add intent-solutions-io/plugins-nixtla
/plugin install timegpt-deployer@nixtla
```

**Q: How do I update plugins to the latest version?**
```bash
# Remove old version
/plugin uninstall timegpt-deployer@nixtla
# Install latest
/plugin install timegpt-deployer@nixtla
```

### Configuration Issues

**Q: Where should I store API keys?**
```bash
# Use environment variables
export NIXTLA_API_KEY="your-key-here"
# Or use .env file (don't commit to git!)
echo "NIXTLA_API_KEY=your-key-here" >> .env
```

**Q: How do I configure multiple environments?**
```python
# Use environment-specific config files
config/
├── dev.yaml
├── staging.yaml
└── production.yaml
```

### Usage Questions

**Q: Can I use multiple forecasting models in one pipeline?**
```bash
# Yes! Use the ensemble capabilities
/validate-forecasts --models [timegpt, statsforecast, mlforecast] --ensemble weighted
```

**Q: How do I handle missing data in time series?**
```python
# Plugins handle this automatically, but you can configure:
/forecast --interpolation "linear" --max-missing 0.1
```

### Performance Issues

**Q: Forecasting is slow on large datasets**
```bash
# Enable parallel processing
/forecast --parallel --workers 4
# Or use sampling for testing
/forecast --sample 0.1 --dev-mode
```

**Q: Memory errors with big data**
```python
# Use chunking for large datasets
/process-data --chunk-size 10000 --streaming
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Import Errors
```python
# Error: ModuleNotFoundError: No module named 'nixtla'
# Solution:
pip install nixtla
```

#### 2. Authentication Failures
```python
# Error: Invalid API key
# Solution: Verify key is set correctly
echo $NIXTLA_API_KEY  # Should show your key
```

#### 3. Network Issues
```python
# Error: Connection timeout
# Solution: Check proxy settings
export HTTPS_PROXY=your-proxy:port
```

#### 4. Version Conflicts
```bash
# Error: Incompatible versions
# Solution: Use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Support Commitment

For Nixtla collaboration:

| Service | Commitment |
|---------|------------|
| Response Time | As fast as possible |
| Availability | On-demand via Slack, email, or cell |
| Priority Level | Highest priority |
| Support Hours | Flexible based on your needs |

## Service Agreement

For this collaboration:
- Immediate response via Slack or direct contact
- No formal SLA needed - we respond as quickly as possible
- Direct escalation to Jeremy: 251.213.1115

## Feedback

We value your feedback! Help us improve:

### Product Feedback
- Feature requests via [GitHub Issues](https://github.com/intent-solutions-io/plugins-nixtla/issues)
- General feedback via [Discussions](https://github.com/intent-solutions-io/plugins-nixtla/discussions)

### Documentation Feedback
- Submit PRs for documentation improvements
- Report unclear documentation as issues

### Support Experience Feedback
- Email feedback to: jeremy@intentsolutions.io

## Stay Connected

- **GitHub**: [@jeremylongshore](https://github.com/jeremylongshore)
- **Email**: jeremy@intentsolutions.io
- **Cell**: 251.213.1115

## Acknowledgments

Special thanks to:
- The Nixtla team for their incredible forecasting libraries
- Anthropic for Claude Code and the plugin architecture
- Our community of contributors and users

---

**Support Email**: jeremy@intentsolutions.io
**Cell**: 251.213.1115
**Slack**: Intent Solutions IO workspace