---
description: Automated setup for context-efficient documentation architecture
---

# Setup Command - Automated Architecture Scaffolding

This command automatically detects your project structure and scaffolds the context-efficient documentation architecture with minimal user input.

## Commands

- `/setup init` - Initial setup (auto-detects everything)
- `/setup validate` - Check health of existing setup
- `/setup update` - Update configuration without changing files
- `/setup update-line-numbers` - Refresh line number references
- `/setup add-agent [name]` - Add additional agent
- `/setup add-patterns` - Add integration patterns catalog

---

## /setup init

Run automated setup to instantiate agents, commands, and documentation from generic templates.

**Prerequisites**: Ensure `AI Tools/` directory exists with generic templates (agents, commands, docs).

### Pre-Flight Check (Before Any Changes)

**Check for existing setup:**

```bash
# Check for setup-config.json
if [ -f ".claude/setup-config.json" ]; then
  # Setup already exists
  SETUP_DATE=$(jq -r '.setupDate' .claude/setup-config.json)
  LAST_VALIDATED=$(jq -r '.lastValidated' .claude/setup-config.json)

  echo "⚠️  Setup already exists!"
  echo ""
  echo "Setup Date: $SETUP_DATE"
  echo "Last Validated: $LAST_VALIDATED"
  echo ""
  echo "Detected components:"
  echo "  - $(ls .claude/agents/*.md 2>/dev/null | wc -l) agents"
  echo "  - $(ls .claude/commands/*.md 2>/dev/null | wc -l) commands"
  echo "  - Documentation: $(jq -r '.files.architectureDoc' .claude/setup-config.json)"
  echo ""
  echo "Options:"
  echo "  1. /setup validate     - Check health of existing setup"
  echo "  2. /setup update       - Update configuration without changing files"
  echo "  3. /setup init --force - Overwrite everything (backup first!)"
  echo "  4. Cancel              - Exit without changes"
  echo ""
  read -p "Enter your choice [1-4]: " CHOICE

  case $CHOICE in
    1)
      exec /setup validate
      ;;
    2)
      exec /setup update
      ;;
    3)
      echo "Creating backup..."
      tar -czf ".backup/setup-backup-$(date +%Y%m%d-%H%M%S).tar.gz" .claude/
      echo "✓ Backup created"
      # Continue with setup
      ;;
    4)
      echo "Setup cancelled."
      exit 0
      ;;
    *)
      echo "Invalid choice. Exiting."
      exit 1
      ;;
  esac
fi
```

**If no setup exists, proceed with detection:**

### Execution Steps

**Step 1: Automated Detection (No user input required)**

Detect the following by analyzing the codebase:

1. **Tech Stack Detection:**
   ```
   Search for manifest files in root and subdirectories:
   - package.json → Node.js (check dependencies for Express/Next/Nest/React)
   - requirements.txt or pyproject.toml → Python (check for Django/Flask/FastAPI)
   - pom.xml or build.gradle → Java (check for Spring Boot)
   - *.csproj or *.sln → .NET (check <TargetFramework> for version, check for AspNetCore)
   - go.mod → Go
   - Cargo.toml → Rust
   - Gemfile → Ruby (check for Rails)
   - mix.exs → Elixir (check for Phoenix)

   Database detection (grep config files):
   - Search .env, appsettings.json, config/, application.yml for connection strings
   - "postgresql://" or "postgres://" → PostgreSQL
   - "mongodb://" → MongoDB
   - "mysql://" → MySQL
   - "redis://" → Redis

   Message queue detection (grep manifests + configs):
   - "sqs" or "aws-sdk" with queue configs → AWS SQS
   - "kafka" → Apache Kafka
   - "rabbitmq" or "amqp" → RabbitMQ
   - "@google-cloud/pubsub" → Google Pub/Sub
   ```

2. **Service Count & Architecture:**
   ```
   Count services:
   - Find all directories with manifest files (excluding node_modules, bin, obj)
   - Check for common service directories: apps/, services/, microservices/, packages/, projects/
   - Count unique services

   Architecture type:
   - 1-2 services + single src/ directory → Monolith
   - 3+ services in subdirectories → Microservices
   - Check for k8s/, kubernetes/, helm/, docker-compose.yml → Container orchestration
   - Check for Istio, Linkerd configs → Service mesh

   Classification:
   - 1-3 services → Small
   - 4-10 services → Medium
   - 11-30 services → Large
   - 31+ services → Enterprise
   ```

