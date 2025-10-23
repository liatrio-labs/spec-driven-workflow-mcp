---
name: generate-context
description: "Generate codebase context by analyzing architecture, patterns, and conventions for spec-driven development"
tags:
  - analysis
  - architecture
  - discovery
arguments:
  - name: no_questions
    description: "Skip interactive questions and generate analysis autonomously (default: false)"
    required: false
meta:
  category: spec-development
  allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch
---

## Generate Codebase Context

## Goal

To guide an AI assistant in thoroughly analyzing and understanding a codebase's architecture, structure, patterns, and conventions. This analysis provides essential context for spec-driven feature development, ensuring new features integrate seamlessly with existing code and follow established patterns.

**Core Principle:** Code explains WHAT the system does and HOW it's built. Documentation explains WHY choices were made. Users provide goals and intent. Keep these separate and clearly attributed.

---

## ⚠️ CRITICAL EXECUTION RULE - READ FIRST

### Interactive Mode (Default)

**This is an INTERACTIVE, MULTI-TURN conversational process.**

You **MUST** follow this workflow:

1. **Complete Phase 1** → ASK QUESTIONS → **STOP and WAIT** for user answers
2. **Complete Phase 2** → IF questions needed, ASK and WAIT; OTHERWISE proceed to Phase 3
3. **Complete Phase 3** → ASK VALIDATION QUESTIONS → **STOP and WAIT** for user answers
4. **Complete Phase 3.5** → PRESENT FINDINGS → **STOP and WAIT** for user to discuss
5. **Complete Phase 4** → IF integration issues found, ASK and WAIT; OTHERWISE proceed to Phase 5
6. **Complete Phase 5** → IF gaps found, ASK and WAIT; OTHERWISE proceed to Phase 6
7. **Finally, Phase 6** → Generate final document

**Auto-Continue Rules:**
- **Phase 2**: If no conflicts or gaps found in documentation, state "No clarification needed" and proceed to Phase 3
- **Phase 4**: If no integration/dependency issues found, state "No integration issues" and proceed to Phase 5
- **Phase 5**: If no gaps/unknowns found, state "No significant gaps identified" and proceed to Phase 6
- **All other phases**: MUST stop and wait for user input

**NEVER skip checkpoints when questions exist. NEVER proceed without user input at ⛔ STOP points that require answers.**

If you find yourself generating the final document without having asked questions and received answers (when questions were needed), **YOU HAVE FAILED TO FOLLOW INSTRUCTIONS.**

### No-Questions Mode (--no_questions flag)

**When `no_questions=true` is specified:**

- **Skip all STOP checkpoints** - proceed through all phases autonomously
- **Make reasonable assumptions** - document assumptions clearly with 🔵 Assumed confidence level
- **Flag all assumptions** - list all assumptions made in a dedicated section
- **Note uncertainties** - mark areas where user input would improve accuracy
- **Generate complete document** - proceed directly to Phase 6 after analysis

**Assumed findings format:** "PostgreSQL used (package.json:23) 🔵 Assumed: chosen for ACID compliance (no documented rationale)"

---

## AI Behavior Guidelines

**Critical Rules for Execution:**

- **Do not summarize without evidence:** Every claim must be backed by file:line citations or doc references
- **Use citations before synthesis:** Gather evidence first, then draw conclusions
- **When uncertain, explicitly state "Cannot confirm":** Better to flag unknowns than guess
- **Never infer rationale (WHY) unless documented or confirmed by user:** Stay in your lane
- **Ask 3-5 focused questions per round:** Not long questionnaires - short, conversational iteration
- **Present findings incrementally:** Don't wait until the end - engage user throughout
- **Flag Medium/Low confidence items immediately:** Users should validate uncertain findings early

## Tool Usage by Phase

This prompt requires specific tools for different analysis phases:

- **Phase 1 (Repository Structure):**
  - `Glob` - Enumerate files and directories, detect project structure
  - `Read` - Inspect key configuration files (package.json, requirements.txt, etc.)

- **Phase 2 (Documentation Audit):**
  - `Glob` - Find documentation files (`**/*.md`, `**/docs/**`)
  - `Read` - Extract content and metadata from docs
  - `Grep` - Search for specific decision rationale or WHY statements

- **Phase 3 (Code Analysis):**
  - `Grep` - Search for patterns, imports, framework usage
  - `Read` - Inspect specific files for WHAT and HOW
  - `Glob` - Find related files (e.g., all controllers, all services)

- **Phase 3.5 (Pattern Recognition):**
  - `Grep` - Detect recurring patterns across files
  - `Read` - Verify pattern implementation details

- **Phase 4 (Integration Points):**
  - `Grep` - Find API calls, database queries, external service usage
  - `Read` - Understand integration implementation

- **Phase 5 (Gaps & User Collaboration):**
  - No tools - conversational phase with user

- **Phase 6 (Document Generation):**
  - `Write` - Create final analysis document

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/docs/`
- **Filename:** `00[n]-SYSTEM.md` (Where `n` is a single digit starting from 1, e.g., `001-SYSTEM.md`, `002-SYSTEM.md`, etc.)

## Evidence Citation Standards

**Every finding MUST include evidence:**

### For Code Findings

- **Format:** `path/to/file.ts:45-67` (include line range when relevant)
- **Example:** "Authentication uses JWT tokens (src/auth/AuthService.ts:23-45)"
- Always provide specific line numbers, not just file names

### For Documentation Findings

- **Format:** `path/to/doc.md#section-heading` or `path/to/doc.md:page-N`
- **Example:** "PostgreSQL chosen for ACID guarantees (docs/architecture.md#database-decision)"
- Include last modified timestamp when available: `(docs/ADR-001.md, updated 2024-12-15)`

### For User-Provided Information

- **Format:** "[User confirmed: YYYY-MM-DD]" or "[User stated: 'direct quote']"
- **Example:** "OAuth2 required by compliance team [User confirmed: 2025-01-21]"
- Use direct quotes when possible to preserve exact meaning

## Confidence Assessment

Categorize every finding by confidence level:

### Assumed (🔵) - No-Questions Mode Only

- **Criteria:** Reasonable inference made during autonomous analysis without user confirmation
- **Usage:** Only used when `no_questions=true` flag is set
- **Examples:**
  - "PostgreSQL used (package.json:23) 🔵 Assumed: chosen for ACID compliance (no documented rationale)"
  - "Microservices pattern (inferred from directory structure) 🔵 Assumed: supports team autonomy"
- **Note:** All assumed findings should be listed in a dedicated "Assumptions Made" section

### High Confidence (🟢)

- **Criteria:** Strong evidence from working code or explicit documentation
- **Automation Examples:**
  - `Grep` confirms 3+ consistent code references across different files
  - Feature exists in working code with traced execution path
  - Technology explicitly listed in dependencies AND usage found in code
  - Design decision documented in ADR with matching code implementation
- **Manual Verification:**
  - Feature exists with traced working code path
  - Explicit documentation with recent timestamps
  - Active usage in production code (not commented out)

