# Research Synthesis: Integrating Best Practices into MCP Prompts

**Date:** 2025-01-21
**Purpose:** Synthesize findings from Claude Code feature-dev analysis and existing research files to create actionable recommendations for improving our MCP prompts

---

## Key Sources Analyzed

1. **Claude Code feature-dev plugin** - Battle-tested 7-phase workflow with agent-based architecture
2. **information-analyst.md** - Specialized agent for extracting "WHY" from documentation
3. **code-analyst.md** - Specialized agent for discovering "WHAT" and "HOW" from code
4. **context_bootstrap.md** - Manager agent orchestrating code+info analysts for reverse-engineering

---

## Major Insights from Research Files

### 🎯 Core Philosophy from context_bootstrap.md

**"Code explains HOW the system currently behaves; the user supplies WHAT it is supposed to achieve and WHY choices were made."**

This is **critical** - it separates:
- What can be discovered automatically (code analysis)
- What must be asked (requirements, rationale, decisions)

**Application to Our Prompts:**
- `generate-codebase-context` should focus on WHAT and HOW (from code)
- Must have explicit phase to ask user for WHY and goals
- Cannot infer intent from code alone

---

### 🔬 Two-Agent Specialization Pattern

**Pattern:** Separate concerns into specialized agents with clear boundaries

#### Code Analyst (from code-analyst.md)

**Responsibilities:**
- Discover WHAT the system does (features, workflows, business rules)
- Discover HOW it's structured (architecture, patterns, components)
- Identify WHAT technologies are used

**Output Format:**
```markdown
## Code Analysis Summary
### System Capabilities
- Features Discovered (with file:line evidence)
- User Workflows (traced through code)
- Business Rules (from validation logic)
- External Integrations (working API clients)

### Technology Stack
- Languages & Frameworks (names only, NO versions)
- Data Storage (types, evidence)
- Infrastructure (cloud provider, deployment pattern)

### Architecture
- Components/Services (location, purpose, responsibilities)
- Communication Patterns (with file:line evidence)
- Service Boundaries
- Architectural Patterns (with evidence)

### Confidence & Gaps
- High Confidence (strong evidence)
- Needs Validation (feature toggles, dormant paths)
- Unknowns (areas code cannot resolve)
```

**Key Principles:**
1. Code is ground truth - report what actually exists
2. Be specific - reference exact file:line for evidence
3. Distinguish fact from inference
4. Flag toggles and dormant paths
5. Flag gaps - be clear what you can't determine
6. **Stay in your lane** - don't guess at "why"

**What NOT to include:**
- ❌ Internal data models (implementation detail)
- ❌ Missing/planned features (belongs in roadmap)
- ❌ Code quality judgments
- ❌ Specific dependency versions (too volatile)
- ❌ Testing infrastructure details

---

#### Information Analyst (from information-analyst.md)

**Responsibilities:**
- Discover WHY the system was built this way
- Extract rationale from documentation
- Find decision context and trade-offs
- Capture historical evolution

**Primary Job:** Extract "WHY" - this is what code analysis can't provide

**Output Format:**
```markdown
## Information Analysis Summary
### Documentation Found
- In Repository (with paths, titles, last updated timestamps)
- External (if provided)

### System Context
- Purpose & Goals
- Target Users
- Business Value
- Success Metrics
- Use Cases

### Decision Rationale (CRITICAL)
#### Technology Decisions
- **[Technology]**:
  - Why chosen: "[Direct quote from docs]"
  - Source: `path/to/doc.md#section-heading`
  - Alternatives considered
  - Trade-offs

#### Architecture Decisions
- **[Pattern]**:
  - Why chosen
  - Problem it solved
  - Source reference

### Intended Architecture (from diagrams/docs)
- Components (intended purpose from design)
- Intended Communication
- Design Patterns with rationale

### Historical Context
- Evolution timeline
- Migrations & Changes

### Conflicts & Discrepancies
- Between documents
- Gaps in rationale
- Outdated information

### Confidence Levels
- High (explicit in docs)
- Medium (implied)
- Low (ambiguous/missing)

