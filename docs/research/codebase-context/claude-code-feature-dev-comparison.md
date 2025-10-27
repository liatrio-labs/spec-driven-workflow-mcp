# Claude Code Feature-Dev Plugin Analysis & Comparison

**Date:** 2025-01-21
**Purpose:** Analyze the Claude Code feature-dev plugin workflow and compare with our MCP spec-driven development prompts to identify improvement opportunities

---

## Executive Summary

The Claude Code feature-dev plugin implements a battle-tested 7-phase workflow that emphasizes:

1. **Explicit clarifying questions** before design (prevents building wrong things)
2. **Multi-approach architecture** with trade-off analysis (enables better decisions)
3. **Agent-based parallel exploration** for efficiency
4. **Quality review gates** before completion (catches issues early)

**Key Finding:** Our current workflow is missing critical phases for clarification, architecture comparison, and quality review that the Claude Code workflow proves essential.

---

## Claude Code Feature-Dev Workflow (7 Phases)

### Phase 1: Discovery

**Goal:** Understand what needs to be built

**Process:**

- Create todo list with all phases
- If feature unclear, ask user for problem, requirements, constraints
- Summarize understanding and confirm with user

**Key Pattern:** Early validation of understanding

---

### Phase 2: Codebase Exploration

**Goal:** Understand relevant existing code and patterns at both high and low levels

**Process:**

1. Launch 2-3 `code-explorer` agents in parallel
2. Each agent targets different aspect (similar features, architecture, UX patterns)
3. **Critical:** Each agent returns **list of 5-10 key files to read**
4. After agents return, **read all identified files** to build deep understanding
5. Present comprehensive summary

**Example Agent Prompts:**

- "Find features similar to [feature] and trace through implementation comprehensively"
- "Map the architecture and abstractions for [feature area]"
- "Analyze current implementation of [existing feature/area]"

**Key Pattern:** Agent-based parallel discovery + explicit file reading

### Agent: code-explorer

- **Tools:** Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch
- **Model:** Sonnet
- **Focus:** Trace execution paths from entry points to data storage
- **Output:** Entry points, step-by-step flow, architecture insights, key files list

---

### Phase 3: Clarifying Questions ⭐ CRITICAL

**Goal:** Fill in gaps and resolve ALL ambiguities before designing

**Process:**

1. Review codebase findings and original feature request
2. Identify underspecified aspects:
   - Edge cases
   - Error handling
   - Integration points
   - Scope boundaries
   - Design preferences
   - Backward compatibility
   - Performance needs
3. **Present ALL questions in organized list**
4. **WAIT FOR ANSWERS** before proceeding to architecture design

**Key Pattern:** Explicit stop point - NO assumptions, NO "whatever you think is best" without confirmation

**Why Critical:** This prevents building the wrong thing. Most feature failures come from misunderstood requirements.

---

### Phase 4: Architecture Design

**Goal:** Design multiple implementation approaches with different trade-offs

**Process:**

1. Launch 2-3 `code-architect` agents in parallel with different focuses:
   - **Minimal changes:** Smallest change, maximum reuse
   - **Clean architecture:** Maintainability, elegant abstractions
   - **Pragmatic balance:** Speed + quality
2. Review all approaches and form opinion on which fits best
3. Present to user:
   - Brief summary of each approach
   - Trade-offs comparison
   - **Recommendation with reasoning**
   - Concrete implementation differences
4. **Ask user which approach they prefer**

**Key Pattern:** Options with trade-offs + recommendation, not just one solution

### Agent: code-architect

- **Tools:** Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch
- **Model:** Sonnet
- **Focus:** Design complete architecture with confident decisions
- **Output:**
  - Patterns & conventions found (with file:line refs)
  - Architecture decision with rationale
  - Component design (files, responsibilities, dependencies)
  - Implementation map (specific files to create/modify)
  - Data flow diagrams
  - Build sequence (phased checklist)
  - Critical details (error handling, state, testing, performance, security)

---

### Phase 5: Implementation

**Goal:** Build the feature

**Process:**

1. **DO NOT START WITHOUT USER APPROVAL**
2. Wait for explicit user approval
3. Read all relevant files identified in previous phases
4. Implement following chosen architecture
5. Follow codebase conventions strictly
6. Write clean, well-documented code
7. Update todos as you progress

**Key Pattern:** Explicit approval gate before code changes

---

### Phase 6: Quality Review

