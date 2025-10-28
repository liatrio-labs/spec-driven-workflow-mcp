# Shared Templates Index

Quick reference for all generic templates in this folder.

---

## Agents

Located in `/agents`

| Template | Purpose | Token Efficiency | Use When |
|----------|---------|------------------|----------|
| [code-reusability-agent.md](agents/code-reusability-agent.md) | Find existing libraries/patterns | 97.5% reduction (5K vs 200K) | Before implementing new functionality |
| [microservices-architect-agent.md](agents/microservices-architect-agent.md) | Design/review architectures | 95.6% reduction (10K vs 230K) | Architecture decisions, service design |
| [debugger-agent.md](agents/debugger-agent.md) | Diagnose errors efficiently | 96% reduction (6K vs 150K) | Errors, test failures, issues |
| [developer-agent.md](agents/developer-agent.md) | Execute PRD implementations | 85-90% reduction (20-30K vs 150K+) | Implementing features from PRDs |
| [enterprise-codebase-documenter-agent.md](agents/enterprise-codebase-documenter-agent.md) | Analyze large codebases | 92.2% reduction (9K vs 115K) | Multi-repo analysis, dependency mapping |

---

## Commands

Located in `/commands`

| Template | Purpose | Token Efficiency | Use When |
|----------|---------|------------------|----------|
| [setup.md](commands/setup.md) | Automated project setup | N/A (one-time setup) | Initial project configuration |
| [architecture.md](commands/architecture.md) | Query architecture docs | 97% reduction (1K vs 35K) | Quick architecture questions |
| [find-library-usage.md](commands/find-library-usage.md) | Find library usage examples | 90% reduction (10K vs 100K) | Need real code examples |
| [jira-to-prd.md](commands/jira-to-prd.md) | Generate PRD from Jira story | 94% reduction (12K vs 200K) | Converting Jira stories to detailed PRDs |

---

## Documentation

| File | Purpose |
|------|---------|
| [README.md](README.md) | Overview, concepts, and usage instructions |
| [SETUP-GUIDE.md](SETUP-GUIDE.md) | Step-by-step automated setup guide |
| [DUPLICATE-PREVENTION.md](DUPLICATE-PREVENTION.md) | Duplicate detection and conflict resolution |
| [CREATION-SUMMARY.md](CREATION-SUMMARY.md) | Development history and implementation notes |

## Templates

| File | Purpose |
|------|---------|
| [templates/WORKING-NOTES.md](templates/WORKING-NOTES.md) | Shared working document template for agent collaboration |

---

## Agent Collaboration Pattern

**Problem**: Agents create separate files instead of collaborating, leading to fragmented information.

**Solution**: Use shared `WORKING-NOTES.md` per ticket where all agents collaborate on open questions, decisions, findings, and action items.

**Template**: See [templates/WORKING-NOTES.md](templates/WORKING-NOTES.md)

---

## Quick Start

### Automated Setup (Recommended)

1. **Copy** agent files from `agents/` to your project's `.claude/agents/` directory
2. **Copy** command files from `commands/` to your project's `.claude/commands/` directory
3. **Run** `/setup init` to detect your tech stack and generate customization instructions
4. **Follow** the customization guidance to replace placeholders
5. **Validate** with `/setup validate`

### Manual Setup (Advanced)

1. **Read** [README.md](README.md) for overview and concepts
2. **Review** templates relevant to your needs
3. **Customize** templates for your project (see customization notes in each)
4. **Create** supporting documentation (architecture doc, implementation guide)
5. **Implement** in your agent system
6. **Measure** efficiency gains

---

## Customization Priority

**Start with these (highest ROI):**
1. code-reusability-agent.md - Prevents duplication
2. architecture.md - Fast queries
3. debugger-agent.md - Faster troubleshooting

**Add next (expand coverage):**
4. find-library-usage.md - Real examples
5. microservices-architect-agent.md - Architecture guidance

**Optional (for large orgs):**
6. enterprise-codebase-documenter-agent.md - Multi-repo analysis

---

## Key Files to Create

Before implementing these templates, create:

1. **Architecture Documentation** with:
   - "For Agents" metadata (line numbers)
   - Service catalog
   - Library decision matrix
   - Common commands
   - Troubleshooting section

2. **Implementation Guide** with:
   - Library integration examples
   - Code patterns
   - Anti-patterns
   - Step-by-step guides

3. **Task-to-Agent Mapping** (optional):
   - "I need to..." → "Use this tool" guide
   - Decision matrix

4. **Integration Patterns Catalog** (optional):
   - Communication patterns
   - Decision trees
   - Complete examples

---

## Expected Results

After full implementation:

- **Token Usage**: 80-95% reduction across workflows
- **Onboarding Time**: 50-75% faster for new developers
- **Code Duplication**: 60-80% reduction
- **Troubleshooting Speed**: 40-60% faster during incidents
- **Pattern Adoption**: 90%+ use existing patterns vs custom

---

## Maintenance

**Monthly:**
- Update line numbers if docs change
- Review common queries
- Expand documentation coverage

**Quarterly:**
- Measure efficiency metrics
- Gather user feedback
- Update templates based on usage
- Review memorized error patterns

---

## Support

For issues:
1. Check customization notes in each template
2. Verify supporting documentation exists
3. Confirm line numbers match your docs
4. Review README.md for prerequisites

---

**Version**: 1.0
**Last Updated**: 2025-10-23
