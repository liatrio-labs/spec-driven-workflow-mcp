# Research: Reverse Engineering & Codebase Analysis Patterns

**Last Updated:** 2025-01-21
**Status:** Research Complete - Implementation Phase 1 Complete

---

## Overview

This directory contains research and analysis conducted to improve our MCP spec-driven development prompts. The research synthesizes patterns from:

1. **Claude Code feature-dev plugin** - Production-tested 7-phase workflow
2. **Existing research files** - code-analyst, information-analyst, context_bootstrap patterns
3. **Best practices** - Evidence-based analysis, confidence assessment, interactive questioning

**Primary Goal:** Enhance prompts with battle-tested patterns for better feature development outcomes.

---

## Research Documents

### 1. Claude Code Feature-Dev Comparison

**File:** [`claude-code-feature-dev-comparison.md`](./claude-code-feature-dev-comparison.md)
**Size:** 18,287 words
**Purpose:** Comprehensive analysis of Claude Code's feature-dev plugin

**Contents:**

- Complete 7-phase workflow breakdown
- Agent specifications (code-explorer, code-architect, code-reviewer)
- Comparison with our current MCP prompts
- Gap analysis with priority ratings (Critical/Important/Minor)
- Implementation roadmap (3 sprints)
- Updated workflow diagrams
- Detailed recommendations

**Key Findings:**

- ❌ Missing mandatory clarifying questions phase
- ❌ No architecture options comparison
- ❌ No quality review before completion
- ✅ Good: Document-based artifacts
- ✅ Good: Explicit sequencing
- ✅ Good: Comprehensive analysis

**Use This For:**

- Understanding Claude Code's proven workflow
- Identifying gaps in our current approach
- Planning future enhancements
- Architecture decision justification

---

### 2. Research Synthesis

**File:** [`research-synthesis.md`](./research-synthesis.md)
**Size:** 8,000+ words
**Purpose:** Actionable integration plan combining all research sources

**Contents:**

- Core philosophy: Code (WHAT/HOW) vs Docs (WHY) vs User (Intent)
- Two-agent specialization pattern (code-analyst + information-analyst)
- Manager orchestration pattern (context_bootstrap)
- Comparison matrix: Our approach vs Research best practices
- Actionable recommendations with priority matrix
- Specific enhancements for each prompt
- Implementation roadmap (3 sprints)
- Success metrics

**Key Recommendations:**