3. **Existing Documentation:**
   ```
   Scan root for (in priority order):
   1. CLAUDE.md → Check for "For Agents" section
   2. DEVELOPER_GUIDE.md or DEVELOPERS.md
   3. CONTRIBUTING.md
   4. README.md (if >500 lines with Architecture/Development sections)
   5. docs/README.md or docs/architecture.md

   Decision logic:
   - If found + substantial (>300 lines) → Enhance existing (add metadata)
   - If found + small → Create new architecture.md, reference existing
   - If not found → Create new docs/architecture.md + implementation-guide.md
   ```

4. **Integration Patterns Need:**
   ```
   Auto-include patterns if:
   - Microservices detected (3+ services) AND
   - Service count >= 5 AND
   - Communication libraries detected (HTTP clients, message queues)

   Skip if:
   - Single service or monolith
   - Service count < 5
   - docs/integration-patterns.md already exists
   ```

**Step 2: Check for Existing Agents/Commands (Prevent Duplicates)**

**CRITICAL: Scan all possible locations to avoid duplicates:**

```bash
# Check for existing agents
.claude/agents/*.md
claude/agents/*.md
.ai/agents/*.md
ai/agents/*.md
tools/agents/*.md

# Check for existing commands
.claude/commands/*.md
claude/commands/*.md
.ai/commands/*.md
ai/commands/*.md
tools/commands/*.md

# Check for existing slash commands (different naming)
.claude/*.md (look for --- description: --- frontmatter)
```

**Conflict Resolution Strategy:**

1. **If agents/commands already exist:**
   - List existing agents/commands with their locations
   - Ask user: "Found existing agents in `.claude/agents/`. Options:
     - [S]kip - Don't create duplicates, use existing
     - [M]erge - Enhance existing with efficiency strategies
     - [B]ackup - Backup existing to `.claude/agents.backup/`, create new
     - [A]bort - Exit setup without changes"

2. **If template sources found (AI Tools/, tasks/shared/, etc.):**
   - Warn: "Found template sources in multiple locations:
     - AI Tools/agents/ (4 templates)
     - tasks/shared/agents/ (4 templates)
     Which location should be used as source? [AI Tools]"

3. **If setup-config.json exists:**
   - Detect previous setup: "Setup already run on [date]. Options:
     - [U]pdate - Re-detect and update configuration
     - [V]alidate - Check health without changes
     - [F]orce - Overwrite everything (backup first)
     - [C]ancel"

**Step 3: Generate Configuration**

Create `.claude/setup-config.json`:

```json
{
  "version": "1.0",
  "setupDate": "2025-10-23T14:30:00Z",
  "lastValidated": "2025-10-23T14:30:00Z",
  "detection": {
    "confidence": {
      "techStack": "high|medium|low",
      "architecture": "high|medium|low",
      "documentation": "high|medium|low"
    },
    "existingSetup": {
      "hasAgents": false,
      "hasCommands": false,
      "agentLocations": [],
      "commandLocations": [],
      "templateSources": ["AI Tools/"]
    }
  },
  "project": {
    "name": "detected-from-package.json-or-*.sln",
    "techStack": {
      "primary": "nodejs|python|java|dotnet|go|rust|ruby|elixir",
      "framework": "express|django|spring-boot|aspnet-core|etc",
      "database": "postgresql|mongodb|mysql|redis|etc",
      "messageQueue": "sqs|kafka|rabbitmq|pubsub|none"
    },
    "structure": {
      "servicesDir": "apps/|services/|microservices/|src/",
      "sharedLibsDir": "packages/|libs/|shared/|common/",
      "docsDir": "docs/|documentation/"
    },
    "manifestFiles": {
      "type": "package.json|*.csproj|pom.xml|go.mod|Cargo.toml|Gemfile|mix.exs",
      "configFiles": ".env|appsettings.json|application.yml|config.js"
    }
  },
  "architecture": {
    "type": "microservices|monolith|hybrid",
    "serviceCount": 0,
    "scale": "small|medium|large|enterprise",
    "orchestration": "kubernetes|docker-compose|none",
    "serviceMesh": "istio|linkerd|none"
  },
  "features": {
    "microservices": true,
    "integrationPatterns": true,
    "multiTenant": false
  },
  "agents": [
    "code-reusability",
    "microservices-architect",
    "debugger",
    "enterprise-codebase-documenter"
  ],
  "commands": [
    "architecture",
    "find-library-usage"
  ],
  "files": {
    "architectureDoc": "docs/architecture.md",
    "implementationGuide": "CLAUDE.md|docs/implementation-guide.md",
    "integrationPatterns": "docs/integration-patterns.md",
    "taskMapping": "docs/task-to-agent-mapping.md"
  }
}
```

