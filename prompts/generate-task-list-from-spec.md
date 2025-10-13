---
name: generate-task-list-from-spec
title: Generate Task List From Spec
description: Generate a task list from a Spec
tags:
  - planning
  - tasks
arguments: []
meta:
  category: spec-development
  allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch
---

## Generate Task List From Spec

## Goal

To guide an AI assistant in creating a detailed, step-by-step task list in Markdown format based on an existing Specification (Spec). The task list should guide a developer through implementation.

## Output

- **Format:** Markdown (`.md`)
- **Location:** `/tasks/`
- **Filename:** `tasks-[spec-file-name].md` (e.g., if the Spec is `0001-spec-user-profile-editing.md`, save as `tasks-0001-spec-user-profile-editing.md`)

## Process

1. **Receive Spec Reference:** The user points the AI to a specific Spec file
2. **Analyze Spec:** The AI reads and analyzes the functional requirements, user stories, and other sections of the specified Spec.
3. **Define Demoable Units of Work:** Identify thin, end-to-end vertical slices from the Spec. Each parent task must correspond to a demoable unit of work.
4. **Assess Current State:** Review the existing codebase to understand existing infrastructre, architectural patterns and conventions. Also, identify any existing components or features that already exist and could be relevant to the Spec requirements. Then, identify existing related files, components, and utilities that can be leveraged or need modification.
5. **Phase 1: Generate Parent Tasks:** Based on the Spec analysis and current state assessment, create the file and generate the main, high-level tasks required to implement the feature. Use your judgement on how many high-level tasks to use. It's likely to be about five tasks.
6. **Inform the user:** Present these tasks to the user in the specified format (without sub-tasks yet) For example, say "I have generated the high-level tasks based on the Spec. Ready to generate the sub-tasks? Respond with 'Generate sub tasks' to proceed." .
7. **Wait for Confirmation:** Pause and wait for the user to respond with "Generate sub tasks".
8. **Phase 2: Generate Sub-Tasks:** Once the user confirms, break down each parent task into smaller, actionable sub-tasks necessary to complete the parent task. Ensure sub-tasks logically follow from the parent task, cover the implementation details implied by the Spec, and consider existing codebase patterns where relevant without being constrained by them.
9. **Identify Relevant Files:** Based on the tasks and Spec, identify potential files that will need to be created or modified. List these under the `Relevant Files` section, including corresponding test files if applicable.
10. **Generate Final Output:** Combine the parent tasks, sub-tasks, relevant files, and notes into the final Markdown structure.
11. **Save Task List:** Save the generated document in the `/tasks/` directory with the filename `tasks-[spec-file-name].md`, where `[spec-file-name]` matches the base name of the input Spec file (e.g., if the input was `0001-spec-user-profile-editing.md`, the output is `tasks-0001-spec-user-profile-editing.md`).

## Output Format

Every parent task must include **Demo Criteria** and **Proof Artifact(s)**. These are mandatory.

The generated task list _must_ follow this example structure:

```markdown
## Relevant Files

- `path/to/potential/file1.ts` - Brief description of why this file is relevant (e.g., Contains the main component for this feature).
- `path/to/file1.test.ts` - Unit tests for `file1.ts`.
- `path/to/another/file.tsx` - Brief description (e.g., API route handler for data submission).
- `path/to/another/file.test.tsx` - Unit tests for `another/file.tsx`.
- `lib/utils/helpers.ts` - Brief description (e.g., Utility functions needed for calculations).
- `lib/utils/helpers.test.ts` - Unit tests for `helpers.ts`.

### Notes

- Unit tests should typically be placed alongside the code files they are testing (e.g., `MyComponent.tsx` and `MyComponent.test.tsx` in the same directory).
- Use `npx jest [optional/path/to/test/file]` to run tests. Running without a path executes all tests found by the Jest configuration.

## Tasks

- [ ] 1.0 Parent Task Title
  - Demo Criteria: "Open /path and complete X end-to-end; acceptance: Y visible/returned"
  - Proof Artifact(s): "URL: https://..., CLI: command & expected output, Test: MyFeature.test.ts"
  - [ ] 1.1 [Sub-task description 1.1]
  - [ ] 1.2 [Sub-task description 1.2]
- [ ] 2.0 Parent Task Title
  - Demo Criteria: "User can perform Z with persisted state"
  - Proof Artifact(s): "Screenshot of flow; link to test suite section"
  - [ ] 2.1 [Sub-task description 2.1]
- [ ] 3.0 Parent Task Title (may not require sub-tasks if purely structural or configuration)
  - Demo Criteria: "Configuration is verifiable via command/output"
  - Proof Artifact(s): "CLI: config get … -> expected value; log line; diff link"
```

## Interaction Model

The process explicitly requires a pause after generating parent tasks to get user confirmation ("Go") before proceeding to generate the detailed sub-tasks. This ensures the high-level plan aligns with user expectations before diving into details.

## Target Audience

Assume the primary reader of the task list is a **junior developer** who will implement the feature with awareness of the existing codebase context.

## After Subtask Generation

- Prompt the user to review the generated task list and provide feedback.
- Wait for instructions on next steps.
- DO NOT begin implementation; that will be handled through other means.
- Prioritize execution so each completed parent task yields a demoable increment with Demo Criteria and Proof Artifact(s) verified.