### Medium Confidence (🟡 Needs Validation)

- **Criteria:** Inferred from context, behind feature flags, or implied
- **Automation Examples:**
  - Evidence only appears in code comments (not executable code)
  - `Grep` finds 1-2 references only (limited usage)
  - Pattern inferred from file structure but not explicitly implemented
  - Dependency listed but no usage found in code
- **Manual Verification:**
  - Feature toggle currently disabled (code exists but may not be active)
  - Pattern inferred from code structure (not explicitly documented)
  - Outdated documentation (>6 months old) that may not reflect current code

### Low Confidence (🔴 Unknown)

- **Criteria:** Cannot determine from available information
- **Automation Examples:**
  - No code references found via `Grep`
  - Conflicting dependency versions
  - Files exist but appear unreferenced
- **Manual Verification:**
  - Rationale missing from both docs and code
  - Conflicting information between sources (code vs. docs)
  - Experimental or dormant code paths
  - Dead code that may no longer be used

**Automatic Confidence Rules:**

- If `Grep/Glob` confirms ≥3 consistent references → Start with Medium, verify for High
- If evidence only in comments → Maximum Medium Confidence
- If no code references found → Start with Low Confidence
- If docs are >6 months old without code confirmation → Maximum Medium Confidence

### Always Flag Medium and Low Confidence Items for User Validation

## Process

This is a **conversational, iterative analysis process**. The AI should engage the user throughout, asking focused questions and presenting findings for validation.

**Important:** Ask short, focused questions. NOT long questionnaires. Get answers, then ask follow-ups based on those answers.

---

### Phase 1: Repository Structure Analysis

**Goal:** Understand the overall repository layout and scope

#### Automated Discovery

Automatically detect and analyze:

