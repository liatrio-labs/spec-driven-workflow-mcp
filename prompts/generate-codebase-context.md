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

### High Confidence
- **Criteria:** Strong evidence from working code or explicit documentation
- **Examples:**
  - Feature exists with traced working code path
  - Technology explicitly listed in dependencies with usage found
  - Design decision documented in ADR or architecture docs

### Medium Confidence (Needs Validation)
- **Criteria:** Inferred from context, behind feature flags, or implied
- **Examples:**
  - Feature toggle currently disabled (code exists but may not be active)
  - Pattern inferred from code structure (not explicitly documented)
  - Technology mentioned in comments only
  - Outdated documentation that may not reflect current code

### Low Confidence (Unknown)
- **Criteria:** Cannot determine from available information
- **Examples:**
  - Rationale missing from both docs and code
  - Conflicting information between sources
  - Experimental or dormant code paths
  - Dead code that may no longer be used

**Always flag Medium and Low confidence items for user validation in the analysis**

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

**⛔ STOP - Wait for answers before proceeding**

---

### Phase 2: Documentation Audit

**Goal:** Inventory existing documentation and extract any recorded rationale

#### Scan for Documentation

Find and catalog:

1. **In-Repository Documentation:**
   - README files (all levels)
   - docs/, documentation/, wiki/ directories
   - ARCHITECTURE.md, DESIGN.md, CONTRIBUTING.md
   - Architecture diagrams (*.png, *.jpg, *.svg, *.drawio in docs/)
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

**⛔ STOP - Wait for any needed clarifications**

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

```
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
```
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
```
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

**⛔ STOP - Ask user to validate findings, especially Medium/Low confidence items**

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
```
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

**Present findings:** Integration inventory with evidence.

---

### Phase 5: Gap Identification & User Collaboration

**Goal:** Identify what cannot be determined from code/docs and get answers from user

#### Automated Gap Detection

Compare code analysis vs. documentation to find:

1. **Missing Rationale:**
   - Technologies used in code but no "why" in docs
   - Patterns implemented but no decision record
   - Architectural choices without explanation

2. **Conflicts:**
   - Code contradicts documentation
   - Diagrams show different structure than code
   - Comments claim one thing, code does another

3. **Unknowns:**
   - Feature toggles (which are active?)
   - Experimental code (what's the status?)
   - Dead code (can it be removed?)
   - Performance requirements (what are the targets?)

#### User Questions (Focused, NOT Batch)

Ask 3-5 targeted questions based on gaps found:

Example:
```
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

**⛔ STOP - Wait for user answers**

**Capture answers as direct quotes:**
```
[User confirmed: 2025-01-21: "MongoDB was from an early experiment, it's safe to remove."]
[User stated: "JWT chosen because we needed stateless auth for mobile clients."]
```

---

### Phase 6: Generate Comprehensive Analysis Document

**Goal:** Create complete, evidence-based codebase context document

#### Document Structure

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

### 4.2 Communication Patterns

**API → Services → Repositories → Database:**
```
src/api/routes/users.ts:25 (HTTP endpoint)
  → UserService.createUser() (src/services/UserService.ts:67)
    → UserRepository.insert() (src/repositories/UserRepository.ts:45)
      → Database INSERT query
```

**Event-Driven (Async):**
```
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

```
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

```
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
```

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
