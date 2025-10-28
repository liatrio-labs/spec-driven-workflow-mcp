# Architecture Query Command - Generic Template

**Command Name**: `/architecture` (or customize to your preference)

**Purpose**: Quickly retrieve specific information from comprehensive architecture documentation without reading the entire document.

**Token Efficiency**: Returns 800-2,400 tokens vs reading full 35K+ token architecture document (93-97% reduction)

---

## How It Works

This slash command acts as a targeted query interface to your architecture documentation. Instead of reading a massive document, users get precisely the information they need.

### Input
User provides a query: `/architecture [query]`

### Output
Returns targeted sections from architecture documentation with:
- Relevant information (200-600 words)
- Line number references for further reading
- Related resources
- Quick action items

---

## Implementation Guide

### 1. Create Architecture Documentation

First, create comprehensive architecture documentation with:
- **"For Agents" metadata section** at the top with line number ranges
- **Table of contents** with clear sections
- **Cross-references** to implementation guides
- **Common commands** section
- **Troubleshooting** section
- **Service catalog**

### 2. Add Line Number Metadata

At the top of your architecture doc:

```markdown
## For Agents & LLMs

**Key sections for automated processing:**

**Quick Lookups:**
- **Service Catalog** (lines 330-401): All services with dependencies
- **Library Decision Matrix** (lines 697-732): Which library for what task
- **Communication Patterns** (lines 402-418): How services interact
- **Common Commands** (lines 1822-1960): Executable commands
- **Troubleshooting** (lines 1995-2037): Common issues and fixes
- **Port Reference** (lines 1963-1975): Service ports
```

### 3. Create Section Reference Guide

Map common queries to document sections:

| Query Type | Section | Line Range |
|------------|---------|------------|
| Service lists | Microservices Catalog | 330-401 |
| Library selection | Library Decision Matrix | 697-732 |
| Data/message flows | Communication Patterns | 402-418 |
| Commands | Common Commands | 1822-1960 |
| Ports | Port Reference | 1963-1975 |
| Troubleshooting | Troubleshooting Quick Fixes | 1995-2037 |

### 4. Implement Query Logic

When user queries, return the relevant section with context:

```markdown
## [Section Title]

[Targeted content from architecture doc, 200-600 words]

**Source:** Architecture Documentation (lines X-Y)

### Related Resources
- [Cross-reference to implementation guide]
- [Link to related command]

### Quick Actions
1. [Actionable step]
2. [Actionable step]
```

---

## Example Queries and Responses

### Query: "which library for s3"

**Response:**
```markdown
## Library for S3/Object Storage Operations

Use **[YourStorageLibrary]** for object storage integration.

**Capabilities:**
- Interface: `IStorageService`
- Methods: `UploadAsync()`, `DownloadAsync()`, `DeleteAsync()`
- Stream-based async operations for large files
- Local development support

**Quick Example:**
[Code example]

**Source:** Architecture Documentation (lines 531-558)

### Related Resources
- Full implementation: [link to implementation guide]
- Real examples: `/find-library-usage IStorageService`

### Quick Actions
1. Add package: `[YourStorageLibrary]`
2. Register: `services.AddStorageService(config)`
3. Inject: `IStorageService` in your service
```

### Query: "pod crashloop" or "troubleshooting pod crash"

**Response:**
```markdown
## Troubleshooting: Pod/Container Crashes

### Diagnostic Commands (Run in order)

**1. View container logs:**
```bash
kubectl logs [pod-name] -n [namespace] --previous
```

**2. Check recent events:**
```bash
kubectl get events -n [namespace] --sort-by='.lastTimestamp' | grep [service]
```

**3. Describe pod for details:**
```bash
kubectl describe pod [pod-name] -n [namespace]
```

### Common Root Causes

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Connection refused" | Database connection issue | Check connection string in secrets |
| "Unable to load" | Missing dependency | Check package manifest |
| "Health check failed" | Endpoint failing | Check service dependencies |
| "Image pull error" | Wrong image tag or auth | Verify registry credentials |

**Source:** Architecture Documentation (lines 1996-2006)

### Next Steps
1. Run diagnostic commands above
2. Check monitoring dashboards
3. Review recent deployments
4. If database issue: `/architecture database troubleshooting`
```

### Query: "service dependencies" or "[service] dependencies"

