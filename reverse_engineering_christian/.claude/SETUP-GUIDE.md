# Setup Guide - Context-Efficient Documentation Architecture

This guide walks you through setting up the context-efficient documentation architecture for your project using the automated `/setup` command.

**Prerequisites**: Copy the `AI Tools/` folder to your project root. This contains generic templates for agents, commands, and documentation.

---

## Quick Start (10 seconds)

```bash
# In your Claude Code environment
/setup init
```

**If setup already exists**, you'll see:
```
⚠️  Setup already exists!

Setup Date: 2025-10-23
Last Validated: 2025-10-23

Detected components:
  - 4 agents
  - 2 commands
  - Documentation: docs/architecture.md

Options:
  1. /setup validate     - Check health of existing setup
  2. /setup update       - Update configuration without changing files
  3. /setup init --force - Overwrite everything (backup first!)
  4. Cancel              - Exit without changes

Enter your choice [1-4]:
```

**If no setup exists**, it will:
- ✅ Detect your tech stack automatically
- ✅ Count your services and determine architecture type
- ✅ Find or create documentation files
- ✅ Copy templates from AI Tools/ and customize for your stack
- ✅ Instantiate 4 agents + 2 commands + documentation

**Expected output**: 80-95% token reduction across all operations

---

## What Gets Created

### Agents (`.claude/agents/`)

Instantiated from `AI Tools/agents/` templates and customized for your tech stack:

1. **code-reusability.md** - Prevents code duplication by finding existing libraries
   - Source: `AI Tools/agents/code-reusability-agent.md`
   - Token efficiency: 97.5% reduction (5K vs 200K)
   - Use before implementing new functionality

2. **debugger.md** - Diagnoses errors efficiently
   - Source: `AI Tools/agents/debugger-agent.md`
   - Token efficiency: 96% reduction (6K vs 150K)
   - Use for errors, test failures, issues

3. **microservices-architect.md** (optional, microservices only)
   - Source: `AI Tools/agents/microservices-architect-agent.md`
   - Token efficiency: 95.6% reduction (10K vs 230K)
   - Use for architecture decisions

4. **enterprise-codebase-documenter.md** (optional, 10+ services)
   - Source: `AI Tools/agents/enterprise-codebase-documenter-agent.md`
   - Token efficiency: 92.2% reduction (9K vs 115K)
   - Use for multi-repo analysis

### Commands (`.claude/commands/`)

Instantiated from `AI Tools/commands/` templates:

1. **architecture.md** - Query architecture docs
   - Source: `AI Tools/commands/architecture.md`
   - Usage: `/architecture [query]`
   - Example: `/architecture which library for storage`

2. **find-library-usage.md** - Find library usage across services
   - Source: `AI Tools/commands/find-library-usage.md`
   - Usage: `/find-library-usage [library-name]`
   - Example: `/find-library-usage IStorageService`

### Documentation

1. **Architecture Documentation** (enhanced or created)
   - Location: Detected or created at `docs/architecture.md`
   - Includes "For Agents" metadata with line numbers
   - Service catalog, library decision matrix, troubleshooting

2. **Implementation Guide** (enhanced or created)
   - Location: Detected or created based on existing docs
   - Code examples, integration patterns, anti-patterns

3. **Integration Patterns Catalog** (optional, microservices with 5+ services)
   - Communication patterns, decision trees, complete examples

4. **Task-to-Agent Mapping** (optional)
   - "I need to..." → "Use this tool" quick reference

### Configuration

**setup-config.json** - Tracks detection results and setup state
```json
{
  "project": {
    "name": "your-project",
    "techStack": {
      "primary": "nodejs",
      "framework": "express",
      "version": "20.x"
    },
    "structure": {
      "servicesDir": "apps/",
      "sharedLibrariesDir": "packages/shared/",
      "docsDir": "docs/"
    }
  },
  "detection": {
    "confidence": "high",
    "detectedAt": "2025-10-23T10:30:00Z"
  }
}
```

---

## Detection Process

The `/setup init` command performs automated detection without asking questions:

### 1. Tech Stack Detection

**Scans for manifest files:**
- `package.json` → Node.js
- `*.csproj` → .NET
- `pom.xml` / `build.gradle` → Java
- `go.mod` → Go
- `Cargo.toml` → Rust
- `requirements.txt` / `pyproject.toml` → Python

