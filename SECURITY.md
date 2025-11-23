# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Which versions are eligible for receiving such patches depends on the CVSS v3.0 Rating:

| Version | Supported          | Status |
| ------- | ------------------ | ------ |
| 1.0.x   | :white_check_mark: | Current release |
| 0.9.x   | :x:                | Beta (unsupported) |
| < 0.9   | :x:                | Alpha (unsupported) |

## Reporting a Vulnerability

We take the security of Claude Code Plugins for Nixtla seriously. If you believe you have found a security vulnerability, please report it to us as described below.

### Please do NOT:

- Open a public GitHub issue for security vulnerabilities
- Post about the vulnerability on social media
- Attempt to exploit the vulnerability on production systems

### Please DO:

**Email us directly at**: security@intentsolutions.io

Include the following information:

1. **Type of issue** (e.g., buffer overflow, SQL injection, cross-site scripting, credential exposure)
2. **Full paths of source file(s)** related to the manifestation of the issue
3. **Location of the affected source code** (tag/branch/commit or direct URL)
4. **Special configuration** required to reproduce the issue
5. **Step-by-step instructions** to reproduce the issue
6. **Proof-of-concept or exploit code** (if possible)
7. **Impact of the issue**, including how an attacker might exploit it

### What to Expect

- **Acknowledgment**: Within 24 hours of receipt
- **Initial Assessment**: Within 48 hours
- **Status Update**: Within 5 business days
- **Resolution Timeline**: Depends on severity (see below)

### Severity Levels and Response Times

| Severity | CVSS Score | Examples | Target Resolution |
|----------|------------|----------|------------------|
| Critical | 9.0-10.0 | Remote code execution, credential theft | 24 hours |
| High | 7.0-8.9 | Privilege escalation, data exposure | 7 days |
| Medium | 4.0-6.9 | Cross-site scripting, denial of service | 30 days |
| Low | 0.1-3.9 | Information disclosure, minor bugs | 90 days |

## Security Best Practices

When using Claude Code Plugins for Nixtla, follow these security best practices:

### 1. Credential Management

**Never hardcode credentials** in plugins or scripts:

```python
# ❌ BAD - Never do this
api_key = "sk-abc123xyz789"

# ✅ GOOD - Use environment variables
api_key = os.environ.get("NIXTLA_API_KEY")
```

### 2. Input Validation

Always validate and sanitize inputs:

```python
def validate_environment(env: str) -> str:
    """Validate environment parameter."""
    allowed_envs = ["dev", "staging", "production"]
    if env not in allowed_envs:
        raise ValueError(f"Invalid environment: {env}")
    return env
```

### 3. Secure Communication

- Always use HTTPS for API calls
- Verify SSL certificates
- Use secure WebSocket connections (WSS)

```python
# ✅ GOOD - Enforce HTTPS
response = requests.get(
    "https://api.nixtla.io/forecast",
    verify=True  # Verify SSL certificate
)
```

### 4. Least Privilege Principle

Plugins should request only the minimum permissions needed:

```json
{
  "permissions": {
    "read": ["./data/*.csv"],
    "write": ["./outputs/"],
    "execute": []
  }
}
```

### 5. Dependency Security

Regularly update and audit dependencies:

```bash
# Check for known vulnerabilities
pip audit

# Update dependencies
pip install --upgrade -r requirements.txt

# Use locked versions in production
pip freeze > requirements.lock
```

### 6. Data Protection

- Encrypt sensitive data at rest
- Use secure deletion for temporary files
- Implement proper data retention policies

```python
import tempfile
import os

# Use secure temporary files
with tempfile.NamedTemporaryFile(mode='w', delete=True) as tmp:
    tmp.write(sensitive_data)
    tmp.flush()
    # File is automatically deleted when context exits
```

### 7. Logging and Monitoring

- Log security events
- Never log sensitive data
- Monitor for unusual activity

```python
import logging

# Configure secure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log security events
logger.info(f"User {user_id} accessed forecast endpoint")
# Never log credentials or sensitive data
logger.info("Authentication successful")  # Not the actual token
```

## Security Features

### Built-in Protections

1. **Sandboxed Execution**: Plugins run in isolated environments
2. **Permission System**: Fine-grained access control
3. **Input Sanitization**: Automatic cleaning of user inputs
4. **Rate Limiting**: Protection against abuse
5. **Audit Logging**: Complete activity trails

### Security Headers

When deploying web interfaces, use these headers:

```python
security_headers = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'"
}
```

## Vulnerability Disclosure Process

1. **Report Received**: Security team acknowledges receipt
2. **Triage**: Assess severity and impact
3. **Fix Development**: Create and test patches
4. **Notification**: Inform affected users (if necessary)
5. **Release**: Deploy fix and publish security advisory
6. **Post-Mortem**: Document lessons learned

## Security Checklist for Contributors

Before submitting a pull request, ensure:

- [ ] No hardcoded credentials or secrets
- [ ] All user inputs are validated
- [ ] Dependencies are up-to-date
- [ ] No sensitive data in logs
- [ ] Error messages don't expose system details
- [ ] File operations use secure paths
- [ ] Network calls use HTTPS
- [ ] Tests cover security edge cases

## Recognition

We appreciate responsible disclosure and will acknowledge security researchers who:
- Follow this security policy
- Provide detailed, actionable reports
- Allow reasonable time for fixes

Recognition includes:
- Credit in security advisories
- Mention in CONTRIBUTORS.md
- Letter of appreciation (upon request)

## Contact

- **Security Issues**: security@intentsolutions.io
- **General Support**: jeremy@intentsolutions.io
- **Response Time**: Within 24 hours for security issues

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Claude Code Security Best Practices](https://claude.ai/docs/security)

---

**Last Updated**: November 2025
**Version**: 1.0.0