**Response:**
```markdown
## Service Dependencies for [ServiceName]

**[ServiceName]** is a [high/medium/low]-traffic dependency called by X services:

### Direct Dependencies

1. **[Service1]** ([purpose])
   - Endpoint: `[API endpoint]`
   - Frequency: [frequency]
   - Critical: [Yes/No]

2. **[Service2]** ([purpose])
   - Endpoint: `[API endpoint]`
   - Frequency: [frequency]
   - Critical: [Yes/No]

### Impact Analysis

**Breaking Change Risk: [HIGH/MEDIUM/LOW]**
- X critical services depend on this API
- [Impact description]

**Recommendation:**
1. Use API versioning
2. Maintain backward compatibility
3. Coordinate deployment with consuming services

**Source:** Architecture Documentation (lines 428-488)

### Related Resources
- Communication patterns: [link]
- API versioning guide: [link]

### Quick Actions
1. Check current version: [command]
2. Plan migration: [command]
3. Notify teams: [list]
```

---

## Common Query Patterns to Support

### Service Information
- "list services"
- "[domain] services" (e.g., "payment services")
- "[service] info"
- "[service] dependencies"

### Library/Tool Selection
- "which library for [task]"
- "how to [task]" (e.g., "how to upload files")
- "[technology] library" (e.g., "s3 library")

### Commands & Operations
- "[command type] commands" (e.g., "kubectl commands", "docker commands")
- "deploy [service]"
- "rollback [service]"

### Troubleshooting
- "[error symptom]" (e.g., "pod crashloop", "connection refused")
- "debug [issue]"
- "fix [problem]"

### Configuration
- "ports"
- "[service] configuration"
- "environment variables"

---

## Best Practices

### For Response Generation

1. **Be Concise**: 200-600 words max
2. **Include Source**: Always reference line numbers
3. **Provide Actions**: Give 2-4 actionable next steps
4. **Cross-Reference**: Link to related resources
5. **Use Examples**: Include code snippets when relevant

### For Maintenance

1. **Keep Line Numbers Updated**: When architecture doc changes
2. **Test Common Queries**: Ensure they return useful results
3. **Monitor Usage**: Track which queries are most common
4. **Expand Coverage**: Add sections for frequently asked questions

### For Users

1. **Teach the Command**: Include in onboarding
2. **Show Examples**: Provide query examples in documentation
3. **Quick Reference Card**: Create cheat sheet of common queries

---

## Integration with Other Tools

**Combine with:**
- `/find-library-usage [library]` - For real code examples after architecture query
- Implementation guide - For detailed implementation after architecture overview
- Troubleshooting runbooks - For deep-dive debugging

**Example Workflow:**
```
1. User: "/architecture which library for queues"
   → Returns library recommendation

2. User: "/find-library-usage IQueueConsumer"
   → Returns real examples from services

3. User: Reads implementation guide (targeted section)
   → Gets detailed implementation guidance
```

---

## Token Efficiency Comparison

| Approach | Tokens | Time | Notes |
|----------|--------|------|-------|
| Read full architecture doc | 35,000 | 10-15 min | Overwhelming, hard to find info |
| `/architecture [query]` | 800-2,400 | 30-60 sec | Targeted, actionable |
| **Efficiency Gain** | **93-97%** | **90%** | Dramatically faster |

---

## Customization Checklist

To implement this command for your project:

- [ ] Create comprehensive architecture documentation
- [ ] Add "For Agents" metadata section with line numbers
- [ ] Create section reference guide (queries → line numbers)
- [ ] Implement query routing logic
- [ ] Test with 10-15 common queries
- [ ] Create user documentation with examples
- [ ] Add to onboarding materials
- [ ] Monitor usage and expand coverage
- [ ] Update line numbers when doc structure changes

---

## Example Architecture Doc Structure

Your architecture documentation should have:

```markdown
# [Project] Architecture Documentation

## For Agents & LLMs
[Line number metadata]

## Table of Contents
[Sections with line numbers]

## Executive Summary
[High-level overview]

## Service Catalog
[All services with dependencies] - Lines 330-401

## Shared Libraries
[Library decision matrix] - Lines 697-732

## Communication Patterns
[How services communicate] - Lines 402-418

## Data Flow
[Data flow patterns]

## Infrastructure
[Platform components]

## Common Commands
[kubectl, docker, etc.] - Lines 1822-1960

## Port Reference
[Service ports] - Lines 1963-1975

## Troubleshooting
[Common issues] - Lines 1995-2037

## Deployment Process
[How to deploy]

## Monitoring & Observability
[How to monitor]
```

---

## Success Metrics

Track:
- Query count per week
- Average response size (aim for 800-2,400 tokens)
- User satisfaction
- Time saved vs reading full docs
- Most common queries (expand documentation coverage)

The command is successful when:
- Users prefer it over reading full docs
- Responses are actionable
- Token usage stays under 2,500 tokens
- Coverage expands based on actual usage
