---
name: generate-spec
description: "Generate a Specification (Spec) for a feature"
tags:
  - planning
  - specification
arguments: []
meta:
  category: spec-development
  allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch
---

## Generate Specification

## Goal

To guide an AI assistant in creating a detailed Specification (Spec) in Markdown format, based on an initial user prompt. The Spec should be clear, actionable, and suitable for a junior developer to understand and implement the feature.

**Core Principle:** The Spec defines WHAT needs to be built and WHY (user value, business goals). The HOW (implementation details) is left to the developer, unless specific architectural constraints exist.

## AI Behavior Guidelines

- **Ask, don't assume:** When requirements are unclear, ask specific questions rather than making assumptions
- **Reference existing context:** If a codebase-context document exists, reference it for architectural alignment
- **Short, focused questions:** Ask 3-5 questions per round, not long questionnaires
- **Provide options:** Use letter/number lists for easy selection
- **Explicit unknowns:** Flag areas needing clarification rather than guessing
- **Evidence-based:** When suggesting technical approaches, cite existing patterns from codebase

## Process

### Phase 1: Initial Analysis (Optional - If Codebase Context Available)

**If** a codebase-context document exists in `/tasks/`, read it to understand:

- Existing architectural patterns
- Technology stack and conventions
- Integration points and dependencies
- Common patterns for similar features

**Tool Usage:** Read (for context document), Grep (to find related existing features)

### Phase 2: Clarifying Questions (Mandatory)

Before writing the Spec, the AI **must** ask clarifying questions to gather sufficient detail.

**Focus on:**

- **WHAT** needs to be built (functionality, features)
- **WHY** it's needed (user value, business goals)
- **Constraints** (technical, scope, timeline)

**Do NOT ask about:**

- Specific implementation details (HOW) - let developers decide
- Low-level technical choices - unless there are architectural constraints

**Guidelines:**

- Ask 3-5 focused questions per round
- Provide multiple-choice options (A/B/C) when possible
- Wait for answers before proceeding

**⛔ STOP - Wait for user answers before proceeding to Phase 3**

### Phase 3: Draft Specification

Based on initial prompt + user answers + codebase context (if available), generate a Spec using the structure outlined below.

**Tool Usage:** Write (to create spec file), Read (to reference existing specs/docs)

### Phase 4: Review & Refinement

Present the spec to the user for review. Ask if they:

- Are satisfied with the level of detail
- Have additional questions or clarifications
- Want to adjust scope or requirements

**⛔ STOP - Wait for user feedback before finalizing**

### Phase 5: Finalize

Save the completed Spec to `/tasks/[n]-spec-[feature-name].md`

**⛔ STOP - Workflow complete. Do NOT proceed to implementation.**

## Clarifying Questions (Examples)

The AI should adapt its questions based on the prompt, but here are some common areas to explore:

- **Problem/Goal:** "What problem does this feature solve for the user?" or "What is the main goal we want to achieve with this feature?"
- **Target User:** "Who is the primary user of this feature?"
- **Core Functionality:** "Can you describe the key actions a user should be able to perform with this feature?"
- **User Stories:** "Could you provide a few user stories? (e.g., As a [type of user], I want to [perform an action] so that [benefit].)"
- **Acceptance Criteria:** "How will we know when this feature is successfully implemented? What are the key success criteria?"
- **Scope/Boundaries:** "Are there any specific things this feature *should not* do (non-goals)?"
- **Data Requirements:** "What kind of data does this feature need to display or manipulate?"
- **Design/UI:** "Are there any existing design mockups or UI guidelines to follow?" or "Can you describe the desired look and feel?"
- **Edge Cases:** "Are there any potential edge cases or error conditions we should consider?"
- **Unit of Work:** "What is the smallest end-to-end slice we can ship that a user or stakeholder can experience, test, or demonstrate?"
- **Demoability:** "For each stage, how will we show working value (e.g., URL, CLI output, screenshot, test run, short demo script)?"

## Spec Structure

The generated Spec should include the following sections:

1. **Introduction/Overview:** Briefly describe the feature and the problem it solves. State the goal.

2. **Goals:** List the specific, measurable objectives for this feature.

3. **User Stories:** Detail the user narratives describing feature usage and benefits.

4. **Demoable Units of Work:** Define small, end-to-end vertical slices. For each slice capture: Purpose and users; Demo Criteria (what will be shown to verify value); Proof Artifact(s) (tangible evidence such as a URL, CLI command & expected output, test names, or screenshot).

5. **Functional Requirements:** List the specific functionalities the feature must have. Use clear, concise language (e.g., "The system must allow users to upload a profile picture."). Number these requirements.

