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

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `[n]-analysis-[codebase-or-component-name].md` (Where `n` is a zero-padded 4-digit sequence starting from 0001, e.g., `0001-analysis-authentication-system.md` or `0001-analysis-full-codebase.md`)

## Process

This is a **conversational, iterative analysis process**. The AI should engage the user throughout, asking clarifying questions and presenting findings for validation.

### Phase 1: Initial Discovery (High-Level Context)

Start by gathering foundational information about the codebase structure and scope.

#### Questions to Ask User:

Present these as a numbered/lettered list for easy responses:

1. **Repository Structure:**
   - a) Is this a single repository (monorepo) or multiple repositories?
   - b) If monorepo: Are there distinct workspaces/packages? Please list them.
   - c) If multiple repos: Which repositories are in scope for this analysis?

2. **Service Architecture:**
   - a) Is this a self-contained application?
   - b) Does it connect to other services/microservices?
   - c) If connected: What are the key external dependencies? (APIs, databases, message queues, etc.)

3. **Analysis Scope:**
   - a) Should I analyze the entire codebase?
   - b) Should I focus on a specific module/component/feature area?
   - c) What's the primary reason for this analysis? (e.g., adding a new feature, refactoring, understanding legacy code)

4. **Priority Areas:**
   - Which of the following are most important for your upcoming work? (Select all that apply)
   - a) Database schema and data models
   - b) API routes and endpoints
   - c) Authentication/authorization patterns
   - d) State management
   - e) UI component architecture
   - f) Testing patterns
   - g) Build and deployment configuration
   - h) Other: [please specify]

#### Initial Automated Discovery:

While waiting for user responses, perform these reconnaissance tasks:

- Identify project type and tech stack (languages, frameworks, libraries)
- Locate configuration files (package.json, requirements.txt, go.mod, Cargo.toml, etc.)
- Find main entry points
- Discover directory structure and organization patterns
- Identify testing frameworks and test file locations
- Locate documentation (README, CONTRIBUTING, docs/ directory)

**Present Initial Findings:** Share discovered tech stack and structure with the user for confirmation before proceeding.

### Phase 2: Deep Architectural Analysis

Based on user responses and priority areas, dive deeper into specific architectural aspects.

#### For Each Priority Area, Ask:

**Database & Data Models:**
- What ORM/query builder is used? (e.g., SQLAlchemy, Prisma, GORM, Diesel)
- Are there migration files I should review?
- What are the key domain entities/models?
- Are there any database design patterns I should note? (e.g., soft deletes, multi-tenancy, audit trails)

**API Architecture:**
- What's the routing pattern? (RESTful, GraphQL, RPC, etc.)
- Where are routes/endpoints defined?
- Is there an API versioning strategy?
- How are requests validated? (schemas, middleware, decorators)
- How is error handling structured?

**Authentication & Authorization:**
- What auth mechanism is used? (JWT, sessions, OAuth, API keys)
- Where is auth logic centralized?
- How are roles/permissions managed?
- Are there middleware/guards/decorators for protected routes?

**Frontend Architecture (if applicable):**
- What's the component structure? (atomic design, feature-based, pages/components)
- What state management is used? (Redux, MobX, Context, Zustand, Pinia, etc.)
- How is routing handled?
- What's the styling approach? (CSS modules, styled-components, Tailwind, etc.)
- Are there reusable UI component libraries or design systems?

**Code Organization Patterns:**
- What's the directory structure philosophy? (feature-based, layer-based, domain-driven)
- Are there naming conventions I should follow?
- How are utilities/helpers organized?
- Where are constants/enums/types defined?
- Is there a dependency injection pattern?

**Testing Strategy:**
- What testing frameworks are used? (pytest, Jest, Vitest, Go testing, etc.)
- What's the test file naming/location convention?
- Are there integration tests? E2E tests?
- What's the test coverage expectation?
- How do I run tests? (commands, CI/CD integration)

**Build & Deployment:**
- What's the build tool? (Vite, webpack, esbuild, cargo, go build, etc.)
- Are there different environments? (dev, staging, production)
- How are environment variables managed?
- Is there a CI/CD pipeline? What does it do?
- Are there docker/containerization configs?

#### Conversational Discovery Flow:

For each area, the AI should:

1. **Explore**: Use Glob, Grep, and Read to discover patterns
2. **Present**: Show findings with specific file examples
3. **Validate**: Ask user "Does this match your understanding?" or "Are there exceptions to this pattern I should know about?"
4. **Clarify**: If inconsistencies found, ask "I noticed [X] and [Y] follow different patterns. Which should new code follow?"
5. **Document**: Record confirmed patterns in the analysis document

### Phase 3: Integration Points & Dependencies

Identify how new code would integrate with existing systems.

#### Questions to Ask:

1. **External Services:**
   - What external APIs/services does this codebase call?
   - Are there rate limits, retry logic, or circuit breakers I should be aware of?
   - How are API keys/credentials managed?

2. **Database Interactions:**
   - Are there transaction patterns to follow?
   - Connection pooling configuration?
   - How are migrations created and applied?

3. **Event/Message Patterns:**
   - Are there pub/sub systems? (Redis, RabbitMQ, Kafka, etc.)
   - Event-driven architecture patterns?
   - WebSocket or real-time communication?

4. **Shared Libraries/Modules:**
   - Are there internal shared libraries?
   - How are they versioned and imported?
   - Any monorepo workspace dependencies?

### Phase 4: Conventions & Standards

Understand the codebase's "style" to ensure consistency.

#### Automated Analysis:

- Linter configurations (.eslintrc, .pylintrc, .golangci.yml, etc.)
- Formatter settings (prettier, black, gofmt, rustfmt)
- Git commit message patterns (conventional commits, etc.)
- Code review practices (if CONTRIBUTING.md exists)

#### Questions to Ask:

1. **Code Style:**
   - Are there specific coding standards I should follow beyond the linter?
   - Preferred patterns for error handling?
   - Logging conventions?

2. **Git Workflow:**
   - What branching strategy is used? (git-flow, trunk-based, feature branches)
   - Are there branch naming conventions?
   - How should I structure commit messages?
   - Should I create an issue/ticket before starting work?

3. **Documentation:**
   - Where should new feature documentation go?
   - Are there inline documentation standards? (JSDoc, docstrings, etc.)
   - Should I update CHANGELOG or similar files?

### Phase 5: Generate Comprehensive Analysis Document

Once all questions are answered and analysis is complete, create the analysis document.

## Analysis Document Structure

The generated analysis should include:

```markdown
# Codebase Analysis: [Project/Component Name]

**Date:** [YYYY-MM-DD]
**Scope:** [Full codebase / Specific component]
**Purpose:** [Why this analysis was performed]

## 1. Overview

- **Project Type:** [Web app, API, CLI tool, library, etc.]
- **Primary Language(s):** [Languages and versions]
- **Core Framework(s):** [Main frameworks/libraries]
- **Repository Structure:** [Monorepo/single repo, workspace details]

## 2. Architecture

### 2.1 System Architecture
- High-level architecture description
- Service dependencies (internal and external)
- Architecture diagram (if applicable) or ASCII art representation

### 2.2 Directory Structure
```
[Show key directory structure with explanations]
```

**Organization Philosophy:** [Feature-based, layer-based, etc.]

## 3. Tech Stack Deep Dive

### 3.1 Core Dependencies
| Dependency | Version | Purpose | Notes |
|------------|---------|---------|-------|
| [name]     | [ver]   | [why]   | [any special notes] |

### 3.2 Development Dependencies
[Key dev tools, testing frameworks, build tools]

## 4. Data Layer

### 4.1 Database(s)
- **Type:** [PostgreSQL, MongoDB, Redis, etc.]
- **ORM/Query Builder:** [Tool name and version]
- **Connection Management:** [How connections are configured]

### 4.2 Key Models/Entities
| Model | Location | Purpose | Key Relationships |
|-------|----------|---------|-------------------|
| User  | models/user.py | User accounts | → Profile (1:1), → Orders (1:many) |

### 4.3 Migration Strategy
- **Migration Tool:** [Tool name]
- **Location:** [Path to migrations]
- **How to Create:** [Command to generate new migration]
- **How to Apply:** [Command to run migrations]

### 4.4 Data Patterns
- Soft deletes: [Yes/No, how implemented]
- Timestamps: [Automatic created_at/updated_at?]
- UUIDs vs Auto-increment: [Which is used for IDs]
- Audit trails: [How changes are tracked]

## 5. API Layer

### 5.1 API Style
- **Type:** [REST, GraphQL, gRPC, etc.]
- **Versioning:** [How versions are managed]
- **Base Path:** [e.g., /api/v1/]

### 5.2 Route Definitions
- **Location:** [Where routes are defined]
- **Pattern Example:**
```[language]
[Example route definition from codebase]
```

### 5.3 Request/Response Patterns
- **Validation:** [How requests are validated - Zod, Joi, Pydantic, etc.]
- **Serialization:** [How responses are formatted]
- **Error Format:** [Standard error response structure]

### 5.4 Middleware/Guards
- Authentication middleware: [Location and how it works]
- Authorization: [Role/permission checking approach]
- Rate limiting: [If applicable]
- CORS configuration: [If applicable]

## 6. Authentication & Authorization

### 6.1 Authentication Strategy
- **Method:** [JWT, sessions, OAuth, etc.]
- **Token Storage:** [How and where tokens are stored]
- **Implementation Files:** [Key files for auth logic]

### 6.2 Authorization
- **Pattern:** [RBAC, ABAC, simple boolean flags, etc.]
- **Roles/Permissions:** [How defined and checked]
- **Protected Route Pattern:**
```[language]
[Example of protecting a route]
```

## 7. Frontend Architecture (if applicable)

### 7.1 Framework & Routing
- **Framework:** [React, Vue, Angular, Svelte, etc.]
- **Router:** [React Router, Vue Router, etc.]
- **Routing Pattern:** [File-based, explicit routes, etc.]

### 7.2 Component Organization
```
[Component directory structure]
```
- **Pattern:** [Atomic design, feature-based, etc.]
- **Component Example Location:** [Path to reference component]

### 7.3 State Management
- **Tool:** [Redux, Context, Pinia, etc.]
- **Pattern:** [How state is organized]
- **Location:** [Where state logic lives]

### 7.4 Styling
- **Approach:** [CSS modules, Tailwind, styled-components, etc.]
- **Theme/Design System:** [If exists, where it's defined]
- **Global Styles:** [Location of global CSS/theme]

### 7.5 Key UI Patterns
- Form handling: [How forms are built and validated]
- Data fetching: [React Query, SWR, custom hooks, etc.]
- Error boundaries: [How errors are caught and displayed]

## 8. Testing Strategy

### 8.1 Testing Frameworks
- **Unit Tests:** [Jest, pytest, etc.]
- **Integration Tests:** [Framework and approach]
- **E2E Tests:** [Playwright, Cypress, etc.]

### 8.2 Test File Conventions
- **Location:** [Co-located, separate test directory]
- **Naming:** [*.test.ts, *_test.py, etc.]
- **Example Pattern:**
```[language]
[Example test from codebase]
```

### 8.3 Running Tests
```bash
# Unit tests
[command]

# Integration tests
[command]

# E2E tests
[command]

