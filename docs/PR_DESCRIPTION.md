# PR: Add codebase context generation with evidence-based analysis

## Summary

Creates a new `generate-codebase-context` prompt with comprehensive research-driven analysis capabilities. This prompt provides evidence-based codebase analysis with confidence assessment, supporting spec-driven feature development.

## What's New in This PR

### 1. New Prompt: `generate-codebase-context` ✨

**File:** `prompts/generate-codebase-context.md` (877 lines)

A comprehensive prompt for analyzing codebases before feature development, incorporating battle-tested patterns from Claude Code and research best practices.

**Core Capabilities:**
- **6-Phase Analysis Process:**
  1. Repository structure detection
  2. Documentation audit with rationale extraction
  3. Code analysis (WHAT + HOW)
  4. Integration points mapping
  5. Gap identification
  6. Evidence-based documentation generation

- **Evidence Citation Standards:**
  - Code findings: `path/to/file.ts:45-67` (with line ranges)
  - Documentation findings: `path/to/doc.md#section-heading` (with anchors)
  - User input: `[User confirmed: YYYY-MM-DD]` (dated quotes)

- **Confidence Assessment:**
  - 🟢 High: Strong evidence from working code or explicit docs
  - 🟡 Medium: Inferred from context, feature flags, or implied
  - 🔴 Low: Cannot determine, conflicts, or unknowns

- **Key Features:**
  - Execution path tracing (step-by-step flows)
  - Essential files list (5-10 priority files with line ranges)
  - Interactive short questions (not batch questionnaires)
  - Separation of WHAT/HOW (code) vs WHY (docs) vs Intent (user)
  - Comprehensive example output structure
  - Quality checklist before completion

**Why This Prompt?**
Before this PR, we had no systematic way to analyze codebases before feature development. This prompt fills that critical gap by providing structured, evidence-based context that informs all subsequent spec-driven development steps.

### 2. Comprehensive Research Analysis 📚

**New Research Documents:**

- **`docs/research/reverse-engineer-prompts/claude-code-feature-dev-comparison.md`** (18,287 words)
  - Complete analysis of Claude Code's 7-phase feature-dev workflow
  - Agent specifications (code-explorer, code-architect, code-reviewer)
  - Gap analysis comparing our workflow to Claude Code's
  - Implementation roadmap with 3 phases

- **`docs/research/reverse-engineer-prompts/research-synthesis.md`** (8,000+ words)
  - Integration of Claude Code analysis + existing research patterns
  - Actionable recommendations with priority matrix
  - Specific enhancements for each prompt
  - Success metrics and implementation checklist

- **`docs/research/reverse-engineer-prompts/README.md`**
  - Overview of all research documents
  - How research was applied to this PR
  - Key insights and success metrics

**Cataloged Existing Research:**
- `code-analyst.md` - Pattern for extracting WHAT/HOW from code
- `information-analyst.md` - Pattern for extracting WHY from documentation
- `context_bootstrap.md` - Manager orchestration pattern

### 3. Progress Tracking & Roadmap 🗺️

**`docs/PROGRESS.md`** - Complete implementation tracking:
- Phase 1 (This PR): New codebase-context prompt ✅
- Phase 2 (Next PR): Enhance spec, add architecture-options, add review-implementation
- Phase 3 (Future): Examples, tutorials, polish
- Success metrics for each phase
- Key decisions documented

## Changes by File

### New Files
```
prompts/generate-codebase-context.md (877 lines)
docs/research/reverse-engineer-prompts/claude-code-feature-dev-comparison.md
docs/research/reverse-engineer-prompts/research-synthesis.md
docs/research/reverse-engineer-prompts/README.md
docs/PROGRESS.md
```

### Existing Files (Cataloged)
```
docs/research/reverse-engineer-prompts/code-analyst.md
docs/research/reverse-engineer-prompts/information-analyst.md
docs/research/reverse-engineer-prompts/context_bootstrap.md
```

## Research Foundation

This prompt is based on proven patterns from:

1. **Claude Code feature-dev plugin**
   - Production-tested 7-phase workflow
   - Specialized agents (code-explorer, code-architect, code-reviewer)
   - Evidence-based analysis approach
   - Mandatory user checkpoints

2. **Existing research patterns**
   - code-analyst: WHAT/HOW from code analysis
   - information-analyst: WHY from documentation
   - context_bootstrap: Manager orchestration

3. **Best practices**
   - Evidence citations for traceability
   - Confidence levels to distinguish facts from inferences
   - Interactive questioning for better engagement
   - Phased analysis for thoroughness

## Key Principles Implemented