**Step 3: Create Directory Structure**

```
Create if not exists:
.claude/
├── agents/
├── commands/
└── setup-config.json

Create if not exists:
docs/                    (or tasks/ or documentation/ based on detection)
├── architecture.md
├── implementation-guide.md  (or enhance existing CLAUDE.md)
├── integration-patterns.md  (if microservices)
└── task-to-agent-mapping.md
```

**Step 4: Generate Copy Instructions for User**

**IMPORTANT**: Setup command does NOT copy files automatically. Instead, it generates instructions for the user to copy files themselves.

**Output clear instructions:**

```markdown
## Setup Instructions

Based on your detected configuration, please copy the following files:

### Step 1: Copy Agents

**From**: `AI Tools/agents/`
**To**: `.claude/agents/`

Copy these agents:
- ✅ code-reusability-agent.md → code-reusability.md (Required for all projects)
- ✅ debugger-agent.md → debugger.md (Required for all projects)
- ✅ microservices-architect-agent.md → microservices-architect.md (Recommended: 3+ services detected)
- ⚠️  enterprise-codebase-documenter-agent.md → enterprise-codebase-documenter.md (Optional: Recommended for 10+ services, you have 8)

### Step 2: Copy Commands

**From**: `AI Tools/commands/`
**To**: `.claude/commands/`

Copy these commands:
- ✅ architecture.md → architecture.md (Required)
- ✅ find-library-usage.md → find-library-usage.md (Recommended: 5+ services detected)

### Step 3: Customize Templates (Optional but Recommended)

After copying, you should customize placeholders in the files:
```

**Then provide customization guidance based on detection:**

   ```
   Replace placeholders in copied files:
   - [Your framework] → Detected framework (Express, Django, ASP.NET Core, etc.)
   - [Your database] → Detected database (PostgreSQL, MongoDB, etc.)
   - [Your message queue] → Detected queue (SQS, Kafka, RabbitMQ, etc.)
   - [Your orchestration] → Detected platform (Kubernetes, Docker Swarm, etc.)
   - *.csproj → Detected manifest type (package.json, pom.xml, etc.)
   - appsettings.json → Detected config files (.env, application.yml, etc.)
   - services/ → Detected services directory
   - shared-libraries/ → Detected shared libs directory
   - dotnet → Detected build command (npm, mvn, cargo, etc.)
   - kubectl → Detected orchestration command
   ```

3. **Add tech-specific error patterns** to debugger agent:
   ```
   Node.js:
   - "Cannot find module" → Missing npm install
   - "ECONNREFUSED" → Service not running
   - "EADDRINUSE" → Port already in use

   .NET:
   - "CS0246: The type or namespace 'X' could not be found" → Missing NuGet package
   - "SqlException" → Database connection issue

   Python:
   - "ModuleNotFoundError" → Missing pip install
   - "ConnectionRefusedError" → Service not running

   Java:
   - "ClassNotFoundException" → Missing Maven dependency
   - "JDBCConnectionException" → Database connection issue

   Go:
   - "cannot find package" → Missing go get
   - "dial tcp: connection refused" → Service not running
   ```

4. **Update agent references** to actual file paths from config

**Agents to Instantiate (conditionally):**