1. **Repository Type:**
   - Single application (src/, config/, tests/)
   - Monorepo with packages/apps (packages/*, apps/*)
   - Multi-service workspace (multiple peer directories with independent build tools)
   - Hybrid or custom structure

2. **Tech Stack Detection:**
   - Languages (from file extensions and config files)
   - Build tools (package.json, requirements.txt, Cargo.toml, go.mod, pom.xml, etc.)
   - Frameworks (from dependencies)
   - Testing frameworks (from devDependencies or test config)

3. **Entry Points:**
   - Main application files
   - API route definitions
   - CLI entry points
   - Background job/worker entry points

4. **Directory Structure:**
   - Map high-level organization
   - Identify patterns (feature-based, layer-based, domain-driven)

5. **Repository Size Assessment:**
   - Count total files (use `Glob` with appropriate patterns)
   - Estimate total lines of code (sample representative files)
   - Check for large binary assets or dependencies

#### Scoping Controls (Automatic)

**If repository exceeds these thresholds, request narrowed scope:**

- **>5,000 files:** "This repository has [N] files. To ensure focused analysis, please specify which components or directories to analyze."
- **>100 MB of source code:** "This is a large codebase. Would you like me to focus on specific modules or services?"
- **Multiple independent apps:** "I've detected [N] independent applications. Should I analyze all, or focus on specific ones?"

**Scoping Options to Present:**

- Option A: Full repository analysis (may take significant time)
- Option B: Focus on specific directory/module (e.g., `src/auth/`, `packages/api/`)
- Option C: Focus on specific functionality (e.g., "authentication flow", "payment processing")

**Present to user:** "I've detected [structure type] with [key components]. Is this correct?"

#### Questions for User (Short - 3 questions max)

1. **Scope:** Should I analyze the entire codebase, or focus on specific components? If specific, which ones?

2. **Purpose:** What's the primary reason for this analysis?
   - a) Adding a new feature
   - b) Refactoring existing code
   - c) Understanding legacy system
   - d) Onboarding new team members
   - e) Other: [specify]

3. **Priority Areas:** Which are most important for your upcoming work? (Select all that apply)
   - a) Database/Data layer
   - b) API/Routes
   - c) Authentication/Authorization
   - d) Frontend/UI
   - e) Testing approach
   - f) Build/Deploy pipeline
   - g) Other: [specify]

---

## 🛑 STOP HERE - PHASE 1 COMPLETE

### ⛔ DO NOT PROCEED TO PHASE 2 WITHOUT USER ANSWERS

**You MUST wait for the user to respond to the 3 questions above.**

**If you proceed without answers, you are violating the critical execution rule.**

---

### Phase 2: Documentation Audit

**Goal:** Inventory existing documentation and extract any recorded rationale

#### Scan for Documentation

Find and catalog:

1. **In-Repository Documentation:**
   - README files (all levels)
   - docs/, documentation/, wiki/ directories
   - ARCHITECTURE.md, DESIGN.md, CONTRIBUTING.md
   - Architecture diagrams (*.png,*.jpg, *.svg,*.drawio in docs/)
   - ADRs (Architecture Decision Records)
   - CHANGELOG.md, migration guides

2. **Capture Metadata:**
   - Relative path from repo root
   - Document title/heading
   - Last modified timestamp (if available from git)
   - Brief description of content

#### Extract Decision Rationale

**This is critical - look for WHY:**

- Why was [technology X] chosen?
- Why [pattern Y] over alternatives?
- What constraints drove decisions?
- What trade-offs were considered?
- What problems were these choices solving?

**For each rationale found:**

- Extract as direct quote
- Note source: `path/to/doc.md#section-heading`
- Include timestamp if available
- Mark confidence level (explicit vs. implied)

#### Flag Issues

- **Conflicts:** Where docs contradict each other or the code
- **Gaps:** Technologies used but no "why" documented
- **Outdated:** Docs that appear old (check timestamps)

**Present to user:** Summary of documentation found and any conflicts/gaps discovered. Ask for clarification if needed.

---

## 🛑 STOP HERE - PHASE 2 COMPLETE

### ⛔ CHECKPOINT - AUTO-CONTINUE OR WAIT FOR USER

**If you found conflicts or gaps:**
- Ask for clarification and **WAIT** for user responses

**If no clarification is needed:**
- Present your findings summary
- State "No conflicts or gaps found - proceeding to Phase 3"
- **Auto-continue to Phase 3** (no user acknowledgment required)

---

### Phase 3: Code Analysis (WHAT + HOW)

**Goal:** Discover what the system does and how it's structured by analyzing code

**Remember:** You are discovering WHAT and HOW from code. Do NOT infer WHY - that comes from docs or user.

#### 3.1: System Capabilities (WHAT it does)

**Discover working features:**

Trace from entry points to understand:

- **Features:** What functional capabilities exist right now?
- **User Workflows:** What complete user journeys are supported?
- **Business Rules:** What validation/calculation logic is enforced?
- **External Integrations:** What external systems does it integrate with (working API clients, SDKs)?

**For each capability:**

- Provide entry point with file:line (e.g., `src/api/routes/users.ts:12`)
- Brief description of what it does
- Key logic location (e.g., `src/services/UserService.ts:45-89`)
- Confidence level (High if working code path, Medium if behind feature toggle)

**Trace execution paths:**

For key workflows, provide step-by-step execution trace:

```text
User Login Flow:
1. POST /api/auth/login → src/api/routes/auth.ts:23
2. AuthController.login() → src/controllers/AuthController.ts:45
3. AuthService.validateCredentials() → src/services/AuthService.ts:67
4. UserRepository.findByEmail() → src/repositories/UserRepository.ts:34
5. Database query → models/User.ts:89
6. JWT generation → src/utils/jwt.ts:12
7. Response with token → src/controllers/AuthController.ts:52
```

**What NOT to include:**

- ❌ Internal data models (implementation detail, not user-facing)
- ❌ Missing or planned features (belongs in roadmap)
- ❌ Code quality judgments (not your job)
- ❌ Specific dependency versions (too volatile)
- ❌ Testing infrastructure details

#### 3.2: Technology Stack (WHAT technologies are used)

**Identify major technologies:**

From dependency files and imports, catalog:

- **Languages:** Name only (NO version numbers)
- **Major Frameworks:** Name only (e.g., "React", "Django", "Spring Boot")
- **Databases:** Type and evidence (e.g., "PostgreSQL - connection config in src/db/config.ts:10")
- **Cloud Services:** Provider only (e.g., "AWS - SDK imports in src/aws/")
- **API Style:** REST/GraphQL/gRPC (inferred from route definitions)
- **Authentication Approach:** JWT/OAuth/Sessions (from auth code)

**Evidence format:**

```text
- **Framework:** React (package.json:15, imports in src/components/*.tsx)
- **Database:** PostgreSQL (package.json:23 'pg', connection in src/db/pool.ts:8)
- **Cache:** Redis (docker-compose.yml:34, client in src/cache/redis.ts:12)
```

**What NOT to include:**

- ❌ Specific versions (e.g., "React 18.2.0" - too volatile)
- ❌ Minor utility libraries
- ❌ Testing frameworks (unless part of priority areas)

#### 3.3: Architecture & Patterns (HOW it's structured)

**Map components and boundaries:**

- **Components/Services:** What are the main logical units?
  - Location (directory/module)
  - Purpose (inferred from code)
  - Responsibilities (what it handles)
  - Evidence (key files with line numbers)

- **Communication Patterns:**
  - How do components talk? (API calls, events, direct imports)
  - Evidence with file:line references
  - Data exchanged (brief description)

Example:

```text
- **API Service → Database:**
  - Method: Direct ORM queries
  - Evidence: src/services/UserService.ts:45 calls UserRepository.findById()
  - Data: User entities
```

- **Service Boundaries:**
  - Proper: Components that communicate via APIs/events
  - Violations: Direct database access across service boundaries (flag these)

- **Architectural Patterns:**
  - Pattern name (e.g., "Layered Architecture", "Event-Driven", "CQRS")
  - Evidence from code structure
  - Example: "Event-driven - found publishers (src/events/publisher.ts:12) and subscribers (src/events/handlers/*.ts)"

**Flag dormant code:**

- Feature toggles currently disabled
- Experimental directories
- Dead code (imports show it's unused)

#### 3.4: Conventions & Standards

**Code organization:**

- File naming (camelCase, kebab-case, snake_case)
- Directory patterns (feature-based, layer-based)
- Module boundaries (what imports what)

**Code style:**

- Linter configuration (if found)
- Formatter settings
- Key conventions from codebase

**Git workflow:**

- Branching strategy (from branch names if visible)
- Commit conventions (conventional commits, other patterns)

**Present findings:** Share code analysis summary with file:line citations and confidence levels.

---

## 🛑 STOP HERE - PHASE 3 COMPLETE

### ⛔ DO NOT PROCEED TO PHASE 3.5 WITHOUT USER VALIDATION

**You MUST present your findings and explicitly ask the user to validate them.**

**Pay special attention to Medium (🟡) and Low (🔴) confidence items - these MUST be validated before proceeding.**

**Ask questions like:**
- "Does this analysis match your understanding of the system?"
- "Are there any inaccuracies in what I found?"
- "For the Medium confidence items, can you confirm [specific finding]?"

**Wait for user responses before continuing.**

---

### Phase 3.5: Pattern Recognition & Architectural Philosophy

**Goal:** Bridge raw analysis with system-level architectural understanding

**Purpose:** This phase synthesizes code findings into architectural patterns and design philosophies that guide system evolution.

#### Design Patterns Detection

**Automatically detect and document recurring patterns:**

1. **Structural Patterns:**
   - Repository pattern (data access layer)
   - Factory pattern (object creation)
   - Singleton pattern (shared instances)
   - Adapter pattern (interface translation)
   - **Evidence Format:** "Repository pattern used (UserRepository.ts:23-45, ProductRepository.ts:34-67, OrderRepository.ts:45-89)"

2. **Architectural Patterns:**
   - CQRS (Command Query Responsibility Segregation)
   - Event Sourcing
   - Microservices communication patterns
   - Layered architecture (presentation, business, data)
   - **Evidence Format:** "CQRS pattern: Commands in commands/, Queries in queries/ (found 12 command handlers, 8 query handlers)"

3. **Framework-Specific Conventions:**
   - NestJS modules and providers
   - Django apps structure
   - Rails MVC conventions
   - Spring Boot controllers and services
   - **Evidence Format:** "NestJS module pattern: Each feature has .module.ts, .controller.ts, .service.ts (auth/, users/, products/)"

#### Anti-Pattern Detection

**Flag concerning patterns that may indicate technical debt:**

1. **Cyclic Dependencies:**
   - Use `Grep` to detect circular imports
   - **Example:** "Potential cycle: AuthService imports UserService, UserService imports AuthService"
   - **Confidence:** 🔴 Low if inferred, 🟢 High if confirmed via import analysis

2. **Cross-Layer Violations:**
   - Controllers directly accessing database
   - Business logic in views/templates
   - Data layer calling API layer
   - **Example:** "Anti-pattern: Controller directly queries database (UserController.ts:45 has SQL query)"

3. **God Objects / Large Classes:**
   - Files exceeding 500 lines
   - Classes with >10 public methods
   - **Example:** "Large class warning: UserService.ts (847 lines, 23 public methods)"

#### Architectural Philosophy Synthesis

**Infer the system's architectural philosophy (with evidence):**

- **Modularity Approach:**
  - "Highly modular: Each feature isolated in packages/ (8 independent modules found)"
  - "Monolithic: Shared state across src/ (no module boundaries detected)"

- **Coupling Level:**
  - "Loose coupling: Dependency injection used (12 constructors inject interfaces)"
  - "Tight coupling: Direct instantiation pattern (14 files use 'new' keyword for dependencies)"

- **Consistency:**
  - "High consistency: 95% of files follow UserModule pattern"
  - "Mixed patterns: 3 different controller patterns found (REST, GraphQL, gRPC)"

**Present findings:** "I've identified [N] architectural patterns and [M] potential anti-patterns. Key philosophy appears to be [description]."

---

## 🛑 STOP HERE - PHASE 3.5 COMPLETE

### ⛔ DO NOT PROCEED TO PHASE 4 WITHOUT USER DISCUSSION

**You MUST present your pattern findings and give the user a chance to discuss them.**

**Ask questions like:**
- "Does this architectural philosophy match your understanding?"
- "Are there any patterns I've missed or misidentified?"
- "Would you like me to elaborate on any of these patterns before I continue?"

**Wait for user acknowledgment or questions before proceeding.**

---

### Phase 4: Integration Points & Dependencies

**Goal:** Understand how the system integrates with external systems

#### External Services

For each external integration found:

- **Service Name**
- **How it's used:** (API calls, SDK usage, webhooks)
- **Evidence:** File and line numbers where integration occurs
- **Configuration:** Where credentials/endpoints are configured
- **Error handling:** How failures are handled

Example:

```text
- **Stripe (Payment Processing):**
  - Usage: Charges, subscriptions, webhooks
  - Evidence: src/services/PaymentService.ts:23-156
  - Config: env vars in .env.example:12-15
  - Error handling: Retry logic in src/utils/stripe-retry.ts:8
  - Confidence: High (working code with tests)
```

#### Internal Dependencies

- Shared libraries/modules
- Monorepo package dependencies
- Service-to-service communication

#### Event/Message Patterns

- Pub/sub systems (Redis, RabbitMQ, Kafka)
- Event-driven patterns
- WebSocket or real-time communication

#### Crosscutting Concerns

**Goal:** Analyze system-wide quality attributes that cut across all components

These concerns are often overlooked but critical for understanding system maturity:

1. **Logging & Observability:**
   - Logging framework used (Winston, Log4j, Serilog, etc.)
   - Log levels and structure (structured logging JSON, plain text)
   - Distributed tracing (OpenTelemetry, Jaeger, Zipkin)
   - Metrics collection (Prometheus, StatsD, custom)
   - **Evidence:** `Grep` for logger imports/usage, configuration files
   - **Example:** "Structured logging with Winston (src/config/logger.ts:12, used in 47 files)"

2. **Error Handling & Resilience:**
   - Global error handling strategy
   - Retry mechanisms
   - Circuit breaker patterns
   - Graceful degradation
   - **Evidence:** Error handler middleware, retry decorators, error classes
   - **Example:** "Global error handler (src/middleware/errorHandler.ts:23), Retry decorator (src/decorators/retry.ts:12-45)"

3. **Configuration Management:**
   - Environment variables strategy (.env, config files)
   - Secrets management (AWS Secrets Manager, HashiCorp Vault, etc.)
   - Feature flags/toggles
   - Multi-environment configuration (dev, staging, prod)
   - **Evidence:** Config files, environment variable usage
   - **Example:** "Config via dotenv (config/.env.example has 34 vars), no secrets manager detected"

4. **Security Practices:**
   - Authentication middleware (JWT, OAuth, session-based)
   - Authorization patterns (RBAC, ABAC, ACL)
   - Input validation (sanitization, schema validation)
   - CORS configuration
   - Rate limiting
   - **Evidence:** Auth middleware, validators, security headers
   - **Example:** "JWT auth middleware (src/middleware/auth.ts:23), Joi validation (src/validators/, 12 schemas)"

5. **Performance & Caching:**
   - Caching strategy (Redis, in-memory, CDN)
   - Database query optimization
   - Lazy loading patterns
   - Pagination strategies
   - **Evidence:** Cache imports, query patterns
   - **Example:** "Redis caching layer (src/cache/redis.ts:12, used in 8 services)"

6. **Testing Approach:**
   - Test frameworks (Jest, PyTest, JUnit, etc.)
   - Test coverage strategy
   - Testing patterns (unit, integration, e2e)
   - Mocking/stubbing approach
   - **Evidence:** Test file structure, configuration files
   - **Example:** "Jest with 73% coverage (jest.config.js, 234 test files in **/*.spec.ts)"