# Coverage report
[command]
```

### 8.4 Test Coverage
- **Current Coverage:** [If available]
- **Expected Coverage:** [Target or requirement]
- **CI Integration:** [How tests run in CI]

## 9. Build & Deployment

### 9.1 Build Configuration
- **Build Tool:** [Vite, webpack, etc.]
- **Build Command:** `[command]`
- **Output Directory:** [dist/, build/, target/, etc.]

### 9.2 Environment Management
- **Environment Files:** [.env, .env.local, etc.]
- **Required Variables:** [List key env vars]
- **Environment-Specific Configs:** [dev/staging/prod differences]

### 9.3 Deployment
- **CI/CD:** [GitHub Actions, GitLab CI, etc.]
- **Pipeline Location:** [Path to CI config]
- **Deployment Targets:** [Where app is deployed]
- **Containerization:** [Docker, if applicable]

## 10. Code Patterns & Conventions

### 10.1 Code Style
- **Linter:** [ESLint, Pylint, etc.] - Config: [path to config]
- **Formatter:** [Prettier, Black, etc.] - Config: [path to config]
- **Key Style Rules:** [Notable conventions]

### 10.2 Common Patterns

#### Error Handling
```[language]
[Example error handling pattern]
```

#### Logging
```[language]
[Example logging pattern]
```

#### Dependency Injection (if applicable)
```[language]
[Example DI pattern]
```

#### Async Patterns
```[language]
[Example async/await or promise patterns]
```

### 10.3 Naming Conventions
- **Files:** [camelCase, kebab-case, snake_case]
- **Variables:** [Convention]
- **Functions:** [Convention]
- **Classes:** [Convention]
- **Constants:** [Convention]

### 10.4 File Organization Pattern
[Describe typical file structure for a new feature]

## 11. Integration Points

### 11.1 External Services
| Service | Purpose | Configuration | Retry/Error Handling |
|---------|---------|---------------|----------------------|
| Stripe  | Payments | env: STRIPE_KEY | Webhook verification |

### 11.2 Internal Service Communication
[If microservices or modular monolith]
- Communication method: [REST, gRPC, message queue]
- Service discovery: [If applicable]

### 11.3 Event Systems
- **Event Bus/Queue:** [If applicable]
- **Event Patterns:** [How events are published/consumed]

## 12. Git Workflow & Contribution

### 12.1 Branching Strategy
- **Model:** [git-flow, trunk-based, feature branches]
- **Branch Naming:** [e.g., feature/*, bugfix/*, etc.]
- **Protected Branches:** [main, develop, etc.]

### 12.2 Commit Conventions
- **Format:** [Conventional commits, custom format]
- **Example:**
```
feat: add user profile editing
```

### 12.3 Pull Request Process
- Pre-merge requirements: [Tests pass, reviews, etc.]
- PR template: [If exists, location]
- Review guidelines: [From CONTRIBUTING.md if exists]

## 13. Documentation

### 13.1 Existing Documentation
- README: [Summary of what it covers]
- API docs: [If exists, location and tool]
- Architecture docs: [If exists]
- Inline docs: [JSDoc, docstrings standard]

### 13.2 Documentation Requirements for New Code
- [What documentation should be added with new features]

## 14. Key Files Reference

### 14.1 Configuration Files
- `[path]` - [What it configures]
- `[path]` - [What it configures]

### 14.2 Entry Points
- `[path]` - [Description]

### 14.3 Core Utilities
- `[path]` - [What utilities it provides]

### 14.4 Example Feature Implementation
- `[path to well-implemented feature]` - Use this as a reference for patterns

## 15. Recommendations for New Feature Development

Based on this analysis, when adding new features:

1. **Follow [X] directory structure pattern** - Place new feature in [location]
2. **Use [Y] for data models** - Follow examples in [file]
3. **API routes should** - [Pattern to follow]
4. **Tests should be** - [Where and how to write them]
5. **Styling should use** - [Approach]
6. **State management via** - [Tool/pattern]
7. **Error handling via** - [Pattern]
8. **Commit messages following** - [Format]

## 16. Open Questions & Further Investigation

- [ ] [Question or area needing more investigation]
- [ ] [Uncertainty to clarify with team]

## 17. Next Steps

After this analysis, proceed with:
1. Use the `generate-spec` prompt to create a detailed specification for your feature
2. Reference this analysis document when making architectural decisions
3. Use patterns identified here to ensure consistency
4. Update this analysis if you discover new patterns during implementation

---

**Analysis completed by:** [AI/Human]
**Last updated:** [Date]
```

## Final Instructions

1. **Engage conversationally** - This is not a one-shot analysis. Ask questions, present findings, get feedback.
2. **Be thorough but focused** - Prioritize areas relevant to upcoming work based on user's responses.
3. **Provide examples** - Always include actual code snippets from the codebase as references.
4. **Validate findings** - After each major section, check with user: "Does this analysis match your understanding?"
5. **Surface inconsistencies** - If you find conflicting patterns, ask which is preferred for new code.
6. **Document unknowns** - If something is unclear, note it in "Open Questions" rather than guessing.
7. **Save incrementally** - Update the analysis document as you discover information, don't wait until the end.
8. **Make it actionable** - The analysis should directly inform how to write new code, not just describe existing code.
9. **Cross-reference** - If relevant docs exist (CONTRIBUTING.md, architecture diagrams), reference them.
10. **Keep it current** - Date the analysis and note it's a snapshot; codebases evolve.

## After Analysis Completion

Once the analysis document is complete:

1. **Present summary** - Give user a high-level summary of key findings and recommendations.
2. **Ask for validation** - "Does this analysis accurately capture the codebase? Any corrections needed?"
3. **Suggest next steps** - "Would you like me to proceed with the `generate-spec` prompt for your feature using this context?"
4. **Save the document** - Store in `/tasks/` with proper filename.
5. **Stop and wait** - Don't automatically move to next phase; wait for user direction.

This analysis becomes the foundation for all subsequent spec-driven development work, ensuring new features integrate seamlessly with existing architecture and conventions.
