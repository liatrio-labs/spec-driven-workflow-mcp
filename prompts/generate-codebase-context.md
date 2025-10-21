---
name: generate-codebase-context
description: "Generate codebase context by analyzing architecture, patterns, and conventions for spec-driven development"
tags:
  - analysis
  - architecture
  - discovery
arguments: []
meta:
  category: spec-development
  allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch
---

## Generate Codebase Context

## Goal

To guide an AI assistant in thoroughly analyzing and understanding a codebase's architecture, structure, patterns, and conventions. This analysis provides essential context for spec-driven feature development, ensuring new features integrate seamlessly with existing code and follow established patterns.

**Core Principle:** Code explains WHAT the system does and HOW it's built. Documentation explains WHY choices were made. Users provide goals and intent. Keep these separate and clearly attributed.

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
- **Location:** `/tasks/`
- **Filename:** `[n]-context-[codebase-or-component-name].md` (Where `n` is a zero-padded 4-digit sequence starting from 0001, e.g., `0001-context-authentication-system.md` or `0001-context-full-codebase.md`)

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

### ⛔ STOP - Wait for Answers Before Proceeding

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

### ⛔ STOP - Wait for Any Needed Clarifications

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

### ⛔ STOP - Ask User to Validate Findings, Especially Medium/Low Confidence Items

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

### ⛔ STOP - User may want to discuss pattern findings before proceeding

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

### ⛔ STOP - Wait for User Answers

**Capture answers as direct quotes:**

```text
[User confirmed: 2025-01-21: "MongoDB was from an early experiment, it's safe to remove."]
[User stated: "JWT chosen because we needed stateless auth for mobile clients."]
```

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

**Date:** YYYY-MM-DD | **Analysis Scope:** [Full/Partial]

## Quick Facts
- Repository Type, Languages, Architecture, Key Technologies, Maturity Level

## Strengths
- ✅ List 3-5 key strengths with evidence

## Areas Needing Attention
- ⚠️ List 3-5 priority concerns with priority levels (🟥🟧🟨)

## Recommended Next Steps
1-3 actionable next steps

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

### 1.1 Structure & Stack
- **Type:** [Monorepo / Single app / Multi-service workspace]
- **Components:** [List main components with evidence]
- **Languages & Frameworks:** [List with file:line evidence]
- **Databases & Infrastructure:** [List with evidence]

### 1.2 Version Control Patterns (if Git history available)
- **Commit activity:** Total commits, contributors, frequency
- **High-churn files:** [file.ts - N commits] - indicates active development
- **Stable files:** [dir/ - few commits] - mature foundation
- **Key maintainers:** [email patterns] - domain ownership
- **Evolution:** Major architectural changes with timeline
- **Confidence:** 🟡 Medium (depends on Git history)

---

## 2. Documentation Inventory

### 2.1 Found Documentation
- List files with path, title, last modified date