**Confidence Assessment for Crosscutting Concerns:**

- 🟢 High: Active implementation found with configuration and usage
- 🟡 Medium: Partial implementation or inconsistent usage
- 🔴 Low: Not implemented or unclear strategy

**Present findings:** Crosscutting concerns summary with quality attribute assessment.

---

### Phase 5: Gap Identification & User Collaboration

**Goal:** Identify what cannot be determined from code/docs and get answers from user

#### Automated Gap Detection

Compare code analysis vs. documentation to find gaps, then **prioritize them**:

**Priority Levels:**

- 🟥 **Critical:** Blocks new development or introduces significant risk
- 🟧 **Important:** Should be resolved soon, impacts architectural decisions
- 🟨 **Minor:** Cosmetic, informational, or low-impact

**Gap Categories with Prioritization:**

1. **Missing Rationale:**
   - Technologies used in code but no "why" in docs
   - Patterns implemented but no decision record
   - Architectural choices without explanation
   - **Priority Assessment:**
     - 🟥 Critical: Core authentication/security decisions undocumented
     - 🟧 Important: Database choice, framework selection without rationale
     - 🟨 Minor: Utility library choices, formatting tools

2. **Conflicts:**
   - Code contradicts documentation
   - Diagrams show different structure than code
   - Comments claim one thing, code does another
   - **Priority Assessment:**
     - 🟥 Critical: Security/auth flows mismatch code vs docs
     - 🟧 Important: API contracts differ from implementation
     - 🟨 Minor: Outdated diagram with minor structural differences

