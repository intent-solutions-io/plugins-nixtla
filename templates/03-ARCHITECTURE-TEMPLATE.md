# [Plugin Name] - Architecture

**Plugin:** [plugin-slug]
**Version:** 0.1.0
**Last Updated:** [TODAY]

---

## System Context

[Where does this plugin fit in the broader ecosystem?]

```
┌─────────────────────────────────────────────────────────────┐
│                      User's Terminal                         │
├─────────────────────────────────────────────────────────────┤
│                      Claude Code CLI                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              [Plugin Name]                           │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐             │   │
│  │  │ Command │  │  Skill  │  │  MCP    │             │   │
│  │  └────┬────┘  └────┬────┘  └────┬────┘             │   │
│  └───────┼────────────┼────────────┼───────────────────┘   │
│          │            │            │                        │
│          ▼            ▼            ▼                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              External APIs / Services                │   │
│  │         ([COMPANY] SDK, databases, etc.)            │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Design

### Components

| Component | Responsibility | Location |
|-----------|---------------|----------|
| [Component 1] | [What it does] | `path/to/file` |
| [Component 2] | [What it does] | `path/to/file` |

### Component Interactions

```
[Component 1] ──▶ [Component 2] ──▶ [External Service]
       │                │
       ▼                ▼
   [Output 1]       [Output 2]
```

---

## Data Flow

### Input
[What data comes in, from where, in what format]

### Processing
[What transformations/operations happen]

### Output
[What data goes out, to where, in what format]

---

## Integrations

| System | Type | Direction | Purpose | Auth Method |
|--------|------|-----------|---------|-------------|
| [System 1] | API | Inbound/Outbound | [Purpose] | [API Key/OAuth/None] |
| [System 2] | SDK | Outbound | [Purpose] | [Auth method] |

---

## Technical Constraints

- **Constraint 1:** [Description and rationale]
- **Constraint 2:** [Description and rationale]
- **Constraint 3:** [Description and rationale]

---

## Security Considerations

### Authentication
[How users/services authenticate]

### Authorization
[What permissions are required]

### Data Handling
[Sensitive data, encryption, retention]

### Secrets Management
[How API keys/credentials are handled]

---

## Scalability

### Current Limits
| Resource | Limit | Mitigation if exceeded |
|----------|-------|----------------------|
| [Resource 1] | [Limit] | [What to do] |

### Future Scaling
[How to scale if needed]

---

## Error Handling

| Error Type | Detection | Response | Recovery |
|------------|-----------|----------|----------|
| [Error 1] | [How detected] | [What happens] | [How to recover] |

---

## Observability

### Logging
[What gets logged, where, log levels]

### Metrics
[What metrics are tracked]

### Alerting
[What triggers alerts]