**Parses dependencies for framework:**
- `"express"` → Express
- `"@nestjs/core"` → NestJS
- `"Microsoft.AspNetCore"` → ASP.NET Core
- `"spring-boot-starter"` → Spring Boot
- etc.

**Greps config files for infrastructure:**
- `.env`, `appsettings.json`, `application.yml`
- Patterns: `postgresql://`, `mongodb://`, `redis://`
- Packages: `sqs`, `kafka`, `rabbitmq`, `sns`

**Confidence scoring:**
- High (>90%): Proceed automatically
- Medium (60-90%): Suggest default, allow override
- Low (<60%): Prompt user (rare)

### 2. Service Count & Architecture

**Counts services:**
- Scan subdirectories for manifest files
- Count directories with services
- Classify: 1-3 (small), 4-10 (medium), 11-30 (large), 31+ (enterprise)

**Determines architecture type:**
- 3+ services in subdirectories → Microservices
- Kubernetes/Docker Compose files → Microservices
- 1-2 services → Monolith

### 3. Documentation Discovery

**Scans for existing docs:**
- `CLAUDE.md`, `DEVELOPER_GUIDE.md`, `README.md`
- `docs/architecture.md`, `ARCHITECTURE.md`
- Checks line count (>300 lines = enhance, <300 = create new)

**Creates if missing:**
- Architecture documentation with "For Agents" metadata
- Implementation guide with code examples
- Integration patterns catalog (if microservices)

### 4. Integration Patterns Need

**Auto-includes if:**
- Architecture type = microservices
- Service count >= 5
- Has communication libraries (SQS, Kafka, gRPC, etc.)

**Skips if:**
- Single service or <5 services
- No communication libraries detected

---

## Customization Applied

All templates from `AI Tools/` are copied and customized for your detected tech stack during the instantiation process:

### Tech-Specific Replacements

**Original (generic)**:
```markdown
- Check manifest files (*.csproj, package.json, pom.xml)
- Use [your framework]
- Common error: [generic error]
```

**Customized for Node.js + Express**:
```markdown
- Check manifest files (package.json)
- Use Express framework
- Common error: "Cannot find module" → Run `npm install`
```

**Customized for .NET + ASP.NET Core**:
```markdown
- Check manifest files (*.csproj)
- Use ASP.NET Core framework
- Common error: "CS0246: type not found" → Run `dotnet restore`
```

### Directory Structure Replacements

**Detected structure**:
```
your-project/
├── apps/              # Services directory (detected)
├── packages/shared/   # Shared libraries (detected)
├── docs/              # Documentation (detected)
```

**Templates updated with**:
- `services/` → `apps/`
- `shared-libraries/` → `packages/shared/`
- `docs/` → `docs/`

### Error Pattern Library

Each tech stack gets specific error patterns in the debugger agent:

**Node.js errors**:
- `Cannot find module` → Missing npm install
- `ECONNREFUSED` → Service not running
- `EADDRINUSE` → Port in use

**.NET errors**:
- `CS0246: type not found` → Missing NuGet package
- `SqlException` → Database connection issue
- `address already in use` → Port in use

**Python errors**:
- `ModuleNotFoundError` → Missing pip install
- `OperationalError` → Database issue
- `django.db.migrations.exceptions` → Run migrations

---

## Validation & Health Checks

### Run Validation

```bash
/setup validate
```

**Checks performed:**
- ✓ **Duplicate detection** (CRITICAL - scans .claude/, claude/, .ai/, ai/, tools/ for conflicts)
- ✓ File existence (all agents, commands, docs created)
- ✓ Line number accuracy (metadata matches actual sections)
- ✓ Cross-reference integrity (all links valid)
- ✓ No placeholder text remaining (all [brackets] replaced)
- ✓ Tech stack drift detection (manifest files changed since setup)
- ✓ Template source integrity (AI Tools/ exists, no conflicting sources)

