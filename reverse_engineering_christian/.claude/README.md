# Shared Templates - Context-Efficient Documentation Architecture

This folder contains **generic, reusable templates** for implementing context-efficient documentation architecture in any software project. These templates can be adapted to any tech stack or organization.

**Purpose**: These templates are **instantiated** (copied and customized) by the `/setup init` command to create project-specific agents, commands, and documentation tailored to your detected tech stack.

**How to Use**:
1. **Clone/Copy** this entire repository to `AI Tools/` folder in your project root
2. **Copy** agent files from `AI Tools/agents/` to `.claude/agents/` directory
3. **Copy** command files from `AI Tools/commands/` to `.claude/commands/` directory
4. **Run** `/setup init` to detect your tech stack and generate customization instructions
5. **Follow** the customization guidance to replace placeholders with your detected tech stack

**Note**: Keep the `AI Tools/` folder as reference documentation. The `/setup` command and agents will refer to it.

**Origin**: These templates are based on a production implementation that achieved **80-95% reduction in token usage** while maintaining or improving result quality. The architectural approach is documented in ADR-0015 (available in the implementing organization's repository).

---

## What's Included

### Agents (`/agents`)

Specialized AI agent templates with built-in context efficiency strategies:

1. **code-reusability-agent.md** - Prevents code duplication by identifying existing shared libraries
2. **microservices-architect-agent.md** - Designs and reviews distributed architectures
3. **debugger-agent.md** - Diagnoses errors and issues efficiently
4. **developer-agent.md** - Executes PRD implementations with phased, incremental approach
5. **enterprise-codebase-documenter-agent.md** - Analyzes large multi-repo codebases

### Commands (`/commands`)

User-facing slash command templates:

1. **setup.md** - Automated tech stack detection and project setup
2. **architecture.md** - Quick queries to architecture documentation
3. **find-library-usage.md** - Search for library usage across services
4. **jira-to-prd.md** - Generate detailed PRDs from Jira stories with architecture awareness

### Templates (`/templates`)

Collaboration templates for multi-agent workflows:

1. **WORKING-NOTES.md** - Shared working document template for agent collaboration on tickets/tasks

---

## Agent Collaboration Pattern

**Problem**: Multiple agents create separate files, leading to fragmented information.

**Solution**: Use a shared `WORKING-NOTES.md` file per ticket where all agents collaborate on:
- Open questions needing answers
- Decisions made with rationale
- Technical findings from each agent
- Action items for implementation

See [templates/WORKING-NOTES.md](templates/WORKING-NOTES.md) for the template.

---

## Key Concepts

### Context Efficiency Strategy

All templates implement the same core strategy:

```
DO THIS (Efficient):
1. Check task-to-agent mapping (1K tokens)
2. Read targeted doc sections by line number (2-5K tokens)
3. Reference existing patterns instead of creating new (2K tokens)
4. Suggest user run commands when appropriate (saves agent tokens)
Total: 5-10K tokens

DON'T DO THIS (Wasteful):
1. Read entire implementation guide (60K tokens)
2. Read entire architecture doc (40K tokens)
3. Scan all services (100K+ tokens)
Total: 200K+ tokens
```

### Hierarchical Documentation

The architecture assumes three-tier documentation:

1. **Architecture Documentation** (WHAT exists, descriptive)
   - Service catalog
   - Dependency graphs
   - Platform overview
   - Common commands

2. **Implementation Guide** (HOW to implement, prescriptive)
   - Code examples
   - Integration patterns
   - Anti-patterns
   - Library usage

3. **Integration Patterns Catalog** (Production-ready patterns)
   - Communication patterns
   - Decision trees
   - Complete code examples

### Targeted Reading with Line Numbers

Documents include "For Agents" metadata sections:

```markdown
## For Agents & LLMs

**Quick Lookups:**
- Service Catalog: lines 330-401 (3K tokens)
- Library Decision Matrix: lines 697-732 (2K tokens)
- Common Commands: lines 1822-1960 (5K tokens)
```

Agents read only needed sections, not entire documents.

---

## How to Use These Templates

### Step 1: Review the Templates

Read through each template to understand:
- Context efficiency strategies
- Working processes
- Output formats
- Customization points

### Step 2: Customize for Your Project

Each template has a "Customization Notes" section at the bottom. Replace:

- **Generic terms** with your actual names:
  - "implementation guide" → Your doc name (DEVELOPER_GUIDE.md, README.md, etc.)
  - "shared-libraries/" → Your shared code directory
  - "services/" → Your services/apps directory

- **Technology stack** references:
  - ".csproj" → Your manifest files (package.json, pom.xml, etc.)
  - Framework names → Your actual frameworks
  - Tool names → Your actual tools

- **Command names**:
  - `/architecture` → Your command name
  - `/find-library-usage` → Your command name

- **Line numbers**:
  - Update to match your actual documentation structure

### Step 3: Create Supporting Documentation

To use these agents effectively, you need:

1. **Comprehensive Architecture Documentation** with:
   - "For Agents" metadata section at top
   - Table of contents with line numbers
   - Service catalog
   - Library decision matrix
   - Common commands
   - Troubleshooting section

2. **Implementation Guide** with:
   - Library integration patterns
   - Code examples
   - Anti-patterns to avoid
   - Step-by-step guides

3. **Integration Patterns Catalog** (optional but recommended):
   - Proven communication patterns
   - Decision trees
   - Complete code examples

4. **Task-to-Agent Mapping** (optional but recommended):
   - "I need to..." → "Use this tool" guide
   - Quick decision matrix

### Step 4: Implement the Agents

Copy templates to your project's agent directory (e.g., `.claude/agents/`) and customize.

### Step 5: Implement the Commands

Copy command templates to your project's commands directory (e.g., `.claude/commands/`) and customize.

### Step 6: Measure and Iterate

Track:
- Token usage per task
- Time saved
- User satisfaction
- Common queries (expand documentation)

---

## Efficiency Gains

Based on production implementation:

| Agent/Command | Before | After | Reduction |
|---------------|--------|-------|-----------|
| code-reusability | 200K tokens | 5K tokens | 97.5% |
| microservices-architect | 230K tokens | 10K tokens | 95.6% |
| debugger | 150K tokens | 6K tokens | 96.0% |
| developer | 150K tokens | 20-30K tokens | 80-90% |
| enterprise-codebase-documenter | 115K tokens | 9K tokens | 92.2% |
| architecture command | 35K tokens | 1K tokens | 97.1% |
| find-library-usage | 100K tokens | 10K tokens | 90.0% |
| jira-to-prd | 200K tokens | 12K tokens | 94.0% |

**Average: 80-95% reduction** in token usage across all workflows.

---

## Core Principles

These templates are based on these principles:

### 1. 80/20 Rule
80% of queries need only 20% of documentation. Provide targeted access to that 20%.

### 2. Pattern Reuse Over Custom Design
90% of cases fit existing patterns. Reference existing patterns instead of designing new ones.

### 3. Progressive Disclosure
Start with 5K token quick assessment, ask user before expanding to 50K deep dive.

### 4. Memorize Common Patterns
Agents memorize common errors/patterns for instant diagnosis (0 tokens).

### 5. Suggest Commands Over Reading
Agents suggest user run commands instead of consuming tokens themselves.

### 6. Hierarchical Information Architecture
High-level (architecture) → Mid-level (implementation) → Low-level (code examples).

---

## Prerequisites

To use these templates effectively, your project should have:

- [ ] Multiple services or a large codebase (>10 services or 100K+ LOC)
- [ ] Shared libraries or common patterns used across services
- [ ] Some form of documentation (or willingness to create it)
- [ ] AI/LLM agent system (like Claude, GPT, or similar)
- [ ] Version control system (Git recommended)

---

## Getting Started Checklist

- [ ] Review all templates in `/agents` and `/commands`
- [ ] Assess your current documentation structure
- [ ] Identify customization points for your project
- [ ] Create comprehensive architecture documentation
- [ ] Add "For Agents" metadata sections to docs
- [ ] Create implementation guide with code examples
- [ ] (Optional) Create integration patterns catalog
- [ ] (Optional) Create task-to-agent mapping
- [ ] Customize agent templates for your tech stack
- [ ] Customize command templates
- [ ] Implement in your agent system
- [ ] Test with 10-15 common queries
- [ ] Measure token usage and efficiency
- [ ] Iterate based on usage patterns

---

## Anti-Patterns to Avoid

**❌ Don't:**
- Copy templates without customization
- Use line numbers without updating
- Skip creating supporting documentation
- Implement all agents at once (start with 2-3)
- Forget to measure efficiency gains
- Neglect maintenance (line numbers go stale)

**✅ Do:**
- Customize thoroughly for your project
- Update line numbers to match your docs
- Create high-quality supporting docs first
- Start with 2-3 most valuable agents
- Track metrics and demonstrate ROI
- Schedule quarterly maintenance reviews

---

## Example Adaptation Path

### Week 1-2: Documentation
- Create architecture documentation
- Add "For Agents" metadata section
- Create implementation guide with examples

### Week 3: First Agent
- Customize code-reusability agent
- Test with 10 common queries
- Measure token usage

### Week 4: First Command
- Implement `/architecture` command
- Create section reference guide
- Train team on usage

### Week 5-6: Expand
- Add debugger agent
- Add microservices-architect agent
- Implement `/find-library-usage` command

### Week 7-8: Measure & Iterate
- Gather usage metrics
- Collect user feedback
- Optimize based on data
- Expand documentation coverage

---

## Success Stories

Organizations using similar approaches have reported:

- **80-95% reduction** in token usage for common tasks
- **50-75% faster** onboarding for new developers
- **60-80% reduction** in code duplication
- **40-60% faster** troubleshooting during incidents
- **90%+ adoption** of existing patterns over custom solutions

---

## Support and Contributions

These templates are provided as-is based on proven implementation. For:

- **Questions**: Review the customization notes in each template
- **Issues**: Check that line numbers match your docs, supporting docs exist
- **Improvements**: Fork and adapt to your needs, share learnings

---

## Related Resources

- **Architectural Decision**: The implementing organization documented this approach in ADR-0015, covering rationale, assumptions, and trade-offs
- **Further Reading**: For detailed implementation notes, see the CREATION-SUMMARY.md file in this repository

---

## License

These templates are provided as open reference implementations for building context-efficient AI agent systems. Customize freely for your organization's needs.

---

**Version**: 1.0
**Last Updated**: 2025-10-23
**Maintainer**: Platform Architecture Team
