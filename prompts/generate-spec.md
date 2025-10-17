---
name: generate-spec
description: Generate a Specification (Spec) for a feature
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

## Process

1. **Receive Initial Prompt:** The user provides a brief description or request for a new feature or functionality.
2. **Ask Clarifying Questions:** Before writing the Spec, the AI *must* ask clarifying questions to gather sufficient detail. The goal is to understand the "what" and "why" of the feature, not necessarily the "how" (which the developer will figure out). Make sure to provide options in letter/number lists so I can respond easily with my selections.
3. **Generate Spec:** Based on the initial prompt and the user's answers to the clarifying questions, generate a Spec using the structure outlined below.
4. **Save Spec:** Save the generated document as `[n]-spec-[feature-name].md` inside the `/tasks` directory. (Where `n` is a zero-padded 4-digit sequence starting from 0001, e.g., `0001-spec-user-authentication.md`.)

## Clarifying Questions (Examples)

The AI should adapt its questions based on the prompt, but here are some common areas to explore:

* **Problem/Goal:** "What problem does this feature solve for the user?" or "What is the main goal we want to achieve with this feature?"
* **Target User:** "Who is the primary user of this feature?"
* **Core Functionality:** "Can you describe the key actions a user should be able to perform with this feature?"
* **User Stories:** "Could you provide a few user stories? (e.g., As a [type of user], I want to [perform an action] so that [benefit].)"
* **Acceptance Criteria:** "How will we know when this feature is successfully implemented? What are the key success criteria?"
* **Scope/Boundaries:** "Are there any specific things this feature *should not* do (non-goals)?"
* **Data Requirements:** "What kind of data does this feature need to display or manipulate?"
* **Design/UI:** "Are there any existing design mockups or UI guidelines to follow?" or "Can you describe the desired look and feel?"
* **Edge Cases:** "Are there any potential edge cases or error conditions we should consider?"
* **Unit of Work:** "What is the smallest end-to-end slice we can ship that a user or stakeholder can experience, test, or demonstrate?"
* **Demoability:** "For each stage, how will we show working value (e.g., URL, CLI output, screenshot, test run, short demo script)?"

## Spec Structure

The generated Spec should include the following sections:

1. **Introduction/Overview:** Briefly describe the feature and the problem it solves. State the goal.
2. **Goals:** List the specific, measurable objectives for this feature.
3. **User Stories:** Detail the user narratives describing feature usage and benefits.
4. **Demoable Units of Work:** Define small, end-to-end vertical slices. For each slice capture: Purpose and users; Demo Criteria (what will be shown to verify value); Proof Artifact(s) (tangible evidence such as a URL, CLI command & expected output, test names, or screenshot).
5. **Functional Requirements:** List the specific functionalities the feature must have. Use clear, concise language (e.g., "The system must allow users to upload a profile picture."). Number these requirements.
6. **Non-Goals (Out of Scope):** Clearly state what this feature will *not* include to manage scope.
7. **Design Considerations (Optional):** Link to mockups, describe UI/UX requirements, or mention relevant components/styles if applicable.
8. **Technical Considerations (Optional):** Mention any known technical constraints, dependencies, or suggestions (e.g., "Should integrate with the existing Auth module").
9. **Success Metrics:** How will the success of this feature be measured? (e.g., "Increase user engagement by 10%", "Reduce support tickets related to X").
10. **Open Questions:** List any remaining questions or areas needing further clarification.

## Target Audience

Assume the primary reader of the Spec is a **junior developer**. Therefore, requirements should be explicit, unambiguous, and avoid jargon where possible. Provide enough detail for them to understand the feature's purpose and core logic.

## Output

* **Format:** Markdown (`.md`)
* **Location:** `/tasks/`
* **Filename:** `[n]-spec-[feature-name].md`

## Final instructions

1. Do NOT start implementing the Spec
2. Make sure to ask the user clarifying questions
3. Take the user's answers to the clarifying questions and improve the Spec
4. Save the completed Spec to `/tasks/[n]-spec-[feature-name].md`
5. Ask the user if they are satisfied with it and if they have any additional questions or clarifications
6. Once the user is satisfied with the Spec, this workflow is complete and you should stop working