1. **Evidence-Based:** Every finding requires file:line or path#heading citation
2. **Confidence Assessment:** All findings categorized as High/Medium/Low
3. **Separation of Concerns:** Code (WHAT/HOW) vs Docs (WHY) vs User (Intent)
4. **Stay in Lane:** Don't infer WHY from code - flag as gap for user
5. **Interactive Not Batch:** Short focused questions (3-5 max per round)
6. **Flag Gaps Explicitly:** Better to document "Unknown" than guess
7. **Actionable Outputs:** Specific file lists, execution traces, clear recommendations

## Example Output

The prompt generates comprehensive analysis documents like:

```markdown
# Codebase Context: [Project Name]

## 1. Repository Overview
- Type, components, organization with evidence

## 2. Documentation Inventory
- Found docs with timestamps
- Extracted rationale with source citations
- Conflicts and gaps flagged

## 3. System Capabilities (WHAT)
🟢 High Confidence Features (with file:line evidence)
🟡 Medium Confidence (feature toggles, experimental)
🔴 Low Confidence (dead code, unknowns)

## 4. Architecture (HOW)
- Components with responsibilities and evidence
- Communication patterns with file:line refs
- Architectural patterns with examples

## 8. Essential Files to Read
1. src/api/routes/index.ts:12-89 - Main route definitions
2. src/services/UserService.ts:45-234 - Core user logic
...

## 9. Execution Path Examples
User Login Flow:
1. POST /api/auth/login → src/api/routes/auth.ts:23
2. AuthController.login() → src/controllers/AuthController.ts:45
...

## 10. Confidence Summary
High Confidence: [list with evidence]
Medium Confidence: [list needing validation]
Low Confidence: [unknowns]
```

## Testing

- ✅ Prompt YAML frontmatter validated with prompt loader
- ✅ Example output structure verified
- ✅ Evidence citation format tested
- ✅ Confidence assessment categories validated
- ✅ Documentation completeness reviewed

## Breaking Changes

None - this is purely additive.

## Impact on Existing Workflow

### Before This PR
```
1. generate-spec → Create specification
2. generate-task-list-from-spec → Break into tasks
3. manage-tasks → Execute
```

### After This PR
```
1. generate-codebase-context → Analyze codebase (NEW)
   ↓
2. generate-spec → Create specification (can reference context)
3. generate-task-list-from-spec → Break into tasks
4. manage-tasks → Execute
```

The new prompt is **optional but recommended** - it provides valuable context for better spec generation.

## Future Enhancements (Not in This PR)

Documented in `docs/PROGRESS.md` for future PRs:

### Phase 2 (Next PR)
- Enhance `generate-spec` with mandatory clarifying phase
- Create `generate-architecture-options` prompt (NEW)
- Create `review-implementation` prompt (NEW)
- Update workflow documentation
- Create ADR template

### Phase 3 (Future PR)
- Complete example walkthroughs
- Best practices guide
- Troubleshooting documentation

## Success Metrics (Phase 1)

- ✅ Evidence citations in 100% of code findings
- ✅ Confidence levels marked for all findings
- ✅ Documentation audit phase included
- ✅ Interactive questioning approach (3-5 questions per round)
- ✅ Essential files list structure (5-10 files with line ranges)
- ✅ Execution path traces in examples
- ✅ Complete roadmap for Phase 2 and 3

## How to Use

Once merged, users can invoke the prompt:

```python
# Via MCP client
{
  "method": "prompts/get",
  "params": {
    "name": "generate-codebase-context"
  }
}
```

The prompt will guide through a 6-phase interactive analysis, producing an evidence-based codebase context document in `/tasks/[n]-context-[name].md`.

## Review Focus Areas

1. **Prompt Quality:** Does the `generate-codebase-context` prompt provide clear, actionable guidance?
2. **Research Depth:** Is the research analysis comprehensive and well-documented?
3. **Evidence Standards:** Are the citation formats clear and consistent?
4. **Confidence Assessment:** Are the confidence levels well-defined?
5. **Example Output:** Does the example structure make sense?
6. **Future Roadmap:** Is the Phase 2/3 plan clear and actionable?

## Related Issues

This PR addresses findings from internal research showing:
- ❌ Gap: No systematic codebase analysis before feature development
- ❌ Gap: No evidence citation standards
- ❌ Gap: No confidence assessment for findings
- ❌ Gap: Batch questionnaires instead of interactive dialog

All addressed in this PR.

## Checklist

- [x] New prompt created with comprehensive examples
- [x] Prompt YAML frontmatter validated
- [x] Research analysis complete and documented
- [x] Progress tracking established
- [x] Future roadmap defined
- [x] Commit messages follow conventional commits
- [x] All commits are focused and well-documented
- [ ] PR review approved
- [ ] Tests passing (if applicable)

---

**Created by:** Research-driven development based on Claude Code analysis
**Documentation:** See `docs/PROGRESS.md` for complete implementation plan
**Next Steps:** Phase 2 PR will enhance spec generation and add architecture/review prompts