- ✅ Always: Copy `AI Tools/agents/code-reusability-agent.md` → `.claude/agents/code-reusability.md`
- ✅ Always: Copy `AI Tools/agents/debugger-agent.md` → `.claude/agents/debugger.md`
- ✅ If microservices (3+ services): Copy `AI Tools/agents/microservices-architect-agent.md` → `.claude/agents/microservices-architect.md`
- ✅ If enterprise (10+ services): Copy `AI Tools/agents/enterprise-codebase-documenter-agent.md` → `.claude/agents/enterprise-codebase-documenter.md`

**Commands to Instantiate:**

- ✅ Always: Copy `AI Tools/commands/architecture.md` → `.claude/commands/architecture.md`
- ✅ If 5+ services: Copy `AI Tools/commands/find-library-usage.md` → `.claude/commands/find-library-usage.md`

**Step 5: Create/Enhance Documentation**

**If existing doc found (e.g., CLAUDE.md):**
```markdown
Add to top of file (after title):

---

## For Agents & LLMs

This document is optimized for both human and programmatic reading.

**Quick Lookups:**
- **Service Catalog** (lines TBD): All services with dependencies
- **Library Decision Matrix** (lines TBD): Which library for what task
- **Common Commands** (lines TBD): Executable commands
- **Troubleshooting** (lines TBD): Common issues and fixes

**Document Relationship:**
- **This Document**: Implementation guidance and patterns (prescriptive)
- **[docs/architecture.md](docs/architecture.md)**: System overview (descriptive)
- **Together**: Complete reference for development

**Query This Document:** Use `/architecture [query]` for quick lookups.

**Architectural Decision**: This documentation architecture is documented in ADR-XXXX.

---

[Rest of existing content preserved]
```

**If creating new docs/architecture.md:**
```markdown
# [Project Name] - Architecture Documentation

**Generated:** [Date]
**Last Updated:** [Date]
**Services Analyzed:** [Count]

---

## For Agents & LLMs

This document is optimized for both human and programmatic reading.

**Quick Lookups:**
- **Service Catalog** (lines 50-120): All services with dependencies
- **Library Decision Matrix** (lines 150-200): Which library for what task
- **Communication Patterns** (lines 220-280): How services interact
- **Common Commands** (lines 300-400): Executable commands
- **Troubleshooting** (lines 420-500): Common issues and fixes

**Cross-References:**
- For implementation details → See [implementation-guide.md](implementation-guide.md)
- For real-world usage → Use `/find-library-usage [library-name]`
- For architectural decisions → See ADRs if available

**Query This Document:** Use `/architecture [query]` for quick lookups.

---

## Executive Summary

[Auto-generated based on detection:
- Primary tech stack
- Architecture type (microservices/monolith)
- Service count
- Key technologies (database, message queue, orchestration)]

## Service Catalog

[Template for user to fill in:
Table with columns: Service Name, Purpose, Tech Stack, Dependencies, Data Stores]

## Communication Patterns

[Template based on detection:
- If message queue detected → Document async patterns
- If HTTP clients detected → Document REST patterns
- If both → Document hybrid patterns]

## Common Commands

[Auto-populated based on tech stack:
- Build: npm run build / dotnet build / mvn package / cargo build
- Test: npm test / dotnet test / pytest / go test
- Run: npm start / dotnet run / java -jar / cargo run
- Deploy: kubectl apply / docker-compose up / etc.]

## Troubleshooting

[Template with common issues for detected stack]

## Port Reference

[Template for user to document service ports]
```

**If creating integration-patterns.md:**
```markdown
# Integration Patterns Catalog

**Purpose:** Proven patterns for service-to-service communication.
**Last Updated:** [Date]

This catalog is part of the context-efficient documentation architecture.

---

## Quick Pattern Selection

```
Need real-time response?
├─ Yes → Pattern 1: Synchronous REST API
└─ No → Asynchronous communication
    ├─ 1-to-many broadcast? → Pattern 2: Asynchronous Events
    ├─ Ordered processing? → Pattern 3: Queue-Based Workflow
    └─ etc.