- 🔴 HIGH: Evidence citation standards (file:line, path#heading)
- 🔴 HIGH: Confidence assessment (High/Medium/Low)
- 🔴 HIGH: Mandatory clarifying phase in spec generation
- 🔴 HIGH: Architecture options prompt (new)
- 🔴 HIGH: Implementation review prompt (new)
- 🟡 MEDIUM: Interactive phased questioning
- 🟡 MEDIUM: ADR template creation

**Use This For:**

- Planning specific prompt enhancements
- Understanding priority of improvements
- Implementation guidance with examples
- Success criteria for each enhancement

---

### 3. Code Analyst Pattern

**File:** [`code-analyst.md`](./code-analyst.md)
**Source:** Existing research file (cataloged)
**Purpose:** Specialized agent for discovering WHAT and HOW from code

**Responsibilities:**

- Discover WHAT system does (features, workflows, business rules)
- Discover HOW it's structured (architecture, patterns, communication)
- Identify WHAT technologies are used

**Key Principles:**

- Code is ground truth - report what exists
- Be specific - reference exact file:line
- Distinguish fact from inference
- Flag feature toggles and dormant code
- **Stay in lane** - don't infer WHY

**What NOT to include:**

- ❌ Internal data models (implementation detail)
- ❌ Missing/planned features (belongs in roadmap)
- ❌ Code quality judgments
- ❌ Specific versions (too volatile)
- ❌ Testing infrastructure details

**Applied To:** `generate-codebase-context` Phase 3 (Code Analysis)

---

### 4. Information Analyst Pattern

**File:** [`information-analyst.md`](./information-analyst.md)
**Source:** Existing research file (cataloged)
**Purpose:** Specialized agent for extracting WHY from documentation

**Primary Job:** Extract decision rationale from docs (not discoverable from code)

**Responsibilities:**

- Discover WHY system was built this way
- Extract rationale from documentation
- Find decision context and trade-offs
- Capture historical evolution

**What to Look For:**

- Why was [technology X] chosen?
- Why [pattern Y] over alternatives?
- What constraints drove decisions?
- What trade-offs were considered?

**Key Principles:**

- Direct quotes for "why"
- Source everything (path#heading)
- Attach metadata (timestamps)
- Flag conflicts, don't resolve
- Distinguish explicit vs implicit
- Focus on rationale (unique value)

**Applied To:** `generate-codebase-context` Phase 2 (Documentation Audit)

---

### 5. Context Bootstrap Pattern

**File:** [`context_bootstrap.md`](./context_bootstrap.md)
**Source:** Existing research file (cataloged)
**Purpose:** Manager orchestration pattern for coordinating specialized agents

**Core Philosophy:**
> "Code explains HOW the system currently behaves; the user supplies WHAT it is supposed to achieve and WHY choices were made."

**Six-Phase Workflow:**

1. Analyze repository structure
2. Audit existing documentation
3. Deep code analysis (subprocess: Code Analyst)
4. User collaboration (fill gaps, resolve conflicts)
5. Draft documentation set (PRDs, ADRs, SYSTEM-OVERVIEW)
6. Review with user

**Key Pattern:** "Keep dialog interactive. Ask focused follow-up questions instead of long questionnaires."

**Deliverables:**

- PRDs (Product Requirements)
- ADRs (Architecture Decision Records in MADR format)
- SYSTEM-OVERVIEW.md
- README.md updates

**Applied To:** Overall `generate-codebase-context` structure and phasing

---

## How Research Was Applied

### Phase 1 (Completed) ✅

**Enhanced `generate-codebase-context` Prompt:**

From **code-analyst.md:**

- ✅ File:line evidence citations for all code findings
- ✅ Confidence levels (High/Needs Validation/Unknown)
- ✅ "Stay in your lane" - don't infer WHY from code
- ✅ Flag feature toggles and dormant paths
- ✅ Technology names only (NO versions)
- ✅ Focus on working features, not missing ones

From **information-analyst.md:**

- ✅ Documentation audit phase (scan + timestamp + inventory)
- ✅ Rationale extraction with direct quotes
- ✅ Source references with path#heading format
- ✅ Conflict detection between docs
- ✅ Distinguish explicit vs implicit knowledge

From **context_bootstrap.md:**

- ✅ Repository structure detection (workspace/monorepo/single)
- ✅ User collaboration phase (interactive, not batch)
- ✅ Capture user answers as direct quotes for citation

From **Claude Code feature-dev:**

- ✅ Essential files list with line ranges (5-10 files)
- ✅ Execution path traces (step-by-step flows)
- ✅ Interactive short questions (not batch questionnaires)

---

### Phase 2 (Planned for Next PR)

**Enhancements Planned:**

1. **`generate-spec` Enhancement:**
   - Mandatory clarifying phase (Claude Code Phase 3)
   - Phased interactive questioning (context_bootstrap pattern)
   - WHY questions (information-analyst focus)

2. **`generate-architecture-options` (NEW):**
   - Based on Claude Code code-architect agent
   - Generate 2-3 approaches with trade-offs
   - User must choose before proceeding

3. **`review-implementation` (NEW):**
   - Based on Claude Code code-reviewer agent
   - Multi-focus review (bugs, quality, conventions)
   - Confidence-based filtering (≥80%)

See [`../../PROGRESS.md`](../../PROGRESS.md) for detailed roadmap.

---

## Key Insights

### 1. Separation of Concerns

**Discovery:** Code, docs, and users each provide different information

- **Code → WHAT + HOW:** Features, architecture, patterns (observable facts)
- **Docs → WHY:** Decisions, rationale, trade-offs (recorded intent)
- **User → Goals + Intent:** Purpose, value, strategic fit (current direction)

**Application:** Don't conflate these sources - keep them separate and clearly attributed

---

### 2. Evidence-Based Analysis

**Discovery:** Every claim needs proof

- Code findings: `file.ts:45-67` (line ranges)
- Doc findings: `doc.md#heading` (section anchors)
- User input: `[User confirmed: YYYY-MM-DD]` (dated quotes)

**Application:** Traceability and accountability for all findings

---

### 3. Confidence Assessment

**Discovery:** Distinguish facts from inferences

- High: Strong evidence from working code or explicit docs
- Medium: Inferred from context, feature flags, implied
- Low: Cannot determine, conflicts, unknowns

**Application:** Flag gaps explicitly rather than guessing

---

### 4. Interactive Collaboration

**Discovery:** Short focused conversations > long questionnaires

- Ask 3-5 questions, wait for answers
- Use answers to inform next round of questions
- Capture direct quotes for later citation

**Application:** Better engagement, more thoughtful answers

---

### 5. Mandatory Checkpoints

**Discovery:** Critical decisions need explicit user approval

- ⛔ STOP after clarifying questions (don't proceed without answers)
- ⛔ STOP after architecture options (user must choose)
- ⛔ STOP after implementation (user decides what to fix)

**Application:** User control at key decision points

---

## Success Metrics

### Phase 1 Metrics ✅

- ✅ 100% of code findings have file:line citations
- ✅ 100% of findings categorized by confidence level
- ✅ Documentation audit phase included
- ✅ Interactive questioning approach (3-5 questions per round)
- ✅ Essential files list structure (5-10 files with ranges)
- ✅ Execution path traces included in examples

### Phase 2 Metrics (Target)

- [ ] Clarifying questions are mandatory (cannot proceed without)
- [ ] Architecture options always present 2-3 approaches
- [ ] User explicitly chooses architecture before tasks
- [ ] Review catches common issues before PR
- [ ] All prompts use consistent evidence standards

---

## References

### External Sources

- [Claude Code Repository](https://github.com/anthropics/claude-code)
- [Feature-Dev Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [Feature-Dev README](https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/README.md)
- [Code Explorer Agent](https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/agents/code-explorer.md)
- [Code Architect Agent](https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/agents/code-architect.md)
- [Code Reviewer Agent](https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/agents/code-reviewer.md)
- [MADR Format](https://adr.github.io/madr/)

### Internal Documents

- [Progress Tracking](../../PROGRESS.md)
- [Main README](../../../README.md)

---

## Next Steps

1. **Review Phase 1 PR:** `add-reverse-engineer-codebase-prompt` branch
2. **Plan Phase 2 PR:** After Phase 1 merge
3. **Implement remaining enhancements:** Per roadmap in PROGRESS.md

---

**Research Status:** Complete and applied to Phase 1
**Next Research:** None planned - focus on implementation
**Last Updated:** 2025-01-21
