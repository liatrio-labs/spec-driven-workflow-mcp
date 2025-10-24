# Duplicate Prevention Strategy

The `/setup` command includes comprehensive duplicate detection to prevent conflicts and ensure a clean, maintainable setup.

## Why Duplicate Prevention Matters

**Problem**: Without duplicate detection, you can end up with:
- Multiple versions of the same agent in different locations
- Conflicting configurations
- Confusion about which version is active
- Wasted effort maintaining duplicates
- Inconsistent behavior across the project

**Solution**: Multi-location scanning with conflict resolution strategies.

---

## Locations Scanned

### Agents

The setup command scans these locations for duplicate agents:
```
.claude/agents/          ← Canonical location (recommended)
claude/agents/           ← Alternative naming
.ai/agents/              ← Alternative naming
ai/agents/               ← Alternative naming
tools/agents/            ← Legacy location
```

### Commands

The setup command scans these locations for duplicate commands:
```
.claude/commands/        ← Canonical location (recommended)
claude/commands/         ← Alternative naming
.ai/commands/            ← Alternative naming
ai/commands/             ← Alternative naming
tools/commands/          ← Legacy location
```

### Slash Commands

Additional scan for existing slash commands:
```
.claude/*.md             ← Check for --- description: --- frontmatter
```

### Template Sources

Scans for template sources that might cause confusion:
```
AI Tools/agents/         ← Canonical template location
AI Tools/commands/       ← Canonical template location
tasks/shared/agents/     ← Legacy template location
old-templates/           ← Backup/archive locations
templates/               ← Generic template directories
```

---

## Detection Process

### Step 1: Initial Scan

Before creating any files, `/setup init` performs a comprehensive scan:

```bash
/setup init
```

**Scanning locations:**
- ✓ Scanning .claude/agents/ ... (2 files found)
- ✓ Scanning claude/agents/ ... (0 files found)
- ✓ Scanning .ai/agents/ ... (0 files found)
- ✓ Scanning ai/agents/ ... (0 files found)
- ✓ Scanning tools/agents/ ... (3 files found)

**Result**: Found 5 total agents across 2 locations

### Step 2: Conflict Detection

Compares files by:
- **Name**: Is the same agent in multiple locations?
- **Content**: Are the files identical or different?
- **Timestamp**: Which version is more recent?
- **Size**: Are there significant differences?

### Step 3: User Prompt

If conflicts are detected, user is prompted with options:

```
⚠️  CONFLICT DETECTED

Found existing agents in multiple locations:
  Location 1: .claude/agents/ (2 agents, last modified: 2025-10-23)
    - code-reusability.md (3.2 KB)
    - debugger.md (2.8 KB)

  Location 2: tools/agents/ (3 agents, last modified: 2025-10-20)
    - code-reusability.md (2.9 KB) ← Different content!
    - debugger.md (2.8 KB) ← Identical
    - old-agent.md (1.5 KB)

Options:
  [S] Skip - Don't create duplicates, use existing in .claude/agents/
  [M] Merge - Enhance existing with efficiency strategies
  [B] Backup - Backup all locations to .backup/, create fresh setup
  [A] Abort - Exit without changes
  [C] Consolidate - Keep .claude/agents/, remove others

Your choice [B]: _
```

---

## Conflict Resolution Strategies

### Strategy 1: Skip (Safe)

**Use when**: Agents already exist and you want to keep them

**What happens**:
- No new files created
- Existing agents are preserved
- Setup creates documentation and config only
- Validation will check existing agents for efficiency patterns

**Command**:
```bash
/setup init
# Choose [S] when prompted
```

### Strategy 2: Merge (Smart)

**Use when**: Existing agents are custom but you want efficiency features

**What happens**:
- Reads existing agent files
- Identifies missing efficiency strategies
- Adds "Context Efficiency Strategy" section
- Adds "For Agents" metadata references
- Preserves custom content

**Command**:
```bash
/setup init
# Choose [M] when prompted
```

### Strategy 3: Backup (Clean Slate)

**Use when**: Want fresh setup but don't want to lose existing work

**What happens**:
- Creates `.backup/agents-YYYYMMDD/` directory
- Moves all existing agents to backup
- Creates fresh agents from templates
- Preserves old work for reference

**Command**:
```bash
/setup init
# Choose [B] when prompted
```

**Backup location**:
```
.backup/
├── agents-20251023/
│   ├── .claude/agents/
│   ├── tools/agents/
│   └── metadata.json (locations, timestamps, file sizes)
└── commands-20251023/
    └── .claude/commands/
```

### Strategy 4: Abort (Review First)

**Use when**: Need to review conflicts manually

**What happens**:
- Setup exits without changes
- No files created or modified
- User can review conflicts and decide
- Can re-run setup after manual cleanup

**Command**:
```bash
/setup init
# Choose [A] when prompted
```

### Strategy 5: Consolidate (Recommended)

**Use when**: Want to standardize on `.claude/` location

**What happens**:
- Keeps `.claude/agents/` and `.claude/commands/`
- Removes duplicates from other locations
- Updates setup-config.json with canonical paths
- Adds `.gitignore` entries for other locations

**Command**:
```bash
/setup init
# Choose [C] when prompted
```

**Result**:
```bash
✓ Consolidated to .claude/agents/
✓ Removed duplicates from tools/agents/
✓ Removed duplicates from claude/agents/
✓ Updated .gitignore
```