```

## Pattern 1: Synchronous REST API

[Framework-specific example using detected tech stack]

## Pattern 2: Asynchronous Events

[Message queue-specific example using detected queue system]

[Continue for all 7 patterns...]
```

**Step 6: Validation**

Run health checks:
```
✓ All agents created and customized
✓ All commands functional
✓ Documentation created/enhanced
✓ Cross-references valid
✓ setup-config.json created
✓ No placeholder text remaining (except [TBD] for line numbers)
```

**Step 7: Output Report**

```markdown
# Setup Complete! ✨

## Detection Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Tech Stack:** [Primary language/framework]
**Database:** [Detected]
**Message Queue:** [Detected or None]
**Architecture:** [Microservices/Monolith] ([X] services)
**Scale:** [Small/Medium/Large/Enterprise]
**Orchestration:** [Kubernetes/Docker Compose/None]

## Created Files
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**Agents (4):**
✓ .claude/agents/code-reusability.md
✓ .claude/agents/microservices-architect.md
✓ .claude/agents/debugger.md
✓ .claude/agents/enterprise-codebase-documenter.md

**Commands (2):**
✓ .claude/commands/architecture.md
✓ .claude/commands/find-library-usage.md

**Documentation (4):**
✓ docs/architecture.md [CREATED]
✓ CLAUDE.md [ENHANCED - added "For Agents" metadata]
✓ docs/integration-patterns.md [CREATED]
✓ docs/task-to-agent-mapping.md [CREATED]

**Configuration:**
✓ .claude/setup-config.json [CREATED]

## Customizations Applied
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Updated manifest patterns ([manifest type])
✓ Updated config patterns ([config files])
✓ Added [language]-specific error patterns
✓ Updated directory references ([services dir])
✓ Added common [language] commands

## Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. **Test commands:**
   - `/architecture test`
   - `/find-library-usage [any-library]`

2. **Enhance documentation:**
   - Review docs/architecture.md
   - Add service details to catalog section
   - Document your specific patterns

3. **Update line numbers:**
   - After editing docs, run: `/setup update-line-numbers`

4. **Validate setup:**
   - Run: `/setup validate`

## Token Efficiency
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Expected efficiency gains:
- Agent operations: 80-95% reduction
- Architecture queries: 97% reduction
- Library searches: 90% reduction

Run `/setup validate` anytime to check health.
```

---

## /setup validate

Check health of existing setup and detect issues.

### Validation Checks

**1. Duplicate Detection (CRITICAL):**
```
Scan all possible locations:
✓ No duplicate agents found across:
  - .claude/agents/
  - claude/agents/
  - .ai/agents/
  - ai/agents/
  - tools/agents/

✓ No duplicate commands found across:
  - .claude/commands/
  - claude/commands/
  - .ai/commands/
  - ai/commands/
  - tools/commands/

⚠️  Warning: Found agents in multiple locations:
  - .claude/agents/code-reusability.md
  - tools/agents/code-reusability.md
  Action: Consolidate to single location (.claude/agents/)

❌ CONFLICT: Same agent with different content:
  - .claude/agents/debugger.md (1234 bytes, modified 2025-10-23)
  - claude/agents/debugger.md (5678 bytes, modified 2025-10-20)
  Action: Review and keep most recent version
```

**2. File Existence:**
```
✓ .claude/setup-config.json exists
✓ .claude/agents/ directory exists
✓ .claude/commands/ directory exists
✓ Documentation files exist per config
```

**3. Configuration Validity:**
```
✓ setup-config.json is valid JSON
✓ All referenced files in config exist
✓ Tech stack matches detected (warn if changed)
✓ No orphaned entries (files in config that don't exist)
```

**4. Line Number Accuracy:**
```
Read "For Agents" metadata from docs
Compare with actual section locations
Report mismatches:
  ⚠️  Service Catalog metadata says lines 50-120, actually at 180-250
```

**5. Cross-Reference Integrity:**
```
Check agents for broken references:
✓ All file paths in agents exist
✓ All line number ranges valid
✓ All commands reference valid docs
```

**6. Customization Completeness:**
```
Scan agents/commands for placeholder text:
  ❌ Found "[Your framework]" in debugger.md
  ❌ Found "[TBD]" in architecture.md
  ✓ No placeholders in other files
```