**Output**:
```markdown
# Setup Validation Report

Status: ✅ HEALTHY

Duplicates:
✓ No duplicate agents found (scanned 5 locations)
✓ No duplicate commands found (scanned 5 locations)
✓ No conflicting template sources

Files:
✓ 5 agents found and valid
✓ 2 commands found and valid
✓ 4 documentation files found and valid
✓ setup-config.json exists and valid

Line Numbers:
✓ Architecture doc: 47/47 references accurate
✓ Implementation guide: 23/23 references accurate

Cross-References:
✓ All 18 internal links valid
✓ All 5 command references valid

Tech Stack:
✓ No drift detected since setup
✓ All manifest files unchanged
✓ Dependencies match detection

Last Updated: 2025-10-23
Confidence: HIGH
```

### Update Configuration (Tech Stack Changes)

If your tech stack has changed but you don't want to recreate everything:

```bash
/setup update
```

**Use when**:
- Upgraded Node.js/Python/.NET version
- Added a new database (e.g., Redis)
- Increased service count
- Changed framework

**What it does**:
- ✅ Re-runs all detection (tech stack, services, architecture)
- ✅ Compares with current setup-config.json
- ✅ Shows differences clearly
- ✅ Updates configuration if you approve
- ✅ Provides recommendations based on changes
- ❌ Does NOT modify agent/command files
- ❌ Does NOT modify documentation

**Example output**:
```markdown
⚠️  Configuration drift detected!

Changes detected:
  ✓ Tech stack primary: nodejs (unchanged)
  ✓ Framework: express (unchanged)
  ⚠️  Node.js version: 18.x → 20.x (upgraded)
  ⚠️  Database: PostgreSQL → PostgreSQL + Redis (added)
  ⚠️  Service count: 8 → 12 (increased)

Would you like to update setup-config.json? [Y/n]:
```

After update:
```markdown
✓ Configuration updated!

Recommendations:
  ⚠️  Service count increased (8 → 12)
      → Run: /setup add-agent enterprise-codebase-documenter

Next steps:
  1. /setup validate - Validate updated configuration
  2. Review agents for tech stack specific updates
```

### Fix Line Numbers

If your documentation structure changes:

```bash
/setup update-line-numbers
```

This command:
1. Scans all documentation files
2. Finds section headers
3. Updates line number references in "For Agents" metadata
4. Updates agent file references
5. Preserves all other content

---

## Extending the Setup

### Add New Agent

```bash
/setup add-agent [agent-name]
```

**Example**: `/setup add-agent security-scanner`

**Process**:
1. Copies generic agent template
2. Customizes for your tech stack
3. Adds to `.claude/agents/` directory
4. Updates setup-config.json
5. Validates integration

### Add Integration Patterns

If you didn't include patterns initially:

```bash
/setup add-patterns
```

**Creates**:
- `tasks/integration-patterns-catalog.md`
- Communication patterns section
- Decision trees for service integration
- Complete code examples for your tech stack

---

## Manual Customization

While setup is automated, you may want to customize further:

### 1. Add Domain-Specific Patterns

**Location**: `tasks/integration-patterns-catalog.md`

**Example additions**:
- Your specific event schema
- Your API versioning strategy
- Your authentication flow
- Your data consistency patterns

### 2. Expand Architecture Documentation

**Location**: Detected or created architecture doc

**Add**:
- Service dependency diagrams (Mermaid)
- Data flow diagrams
- Security architecture
- Deployment topology

### 3. Add Tech-Specific Error Patterns

**Location**: `.claude/agents/debugger.md`

**Add memorized patterns** for your most common errors:
```markdown
## Memorized Error Patterns (Your Project)

1. **"Connection timeout to Redis"**
   - Cause: Redis container not running in dev
   - Fix: `docker-compose up redis -d`
   - Confidence: HIGH

2. **"Kafka consumer lag > 10000"**
   - Cause: Slow message processing
   - Fix: Check processor performance, scale consumers
   - Confidence: HIGH
```

### 4. Customize Task-to-Agent Mapping

**Location**: `tasks/task-to-agent-mapping.md`

**Add project-specific workflows**:
```markdown
## Custom Workflows

**"I need to add a new payment method"**
1. `/architecture payment integration`
2. Launch code-reusability (find existing payment libs)
3. `/find-library-usage IPaymentGateway`
4. Implement using existing pattern
5. Launch debugger if issues

**"Our service is getting 502 errors"**
1. Launch debugger agent
2. Check memorized patterns first
3. `/architecture troubleshooting 502`
4. Review service logs and dependencies
```

---

