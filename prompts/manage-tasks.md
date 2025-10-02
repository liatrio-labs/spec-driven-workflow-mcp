---
description: Guidelines for managing task lists and working on tasks/subtasks
allowed-tools: Glob, Grep, LS, Read, Edit, MultiEdit, Write, WebFetch, WebSearch
---

# Task List Management

Guidelines for managing task lists in markdown files to track progress on completing a Spec

## Task Implementation

- Tasks can be in one of three states:
  - `[ ]` - Not started
  - `[x]` - Completed
  - `[~]` - In progress
- **One sub-task at a time:** Do **NOT** start the next sub‑task until all previous sub‑tasks are completed.
- **Mark in-progress:** When you start a sub‑task, immediately mark it as in-progress by changing `[ ]` to `[~]`. Update the parent task to `[~]` if it is not already `[~]`.
- **Parent Task and Subtask Relationship:**
  - A parent task can have multiple subtasks
  - A subtask can only have one parent task
  - The status of the parent task must always be inline with the status of its subtasks
- **Completion protocol:**
  1. When you finish a **sub‑task**, immediately mark it as completed by changing `[~]` to `[x]`.
  2. If **all** subtasks underneath a parent task are now `[x]`, follow this sequence:
      - **First**: Run the full test suite (`pytest`, `npm test`, `bin/rails test`, etc.)
      - **Only if all tests pass**: Stage changes (`git add .`)
      - **Validate changes**: Run any additional validation steps as specified in the Spec. Also check that the demo criteria and demo artifacts are met.
      - **Clean up**: Remove any temporary files and temporary code before committing
      - **Commit**: Use a descriptive commit message that:
        - Uses conventional commit format (`feat:`, `fix:`, `refactor:`, etc.)
        - Summarizes what was accomplished in the parent task
        - Lists key changes and additions
        - References the task number and Spec context
        - **Formats the message as a single-line command using `-m` flags**, for example:

            ```bash
            git commit -m "feat: add payment validation logic" -m "- Validates card type and expiry" -m "- Adds unit tests for edge cases" -m "Related to T123 in Spec"
            ```

  3. Once all the subtasks are marked completed and changes have been committed, mark the **parent task** as completed.
  4. After marking a parent task as completed, proceed to the next open task.
  5. If there are no open tasks available in the list, prompt the user for how to proceed.

## Task List Maintenance

1. **Update the task list as you work:**
   - Mark tasks and subtasks as completed (`[x]`) per the protocol above.
   - Add new tasks as they emerge.

2. **Maintain the "Relevant Files" section:**
   - List every file created or modified.
   - Give each file a one‑line description of its purpose.

## Guidelines

When working with task lists, the AI must:

1. Regularly update the task list file after finishing any significant work.
2. Follow the completion protocol outlined above.
3. Add newly discovered tasks.
4. Keep "Relevant Files" accurate and up to date.
5. Before starting work, check which sub‑task is next.
6. After implementing a sub‑task, update the file and then pause for user approval.

## Instructions

1. Find the most recent task list file in the `/tasks/` directory.
2. Follow the guidelines above to manage the task list.
3. Analyze the task list to determine what to do next:
   - If there is a task that is marked as in-progress, stop processing these instructions and continue working on that task.
   - If there are any open tasks in the list, stop processing these instructions and continue working on the next open task.
   - If there are no open tasks available in the list, prompt the user for how to proceed.