**Goal:** Ensure code is simple, DRY, elegant, and functionally correct

**Process:**

1. Launch 3 `code-reviewer` agents in parallel with different focuses:
   - **Simplicity/DRY/Elegance:** Code quality and maintainability
   - **Bugs/Functional Correctness:** Logic errors and bugs
   - **Project Conventions/Abstractions:** CLAUDE.md compliance, patterns
2. Consolidate findings and identify highest severity issues
3. **Present findings and ask what user wants to do:**
   - Fix now
   - Fix later
   - Proceed as-is
4. Address issues based on user decision

**Key Pattern:** Parallel multi-focus review + user decision on fixes

### Agent: code-reviewer

- **Tools:** Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch
- **Model:** Sonnet
- **Focus:** Find bugs, quality issues, guideline violations
- **Filtering:** Only report high-confidence issues (≥80% confidence)
- **Output:**
  - Critical issues (confidence 75-100)
  - Important issues (confidence 50-74)
  - Specific fixes with file:line references
  - Project guideline references

---

### Phase 7: Summary

**Goal:** Document what was accomplished

**Process:**

1. Mark all todos complete
2. Summarize:
   - What was built
   - Key decisions made
   - Files modified
   - Suggested next steps

**Key Pattern:** Documentation of decisions and outcomes

---

## Our Current MCP Workflow

### Prompt 1: generate-context (NEW)

**Goal:** Analyze codebase architecture, patterns, and conventions

**Process:**

- Conversational, iterative analysis
- Ask user about repo structure, service architecture, priority areas
- Automated discovery: tech stack, config files, directory structure
- Deep dive into priority areas (database, API, auth, frontend, testing, etc.)
- Generate comprehensive analysis document in `/tasks/[n]-analysis-[name].md`

**Output Structure:**

- Overview (project type, languages, frameworks)
- Architecture (system design, directory structure)
- Tech stack deep dive
- Data layer (database, ORM, migrations)
- API layer (routes, validation, middleware)
- Auth & authorization
- Frontend architecture (if applicable)
- Testing strategy
- Build & deployment
- Code patterns & conventions
- Integration points
- Git workflow
- Key files reference
- Recommendations for new features
- Open questions

**Strengths:**

- Very comprehensive documentation
- Persistent artifact (`.md` file)
- Covers all architectural aspects

**Gaps vs Claude Code:**

- No explicit "return 5-10 key files to read" instruction
- Less focused on execution path tracing
- More documentation-oriented than action-oriented

---

### Prompt 2: generate-spec

**Goal:** Create detailed specification for a feature

**Process:**

1. Receive initial prompt
2. Ask clarifying questions (examples provided)
3. Generate spec using structured template
4. Save as `/tasks/[n]-spec-[feature-name].md`
5. Ask if user is satisfied
6. Complete when user approves

**Spec Structure:**

- Introduction/Overview
- Goals
- User Stories
- Demoable Units of Work
- Functional Requirements
- Non-Goals
- Design Considerations
- Technical Considerations
- Success Metrics
- Open Questions

**Clarifying Questions (Examples):**

- Problem/Goal
- Target User
- Core Functionality
- User Stories
- Acceptance Criteria
- Scope/Boundaries
- Data Requirements
- Design/UI
- Edge Cases
- Unit of Work
- Demoability

**Strengths:**

- Comprehensive spec structure
- Demoable units focus
- Persistent documentation

**Gaps vs Claude Code:**

- Clarifying questions are examples, not a mandatory phase
- No explicit "WAIT FOR ANSWERS" checkpoint
- Happens before codebase exploration (should be after)
- No architecture options phase follows

---

### Prompt 3: generate-task-list-from-spec

**Goal:** Create detailed task list from spec

**Process:**

1. Receive spec reference
2. Analyze spec
3. Define demoable units of work
4. Assess current state (codebase review)
5. **Phase 1:** Generate parent tasks (high-level)
6. Present tasks to user
7. **Wait for "Generate sub tasks" confirmation**
8. **Phase 2:** Generate sub-tasks for each parent
9. Identify relevant files
10. Save as `/tasks/tasks-[spec-file-name].md`

**Output Structure:**

- Relevant Files (with descriptions)
- Notes (test conventions, commands)
- Tasks (parent + sub-tasks with demo criteria and proof artifacts)

**Strengths:**

- Two-phase generation (parent tasks → sub-tasks)
- Explicit user checkpoint
- Demo criteria and proof artifacts for each parent task
- Codebase-aware task generation