**7. Tech Stack Drift:**
```
Re-run detection and compare to config:
  ⚠️  Config says Node.js, but now detecting .NET
      (User may have changed project structure)
```

**8. Template Source Integrity:**
```
Check if template sources still exist:
✓ AI Tools/agents/ exists with 4 templates
✓ AI Tools/commands/ exists with 2 templates

⚠️  Multiple template sources found:
  - AI Tools/agents/ (4 templates)
  - tasks/shared/agents/ (4 templates)
  - old-templates/agents/ (2 templates)
  Recommendation: Consolidate to AI Tools/
```

### Output Format

```markdown
# Validation Report

## Status: ✅ Healthy | ⚠️ Needs Attention | ❌ Issues Found

## File Health
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All required files exist
✅ Configuration is valid
✅ All cross-references intact

## Line Numbers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  2 sections need updating:
  - Service Catalog: metadata says lines 50-120, actually at 180-250
  - Common Commands: metadata says lines 300-400, actually at 450-550

Run `/setup update-line-numbers` to fix.

## Customization
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❌ Found 3 placeholders:
  - debugger.md:45 → "[Your framework]"
  - architecture.md:120 → "[TBD]"
  - architecture.md:300 → "[TBD]"

Manually update these placeholders.

## Tech Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ No drift detected (still .NET 8)

## Recommendations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Run `/setup update-line-numbers` to fix metadata
2. Edit debugger.md and remove placeholder text
3. Complete architecture.md sections marked [TBD]

Last validated: 2025-10-23T14:30:00Z
```

---

## /setup update

Update setup configuration without modifying agents, commands, or documentation files.

**Use when**:
- Tech stack has changed (upgraded Node.js version, switched database, etc.)
- Service count has increased/decreased
- Want to refresh detection without recreating files
- Need to update setup-config.json with current state

### Process

**1. Re-run all detection logic:**
```bash
# Same detection as /setup init, but non-destructive
- Tech stack detection (manifest files, dependencies)
- Service count & architecture type
- Database & message queue detection
- Orchestration platform detection
```

**2. Compare with existing setup-config.json:**
```json
// Current config
{
  "project": {
    "techStack": {
      "primary": "nodejs",
      "framework": "express",
      "version": "18.x"
    }
  }
}

// Newly detected
{
  "project": {
    "techStack": {
      "primary": "nodejs",
      "framework": "express",
      "version": "20.x"  // ⚠️  Changed!
    }
  }
}
```

**3. Show differences and prompt for update:**
```markdown
⚠️  Configuration drift detected!

Changes detected:
  ✓ Tech stack primary: nodejs (unchanged)
  ✓ Framework: express (unchanged)
  ⚠️  Node.js version: 18.x → 20.x (upgraded)
  ⚠️  Database: PostgreSQL → PostgreSQL + Redis (added)
  ⚠️  Service count: 8 → 12 (increased)

Would you like to update setup-config.json?
  [Y] Yes - Update configuration
  [N] No - Keep existing configuration
  [D] Diff - Show detailed changes
  [A] Abort

Your choice [Y]:
```

**4. Update setup-config.json:**
```bash
# If user chooses Yes
- Update techStack section with new values
- Update serviceCount
- Update lastValidated timestamp
- Preserve agents/commands list (don't change files)
- Add changelog entry:
  "changelog": [
    {
      "date": "2025-10-24",
      "action": "update",
      "changes": ["Node.js 18.x → 20.x", "Added Redis", "Service count 8 → 12"]
    }
  ]
```

**5. Provide recommendations:**
```markdown
✓ Configuration updated!

Recommendations based on changes:
  ⚠️  Node.js version upgraded (18.x → 20.x)
      → Review agents for Node.js 20 specific patterns
      → Update error patterns in debugger.md

  ⚠️  Redis added as new database
      → Consider adding Redis connection patterns to docs
      → Update architecture documentation

  ⚠️  Service count increased (8 → 12)
      → Consider adding find-library-usage command (5+ services recommended)
      → Run /setup add-agent enterprise-codebase-documenter (10+ services)

Next steps:
  1. /setup validate           - Validate updated configuration
  2. /setup update-line-numbers - If docs changed
  3. Review agents for tech stack specific updates
```

