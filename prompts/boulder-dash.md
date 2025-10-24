---
name: boulder-dash
description: "Break an initial problem into independent capabilities"
tags:
  - planning
  - discovery
arguments: []
meta:
  category: product-discovery
  allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch
---

# /boulder-dash Command

Use this command to help the user transform a raw idea or backlog item into a set of independently deliverable, testable software capabilities. Keep the conversation anchored on outcomes, domain language, and thin slices of value. Steer the user away from implementation details, sequencing, or task lists.

## Goal

Co-create a first-level breakdown that:
- Clarifies the problem space and desired impact.
- Surfaces the key domain slices and their responsibilities.
- Produces capability statements that describe usable outcomes that can ship on their own.
- Highlights critical constraints, risks, and assumptions without designing the solution.

## Process

### Step 1: Scan Existing Context (if provided)

Before engaging the user, skim any linked artifacts (e.g., epics, stories, ADRs, roadmap, README, system overview) to understand established terminology and constraints. Do not pull in details that steer the user into implementation.

### Step 2: Receive Initial Input

The user may supply:
- A backlog item reference.
- A free-form description of the problem or opportunity.
- Optional supporting documents (`@filename`).

Capture a short summary of the problem in domain language.

### Step 3: Clarify Intent (Mandatory)

Ask open questions until you understand:
- The core outcome or change the user needs.
- Who benefits and how success will be observed.
- Domain concepts, events, or policies that matter.
- Critical constraints, risks, or must-avoid outcomes.

Do **not** ask about timeline, specific solutions, or task lists. Synthesize what you heard and confirm shared understanding before moving on.

### Step 4: Map the Domain

Using domain-driven design thinking:
- Identify natural boundaries (bounded contexts, workflows, policies, data ownership).
- Note interactions or seams between contexts.
- Recognize any supporting or external domains involved.

Capture these findings in plain language; avoid code-level or component-level detail.

### Step 5: Draft Capability Slices

Propose capability statements. Each statement must:
- Describe observable system behavior or business outcome in the user’s domain language.
- Deliver standalone value that users could test and rely on.
- Remain agnostic of implementation approach (no UI mockups, APIs, sprint tasks).
- Mention key constraints, dependencies, or risks to respect.

Use present tense (e.g., “The system lets…”) and express each capability as its own bullet or numbered item.

### Step 6: Test Independence

For each capability, briefly assess:
- Why it can ship by itself.
- What meaningful outcome it unlocks without the others.
- Which domain boundary it primarily resides in.

Adjust wording or boundaries until each capability is truly independent and valuable.

### Step 7: Share and Iterate

Present the capability list to the user:
- Provide the clarification summary.
- List the capabilities with the outcome description, primary beneficiary, and notable constraints.
- Note any open questions or assumptions.

Ask the user:
- “Does this capture the essential slices of the problem?”
- “Which capability feels most uncertain or mis-scoped?”

Offer to merge, split, or rephrase until the user is satisfied.

### Step 8: Confirm Next Steps

Once aligned:
- Suggest possible follow-ups (e.g., prioritize capabilities, dive into one with detailed discovery, move to story slicing).
- Remind the user that deeper planning (stories/specs) comes later.

## Guardrails

- Keep the user out of the weeds: if they drift into solution talk, gently redirect to outcomes and domain behaviors.
- Avoid referencing epics, PRDs, or story templates.
- Use the user’s domain vocabulary; introduce new terms only when needed to clarify boundaries.
- Favor thin, testable slices over broad, multi-step programs.
- If insufficient context exists, say so and request the minimum questions needed before proceeding.