**Gaps vs Claude Code:**

- No architecture options to choose from
- Codebase assessment is brief, not agent-based
- No "key files to read" from prior analysis

---

### Prompt 4: manage-tasks

**Goal:** Execute and track task progress

**Process:**

- Three task states: `[ ]` not started, `[~]` in-progress, `[x]` completed
- One sub-task at a time
- Mark in-progress immediately
- Completion protocol:
  1. Mark sub-task complete
  2. When all sub-tasks done: run tests
  3. If tests pass: stage changes
  4. Validate against demo criteria
  5. Clean up temporary code
  6. Commit with conventional commit format
  7. Mark parent task complete
- Update "Relevant Files" section as work progresses

**Strengths:**

- Clear state management
- Test-driven completion
- Demo criteria validation
- Git integration with conventional commits

**Gaps vs Claude Code:**

- No quality review phase before completion
- No parallel reviewer agents
- No user checkpoint after implementation

---

## Gap Analysis: What We're Missing

### 🔴 CRITICAL GAPS

| Gap | Claude Code | Our Current | Impact | Priority |
|-----|-------------|-------------|--------|----------|
| **Mandatory Clarifying Questions Phase** | Dedicated Phase 3 with explicit WAIT | Questions are examples in spec prompt | Build wrong features | **HIGH** |
| **Multi-Approach Architecture** | 2-3 parallel architect agents with trade-offs | Single spec, no options | Miss better designs | **HIGH** |
| **Quality Review Before Merge** | Phase 6 with parallel reviewers | No formal review step | Ship bugs and tech debt | **HIGH** |

### 🟡 IMPORTANT GAPS

| Gap | Claude Code | Our Current | Impact | Priority |
|-----|-------------|-------------|--------|----------|
| **Agent-Based File Discovery** | Agents return "5-10 key files to read" | Manual AI discovery | Less efficient exploration | **MEDIUM** |
| **Explicit Approval Gates** | WAIT commands at phases 3, 4, 5 | Implicit in some prompts | Less user control | **MEDIUM** |
| **Execution Path Tracing** | Code-explorer focuses on flow | Context prompt focuses on structure | Miss runtime behavior insights | **MEDIUM** |

### 🟢 MINOR GAPS

| Gap | Claude Code | Our Current | Impact | Priority |
|-----|-------------|-------------|--------|----------|
| **Parallel Agent Execution** | 2-3 agents at once | Sequential single prompt | Slower execution | **LOW** |
| **Summary Phase** | Dedicated Phase 7 | Implicit in task completion | Less visibility on outcomes | **LOW** |

---

## Workflow Comparison

### Claude Code Flow

```text
1. Discovery           →  Understand feature request
                          ↓
2. Codebase           →  Launch 2-3 code-explorer agents
   Exploration            Read identified files
                          ↓
3. Clarifying         →  Ask ALL questions
   Questions              ↓
                       [⛔ WAIT FOR ANSWERS]
                          ↓
4. Architecture       →  Launch 2-3 code-architect agents
   Design                 Present options with trade-offs
                          ↓
                       [⛔ WAIT FOR USER CHOICE]
                          ↓
5. Implementation     →  [⛔ WAIT FOR APPROVAL]
                          Build feature
                          ↓
6. Quality Review     →  Launch 3 code-reviewer agents
                          Present findings
                          ↓
                       [⛔ WAIT FOR FIX DECISION]
                          ↓
7. Summary            →  Document outcomes
```

### Our Current Flow

```text
1. generate-          →  Comprehensive codebase analysis
   codebase-context      Generate analysis document
                          ↓
2. generate-spec      →  Ask clarifying questions (examples)
                          Generate spec document
                          ↓
                       [✓ User approval of spec]
                          ↓
3. generate-task-     →  Generate parent tasks
   list-from-spec        ↓
                       [✓ Wait for "Generate sub tasks"]
                          ↓
                          Generate sub-tasks
                          ↓
4. manage-tasks       →  Execute implementation
                          Run tests
                          Commit with conventional format
```

**Key Differences:**

- ❌ We have no dedicated clarifying phase with mandatory stop
- ❌ We have no architecture options comparison
- ❌ We have no quality review phase
- ✅ We generate persistent documentation artifacts
- ✅ We have explicit demoable units and proof artifacts

---

## Recommended Improvements

### 🎯 Phase 1: Critical Enhancements (Do First)