**Important**: This command does NOT:
- ❌ Modify agent files
- ❌ Modify command files
- ❌ Modify documentation
- ❌ Re-run customization

**It only updates setup-config.json with current detection results.**

---

## /setup update-line-numbers

Automatically scan documentation and update line number references.

### Process

**1. Scan Architecture Doc:**
```
Read docs/architecture.md
Find sections:
  - ## Service Catalog (lines 180-250)
  - ## Library Decision Matrix (lines 280-330)
  - ## Common Commands (lines 450-550)
  - ## Troubleshooting (lines 580-650)
```

**2. Update "For Agents" Metadata:**
```
Update in docs/architecture.md:
  Before:
    - Service Catalog (lines 50-120)
  After:
    - Service Catalog (lines 180-250)
```

**3. Update Agent References:**
```
Scan all agents for line number references:
  architecture.md lines 50-120 → architecture.md lines 180-250
Update in all agent files
```

**4. Report Changes:**
```markdown
# Line Numbers Updated

Updated 8 references:
  architecture.md metadata → 4 sections updated
  code-reusability.md → 2 references updated
  microservices-architect.md → 2 references updated

Run `/setup validate` to confirm.
```

---

## /setup add-agent [name]

Add additional agent from shared templates.

### Usage

```
/setup add-agent security-auditor
/setup add-agent performance-optimizer
/setup add-agent database-optimizer
```

### Process

1. Check if agent exists in shared templates
2. Copy from `AI Tools/agents/[name].md`
3. Customize using setup-config.json (tech stack, paths)
4. Place in `.claude/agents/[name].md`
5. Update setup-config.json agents list
6. Update task-to-agent-mapping.md if exists

---

## /setup add-patterns

Add integration patterns catalog if not created during init.

### Process

1. Check if docs/integration-patterns.md exists
2. If exists → Enhance with additional patterns
3. If not exists → Create from template
4. Customize for detected tech stack and message queue
5. Update setup-config.json

---

## Fallback Behavior (Low Confidence)

If detection confidence is LOW on critical decisions:

```markdown
⚠️  Unable to clearly detect [aspect]

**Found:** [Ambiguous evidence]

**Options:**
1. Auto-setup with best guess [framework/architecture]
2. Skip this component (add later with `/setup add-...`)
3. Specify manually

Recommendation: [1] - You can refine later

Proceed with option [1/2/3]: _
```

Only prompt when truly ambiguous, not for every decision.

---

## Agent Behavior When Setup Missing

All agents should check for setup on first use:

```markdown
⚠️  Context-efficient documentation not detected.

I'll work with what's available, but results will be better with full setup.

**Quick fix:** Run `/setup init` to scaffold architecture (takes ~10 seconds)

For now, I'll operate in basic mode without:
- Integration patterns catalog
- Architecture documentation with line numbers
- Optimized reference documents

Would you like me to continue anyway? (Y/N)
```

---

## Example: Complete Automated Flow

```
User: /setup init

[No questions asked - auto-detection runs]

Scanning codebase... (3 seconds)
✓ Detected: Node.js 20 + TypeScript
✓ Detected: Express framework
✓ Detected: PostgreSQL + Redis
✓ Detected: Kafka message queue
✓ Found: 12 microservices in apps/
✓ Found: Existing README.md (450 lines)
✓ Structure: Monorepo with Docker Compose

Generating configuration... (1 second)

Creating structure... (2 seconds)
✓ .claude/agents/ (4 agents)
✓ .claude/commands/ (2 commands)
✓ docs/ (4 documentation files)

Customizing for Node.js + Express... (2 seconds)
✓ Updated to package.json patterns
✓ Updated to .env config patterns
✓ Added Node.js error patterns
✓ Updated to apps/ directory
✓ Added npm commands

Validating... (1 second)
✓ All checks passed

Setup complete! (9 seconds total)

[Full report displayed]
```

---

## Configuration Schema

See `.claude/setup-config.json` for complete configuration structure used by all agents and commands.