3. **Unknowns:**
   - Feature toggles (which are active?)
   - Experimental code (what's the status?)
   - Dead code (can it be removed?)
   - Performance requirements (what are the targets?)
   - **Priority Assessment:**
     - 🟥 Critical: Feature toggles blocking production features
     - 🟧 Important: Experimental code in main execution paths
     - 🟨 Minor: Old commented-out code, unused utilities

**Prioritization Rules:**

- If gap relates to **security, auth, or data integrity** → 🟥 Critical
- If gap relates to **core business logic or API contracts** → 🟧 Important
- If gap relates to **documentation quality or code cleanup** → 🟨 Minor
- If gap **blocks spec development** → Escalate priority by one level

#### User Questions (Focused, NOT Batch)

Ask 3-5 targeted questions based on gaps found:

Example:

```text
I found some gaps that need your input:

1. **PostgreSQL vs. MongoDB:**
   - Code uses PostgreSQL (src/db/pool.ts:8)
   - But there's MongoDB client code (src/mongo/client.ts:12) that appears unused
   - Question: Is MongoDB deprecated? Can that code be removed?

2. **Feature Toggle 'new_dashboard':**
   - Code exists for new dashboard (src/features/dashboard-v2/)
   - Currently disabled (src/config/features.ts:15: enabled: false)
   - Question: What's the status? Should this be documented as experimental?

3. **Authentication Decision:**
   - JWT tokens are used (src/auth/jwt.ts)
   - No documentation explains why JWT was chosen over sessions
   - Question: Why was JWT selected? (This will help document the decision)
```

---

## 🛑 STOP HERE - PHASE 5 COMPLETE

### ⛔ DO NOT PROCEED TO PHASE 6 (DOCUMENT GENERATION) WITHOUT USER ANSWERS

**This is a CRITICAL checkpoint. You MUST:**

1. **Ask 3-5 specific gap questions** based on what you found
2. **Wait for user to answer each question**
3. **Capture answers as direct quotes with dates**
4. **ONLY THEN proceed to Phase 6**

**If you have NO gaps or questions:**
- Explicitly state "I found no significant gaps"
- **Auto-continue to Phase 6** (no user input required)

**Capture answers as direct quotes:**

```text
[User confirmed: 2025-01-21: "MongoDB was from an early experiment, it's safe to remove."]
[User stated: "JWT chosen because we needed stateless auth for mobile clients."]
```

**Once you have user answers, you may proceed to Phase 6.**

---

### Phase 5.5: Autonomous Answers (Optional Decision Framework)

**Goal:** When gaps exist but user input is not immediately available, provide reasoned autonomous answers

**When to Use Autonomous Answers:**
- User is unavailable or has requested autonomous analysis
- Gap is non-critical (🟨 Minor or some 🟧 Important items)
- Sufficient context exists to make reasonable inference
- Decision can be validated/corrected later

**When NOT to Use Autonomous Answers:**
- 🟥 Critical gaps (security, auth, data integrity decisions)
- Architectural choices with significant long-term impact
- Contradictions between code and documentation
- User has explicitly requested to be consulted

#### Autonomous Answer Framework

For each gap where autonomous answer is appropriate:

1. **State the Gap:**
   ```text
   GAP-003: FastMCP Framework Choice
   - Evidence: FastMCP used extensively (mcp_server/__init__.py:7, 24)
   - Gap: No documentation explains WHY FastMCP over alternatives
   ```

2. **Analyze Available Context:**
   ```text
   Context Analysis:
   - Project is MCP (Model Context Protocol) server
   - FastMCP is official Python framework for MCP
   - Alternative frameworks: (none widely known for MCP in Python)
   - Code shows clean integration, no workarounds
   ```

3. **Make Reasoned Inference:**
   ```text
   Autonomous Answer: 🔵 Assumed
   "FastMCP chosen as the official Python framework for MCP protocol implementation.
   No alternatives with comparable maturity exist for Python-based MCP servers."

   Reasoning:
   - FastMCP is the de-facto standard for MCP in Python
   - Clean code integration suggests good framework fit
   - No evidence of framework-related issues or workarounds
   ```

4. **Flag for Validation:**
   ```text
   Confidence: 🟡 Medium (reasonable inference, should be validated)
   Recommendation: Document in README or ADR for future reference
   Priority: 🟨 Minor (informational, not blocking)
   ```

#### Autonomous Answer Template

```markdown
### GAP-[N]: [Gap Title]

**Evidence:**
- [Finding from code/docs with file:line]
- [What's missing or unclear]

**Context Analysis:**
- [Relevant context from codebase]
- [Industry standards or common practices]
- [Evidence from code patterns]

**Autonomous Answer:** 🔵 Assumed
"[Reasoned answer based on available context]"

**Reasoning:**
- [Why this answer is reasonable]
- [Supporting evidence]
- [Alternative explanations considered and ruled out]

**Confidence:** 🟡 Medium (or appropriate level)
**Recommendation:** [How to validate or document this]
**Priority:** 🟨 Minor (or appropriate level)
```

#### Example: Complete Autonomous Answer

```markdown
### GAP-007: Version Pinning for FastMCP

**Evidence:**
- pyproject.toml:13: `fastmcp>=0.1.0` (not pinned to specific version)
- No version pinning strategy documented

**Context Analysis:**
- Project uses semantic versioning (pyproject.toml:72-96)
- FastMCP is early-stage framework (0.x version)
- Code doesn't use advanced/unstable features
- Similar projects often pin to minor version during 0.x

**Autonomous Answer:** 🔵 Assumed
"Pin FastMCP to minor version (`fastmcp>=0.1.0,<0.2.0`) to prevent breaking changes
while allowing patch updates."

**Reasoning:**
- During 0.x development, minor versions can introduce breaking changes
- Pinning to minor version balances stability with bug fixes
- Project already uses semantic versioning, suggesting version awareness
- Code review shows no dependency on bleeding-edge features

**Confidence:** 🟡 Medium (standard best practice, should confirm with team)
**Recommendation:** Update pyproject.toml and document in CONTRIBUTING.md
**Priority:** 🟨 Minor (preventive measure, not urgent)
```

#### Recording Autonomous Answers in Final Document

**In the main analysis, reference autonomous answers:**

```markdown
## 7. Gaps, Unknowns & Recommendations

### 7.3 Minor Gaps (🟨)

#### GAP-007: Version Pinning for FastMCP
**Autonomous Answer:** Pin to minor version (`fastmcp>=0.1.0,<0.2.0`) 🔵
**Recommendation:** Update pyproject.toml:
\`\`\`toml
dependencies = [
    "fastmcp>=0.1.0,<0.2.0",  # Pin to minor version
    "pyyaml>=6.0.1,<7.0.0",
]
\`\`\`
**Effort:** 5 min | **Impact:** Low | **Priority:** 🟨 Minor
```

**In Appendix, list all autonomous answers:**

```markdown
## Appendix D: Autonomous Answers Made

This analysis made the following autonomous decisions where user input was not available:

1. **GAP-003: FastMCP Framework Choice** 🔵 Assumed
   - Answer: "FastMCP is the official Python framework for MCP"
   - Reasoning: De-facto standard, no alternatives found
   - Validation needed: Confirm in README/docs

2. **GAP-007: Version Pinning** 🔵 Assumed
   - Answer: "Pin to minor version during 0.x development"
   - Reasoning: Standard best practice for pre-1.0 dependencies
   - Validation needed: Confirm with team policy

**Total Autonomous Answers:** 2
**Validation Status:** Pending user review
```

#### Best Practices for Autonomous Answers

1. **Be Conservative:**
   - Only make autonomous answers for 🟨 Minor and some 🟧 Important gaps
   - Never for 🟥 Critical gaps
   - Default to "Unknown" if insufficient context

2. **Show Your Work:**
   - Document reasoning process
   - List alternatives considered
   - Explain why chosen answer is most reasonable

3. **Flag Clearly:**
   - Use 🔵 Assumed confidence level
   - Create dedicated "Autonomous Answers" appendix
   - Mark for user validation

4. **Provide Actionable Next Steps:**
   - How to validate the assumption
   - How to document the decision
   - Priority and effort estimate

5. **Don't Over-Assume:**
   - Better to have 2 well-reasoned autonomous answers than 10 weak ones
   - If reasoning requires speculation, flag as 🔴 Unknown instead

---

### Phase 6: Generate Comprehensive Analysis Document

**Goal:** Create complete, evidence-based codebase context document

**Output Modes:**

- **Full Analysis (Default):** Complete detailed document with all sections (~10-20 pages)
- **Executive Summary Mode (Optional):** 2-page high-level summary first, then full details

**To enable summary mode, user can request:** "Generate an executive summary first"

#### Document Structure

**If Executive Summary Mode requested, start with:**

```markdown
# Executive Summary: [Project Name]

**Date:** YYYY-MM-DD | **Analysis Scope:** [Full/Partial] | **Analyst:** AI Assistant

## Quick Facts
- **Repository Type:** Monorepo with 8 packages
- **Primary Language:** TypeScript (85%), Python (15%)
- **Architecture:** Microservices with shared event bus
- **Key Technologies:** NestJS, PostgreSQL, Redis, Docker
- **Overall Maturity:** Production-ready with good test coverage (78%)

## Strengths
- ✅ Well-documented decision records (12 ADRs)
- ✅ Consistent architectural patterns (Repository + CQRS)
- ✅ Comprehensive testing strategy
- ✅ Active logging and observability

## Areas Needing Attention
- ⚠️ Missing rationale for Redis vs. alternatives
- ⚠️ Experimental features without clear roadmap
- ⚠️ Some anti-patterns in legacy modules

## Recommended Next Steps
1. Document Redis decision in ADR
2. Clarify status of experimental features
3. Refactor legacy modules to match current patterns

---

**Full detailed analysis follows below...**
```

#### Full Analysis Structure

```markdown
# Codebase Context: [Project Name]

**Date:** YYYY-MM-DD
**Scope:** [Full codebase / Specific components]
**Purpose:** [From user's stated purpose]

---

## 1. Repository Overview

### 1.1 Structure
- **Type:** [Monorepo / Single app / Multi-service workspace]
- **Components:** [List of main components/services/packages]
- **Organization:** [Feature-based / Layer-based / Domain-driven]

### 1.2 Technology Stack
- **Languages:** [List with evidence]
- **Frameworks:** [List with evidence]
- **Databases:** [List with evidence]
- **Infrastructure:** [Cloud provider, key services]

### 1.3 High-Level Architecture Diagram

**Use Mermaid diagrams to visualize system architecture when beneficial. Examples:**

**System Components:**

\`\`\`mermaid
graph TB
    subgraph "Entry Points"
        CLI[CLI Tool]
        HTTP[HTTP API :8080]
        WS[WebSocket :8081]
    end

    subgraph "Application Layer"
        API[API Server]
        AUTH[Auth Service]
        WORKER[Background Workers]
    end

    subgraph "Data Layer"
        DB[(PostgreSQL)]
        CACHE[(Redis)]
        QUEUE[Message Queue]
    end

    CLI --> API
    HTTP --> API
    WS --> API
    API --> AUTH
    API --> DB
    API --> CACHE
    WORKER --> QUEUE
    QUEUE --> DB
\`\`\`

**Data Flow:**

\`\`\`mermaid
sequenceDiagram
    participant User
    participant API
    participant Auth
    participant DB
    participant Cache

    User->>API: POST /api/login
    API->>Auth: Validate credentials
    Auth->>DB: Query user
    DB-->>Auth: User data
    Auth->>Cache: Store session
    Auth-->>API: JWT token
    API-->>User: 200 OK + token
\`\`\`

**Only include diagrams if they add clarity - not mandatory.**

### 1.4 Version Control & Evolution Patterns

**Repository Health Indicators (if Git history available):**

#### Commit Activity
- **Total commits:** ~2,450 commits
- **Active contributors:** 8 developers
- **Commit frequency:** ~15 commits/week (healthy pace)
- **Last major refactor:** 3 months ago

#### Code Maturity Signals
- **High-churn files** (volatility indicators):
  - `src/api/routes/users.ts` - 47 commits (high change rate)
  - `src/services/PaymentService.ts` - 34 commits (complex domain)
  - Indicates these are core business logic areas under active development

- **Stable core** (low-churn files):
  - `src/db/migrations/` - 5 commits total (stable schema)
  - `src/config/` - 8 commits (stable configuration)
  - Indicates architectural foundation is mature

#### Ownership Patterns
- **Primary maintainers** (by commit count):
  - alice@example.com: 45% of commits (backend focus)
  - bob@example.com: 30% of commits (frontend focus)
  - team@example.com: 15% (automated commits)

- **Key service owners** (inferred from commit patterns):
  - Auth system: alice@example.com (67% of auth/* commits)
  - Payment system: charlie@example.com (80% of payment/* commits)
  - Indicates domain ownership and expertise areas

#### Architectural Evolution
- **Major changes over time:**
  - 12 months ago: Monolith → Started microservices migration
  - 6 months ago: Added event-driven patterns (Redis pub/sub)
  - 3 months ago: Migrated from REST to GraphQL for mobile API
  - **Evidence:** Commit messages, file creation dates, refactoring commits

- **Migration status:**
  - 60% of services extracted from monolith
  - 40% still in legacy monolith (src/legacy/)
  - **Evidence:** Directory structure + commit history

#### Technical Debt Indicators
- **Files with highest churn + size:**
  - Large + frequently changing = potential refactor targets
  - Example: `src/services/OrderService.ts` (847 lines, 45 commits)
  - Suggests this is a God Object that may need splitting

**Confidence:** 🟡 Medium (depends on Git history availability)

---

## 2. Documentation Inventory

### 2.1 Found Documentation
- `docs/architecture.md` — Architecture overview (Last updated: 2024-11-20)
- `docs/adr/001-database-choice.md` — PostgreSQL decision (Last updated: 2024-10-15)
- `README.md` — Getting started guide (Last updated: 2024-12-01)

### 2.2 Decision Rationale Found
1. **PostgreSQL Database:**
   - **Why:** "Need ACID transactions for financial data" [docs/adr/001-database-choice.md#rationale]
   - **Alternatives considered:** MongoDB, MySQL
   - **Trade-off:** Performance vs. consistency - chose consistency
   - **Confidence:** High (explicit ADR)

2. **React Frontend:**
   - **Why:** "Team familiarity and ecosystem" [docs/architecture.md#frontend]
   - **Confidence:** Medium (documented but no detailed rationale)

### 2.3 Gaps & Conflicts
- ❌ **Gap:** Redis caching used (src/cache/redis.ts:12) but no decision doc
- ⚠️ **Conflict:** Diagram shows microservices, code is monolithic
- ⏰ **Outdated:** API docs dated 2023-06-15, endpoints changed since then

---

## 3. System Capabilities (WHAT)

### 3.1 Core Features

**Confidence Legend:** 🟢 High | 🟡 Medium | 🔴 Low

#### 🟢 User Authentication
- **Entry point:** `POST /api/auth/login` → src/api/routes/auth.ts:23
- **Flow:**
  1. Validate credentials → src/services/AuthService.ts:45
  2. Check user in database → src/repositories/UserRepository.ts:67
  3. Generate JWT → src/utils/jwt.ts:12
  4. Return token → src/api/routes/auth.ts:34
- **Business rules:**
  - Password must be >= 8 characters (src/validators/password.ts:8)
  - Max 5 failed attempts locks account (src/services/AuthService.ts:89)
- **Evidence:** Working code path, tests exist, used in production

#### 🟡 Dashboard Analytics
- **Entry point:** `GET /api/dashboard` → src/api/routes/dashboard.ts:15
- **Note:** Behind feature toggle `enable_new_dashboard = false`
- **Status:** [User confirmed: "Experimental, not ready for production"]
- **Evidence:** Code exists but currently disabled

#### 🔴 Social Login
- **Entry point:** OAuth handlers in src/auth/oauth/*.ts
- **Note:** Code present but imports show it's never called
- **Status:** [User confirmed: "Deprecated, safe to remove"]
- **Evidence:** Dead code (no references found)

### 3.2 External Integrations (Working)

#### Stripe Payment Processing
- **Usage:** Charges, subscriptions, webhook handling
- **Evidence:** src/services/PaymentService.ts:34-178
- **Configuration:** STRIPE_SECRET_KEY in .env
- **Error handling:** Exponential backoff retry (src/utils/payment-retry.ts:12)
- **Confidence:** 🟢 High (active production use)

### 3.3 User Workflows

**User Registration Flow:**
1. Submit form → src/pages/SignUp.tsx:45
2. POST /api/users → src/api/routes/users.ts:12
3. Validate input → src/validators/userSchema.ts:8
4. Hash password → src/utils/bcrypt.ts:15
5. Insert user → src/repositories/UserRepository.ts:23
6. Send welcome email → src/services/EmailService.ts:67
7. Auto-login → redirects to /dashboard

---

## 4. Architecture (HOW)

### 4.1 Components

#### API Service
- **Location:** src/api/
- **Responsibilities:**
  - HTTP routing and request handling
  - Request validation
  - Authentication middleware
- **Key files:**
  - src/api/routes/*.ts:* (route definitions)
  - src/api/middleware/auth.ts:12 (auth middleware)
  - src/api/middleware/validator.ts:8 (request validation)
- **Confidence:** 🟢 High (clear boundaries)

#### Business Logic Layer
- **Location:** src/services/
- **Responsibilities:**
  - Core business rules
  - Transaction orchestration
  - External service integration
- **Key files:**
  - src/services/UserService.ts:45-234 (user management)
  - src/services/PaymentService.ts:34-178 (payment processing)
- **Confidence:** 🟢 High

#### Data Access Layer
- **Location:** src/repositories/
- **Responsibilities:**
  - Database queries
  - ORM interaction
  - Data mapping
- **Key files:**
  - src/repositories/BaseRepository.ts:12 (common patterns)
  - src/repositories/UserRepository.ts:23 (user data access)
- **Confidence:** 🟢 High

**Component Diagram (Optional):**

\`\`\`mermaid
graph TB
    subgraph "API Layer"
        ROUTES[Routes<br/>src/api/routes/]
        MIDDLEWARE[Middleware<br/>src/api/middleware/]
    end

    subgraph "Business Logic"
        USER_SVC[UserService<br/>src/services/UserService.ts]
        PAY_SVC[PaymentService<br/>src/services/PaymentService.ts]
    end

    subgraph "Data Access"
        USER_REPO[UserRepository<br/>src/repositories/]
        BASE_REPO[BaseRepository<br/>Common patterns]
    end

    subgraph "External"
        DB[(Database)]
        CACHE[(Cache)]
    end

    ROUTES --> MIDDLEWARE
    MIDDLEWARE --> USER_SVC
    MIDDLEWARE --> PAY_SVC
    USER_SVC --> USER_REPO
    PAY_SVC --> USER_REPO
    USER_REPO --> BASE_REPO
    USER_REPO --> DB
    USER_SVC --> CACHE
\`\`\`

### 4.2 Communication Patterns

**API → Services → Repositories → Database:**
```text

src/api/routes/users.ts:25 (HTTP endpoint)
  → UserService.createUser() (src/services/UserService.ts:67)
    → UserRepository.insert() (src/repositories/UserRepository.ts:45)
      → Database INSERT query

```

**Event-Driven (Async):**

```text

PaymentService.processCharge() (src/services/PaymentService.ts:89)
  → EventBus.publish('payment.processed') (src/events/bus.ts:23)
    → EmailService listens (src/services/EmailService.ts:12)
      → Sends receipt email

```

### 4.3 Architectural Patterns

#### 🟢 Layered Architecture

- **Evidence:** Clear separation: API → Services → Repositories → Database
- **Rationale:** [Not explicitly documented]
- **[User stated: "Standard pattern for maintainability"]**

#### 🟢 Dependency Injection

- **Evidence:** Services injected via constructor (src/services/*.ts)
- **Implementation:** Custom DI container (src/di/container.ts:12)

#### 🟡 Event-Driven (Partial)

- **Evidence:** Event bus exists (src/events/bus.ts)
- **Usage:** Only for email notifications, not fully adopted
- **[User confirmed: "Plan to expand event usage for audit logging"]**

---

## 5. Conventions & Standards

### 5.1 Code Style

- **Linter:** ESLint (eslintrc.json) - Airbnb config
- **Formatter:** Prettier (prettierrc.json)
- **TypeScript:** Strict mode enabled (tsconfig.json:5)

### 5.2 Naming Conventions

- **Files:** camelCase for TS/JS files (userService.ts)
- **Components:** PascalCase for React (UserProfile.tsx)
- **Functions:** camelCase (getUserById)
- **Classes:** PascalCase (UserService)
- **Constants:** UPPER_SNAKE_CASE (MAX_RETRY_ATTEMPTS)

### 5.3 File Organization

- **Pattern:** Layer-based (api/, services/, repositories/)
- **Co-location:** Tests alongside source (userService.ts + userService.test.ts)
- **Barrel exports:** index.ts files in each directory

### 5.4 Git Workflow

- **Branching:** Feature branches (feature/*, bugfix/*)
- **Commits:** Conventional Commits (feat:, fix:, docs:)
- **PRs:** Required reviews, CI must pass

---

## 6. Testing Strategy

### 6.1 Frameworks

- **Unit:** Jest (package.json:34)
- **Integration:** Jest + Supertest (for API tests)
- **E2E:** [None found]

### 6.2 Coverage

- **Current:** ~75% (from jest.config.js coverage report)
- **Target:** [User stated: "Aiming for 80%"]

### 6.3 Patterns

- **Location:** Co-located (*.test.ts alongside source)
- **Naming:** *.test.ts
- **Run command:** `npm test`

---

## 7. Build & Deployment

### 7.1 Build Process

- **Tool:** Webpack (webpack.config.js)
- **Command:** `npm run build`
- **Output:** dist/ directory

### 7.2 Environments

- **Development:** Local (npm run dev)
- **Staging:** [Not configured yet - User confirmed]
- **Production:** AWS ECS (infrastructure/ecs-task-def.json)

### 7.3 CI/CD

- **Platform:** GitHub Actions (.github/workflows/ci.yml)
- **Pipeline:**
  1. Lint check
  2. Unit tests
  3. Build
  4. Deploy to staging (on main branch)

---

## 8. Essential Files to Read

Priority files for anyone working on this codebase:

1. **src/api/routes/index.ts:12-89** - Main route definitions, entry points
2. **src/services/UserService.ts:45-234** - Core user management logic
3. **src/services/PaymentService.ts:34-178** - Payment processing flow
4. **src/repositories/BaseRepository.ts:12-67** - Common data access patterns
5. **src/utils/jwt.ts:12-45** - Authentication token handling
6. **src/api/middleware/auth.ts:23-67** - Request authentication
7. **docs/architecture.md** - High-level architecture overview
8. **docs/adr/001-database-choice.md** - PostgreSQL decision rationale

---

## 9. Execution Path Examples

### Example 1: User Login

```text

1. User submits credentials via POST /api/auth/login
   Entry: src/api/routes/auth.ts:23

2. Request hits auth middleware (if protected route)
   Middleware: src/api/middleware/validator.ts:8
   Validates: email format, password presence

3. Controller delegates to service
   Controller: src/api/routes/auth.ts:25 calls AuthService.login()

4. Service validates credentials
   Service: src/services/AuthService.ts:45
   → UserRepository.findByEmail(email)
   Repository: src/repositories/UserRepository.ts:34
   → Database SELECT query

5. Service verifies password
   Service: src/services/AuthService.ts:67
   → bcrypt.compare() in src/utils/bcrypt.ts:15

6. Service generates JWT
   Service: src/services/AuthService.ts:78
   → jwt.sign() in src/utils/jwt.ts:12

7. Response sent to client
   Controller: src/api/routes/auth.ts:34
   Returns: { token, user }

```

### Example 2: Background Payment Processing

```text

1. Webhook received from Stripe
   Entry: src/api/routes/webhooks/stripe.ts:12

2. Signature verification
   Middleware: src/api/middleware/stripeWebhook.ts:8

3. Event published to bus
   Handler: src/api/routes/webhooks/stripe.ts:23
   → EventBus.publish('payment.received')
   Bus: src/events/bus.ts:45

4. Multiple subscribers react:
   a) EmailService sends receipt
      Subscriber: src/services/EmailService.ts:67

   b) AnalyticsService tracks event
      Subscriber: src/services/AnalyticsService.ts:34

   c) UserService updates balance
      Subscriber: src/services/UserService.ts:123