#### 1. Enhance `generate-spec` with Mandatory Clarifying Phase

**Current State:**

```markdown
## Clarifying Questions (Examples)
The AI should adapt its questions based on the prompt...
```

**Recommended Change:**

```text
## Phase 1: Initial Understanding
- Receive feature request
- Clarify if unclear

## Phase 2: Codebase Context Review
- **PREREQUISITE:** Must have run generate-context first
- Read the analysis document
- Review key files identified in analysis
- Understand existing patterns

## Phase 3: Clarifying Questions ⭐ CRITICAL - DO NOT SKIP
**MANDATORY STOP POINT**

Based on the feature request and codebase context, identify ALL:
- Edge cases and error scenarios
- Integration points and dependencies
- Scope boundaries (what's in/out)
- Design and UX preferences
- Backward compatibility needs
- Performance requirements
- Security considerations

**Present ALL questions in an organized list**
**WAIT FOR USER ANSWERS BEFORE PROCEEDING**

If user says "whatever you think is best", provide recommendation and get explicit confirmation.

## Phase 4: Generate Specification
- Using answered questions, generate spec
- ...
```

**Rationale:** This makes clarifying questions a mandatory checkpoint, preventing requirement misunderstandings.

---

#### 2. Create NEW Prompt: `generate-architecture-options`

**Location:** `prompts/generate-architecture-options.md`

**Purpose:** Generate and compare multiple architectural approaches before task generation

**Process:**

1. Review spec and codebase context
2. Generate 2-3 approaches:
   - **Minimal Changes:** Smallest change, maximum code reuse, fastest to ship
   - **Clean Architecture:** Best maintainability, elegant abstractions, extensible
   - **Pragmatic Balance:** Balanced trade-off between speed and quality
3. For each approach, document:
   - Key architectural decisions
   - Components and responsibilities
   - Files to create/modify
   - Integration approach
   - Trade-offs (pros/cons)
4. Provide recommendation with reasoning
5. **WAIT FOR USER CHOICE**
6. Save chosen approach to `/tasks/architecture-[spec-number].md`

**Integration Point:** Run after `generate-spec`, before `generate-task-list-from-spec`

**Rationale:** Enables better architectural decisions by comparing trade-offs explicitly.

---

#### 3. Create NEW Prompt: `review-implementation`

**Location:** `prompts/review-implementation.md`

**Purpose:** Quality review of implemented code before considering feature complete

**Process:**

1. **Prerequisite:** Implementation tasks are complete
2. Review all modified/created files
3. Check for:
   - **Bugs and Logic Errors:** Functional correctness, edge cases
   - **Code Quality:** DRY violations, complexity, readability
   - **Project Conventions:** CLAUDE.md compliance, naming, structure
   - **Testing:** Test coverage, test quality
   - **Performance:** Obvious inefficiencies
   - **Security:** Common vulnerabilities
4. Categorize findings:
   - Critical (must fix)
   - Important (should fix)
   - Nice-to-have (optional)
5. **Present findings to user and ask:**
   - Fix all issues now?
   - Fix only critical issues?
   - Fix later (document as tech debt)?
   - Proceed as-is?
6. Take action based on user decision

**Integration Point:** Run after `manage-tasks` completes all tasks, before final commit/PR

**Rationale:** Catches quality issues and bugs before they reach production.

---

### 🎯 Phase 2: Important Enhancements

#### 4. Enhance `generate-context` to be More Actionable

**Current State:** Comprehensive but documentation-focused

**Recommended Changes:**

Add to the **Output** section:

```markdown
## Essential Files to Read

After completing this analysis, provide a prioritized list of 5-10 essential files that anyone working on features in this codebase should read:

1. **[path/to/file.ts:45-120]** - Core [domain concept] implementation
2. **[path/to/file.py:10-50]** - Authentication flow entry point
...

**Rationale for each file:** Briefly explain why this file is essential.
```

Add to **Phase 2: Deep Architectural Analysis**:

```markdown
### Execution Path Tracing

For key user flows, trace the execution path:
- Entry point (API endpoint, UI component, CLI command)
- Request flow through layers
- Data transformations at each step
- Side effects and state changes
- Output/response generation

**Example Flow:**

```text
User Login:

1. POST /api/auth/login → routes/auth.ts:23
2. AuthController.login() → controllers/AuthController.ts:45
3. AuthService.validateCredentials() → services/AuthService.ts:67
4. UserRepository.findByEmail() → repositories/UserRepository.ts:34
5. Database query → models/User.ts:89
6. JWT token generation → utils/jwt.ts:12
7. Response with token → controllers/AuthController.ts:52
```

**Rationale:** Makes codebase context more action-oriented, similar to code-explorer agent.

---

#### 5. Update `generate-task-list-from-spec` to Reference Architecture

**Current State:**

```text
## Process
...
4. Assess current state (codebase review)
5. Generate parent tasks
...
```

**Recommended Change:**

```text
## Process
...
4. **Review Architecture Decision:**
   - **PREREQUISITE:** Must have chosen architecture approach from `generate-architecture-options`
   - Read the architecture document: `/tasks/architecture-[spec-number].md`
   - Understand chosen approach and rationale
5. **Review Codebase Context:**
   - Read key files identified in codebase analysis
   - Understand existing patterns
6. Generate parent tasks following chosen architecture
...
```

**Rationale:** Ensures task generation aligns with chosen architectural approach.

---

### 🎯 Phase 3: Process Improvements

#### 6. Add Explicit Checkpoints to All Prompts

Add checkpoint markers:

```text
## Checkpoints

This prompt has the following user interaction checkpoints:

- ⛔ **STOP 1:** After clarifying questions - WAIT FOR ANSWERS
- ⛔ **STOP 2:** After presenting spec draft - WAIT FOR APPROVAL
- ✅ **PROCEED:** When user approves, save spec and complete
```

**Rationale:** Makes user control points explicit and consistent.

---

#### 7. Document Complete Workflow

Create `docs/workflow.md`:

```markdown
# Spec-Driven Development Workflow

## Complete Flow

1. **Analyze Codebase** - Run `generate-context`
   - Output: Analysis document + key files list

2. **Create Specification** - Run `generate-spec`
   - ⛔ STOP: Answer clarifying questions
   - Output: Spec document

3. **Design Architecture** - Run `generate-architecture-options`
   - ⛔ STOP: Choose architectural approach
   - Output: Architecture document

4. **Generate Tasks** - Run `generate-task-list-from-spec`
   - ⛔ STOP: Approve parent tasks before sub-tasks
   - Output: Task list document

5. **Execute Implementation** - Run `manage-tasks`
   - Output: Code changes, commits

6. **Review Quality** - Run `review-implementation`
   - ⛔ STOP: Decide what issues to fix
   - Output: Review findings, fixes

7. **Complete** - Create PR, deploy, document
```

---

## Updated Workflow Diagram

```text
┌─────────────────────────────────────────────────────────────┐
│                    SPEC-DRIVEN DEVELOPMENT                  │
└─────────────────────────────────────────────────────────────┘

1. generate-context
   └─> Output: /tasks/0001-analysis-[name].md
       └─> Key files list (5-10 essential files)
           └─> Execution path traces
               │
               ↓
2. generate-spec (ENHANCED)
   ├─> Phase 1: Initial understanding
   ├─> Phase 2: Review codebase context + read key files
   ├─> Phase 3: ⛔ CLARIFYING QUESTIONS (MANDATORY STOP)
   │   └─> Wait for user answers
   └─> Phase 4: Generate spec
       └─> Output: /tasks/0001-spec-[feature].md
           │
           ↓
3. generate-architecture-options (NEW)
   ├─> Generate 3 approaches:
   │   ├─> Minimal Changes
   │   ├─> Clean Architecture
   │   └─> Pragmatic Balance
   ├─> Present trade-offs + recommendation
   └─> ⛔ WAIT FOR USER CHOICE
       └─> Output: /tasks/architecture-0001.md
           │
           ↓
4. generate-task-list-from-spec (ENHANCED)
   ├─> Review chosen architecture
   ├─> Review key files from context
   ├─> Generate parent tasks
   ├─> ⛔ WAIT FOR "Generate sub tasks"
   └─> Generate sub-tasks
       └─> Output: /tasks/tasks-0001-spec-[feature].md
           │
           ↓
5. manage-tasks
   ├─> Execute sub-tasks sequentially
   ├─> Run tests after each parent task
   ├─> Validate demo criteria
   └─> Commit with conventional format
       │
       ↓
6. review-implementation (NEW)
   ├─> Review for bugs, quality, conventions
   ├─> Categorize findings (critical/important/nice-to-have)
   ├─> Present to user
   └─> ⛔ WAIT FOR FIX DECISION
       └─> Apply fixes if requested
           │
           ↓