## Maintenance Schedule

### Monthly Tasks

- [ ] Update line numbers: `/setup update-line-numbers`
- [ ] Review common queries (expand documentation coverage)
- [ ] Add new error patterns discovered
- [ ] Update tech stack versions in detection rules

### Quarterly Tasks

- [ ] Run validation: `/setup validate`
- [ ] Measure efficiency metrics (token usage, time saved)
- [ ] Gather user feedback (developer satisfaction)
- [ ] Review memorized error patterns (accuracy, coverage)
- [ ] Update templates based on usage patterns

### After Major Changes

- [ ] Infrastructure changes → Update architecture doc
- [ ] New shared library → Update library decision matrix
- [ ] New service → Update service catalog
- [ ] Tech stack upgrade → Re-run detection: `/setup detect`

---

## Troubleshooting Setup

### Duplicate Agents/Commands Found

**Symptom**: Validation reports agents/commands in multiple locations

**Example**:
```
❌ CONFLICT: Found agents in multiple locations:
  - .claude/agents/debugger.md
  - tools/agents/debugger.md
  - claude/agents/debugger.md
```

**Solutions**:

**Option 1: Keep .claude/ (Recommended)**
```bash
# Backup other locations
cp -r tools/agents/ .backup/tools-agents-$(date +%Y%m%d)/
cp -r claude/agents/ .backup/claude-agents-$(date +%Y%m%d)/

# Remove duplicates
rm -rf tools/agents/
rm -rf claude/agents/

# Validate
/setup validate
```

**Option 2: Consolidate & Compare**
```bash
# Compare files first
diff .claude/agents/debugger.md tools/agents/debugger.md

# If different, manually merge changes
# Then remove duplicates as in Option 1
```

**Option 3: Use Git to Track**
```bash
# Add .claude/ to git if not already
git add .claude/

# Remove untracked duplicates
git clean -fd tools/agents/
git clean -fd claude/agents/
```

**Prevention**:
- Always use `.claude/agents/` and `.claude/commands/` as canonical locations
- Add other locations to `.gitignore`:
  ```
  /tools/agents/
  /claude/agents/
  /ai/agents/
  ```

### Multiple Template Sources

**Symptom**: Found templates in AI Tools/, tasks/shared/, old-templates/, etc.

**Solutions**:
1. **Choose canonical source**: Use `AI Tools/` as standard
2. **Remove old sources**:
   ```bash
   mv tasks/shared/ .backup/tasks-shared-$(date +%Y%m%d)/
   mv old-templates/ .backup/old-templates-$(date +%Y%m%d)/
   ```
3. **Update setup-config.json**:
   ```json
   "detection": {
     "existingSetup": {
       "templateSources": ["AI Tools/"]
     }
   }
   ```

### Setup Already Exists

**Symptom**: Running `/setup init` shows "Setup already exists!" message

**What happened**:
- setup-config.json was found in .claude/ directory
- Setup has already been run previously
- System is preventing accidental overwrites

**Solutions**:

**Option 1: Validate existing setup (recommended)**
```bash
/setup validate
```
Check if everything is working correctly without making changes.

**Option 2: Update configuration only**
```bash
/setup update
```
If your tech stack changed, update setup-config.json without modifying files.

**Option 3: Force re-initialization**
```bash
/setup init --force
```
⚠️ Creates backup first, then overwrites everything.

**Option 4: Manual cleanup**
```bash
# Remove setup tracking (keeps agents/commands)
rm .claude/setup-config.json

# Then re-run
/setup init
```

### Detection Failed

**Symptom**: Setup reports low confidence or incorrect detection

**Solutions**:
1. Check manifest files exist in expected locations
2. Verify dependencies are in standard format
3. Run manual detection: `/setup detect --verbose`
4. Override detection: Edit `setup-config.json` manually

### Templates Not Customized

**Symptom**: Generic placeholders remain (e.g., `[Your framework]`)

**Solutions**:
1. Check `setup-config.json` has correct tech stack
2. Re-run setup: `/setup init --force`
3. Manually replace placeholders using detected values

### Line Numbers Inaccurate

**Symptom**: Validation reports line number mismatches

**Solutions**:
1. Run: `/setup update-line-numbers`
2. If still failing, check documentation structure changed
3. Manually update "For Agents" metadata section