### Questions for Manager
- Conflicting information
- Missing rationale
- Outdated docs
```

**Key Principles:**
1. **Direct quotes for "why"** - quote docs verbatim
2. **Source everything** - always say which doc/diagram
3. **Attach metadata** - path, heading/anchor, timestamp
4. **Flag conflicts, don't resolve**
5. **Note dates** - timestamp information
6. **Distinguish explicit vs implicit**
7. **Focus on rationale** - this is your unique value
8. **Concise summaries** - extract insights, don't repeat docs

---

### 🎭 Manager Orchestration Pattern (context_bootstrap.md)

**Pattern:** Manager coordinates specialized subprocess agents

**Manager Responsibilities:**
1. Detect repository structure (workspace, monorepo, single app)
2. Launch Code Analyst subprocess
3. Launch Information Analyst subprocess
4. Integrate findings from both
5. Ask user clarifying questions based on gaps
6. Draft comprehensive documentation
7. Review with user

**Six-Phase Workflow:**
1. **Analyze repository structure**
2. **Audit existing documentation**
3. **Deep code analysis** (subprocess: Code Analyst)
4. **User collaboration** (fill gaps, resolve conflicts)
5. **Draft documentation set** (PRDs, ADRs, SYSTEM-OVERVIEW, README)
6. **Review with user**

**Key Pattern:** "Keep dialog interactive. Ask focused follow-up questions instead of long questionnaires."

---

## Comparison: Our Prompts vs. Research Patterns

| Aspect | Our Current Approach | Research Best Practice | Gap |
|--------|---------------------|------------------------|-----|
| **Code vs. Docs Separation** | Single `generate-codebase-context` prompt | Separate Code Analyst + Information Analyst | Not separated - conflates WHAT/HOW with WHY |
| **Evidence Citations** | General descriptions | Explicit file:line references + timestamps | Weak evidence trail |
| **Confidence Levels** | Implicit | Explicit (High/Medium/Low with gaps) | No confidence assessment |
| **Documentation Audit** | Not included | Explicit phase: scan + categorize + date-check | Missing documentation review |
| **Rationale Extraction** | Ad-hoc | Dedicated agent focused on WHY | Not systematic |
| **User Collaboration** | Batch Q&A | Iterative short conversations | Too batch-oriented |
| **Output Artifacts** | Analysis markdown | PRDs + ADRs (MADR format) + SYSTEM-OVERVIEW + README | Different artifact structure |

---

## Actionable Recommendations

### 🔴 HIGH PRIORITY: Restructure `generate-codebase-context`

**Current State:** Single monolithic prompt trying to do everything

**Recommended Change:** Split into focused phases matching research patterns

```markdown
## Phase 1: Repository Structure Analysis
- Detect layout (workspace/monorepo/single app)
- Enumerate components/services
- Identify entry points
- **Output:** Structure summary with component list

## Phase 2: Documentation Audit
- Scan for documentation files (README, docs/, *.md, diagrams)
- Capture metadata (path, title, last modified)
- Note existing rationale if found
- Flag outdated or conflicting docs
- **Output:** Documentation inventory with timestamps

## Phase 3: Code Analysis (WHAT + HOW)
Following Code Analyst patterns:
- Discover WHAT: features, workflows, business rules, integrations
- Discover HOW: architecture, patterns, communication, deployment
- Technology stack (names only, NO versions)
- **Provide file:line evidence for ALL findings**
- **Flag confidence levels: High/Needs Validation/Unknown**
- **DO NOT infer WHY** - stay in lane
- **Output:** Code analysis summary with evidence

## Phase 4: Information Analysis (WHY)
Following Information Analyst patterns:
- Extract decision rationale from docs
- Find "why X was chosen" with direct quotes
- Capture alternatives considered and trade-offs
- Note historical context and evolution
- **Provide source references with path#heading**
- **Output:** Rationale summary with citations

## Phase 5: Gap Identification
- Compare code analysis vs. documentation
- Identify conflicts between docs and code
- List missing rationale (tech used but no "why")
- Flag questions that need user answers
- **Output:** Gap analysis with specific questions