7. Complete
   └─> Create PR, deploy, document decisions
```

---

## Implementation Priority

See [docs/roadmap/PROGRESS.md](../../roadmap/PROGRESS.md) for detailed Phase 2 planning,
effort estimates, and acceptance criteria.

### Sprint 1: Critical Gaps (Week 1)

- [ ] Enhance `generate-spec` with mandatory clarifying phase
- [ ] Create `generate-architecture-options` prompt
- [ ] Create `review-implementation` prompt
- [ ] Update workflow documentation

### Sprint 2: Important Improvements (Week 2)

- [ ] Enhance `generate-context` with key files output
- [ ] Add execution path tracing to context analysis
- [ ] Update `generate-task-list-from-spec` to reference architecture
- [ ] Add explicit checkpoints to all prompts

### Sprint 3: Polish (Week 3)

- [ ] Test complete workflow end-to-end
- [ ] Refine based on feedback
- [ ] Document examples and best practices
- [ ] Create tutorial/getting started guide

---

## Key Learnings from Claude Code Plugin

1. **Mandatory Clarification is Critical:** Most feature failures come from misunderstood requirements. An explicit stop point for questions prevents this.

2. **Architecture Deserves Multiple Options:** There's rarely one "right" architecture. Presenting trade-offs enables better decisions.

3. **Quality Review Before Merge:** Catching issues before they ship is vastly cheaper than fixing them in production.

4. **Agent-Based Parallel Execution:** Running multiple focused agents in parallel is more efficient than sequential single-agent work.

5. **Explicit > Implicit:** User checkpoints should be explicit STOP commands, not implicit in the flow.

6. **Action-Oriented Context:** Codebase analysis should produce actionable outputs (key files, execution paths) not just comprehensive documentation.

7. **Focused Agents:** Specialized agents (explorer, architect, reviewer) with narrow focus produce better results than general-purpose analysis.

---

## Appendix: Claude Code Agent Specifications

### code-explorer Agent

```yaml
name: code-explorer
description: Deeply analyzes existing codebase features by tracing execution paths
tools: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch, KillShell, BashOutput
model: sonnet
color: yellow
```

**Output Requirements:**

- Entry points with file:line references
- Step-by-step execution flow with data transformations
- Key components and their responsibilities
- Architecture insights: patterns, layers, design decisions
- Dependencies (external and internal)
- Observations about strengths, issues, opportunities
- **List of 5-10 files essential to understanding the topic**

---

### code-architect Agent

```yaml
name: code-architect
description: Designs feature architectures by analyzing codebase patterns and providing implementation blueprints
tools: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch, KillShell, BashOutput
model: sonnet
color: green
```

**Output Requirements:**

- **Patterns & Conventions Found:** Existing patterns with file:line references
- **Architecture Decision:** Chosen approach with rationale and trade-offs
- **Component Design:** Each component with file path, responsibilities, dependencies, interfaces
- **Implementation Map:** Specific files to create/modify with detailed change descriptions
- **Data Flow:** Complete flow from entry points through transformations to outputs
- **Build Sequence:** Phased implementation steps as a checklist
- **Critical Details:** Error handling, state management, testing, performance, security

**Philosophy:** Make confident architectural choices rather than presenting multiple options (when used standalone). Provide file paths, function names, and concrete steps.

---

### code-reviewer Agent

```yaml
name: code-reviewer
description: Reviews code for bugs, quality issues, and project conventions
tools: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch, KillShell, BashOutput
model: sonnet
color: blue
```

**Focus Areas:**

- Project guideline compliance (CLAUDE.md)
- Bug detection
- Code quality issues
- Confidence-based filtering (only reports high-confidence issues ≥80)

**Output Requirements:**

- Critical issues (confidence 75-100)
- Important issues (confidence 50-74)
- Specific fixes with file:line references
- Project guideline references

---

## References

- Claude Code Repository: https://github.com/anthropics/claude-code
- Feature-Dev Plugin: https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev
- Feature-Dev README: https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/README.md
- Feature-Dev Command: https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/commands/feature-dev.md
- Code Explorer Agent: https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/agents/code-explorer.md
- Code Architect Agent: https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/agents/code-architect.md
- Code Reviewer Agent: https://github.com/anthropics/claude-code/blob/main/plugins/feature-dev/agents/code-reviewer.md