### Agents Not Working

**Symptom**: Agents don't follow efficiency strategies

**Solutions**:
1. Validate setup: `/setup validate`
2. Check agents have "Context Efficiency Strategy" section
3. Verify cross-references to docs are correct
4. Test with simple query: `/architecture test`

---

## Success Metrics

Track these metrics to measure ROI:

### Token Usage (Target: 80-95% reduction)

**Before setup**:
- Architecture query: 35,000 tokens (read full doc)
- Find library: 100,000+ tokens (scan all services)
- Debug error: 150,000 tokens (read logs + search code)

**After setup**:
- Architecture query: 1,000 tokens (97% reduction)
- Find library: 10,000 tokens (90% reduction)
- Debug error: 6,000 tokens (96% reduction)

### Time Saved

**Onboarding new developer**:
- Before: 2-3 days to understand architecture
- After: 2-3 hours with `/architecture` queries

**Implementing new feature**:
- Before: 4 hours researching libraries/patterns
- After: 30 minutes with code-reusability agent

**Troubleshooting incident**:
- Before: 60-90 minutes during outage
- After: 20-30 minutes with debugger agent

### Code Quality

**Code duplication**:
- Before: 60% of new code duplicates existing patterns
- After: <10% duplication (code-reusability catches it)

**Pattern adoption**:
- Before: 50% use custom solutions vs existing patterns
- After: 90%+ use existing patterns

---

## Advanced Usage

### Multi-Repository Projects

If you have multiple repositories:

1. **Run setup in each repo** with `/setup init`
2. **Share detection rules** across repos (copy `setup-config.json`)
3. **Centralize architecture docs** in one repo, reference from others
4. **Use enterprise-codebase-documenter** for cross-repo analysis

### Monorepo with Multiple Stacks

If you have Node.js + Python + .NET in one repo:

1. Setup detects **primary** stack (most services)
2. Customize templates for **secondary** stacks manually
3. Create **per-stack error patterns** in debugger agent
4. Document **polyglot integration patterns**

### CI/CD Integration

**Validate setup in CI**:
```yaml
# .gitlab-ci.yml or .github/workflows/
validate-docs:
  script:
    - /setup validate
    - exit $?
```

**Auto-update line numbers on doc changes**:
```yaml
update-line-numbers:
  script:
    - /setup update-line-numbers
    - git add .
    - git commit -m "chore: update line numbers"
  only:
    - changes:
      - docs/**/*.md
```

---

## Getting Help

### Common Questions

**Q: Can I run setup multiple times?**
A: Yes, but setup detects existing installations and prompts you with options:
- `/setup validate` - Check health without changes
- `/setup update` - Update config only (recommended for tech stack changes)
- `/setup init --force` - Full re-run with backup

**Q: What happens if setup already exists?**
A: Setup detects existing setup-config.json and shows you 4 options instead of running blindly. This prevents accidental overwrites.

**Q: What if my tech stack isn't detected?**
A: Edit `setup-config.json` manually or add detection rules to `detection-rules.json`.

**Q: Do I need to commit setup files?**
A: Yes, commit all `.claude/` files and `tasks/` directory. Do NOT commit `setup-config.json` if it contains secrets.

**Q: Can I customize templates after setup?**
A: Absolutely! Templates are just Markdown files. Edit freely.

**Q: What if detection is wrong?**
A: Override by editing `setup-config.json` and re-running `/setup init --force`.

**Q: How do I add new error patterns?**
A: Edit `.claude/agents/debugger.md` and add to "Memorized Error Patterns" section.

**Q: Can I share templates with other teams?**
A: Yes! The `AI Tools/` templates are designed for reuse. Copy to other projects.

**Q: Does this work with existing documentation?**
A: Yes! Setup enhances existing docs by adding "For Agents" metadata and cross-references.

---

## Next Steps

1. **Run setup**: `/setup init`
2. **Test agents**: Try `/architecture` and `/find-library-usage`
3. **Customize**: Add domain-specific patterns and error cases
4. **Measure**: Track token usage and time saved
5. **Iterate**: Expand documentation based on common queries
6. **Share**: Onboard team with efficiency guides

---

**Version**: 1.0
**Last Updated**: 2025-10-23
**Maintained By**: Platform Architecture Team