## Phase 6: User Collaboration ⛔ MANDATORY STOP
**Interactive, not batch:**
- Ask focused questions about gaps
- Resolve conflicts between docs and code
- Confirm assumptions
- **Capture user answers as direct quotes for citation**
- **Wait for answers before proceeding**

## Phase 7: Generate Analysis Document
- Synthesize all findings
- Include evidence citations (file:line, doc#heading)
- Mark confidence levels
- Document resolved gaps and remaining unknowns
- **Essential Files List:** 5-10 key files with file:line ranges
- **Execution Path Traces:** Key workflows with step-by-step flow
- Save to `/tasks/[n]-context-[name].md`
```

---

### 🔴 HIGH PRIORITY: Add Evidence Citation Standards

Add to ALL prompts that analyze code or docs:

```markdown
## Evidence Citation Standards

Every finding MUST include evidence:

### For Code Findings
- Format: `path/to/file.ts:45-67` (include line range when relevant)
- Example: "Authentication uses JWT tokens (src/auth/AuthService.ts:23)"

### For Documentation Findings
- Format: `path/to/doc.md#section-heading` (include anchor/page)
- Example: "PostgreSQL chosen for ACID guarantees (docs/architecture.md#database-decision)"
- Include last modified timestamp when available

### For User-Provided Information
- Format: "[User confirmed: YYYY-MM-DD]"
- Example: "OAuth2 required by compliance team [User confirmed: 2025-01-21]"
- Use direct quotes when possible
```

---

### 🔴 HIGH PRIORITY: Add Confidence Assessment

Add to `generate-codebase-context` and `review-implementation`:

```markdown
## Confidence Assessment

Categorize every finding:

### High Confidence
- **Criteria:** Strong evidence from code or explicit documentation
- **Examples:**
  - Feature exists with working code path
  - Technology explicitly listed in dependencies
  - Design decision documented in ADR

### Medium Confidence (Needs Validation)
- **Criteria:** Inferred from context or behind feature flags
- **Examples:**
  - Feature toggle currently disabled
  - Pattern inferred from code structure
  - Technology mentioned in code comments only

### Low Confidence (Unknown)
- **Criteria:** Cannot determine from available information
- **Examples:**
  - Rationale missing from docs and code
  - Conflicting information in different sources
  - Experimental/dormant code paths

**Always flag low confidence items for user validation**
```

---

### 🟡 MEDIUM PRIORITY: Enhance `generate-spec` with WHY Questions

Current `generate-spec` asks about functional requirements. Add a dedicated section:

```markdown
## Phase 2A: Context Questions (WHY)

Before designing the feature, understand context:

### Purpose & Value
1. **What problem does this solve?**
   - Who experiences this problem?
   - How do they currently work around it?
   - What's the business value of solving it?

### Strategic Fit
2. **Why build this now?**
   - What makes this a priority?
   - What's driving the timeline?
   - Are there dependencies blocking other work?

### Success Criteria
3. **How will we know it's working?**
   - What metrics indicate success?
   - What does "good enough" look like?
   - What are the acceptance thresholds?

### Constraints & Context
4. **What constraints exist?**
   - Technical limitations
   - Regulatory/compliance requirements
   - Budget/timeline pressures
   - Team/resource constraints

**Capture answers as direct quotes for later reference in spec**
```

---

### 🟡 MEDIUM PRIORITY: Create ADR Template

Based on context_bootstrap.md recommendation for MADR format:

Create `prompts/templates/adr-template.md`:

```markdown
# [short title of solved problem and solution]

**Status:** [proposed | accepted | rejected | deprecated | superseded by [ADR-0005](0005-example.md)]
**Date:** YYYY-MM-DD
**Decision Makers:** [list who was involved]
**Context Source:** [reference to feature spec or analysis document]

## Context and Problem Statement

[Describe the context and problem statement in 1-2 sentences.
Include business value and constraints if relevant.]

## Decision Drivers

* [driver 1, e.g., a force, facing concern, ...]
* [driver 2, e.g., a force, facing concern, ...]
* ... <!-- numbers of drivers can vary -->

## Considered Options

* [option 1]
* [option 2]
* [option 3]
* ... <!-- numbers of options can vary -->

## Decision Outcome

Chosen option: "[option 1]", because [justification. e.g., only option that meets k.o. criterion decision driver | which resolves force | ... | comes out best (see below)].

### Consequences

* Good, because [positive consequence, e.g., improvement of one or more quality attributes, follow-up decisions required]
* Bad, because [negative consequence, e.g., compromising one or more quality attributes, follow-up decisions required]
* ... <!-- numbers of consequences can vary -->

### Confirmation

[Optional: Describe how the decision will be validated]

## Pros and Cons of the Options

### [option 1]

[short description | example | link to more information]

* Good, because [argument a]
* Good, because [argument b]
* Neutral, because [argument c]
* Bad, because [argument d]
* ... <!-- numbers of pros and cons can vary -->

### [option 2]

[same as above]

### [option 3]

[same as above]

## More Information

[Optional: Links to additional resources, related ADRs, or evidence used in decision making]
```

---

### 🟡 MEDIUM PRIORITY: Interactive vs. Batch Questioning

**Current:** `generate-spec` presents all questions at once

**Research Best Practice:** "Keep dialog interactive. Ask focused follow-up questions instead of long questionnaires."

**Recommendation:** Phase the questioning:

```markdown
## Clarifying Questions Approach

### Phase 1: Core Requirements (3-5 questions)
Ask ONLY about:
- What problem is being solved
- Who the user is
- Core functionality needed

**STOP - Wait for answers**

### Phase 2: Context & Constraints (based on answers)
Ask follow-up questions about:
- Edge cases specific to their answers
- Integration points now that we know the domain
- Constraints relevant to the identified problem

**STOP - Wait for answers**

### Phase 3: Refinement (based on gaps)
Ask targeted questions about:
- Ambiguities in their previous answers
- Specific unknowns discovered
- Trade-off preferences

**STOP - Wait for final confirmation**

**Rationale:** Shorter conversations get better engagement and more thoughtful answers than long questionnaires.
```

---

### 🟢 LOW PRIORITY: Artifact Structure

**Research Pattern:** Generate multiple focused documents:
- PRDs (product requirements)
- ADRs (architecture decisions in MADR format)
- SYSTEM-OVERVIEW.md (architecture summary)
- README.md updates

**Our Current:** Single large analysis markdown

**Recommendation:** Consider splitting output but LOW priority - our current structure works well for MCP use case.

---

## Integration Priority Matrix

| Change | Impact | Effort | Priority | Timeline |
|--------|--------|--------|----------|----------|
| Restructure codebase-context into phases | HIGH | MEDIUM | **P0** | Sprint 1 |
| Add evidence citation standards | HIGH | LOW | **P0** | Sprint 1 |
| Add confidence assessment | HIGH | LOW | **P0** | Sprint 1 |
| Enhance spec with WHY questions | MEDIUM | LOW | **P1** | Sprint 2 |
| Create ADR template | MEDIUM | LOW | **P1** | Sprint 2 |
| Move to interactive questioning | MEDIUM | MEDIUM | **P1** | Sprint 2 |
| Split into specialized sub-agents | LOW | HIGH | **P2** | Future |
| Multi-document artifact structure | LOW | MEDIUM | **P2** | Future |

---

## Specific Prompt Enhancements

### For `generate-codebase-context`

**Add from code-analyst.md:**
1. ✅ File:line evidence citations for all findings
2. ✅ Confidence levels (High/Needs Validation/Unknown)
3. ✅ "Stay in your lane" - don't infer WHY from code
4. ✅ Flag feature toggles and dormant paths
5. ✅ Technology names only (NO versions)
6. ✅ Focus on working features, not missing ones
7. ✅ "Essential Files List" with file:line ranges
8. ✅ Execution path traces with step-by-step flows

**Add from information-analyst.md:**
1. ✅ Documentation audit phase (scan + timestamp + inventory)
2. ✅ Rationale extraction with direct quotes
3. ✅ Source references with path#heading format
4. ✅ Conflict detection between docs
5. ✅ Distinguish explicit vs. implicit knowledge
6. ✅ Metadata capture (last modified timestamps)

**Add from context_bootstrap.md:**
1. ✅ Repository structure detection (workspace/monorepo/single)
2. ✅ User collaboration phase (interactive, not batch)
3. ✅ Capture user answers as direct quotes for citation

---

### For `generate-spec`

**Add from research:**
1. ✅ WHY questions (problem, value, strategic fit)
2. ✅ Interactive phased questioning (not batch)
3. ✅ Capture answers as direct quotes
4. ✅ Reference codebase context document explicitly
5. ✅ Include evidence citations when referencing existing code

---

### For `generate-architecture-options` (NEW)

**Inspired by code-architect.md:**
1. ✅ Patterns & conventions found (with file:line refs)
2. ✅ Multiple approaches (minimal/clean/pragmatic)
3. ✅ Complete component design with responsibilities
4. ✅ Implementation map (files to create/modify)
5. ✅ Data flow diagrams
6. ✅ Build sequence as checklist
7. ✅ Critical details (error handling, state, testing, security)

---

### For `review-implementation` (NEW)

**Inspired by code-reviewer.md:**
1. ✅ Confidence-based filtering (≥80% confidence)
2. ✅ Categorize findings (Critical/Important/Nice-to-have)
3. ✅ Specific fixes with file:line references
4. ✅ Check against project guidelines (CLAUDE.md)
5. ✅ Flag high-confidence issues only

---

## Key Principles to Embed

### 1. Separation of Concerns
- **Code tells you WHAT and HOW**
- **Docs tell you WHY**
- **Users tell you goals and intent**
- Don't conflate these sources

### 2. Evidence-Based
- Every claim needs evidence
- File:line for code
- Path#heading for docs
- Direct quotes for users
- Timestamps for currency

### 3. Confidence Assessment
- Distinguish fact from inference
- Flag gaps explicitly
- Mark validation needs
- Document unknowns

### 4. Interactive Collaboration
- Short focused conversations
- Don't batch questions
- Wait for answers between phases
- Capture responses as quotes

### 5. Actionable Outputs
- Specific file lists to read
- Execution path traces
- Concrete next steps
- Clear decision points

---

## Implementation Roadmap

### Sprint 1: Core Evidence & Confidence (Week 1)
**Goal:** Make analysis evidence-based and trustworthy

- [ ] Add evidence citation standards to all prompts
- [ ] Add confidence assessment to codebase-context
- [ ] Enhance codebase-context with code-analyst patterns
- [ ] Add documentation audit phase
- [ ] Test on sample codebase

**Deliverable:** Updated `generate-codebase-context` with evidence citations and confidence levels

---

### Sprint 2: Interactive Collaboration (Week 2)
**Goal:** Improve user engagement and rationale capture

- [ ] Restructure spec questions into phased approach
- [ ] Add WHY questions to spec generation
- [ ] Create ADR template
- [ ] Add rationale extraction to context analysis
- [ ] Test interactive questioning flow

**Deliverable:** Enhanced `generate-spec` with phased questions and WHY capture

---

### Sprint 3: Architecture & Review (Week 3)
**Goal:** Add missing workflow phases from Claude Code

- [ ] Create `generate-architecture-options` prompt
- [ ] Create `review-implementation` prompt
- [ ] Integrate with existing workflow
- [ ] Document complete end-to-end flow
- [ ] Create examples and tutorials

**Deliverable:** Complete workflow with all phases

---

## Success Metrics

### Qualitative
- ✅ Analysis includes file:line citations for all claims
- ✅ Confidence levels clearly marked
- ✅ User questions get thoughtful answers (not "whatever you think")
- ✅ Rationale captured with direct quotes
- ✅ Gaps explicitly documented vs. hidden

### Quantitative
- ✅ 100% of code findings have file:line evidence
- ✅ 100% of doc findings have path#heading source
- ✅ 100% of user answers captured as quotes
- ✅ <5 batch questions per phase (forces interactive dialog)
- ✅ 5-10 essential files identified per analysis

---

## References

- **Claude Code feature-dev:** [Comparison document](./claude-code-feature-dev-comparison.md)
- **code-analyst.md:** Specialized agent for code analysis
- **information-analyst.md:** Specialized agent for documentation analysis
- **context_bootstrap.md:** Manager orchestration pattern
- **MADR Format:** https://adr.github.io/madr/