### 2.2 Decision Rationale (WHY)
For each technology/pattern:
- **Why chosen:** [Direct quote with source path#heading]
- **Alternatives:** [What was considered]
- **Confidence:** 🟢🟡🔴

### 2.3 Gaps & Conflicts
- ❌ **Gaps:** Technologies used but no WHY documented
- ⚠️ **Conflicts:** Code contradicts docs
- ⏰ **Outdated:** Old docs with evidence

---

## 3. System Capabilities (WHAT)

**Format:** For each feature, provide:
- **Entry point:** HTTP endpoint or function with file:line
- **Flow:** Key steps (4-5 steps) with file:line references
- **Business rules:** Critical validation/logic with evidence
- **Confidence:** 🟢🟡🔴

**Example - User Authentication:**
- **Entry:** `POST /api/auth/login` → src/api/routes/auth.ts:23
- **Flow:** Validate → Check DB → Generate JWT → Return token
- **Rules:** Password >=8 chars, 5 failed attempts = lock
- **Confidence:** 🟢 High (working code + tests)

**Group by confidence:**
- 🟢 High: Active production features with tests
- 🟡 Medium: Behind feature toggles, partial implementation
- 🔴 Low: Dead code, deprecated, experimental

### External Integrations

For each integration:
- **Service:** Name and purpose
- **Evidence:** file.ts:line-range
- **Config:** Where credentials/endpoints configured
- **Confidence:** 🟢🟡🔴

---

## 4. Architecture (HOW)

**Format:** For each component, provide:
- **Location & Responsibilities:** Where it lives, what it does
- **Key files:** file:line-range evidence
- **Confidence:** 🟢🟡🔴

**Example Component - API Layer:**
- **Location:** src/api/
- **Responsibilities:** HTTP routing, validation, auth middleware
- **Key files:** src/api/routes/*.ts:*, src/api/middleware/auth.ts:12
- **Confidence:** 🟢 High (clear boundaries)

### Communication Patterns

**Format:** Trace data flow through layers with file:line references

**Example - Request Flow:**
```

API endpoint (file.ts:line)
  → Service method (file.ts:line)
    → Repository method (file.ts:line)
      → Database query

```

### Architectural Patterns

List patterns with evidence and confidence:
- 🟢 **Layered Architecture:** API → Services → Repos → DB (src/ structure)
- 🟢 **Dependency Injection:** Constructor injection via DI container (src/di/container.ts:12)
- 🟡 **Event-Driven (Partial):** Event bus exists (src/events/bus.ts) but limited usage

---

## 5. Technical Implementation Details

### Code Style & Conventions
- **Linter/Formatter:** ESLint (Airbnb) + Prettier (config files in root)
- **TypeScript:** Strict mode (tsconfig.json:5)
- **Naming:** camelCase files, PascalCase classes/components, UPPER_SNAKE_CASE constants
- **File Organization:** Layer-based (api/, services/, repositories/), tests co-located (*.test.ts)
- **Git:** Feature branches (feature/*), Conventional Commits, required PR reviews

### Testing
- **Frameworks:** Jest + Supertest (package.json:34)
- **Coverage:** 75% current, 80% target [User stated]
- **E2E:** None found
- **Pattern:** Co-located *.test.ts, run via `npm test`

### Build & Deployment
- **Build:** Webpack → dist/ (`npm run build`)
- **Environments:** Dev (local), Staging (not configured), Production (AWS ECS)
- **CI/CD:** GitHub Actions (.github/workflows/ci.yml) - lint → test → build → deploy

---

## 6. Essential Files to Read

**List 5-10 priority files** with file:line-range and purpose:
1. **file.ts:line-range** - Description of what it does/why it's essential
2. **docs/file.md** - Decision rationale or architecture overview

**Example:**
1. **src/api/routes/index.ts:12-89** - Main route definitions, entry points
2. **src/services/UserService.ts:45-234** - Core user management logic
3. **docs/adr/001-database-choice.md** - PostgreSQL decision rationale

---

## 7. Execution Path Examples

**Trace 1-2 critical user flows** end-to-end with file:line references at each step.

**Example - User Login:**
```

1. POST /api/auth/login → src/api/routes/auth.ts:23
2. Validation middleware → src/api/middleware/validator.ts:8
3. AuthService.login() → src/services/AuthService.ts:45
4. UserRepository.findByEmail() → src/repositories/UserRepository.ts:34
5. Password verify → src/utils/bcrypt.ts:15
6. Generate JWT → src/utils/jwt.ts:12
7. Return { token, user } → src/api/routes/auth.ts:34

```

---

## 8. Analysis Summary & Next Steps

### Confidence Levels
- **🟢 High:** List key high-confidence findings (code + tests + docs)
- **🟡 Medium:** List findings needing validation (partial evidence)
- **🔴 Low:** List unknowns (gaps in code/docs)

### Open Questions & Gaps
**For User:**
- ❓ List questions needing user clarification (with evidence of what's unclear)

**Documentation Gaps:**
- 📝 List missing or outdated documentation

**Code Gaps:**
- 🔧 List deprecated code, missing tests, or incomplete features

### Recommendations for New Development

**Architecture Patterns to Follow:**
- List key patterns with file:line references (e.g., "Follow layered pattern: API → Service → Repository")

**Integration Points:**
- List existing systems to reuse (e.g., "Use JWT middleware at file.ts:line for auth")

**Standards:**
- List style guides, testing targets, and conventions

### Next Steps
1. Use `generate-spec` prompt to create feature specification
2. Reference this analysis for architectural decisions
3. Follow identified patterns for consistency
4. Address blocking gaps before starting implementation

**Analysis completed:** YYYY-MM-DD | **Status:** Ready for spec generation

---

## Final Checklist

Before saving the analysis document, verify:

- [ ] All findings cite evidence (file:line or path#heading)
- [ ] Confidence levels (🟢🟡🔴) marked for all findings
- [ ] User answers captured as direct quotes with dates
- [ ] Essential files list (5-10 files) with line ranges
- [ ] At least 1-2 execution path traces
- [ ] Gaps and unknowns explicitly documented
- [ ] Recommendations specific and actionable

---

**Output:** Evidence-based, confidence-assessed codebase analysis for spec-driven development.
