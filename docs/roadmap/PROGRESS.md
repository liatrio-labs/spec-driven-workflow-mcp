# MCP Spec-Driven Development - Implementation Progress

**Last Updated:** 2025-01-21
**Current Branch:** `add-reverse-engineer-codebase-prompt`
**Status:** Phase 1 Complete - Ready for Review

---

## Overview

This document tracks the implementation of improvements to our MCP spec-driven development prompts based on research from:

1. Claude Code feature-dev plugin analysis
2. Existing research files (code-analyst.md, information-analyst.md, context_bootstrap.md)

**Goal:** Enhance our prompts with evidence-based analysis, confidence assessment, and mandatory clarifying phases inspired by battle-tested patterns.

---

## Current Status: Phase 1 Complete ✅

### Completed Work (This PR)

#### 1. Research & Analysis ✅

**Branch:** `add-reverse-engineer-codebase-prompt`
**Commits:** 4 commits
**Status:** Complete

**Deliverables:**

- ✅ `docs/research/reverse-engineer-prompts/claude-code-feature-dev-comparison.md` (18,287 words)
  - Complete 7-phase workflow analysis
  - Agent specifications (code-explorer, code-architect, code-reviewer)
  - Gap analysis with priority matrix
  - Implementation roadmap

- ✅ `docs/research/reverse-engineer-prompts/research-synthesis.md` (8,000+ words)
  - Integration of all research sources
  - Actionable recommendations with priorities
  - Specific enhancements for each prompt
  - Implementation checklist

- ✅ Cataloged existing research files:
  - `code-analyst.md` - WHAT/HOW from code
  - `information-analyst.md` - WHY from documentation
  - `context_bootstrap.md` - Manager orchestration pattern

#### 2. Renamed Prompt ✅

- ✅ Renamed `reverse-engineer-codebase` → `generate-context`
  - Better reflects purpose: generating context for development
  - Aligns with workflow terminology
  - Shorter, more concise name

#### 3. Enhanced `generate-context` Prompt ✅

**File:** `prompts/generate-context.md`
**Lines:** 877 lines (up from ~500)
**Status:** Complete and ready for use

**Major Enhancements:**

##### Evidence Citation Standards ✅

- **For Code:** `path/to/file.ts:45-67` with line ranges
- **For Docs:** `path/to/doc.md#section-heading` with timestamps
- **For User Input:** `[User confirmed: YYYY-MM-DD]` with direct quotes
- **Example:** "Authentication uses JWT (src/auth/jwt.ts:23-45)"

##### Confidence Assessment ✅

Every finding must be categorized:

- 🟢 **High Confidence:** Strong evidence from working code or explicit docs
- 🟡 **Medium Confidence:** Inferred, behind feature flags, or implied
- 🔴 **Low Confidence:** Cannot determine, conflicts, or unknowns

Explicitly flags items needing user validation.

##### Separation of Concerns ✅