---

## Validation & Monitoring

### Continuous Monitoring

Run validation regularly to catch drift:

```bash
/setup validate
```

**Duplicate check output**:
```markdown
## Duplicate Detection

Status: ✅ No duplicates found

Locations scanned:
✓ .claude/agents/ (4 agents)
✓ claude/agents/ (0 agents)
✓ .ai/agents/ (0 agents)
✓ ai/agents/ (0 agents)
✓ tools/agents/ (0 agents)

Template sources:
✓ AI Tools/agents/ (4 templates)
✓ No conflicting template sources

Last scanned: 2025-10-23 14:30:00
```

### Warning Scenarios

**Scenario 1: New duplicates appeared**
```markdown
⚠️  WARNING: Duplicates detected since last validation

New duplicates found:
- tools/agents/new-agent.md
  (Duplicate of .claude/agents/new-agent.md created 1 hour ago)

Recommendation: Run consolidation
```

**Scenario 2: Content divergence**
```markdown
❌ CRITICAL: Same agent with different content

Conflict:
  .claude/agents/debugger.md (Last modified: 2025-10-23 10:00)
  tools/agents/debugger.md (Last modified: 2025-10-23 14:00)

Content difference: 45 lines changed

Action required: Manual review and merge
```

---

## Best Practices

### 1. Use Canonical Locations

**Always use**:
- `.claude/agents/` for agents
- `.claude/commands/` for commands
- `AI Tools/` for template sources

**Avoid**:
- Creating agents in random locations
- Multiple template directories
- Inconsistent naming conventions

### 2. Add to .gitignore

Prevent accidental commits of duplicates:

```gitignore
# Prevent duplicate agent locations
/tools/agents/
/claude/agents/
/ai/agents/

# Prevent multiple template sources
/tasks/shared/
/old-templates/
/templates/

# Allow canonical locations
!/.claude/agents/
!/.claude/commands/
!/AI Tools/
```

### 3. Document Your Structure

In your project README:

```markdown
## AI Agent Structure

**Canonical Locations**:
- Agents: `.claude/agents/`
- Commands: `.claude/commands/`
- Templates: `AI Tools/`

**Do NOT create files in**:
- `tools/agents/`
- `claude/agents/` (no dot prefix)
- `ai/agents/`

Run `/setup validate` regularly to check for duplicates.
```

### 4. Automate Validation

Add to CI/CD pipeline:

```yaml
# .github/workflows/validate-setup.yml
name: Validate Setup
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate AI setup
        run: |
          # Run validation
          /setup validate

          # Fail if duplicates found
          if grep -q "❌ CONFLICT" validation-report.md; then
            echo "Duplicate agents/commands detected!"
            exit 1
          fi
```

### 5. Regular Cleanup

Schedule monthly cleanup:

```bash
# Monthly task
/setup validate
# Review any warnings
# Remove any duplicates found
# Update .gitignore if needed
```

---

## Recovery from Conflicts

### If You Accidentally Created Duplicates

**Step 1: Identify duplicates**
```bash
/setup validate > report.md
cat report.md
```

**Step 2: Compare content**
```bash
diff .claude/agents/debugger.md tools/agents/debugger.md
```

**Step 3: Choose resolution**

If **identical**:
```bash
# Just remove duplicates
rm -rf tools/agents/
```

If **different**:
```bash
# Backup first
cp -r tools/agents/ .backup/tools-agents-$(date +%Y%m%d)/

# Manually merge important changes into .claude/agents/
# Then remove duplicates
rm -rf tools/agents/
```

**Step 4: Validate**
```bash
/setup validate
# Should show "No duplicates found"
```

### If Setup Created Duplicates

**This should never happen** - setup includes duplicate detection. If it does:

1. **Report bug** with setup-config.json and validation output
2. **Backup everything**:
   ```bash
   tar -czf backup-$(date +%Y%m%d).tar.gz .claude/ tools/ ai/ claude/
   ```
3. **Run forced consolidation**:
   ```bash
   /setup init --force --consolidate
   ```

---

## FAQ

**Q: Why scan so many locations?**
A: Different projects use different conventions. Some use `.claude/`, others use `claude/` or `tools/`. Scanning all prevents hidden duplicates.

**Q: What if I want agents in multiple locations?**
A: This is not recommended. It leads to confusion and maintenance burden. Use symlinks if you need agents accessible from multiple locations:
```bash
ln -s .claude/agents/ tools/agents
```

**Q: Can I customize which locations are scanned?**
A: Yes, edit `setup-config.json`:
```json
{
  "validation": {
    "scanLocations": {
      "agents": [".claude/agents/", "custom/path/agents/"],
      "commands": [".claude/commands/"]
    }
  }
}
```

**Q: What about slash commands vs agents?**
A: Slash commands (`.claude/*.md` with frontmatter) are different from agents (`.claude/agents/*.md`). Setup scans for both to prevent naming conflicts.

**Q: How long does duplicate detection take?**
A: On a typical project (<100 files scanned), ~2 seconds. Enterprise projects with many services may take ~10 seconds.

**Q: Can I skip duplicate detection?**
A: Not recommended, but possible:
```bash
/setup init --skip-duplicate-check
```
⚠️ Use with caution - may create conflicts!

---

**Version**: 1.0
**Last Updated**: 2025-10-24
**Related**: SETUP-GUIDE.md, setup.md command