6. **Non-Goals (Out of Scope):** Clearly state what this feature will *not* include to manage scope.

7. **Architectural Alignment (If codebase-context available):**
   - Reference existing patterns this feature should follow
   - Identify integration points with existing systems
   - Note any deviations from established conventions (with justification)
   - **Format:** "Authentication will follow existing JWT pattern (src/auth/AuthService.ts:23-45 per codebase-context)"

8. **Technical Feasibility Assessment:**
   - **🟢 High Confidence:** Requirements that align with existing capabilities and patterns
   - **🟡 Medium Confidence:** Requirements that may need research or new dependencies
   - **🔴 Low Confidence:** Requirements with unknown feasibility or significant technical risk
   - Include evidence: reference similar features, existing code, or docs that support feasibility

9. **Design Considerations (Optional):** Link to mockups, describe UI/UX requirements, or mention relevant components/styles if applicable.

10. **Technical Considerations (Optional):** Mention any known technical constraints, dependencies, or suggestions (e.g., "Should integrate with the existing Auth module").

11. **Success Metrics:** How will the success of this feature be measured? (e.g., "Increase user engagement by 10%", "Reduce support tickets related to X").

12. **Open Questions:** List any remaining questions or areas needing further clarification. Include confidence level for each unknown.

## Target Audience

Assume the primary reader of the Spec is a **junior developer**. Therefore, requirements should be explicit, unambiguous, and avoid jargon where possible. Provide enough detail for them to understand the feature's purpose and core logic.

## Output Format

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `[n]-spec-[feature-name].md` (Where `n` is a zero-padded 4-digit sequence starting from 0001)
- **Example:** `/tasks/0001-spec-user-authentication.md`

**Header Format:**

```markdown
# Spec: [Feature Name]

**Status:** Draft | Under Review | Approved
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD
**Author:** AI Assistant (with user input)
**Codebase Context:** [Reference to context doc if used, or "N/A"]
```

## Execution Workflow

**Phase 1 (Optional):** Check for codebase-context document
↓
**Phase 2 (Mandatory):** Ask 3-5 clarifying questions → ⛔ WAIT FOR ANSWERS
↓
**Phase 3:** Draft specification using provided structure
↓
**Phase 4:** Present to user for review → ⛔ WAIT FOR FEEDBACK
↓
**Phase 5:** Finalize and save → ⛔ STOP (Do NOT implement)

## Critical Rules

1. **Never skip Phase 2:** Clarifying questions are mandatory, even if prompt seems clear
2. **Do NOT implement:** This workflow creates the spec only, not the code
3. **Reference context:** Always check for and reference codebase-context if available
4. **Evidence-based:** When suggesting technical approaches, cite existing patterns
5. **Explicit unknowns:** Flag gaps in knowledge rather than guessing
6. **Stop when complete:** Once spec is approved, workflow is done

## What NOT to Do

**Explicitly forbidden actions:**

1. **❌ Do NOT start implementing the spec**
   - This prompt creates specifications only
   - Implementation happens in a separate workflow
   - Stop after Phase 5 - do not write code

2. **❌ Do NOT skip clarifying questions**
   - Even if the request seems clear, ask questions
   - Phase 2 is mandatory, not optional
   - Better to over-clarify than make assumptions

3. **❌ Do NOT make technical decisions without evidence**
   - Don't suggest technologies without checking codebase-context
   - Don't recommend patterns that don't exist in the codebase
   - Always cite existing code or docs when suggesting approaches

4. **❌ Do NOT write specs in isolation**
   - Check for codebase-context document first
   - Check for related existing specs
   - Ask user about integration with existing features

5. **❌ Do NOT proceed without user validation**
   - Stop at every ⛔ checkpoint
   - Wait for user answers before continuing
   - Don't batch all questions at once

6. **❌ Do NOT include implementation details (HOW)**
   - Focus on WHAT (features) and WHY (value)
   - Leave HOW (implementation) to developers
   - Exception: When architectural constraints exist

7. **❌ Do NOT assume requirements**
   - If something is unclear, ask
   - Flag unknowns explicitly in "Open Questions"
   - Mark confidence levels honestly

8. **❌ Do NOT continue after spec is approved**
   - Once user says "approved", workflow ends
   - Do not start task breakdown
   - Do not begin implementation

## Quality Checklist

Before finalizing the spec, verify:

- [ ] All clarifying questions answered
- [ ] User stories include "As a... I want... so that..."
- [ ] Functional requirements are numbered and specific
- [ ] Non-goals explicitly stated
- [ ] Technical feasibility assessed with confidence levels
- [ ] Codebase-context referenced (if available)
- [ ] Open questions documented with confidence levels
- [ ] Output saved to correct location with correct filename format