- **WHAT/HOW:** Discovered from code analysis (stay in lane, don't infer WHY)
- **WHY:** Extracted from documentation (rationale, decisions, trade-offs)
- **Intent/Goals:** Provided by user (fills gaps, resolves conflicts)

##### Phased Analysis Process ✅

1. **Repository Structure Analysis** - Auto-detect layout, tech stack
2. **Documentation Audit** - Scan, inventory, extract rationale, flag gaps
3. **Code Analysis (WHAT + HOW)** - Features, workflows, architecture, patterns
4. **Integration Points** - External services, dependencies, events
5. **Gap Identification** - Missing rationale, conflicts, unknowns
6. **User Collaboration** - Short focused questions (3-5 max), not batch
7. **Generate Analysis** - Complete evidence-based document

##### Interactive Questioning ✅

- **OLD:** Long batch questionnaires
- **NEW:** Short rounds (3-5 questions max), wait for answers, ask follow-ups
- Captures user answers as direct quotes for later citation

##### Execution Path Tracing ✅

Step-by-step flow examples:

```text
User Login Flow:
1. POST /api/auth/login → src/api/routes/auth.ts:23
2. AuthController.login() → src/controllers/AuthController.ts:45
3. AuthService.validateCredentials() → src/services/AuthService.ts:67
...
```

##### Essential Files List ✅

- 5-10 priority files with specific line ranges
- **Example:** `src/services/UserService.ts:45-234` - Core user management logic

##### Comprehensive Example Output ✅

- Full 13-section document structure with real examples
- Shows proper evidence citations, confidence emojis, execution traces
- Includes gap documentation, open questions, next steps

##### Quality Checklist ✅

Pre-completion verification:

- [ ] All code findings have file:line citations
- [ ] All doc findings have path#heading references
- [ ] User answers captured as quotes with dates
- [ ] Confidence levels marked
- [ ] Essential files list complete (5-10 files)
- [ ] At least 2 execution path traces
- [ ] Gaps/unknowns explicitly documented

##### Key Principles Embedded ✅

1. Evidence-based (every claim needs proof)
2. Confidence levels (distinguish fact from inference)
3. Stay in lane (don't guess WHY from code)
4. Flag gaps explicitly (better "Unknown" than guessing)
5. Interactive not batch (short questions)
6. Actionable outputs (specific files, traces, recommendations)

---

## What This PR Includes

### Files Added/Modified

```text
✅ prompts/generate-context.md (enhanced)
✅ docs/research/reverse-engineer-prompts/claude-code-feature-dev-comparison.md (new)
✅ docs/research/reverse-engineer-prompts/research-synthesis.md (new)
✅ docs/research/reverse-engineer-prompts/code-analyst.md (cataloged)
✅ docs/research/reverse-engineer-prompts/information-analyst.md (cataloged)
✅ docs/research/reverse-engineer-prompts/context_bootstrap.md (cataloged)
✅ docs/PROGRESS.md (new - this file)
```

### Commits

1. `feat: add reverse-engineer-codebase prompt for contextual analysis`
2. `refactor: rename reverse-engineer-codebase to generate-context`
3. `docs: add comprehensive research analysis for prompt improvements`
4. `feat: enhance generate-context with evidence citations and confidence levels`

### Ready for Review

- ✅ All code changes committed
- ✅ Research documented
- ✅ Enhanced prompt tested with prompt loader
- ✅ Progress tracked
- ⏳ Awaiting PR review

---

## Phase 2: Future Improvements (Next PR)

The following improvements are **documented and ready to implement** but will be handled in a separate branch/PR to keep this PR focused and reviewable.

### Priority 1: Critical Workflow Enhancements

#### A. Enhance `generate-spec` with Mandatory Clarifying Phase

**File:** `prompts/generate-spec.md`
**Status:** Planned for next PR
**Estimated Effort:** Medium (2-3 hours)

**Changes Needed:**

1. **Add Phase 2A: Context Review (NEW)**
   - Prerequisite: Must have run `generate-context`
   - Read analysis document
   - Review essential files identified
   - Understand existing patterns

2. **Add Phase 3: Clarifying Questions ⭐ CRITICAL (ENHANCED)**
   - **Make it MANDATORY STOP POINT**
   - Add WHY questions:
     - What problem does this solve?
     - Why build this now? (strategic fit)
     - What's the business value?
     - How will we measure success?
   - Phase questions into rounds:
     - Round 1: Core requirements (3-5 questions)
     - **⛔ STOP - Wait for answers**
     - Round 2: Context & constraints (based on Round 1 answers)
     - **⛔ STOP - Wait for answers**
     - Round 3: Refinement (fill remaining gaps)
     - **⛔ STOP - Wait for final confirmation**
   - Capture all answers as direct quotes with dates
   - Reference codebase context document explicitly

3. **Update Spec Structure**
   - Add "Context & Rationale" section (WHY)
   - Include evidence citations when referencing existing code
   - Reference decisions from codebase context analysis

**Impact:** Prevents building wrong features by ensuring all requirements are clear before design begins.

**Research Source:** Claude Code Phase 3 + information-analyst.md patterns

---

#### B. Create `generate-architecture-options` Prompt (NEW)

**File:** `prompts/generate-architecture-options.md`
**Status:** Planned for next PR
**Estimated Effort:** High (4-5 hours)

**Purpose:** Generate 2-3 architectural approaches with trade-off analysis before task generation

**Process:**

1. **Prerequisites Check:**
   - Spec document exists
   - Codebase context analysis exists
   - User has approved spec

2. **Review Context:**
   - Read spec document
   - Read codebase context analysis
   - Review essential files identified

3. **Generate 3 Approaches:**
   - **Minimal Changes:** Smallest change, maximum code reuse, fastest to ship
   - **Clean Architecture:** Best maintainability, elegant abstractions, most extensible
   - **Pragmatic Balance:** Balanced trade-off between speed and quality

4. **For Each Approach:**
   - **Patterns & Conventions Found:** With file:line references
   - **Architecture Decision:** Clear choice with rationale
   - **Component Design:** Files, responsibilities, dependencies, interfaces
   - **Implementation Map:** Specific files to create/modify with details
   - **Data Flow:** Entry → transformations → output
   - **Build Sequence:** Phased checklist
   - **Trade-offs:** Pros and cons explicitly stated
   - **Critical Details:** Error handling, state, testing, performance, security

5. **Present to User:**
   - Brief summary of each approach
   - Trade-offs comparison table
   - **AI recommendation with reasoning** (based on codebase context)
   - Concrete implementation differences

6. **⛔ STOP - User must choose approach**

7. **Save Choice:**
   - Save chosen approach to `/tasks/architecture-[spec-number].md`
   - Document rationale for choice (for future ADR)

**Output Example:**

```markdown
# Architecture Options: User Profile Editing (Spec 0001)

## Approach 1: Minimal Changes
**Summary:** Extend existing UserService, add new endpoint to existing routes
**Pros:**
- Fast (2-3 days)
- Low risk (minimal code changes)
- Uses familiar patterns
**Cons:**
- Couples new feature to existing code
- Harder to test in isolation
- May not scale if requirements expand

## Approach 2: Clean Architecture
**Summary:** New ProfileService with dedicated interface, separate routes
**Pros:**
- Clean separation of concerns
- Easy to test and extend
- Sets good pattern for future features
**Cons:**
- More files (slower initial development)
- Requires refactoring some existing code
- Team needs to learn new pattern

## Approach 3: Pragmatic Balance (RECOMMENDED)
**Summary:** New ProfileService integrated into existing structure
**Pros:**
- Good boundaries without excessive refactoring
- Testable and maintainable
- Fits existing architecture patterns
**Cons:**
- Some coupling remains to UserService

**Recommendation:** Approach 3 - Based on codebase context analysis showing layered architecture with service boundaries, this approach provides clean separation while avoiding extensive refactoring. Aligns with existing patterns in `src/services/PaymentService.ts:34-178`.

**Which approach do you prefer?**
```

**Impact:** Enables better architectural decisions by presenting options with explicit trade-offs rather than single solution.

**Research Source:** Claude Code code-architect agent + Phase 4

---

#### C. Create `review-implementation` Prompt (NEW)

**File:** `prompts/review-implementation.md`
**Status:** Planned for next PR
**Estimated Effort:** High (4-5 hours)

**Purpose:** Quality review before considering feature complete

**Process:**

1. **Prerequisites:**
   - All implementation tasks marked complete in task list
   - Code has been committed (but not pushed/PR'd yet)

2. **Review Scope:**
   - All modified files
   - All created files
   - Related tests

3. **Multi-Focus Review:**
   - **Focus 1: Bugs & Correctness**
     - Logic errors
     - Edge case handling
     - Null/undefined handling
     - Error propagation
     - Race conditions

   - **Focus 2: Code Quality**
     - DRY violations (duplicate code)
     - Complexity (can it be simpler?)
     - Readability (clear intent?)
     - Maintainability (easy to change?)

   - **Focus 3: Project Conventions**
     - CLAUDE.md guidelines compliance
     - Naming conventions
     - File organization patterns
     - Testing patterns
     - Code style (linter rules)

4. **Confidence-Based Filtering:**
   - Only report issues with ≥80% confidence
   - Avoid nitpicks and opinions
   - Focus on objective problems

5. **Categorize Findings:**
   - **Critical (Must Fix):** Bugs, security issues, breaking changes
   - **Important (Should Fix):** Code quality, maintainability concerns
   - **Nice-to-Have (Optional):** Optimizations, minor improvements

6. **Present to User:**

   ```markdown
   ## Review Findings

   ### Critical Issues (Must Fix) 🔴
   1. **Missing error handling in OAuth callback**
      - File: src/auth/oauth.ts:67
      - Issue: Network failures not caught, will crash server
      - Fix: Add try-catch with proper error response
      - Confidence: 95%

   ### Important Issues (Should Fix) 🟡
   1. **Memory leak: OAuth state not cleaned up**
      - File: src/auth/oauth.ts:89
      - Issue: State map grows unbounded
      - Fix: Add TTL or cleanup job
      - Confidence: 85%

   ### Optional Improvements 🟢
   1. **Could simplify token refresh logic**
      - File: src/auth/oauth.ts:120
      - Suggestion: Extract to separate function
      - Confidence: 80%
   ```

7. **⛔ STOP - Ask user what to do:**
   - Fix all issues now?
   - Fix only critical issues?
   - Fix later (document as tech debt)?
   - Proceed as-is?

8. **Take Action:**
   - Apply fixes based on user decision
   - Update task list to mark review complete
   - Document any deferred issues

**Impact:** Catches quality issues and bugs before they reach production/PR.

**Research Source:** Claude Code code-reviewer agent + Phase 6

---

### Priority 2: Documentation & Workflow

#### D. Update Workflow Documentation

**File:** `docs/WORKFLOW.md` (new)
**Status:** Planned for next PR
**Estimated Effort:** Low (1-2 hours)

**Content:**

```markdown
# Spec-Driven Development Workflow

## Complete Flow

1. **Analyze Codebase** - `generate-context`
   - Output: `/docs/00[n]-SYSTEM.md`
   - Evidence-based analysis with citations
   - Confidence levels for all findings
   - Essential files list + execution traces

2. **Create Specification** - `generate-spec`
   - Prerequisites: Context analysis complete
   - ⛔ STOP: Answer clarifying questions (phased)
   - Output: `/tasks/[n]-spec-[feature].md`
   - Includes WHY and evidence citations

3. **Design Architecture** - `generate-architecture-options`
   - Prerequisites: Spec approved
   - Review 3 approaches with trade-offs
   - ⛔ STOP: Choose architectural approach
   - Output: `/tasks/architecture-[n].md`

4. **Generate Tasks** - `generate-task-list-from-spec`
   - Prerequisites: Architecture chosen
   - References chosen approach
   - ⛔ STOP: Approve parent tasks before sub-tasks
   - Output: `/tasks/tasks-[n]-spec-[feature].md`

5. **Execute Implementation** - `manage-tasks`
   - Follow task list sequentially
   - Run tests after each parent task
   - Validate demo criteria
   - Commit with conventional format

6. **Review Quality** - `review-implementation`
   - Prerequisites: All tasks complete
   - Multi-focus review (bugs, quality, conventions)
   - ⛔ STOP: Decide what issues to fix
   - Fix issues as directed

7. **Complete**
   - Create PR
   - Deploy
   - Document decisions (ADRs if needed)

## Workflow Diagram

[Include visual diagram]

## Best Practices

1. Always run codebase-context before starting new features
2. Answer all clarifying questions thoughtfully
3. Review architecture options carefully - impacts long-term maintainability
4. Don't skip quality review - catches issues early
5. Reference context analysis when making decisions

## Example Session

[Include complete example walkthrough]
```

---

#### E. Create ADR Template

**File:** `prompts/templates/adr-template.md` (new)
**Status:** Planned for next PR
**Estimated Effort:** Low (30 minutes)

**Content:**

- MADR format template
- Sections for context, decision drivers, options, outcome, consequences
- Examples of good vs bad ADRs
- Instructions for when to create ADRs

**Usage:** Referenced by `generate-architecture-options` for documenting chosen approach

---

#### F. Create Examples & Tutorials

**Files:** `docs/examples/` (new directory)
**Status:** Planned for future PR
**Estimated Effort:** Medium (3-4 hours)

**Content:**

- Complete example: Full workflow walkthrough
- Before/after examples showing improvements
- Common patterns and solutions
- Troubleshooting guide

---

## Implementation Roadmap

### This PR (Phase 1) ✅ COMPLETE

**Branch:** `add-reverse-engineer-codebase-prompt`
**Timeline:** Complete
**Deliverables:**

- ✅ Research analysis and synthesis
- ✅ Enhanced `generate-context` prompt
- ✅ Progress documentation

**Merge Criteria:**

- [x] All commits clean and documented
- [x] Enhanced prompt tested
- [x] Research findings documented
- [ ] PR review approved
- [ ] Tests passing (if applicable)

---

### Next PR (Phase 2) - Critical Workflow Enhancements

**Branch:** `enhance-spec-and-add-architecture-review` (future)
**Timeline:** 2-3 days work
**Estimated Effort:** High (10-12 hours)

**Deliverables:**

- [ ] Enhanced `generate-spec` with mandatory clarifying phase
- [ ] New `generate-architecture-options` prompt
- [ ] New `review-implementation` prompt
- [ ] Updated workflow documentation
- [ ] ADR template

**Priority:** HIGH - These are critical gaps identified in research
**Blocking:** None (Phase 1 complete)

**Acceptance Criteria:**

- [ ] All 3 prompts work independently
- [ ] Workflow flows smoothly from context → spec → architecture → tasks → review
- [ ] Evidence citations and confidence levels used throughout
- [ ] User checkpoints (⛔ STOP) enforced
- [ ] Documentation complete with examples

---

### Future PR (Phase 3) - Polish & Examples

**Branch:** TBD
**Timeline:** 1-2 days work
**Estimated Effort:** Medium (4-6 hours)

**Deliverables:**

- [ ] Complete example walkthrough
- [ ] Best practices guide
- [ ] Troubleshooting documentation
- [ ] Before/after comparisons

**Priority:** MEDIUM - Improves usability but not blocking
**Blocking:** Phase 2 complete

---

## Success Metrics

### Phase 1 (This PR) ✅

- ✅ Evidence citations present in 100% of code findings
- ✅ Confidence levels marked for all findings
- ✅ Documentation audit phase included
- ✅ Interactive questioning approach documented
- ✅ Essential files list structure defined
- ✅ Execution path traces included in examples

### Phase 2 (Next PR)

- [ ] Clarifying questions are mandatory (cannot proceed without answers)
- [ ] Architecture options always present 2-3 approaches
- [ ] User must explicitly choose architecture before tasks generated
- [ ] Review catches common issues before PR
- [ ] All prompts use evidence citation standards
- [ ] Complete workflow documented with examples

### Phase 3 (Future PR)

- [ ] Examples cover common use cases
- [ ] New users can follow tutorial successfully
- [ ] Troubleshooting guide addresses common issues

---

## Key Decisions Made

### Decision 1: Evidence Citations

**Decision:** Require file:line for code, path#heading for docs, dated quotes for users
**Rationale:** Provides traceability and accountability for all findings
**Source:** code-analyst.md + information-analyst.md patterns

### Decision 2: Confidence Levels

**Decision:** Categorize all findings as High/Medium/Low confidence
**Rationale:** Distinguishes facts from inferences, flags items needing validation
**Source:** Research synthesis recommendations

### Decision 3: Phased Implementation

**Decision:** Split improvements across multiple PRs (Phase 1 = context, Phase 2 = spec+arch+review)
**Rationale:** Keeps PRs focused and reviewable, allows incremental adoption
**Source:** Team decision for maintainability

### Decision 4: Interactive Questioning

**Decision:** Replace batch questionnaires with short focused rounds
**Rationale:** Better user engagement, more thoughtful answers
**Source:** context_bootstrap.md + Claude Code Phase 3 pattern

### Decision 5: Mandatory Clarifying Phase

**Decision:** Make clarifying questions a STOP point in spec generation
**Rationale:** Most feature failures from misunderstood requirements - prevent this
**Source:** Claude Code research showing this as critical phase

---

## References

### Research Documents

- [Claude Code Feature-Dev Comparison](./research/reverse-engineer-prompts/claude-code-feature-dev-comparison.md)
- [Research Synthesis](./research/reverse-engineer-prompts/research-synthesis.md)
- [Code Analyst Pattern](./research/reverse-engineer-prompts/code-analyst.md)
- [Information Analyst Pattern](./research/reverse-engineer-prompts/information-analyst.md)
- [Context Bootstrap Pattern](./research/reverse-engineer-prompts/context_bootstrap.md)

### External Links

- [Claude Code Repository](https://github.com/anthropics/claude-code)
- [Feature-Dev Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev)
- [MADR Format](https://adr.github.io/madr/)

---

## Contact & Questions

For questions about this implementation:

- Review research documents in `docs/research/reverse-engineer-prompts/`
- Check progress updates in this document
- Refer to commit messages for detailed change rationale

---

**Document Status:** Living document - updated with each phase
**Next Update:** After Phase 2 PR merge