```

---

## 10. Confidence Summary

### High Confidence Findings ✅

- Authentication flow (complete code trace + tests)
- Payment integration (active production usage)
- Database choice (explicit ADR)
- Layered architecture (clear code organization)
- Technology stack (explicit dependencies)

### Medium Confidence (Needs Validation) ⚠️

- Event-driven pattern (partially implemented)
- React choice rationale (documented but brief)
- Target code coverage (stated by user)

### Low Confidence (Unknown) ❓

- Redis caching decision (no documentation)
- Deployment to staging (not configured)
- E2E testing strategy (none found)

---

## 11. Open Questions & Gaps

### For User Validation

1. ❓ **Redis Caching:**
   - Used in src/cache/redis.ts:12
   - No decision documentation found
   - Question: Why Redis? What alternatives were considered?

2. ❓ **Staging Environment:**
   - No configuration found for staging
   - User mentioned it exists - where?

### Documentation Gaps

1. 📝 Need ADR for Redis caching choice
2. 📝 Update API documentation (currently outdated: 2023-06-15)
3. 📝 Document event-driven pattern expansion plan
4. 📝 Remove or document deprecated OAuth code

### Code Gaps

1. 🔧 Remove deprecated MongoDB client code
2. 🔧 Remove unused OAuth handlers
3. 🔧 Add E2E testing framework
4. 🔧 Configure staging environment

---

## 12. Recommendations for New Features

When building new features in this codebase:

1. **Architecture:**
   - Follow layered pattern: API → Service → Repository
   - Place routes in src/api/routes/[feature].ts
   - Business logic in src/services/[Feature]Service.ts
   - Data access in src/repositories/[Feature]Repository.ts

2. **Authentication:**
   - Use existing JWT middleware (src/api/middleware/auth.ts:23)
   - Follow pattern in src/api/routes/auth.ts for protected routes

3. **Database:**
   - Use Prisma ORM (already configured)
   - Create migrations with `npm run migrate:create`
   - Follow patterns in src/repositories/BaseRepository.ts

4. **Testing:**
   - Co-locate tests with source (*.test.ts)
   - Aim for 80% coverage (current: 75%)
   - Run tests with `npm test`

5. **Styling:**
   - Follow ESLint + Prettier config
   - Use camelCase for files, PascalCase for classes/components
   - Conventional Commits for commit messages

6. **Events:**
   - Consider using event bus for async operations
   - Follow pattern in src/services/PaymentService.ts:89 for publishing
   - Subscribe in relevant services (src/services/EmailService.ts:12 example)

---

## 13. Next Steps

After this context analysis:

1. **Use `generate-spec` prompt** to create detailed specification for your feature
2. **Reference this analysis** when making architectural decisions
3. **Follow identified patterns** to ensure consistency
4. **Address high-priority gaps** if they block your work
5. **Update this analysis** if you discover new patterns during implementation

---

**Analysis completed:** YYYY-MM-DD
**Last validated with user:** YYYY-MM-DD
**Status:** Ready for feature specification

---

## Key Principles to Remember

1. **Evidence-Based:** Every claim needs file:line or doc#heading citation
2. **Confidence Levels:** Mark High/Medium/Low confidence for all findings
3. **Separate WHAT/HOW/WHY:**
   - Code analysis tells you WHAT and HOW
   - Documentation tells you WHY
   - User fills in gaps and confirms intent
4. **Stay in Your Lane:** Don't infer WHY from code - flag it as a gap for user to answer
5. **Interactive, Not Batch:** Short focused questions, wait for answers, then ask follow-ups
6. **Flag Gaps Explicitly:** Better to document "Unknown" than to guess
7. **Actionable Outputs:**
   - Specific file lists with line numbers
   - Execution path traces
   - Clear recommendations for new development
8. **Preserve User Input:** Capture direct quotes for later citation in specs/ADRs

---

## Final Checklist Before Completing

Before saving the analysis document, verify:

- [ ] All code findings have file:line citations
- [ ] All documentation findings have path#heading references
- [ ] User answers captured as direct quotes with dates
- [ ] Confidence levels marked for all findings
- [ ] Essential files list includes 5-10 key files with line ranges
- [ ] At least 2 execution path traces provided
- [ ] Gaps and unknowns explicitly documented (not hidden)
- [ ] Recommendations are specific and actionable
- [ ] High/Medium/Low confidence findings categorized
- [ ] Open questions listed for future resolution

---

This enhanced prompt will produce **evidence-based, confidence-assessed codebase analysis** that serves as a strong foundation for spec-driven development. The analysis clearly separates facts from inferences, documents gaps explicitly, and provides actionable guidance for building new features.
