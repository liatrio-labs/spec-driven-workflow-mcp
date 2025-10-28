# Command: Generate PRD from Jira Story

## Purpose

This command researches a Jira story using the Atlassian MCP integration, gathers relevant architecture context, and generates a comprehensive Product Requirements Document (PRD) suitable for implementation by a junior developer.

## Usage

```
/jira-to-prd <JIRA-KEY> [--update]
```

**Examples**:
- `/jira-to-prd PROJ-1234` - Generate new PRD
- `/jira-to-prd PROJ-1234 --update` - Update existing PRD with latest Jira changes

## Prerequisites

- **Atlassian MCP server** must be configured and running
- User must have access to the Jira project/story
- Architecture documentation should exist (uses `/architecture` command)

## Workflow

### Phase 0: Determine Mode (New vs Update)

**If `--update` flag is present**:
1. **Check for existing PRD**:
   - Search `tasks/` directory for `prd-[jira-key]-*.md`
   - If found, proceed to Update Mode workflow
   - If not found, warn user and proceed with New PRD workflow

**If no `--update` flag**:
- Proceed directly to Phase 1 (New PRD workflow)

---

## New PRD Workflow

### Phase 1: Research Jira Story

1. **Fetch Jira Story Details** using Atlassian MCP:
   - Use `mcp__jira_get_issue` (or equivalent MCP tool) to retrieve story details
   - Extract: Title, Description, Acceptance Criteria, Comments, Subtasks, Linked Issues
   - Capture: Status, Priority, Assignee, Reporter, Labels, Story Points

2. **Analyze Story Context**:
   - Identify mentioned components/services in description
   - Extract technical requirements from acceptance criteria
   - Parse user stories if present in description
   - Note any referenced documentation or design links

### Phase 2: Gather Architecture Context

3. **Query Architecture Documentation**:
   - Run `/architecture [components-mentioned-in-story]` to understand:
     - Existing services and their responsibilities
     - Shared libraries that should be used
     - Data storage patterns (PostgreSQL, DynamoDB, S3)
     - Messaging patterns (SQS/SNS)
     - Authentication/authorization mechanisms
   - Identify related microservices that may need changes
   - Check for existing similar features to reference

4. **Check for Shared Library Usage**:
   - If story involves common patterns (queues, events, storage, auth), use `/find-library-usage` to find examples
   - Identify which shared libraries (e.g., `SHARED-LIB-PREFIX.Shared.*`) should be leveraged
   - Note anti-patterns to avoid based on library documentation

### Phase 3: Interactive Clarification

5. **Ask Clarifying Questions** (adapt based on Jira story completeness):
   - **Problem/Goal**: "What problem does this feature solve for the user?" (if not clear from Jira)
   - **Target User**: "Who is the primary user of this feature?" (supplement Jira persona)
   - **Core Functionality**: "Can you describe the key actions a user should be able to perform?" (beyond acceptance criteria)
   - **User Stories**: "Are there additional user stories beyond what's in Jira?"
   - **Acceptance Criteria**: "Are there additional success criteria not captured in the Jira story?"
   - **Scope/Boundaries**: "Are there specific things this feature *should not* do (non-goals)?"
   - **Data Requirements**: "What kind of data does this feature need to display or manipulate?"
   - **Design/UI**: "Are there design mockups or UI guidelines to follow?" (check Jira attachments first)
   - **Edge Cases**: "Are there potential edge cases or error conditions we should consider?"
   - **Architecture Fit**: "Should this be a new service, or enhance existing service [X]?" (based on architecture query)
   - **Shared Libraries**: "Should we use [discovered shared library] for [functionality]?" (based on library search)

   **Format**: Provide options as letter/number lists for easy responses.

### Phase 4: Generate PRD

6. **Create Comprehensive PRD** using this structure:

   ```markdown
   # PRD: [Feature Name from Jira]

   **Jira Story**: [JIRA-KEY] - [Link to Jira]
   **Status**: [Current Jira Status]
   **Priority**: [Jira Priority]
   **Story Points**: [Points if available]

   ---

   ## Table of Contents

   **IMPORTANT**: Include actual line numbers when creating the document. Agents can then reference specific sections efficiently (e.g., "See lines 45-67 for Functional Requirements").

   - [Introduction/Overview](#1-introductionoverview) (lines ~15-25)
   - [Goals](#2-goals) (lines ~27-35)
   - [User Stories](#3-user-stories) (lines ~37-50)
   - [Functional Requirements](#4-functional-requirements) (lines ~52-75)
   - [Non-Goals](#5-non-goals-out-of-scope) (lines ~77-85)
   - [Architecture & Technical Considerations](#6-architecture--technical-considerations) (lines ~87-130)
   - [Design Considerations](#7-design-considerations) (lines ~132-145)
   - [Success Metrics](#8-success-metrics) (lines ~147-165)
   - [Implementation Guidance](#9-implementation-guidance) (lines ~167-190)
   - [Dependencies & Risks](#10-dependencies--risks) (lines ~192-210)
   - [Open Questions](#11-open-questions) (lines ~212-225)

   ---

   ## 1. Introduction/Overview

   [Brief description from Jira + problem statement]

   **Source**: This PRD is based on Jira story [JIRA-KEY] and supplemented with architecture research.

   ## 2. Goals

   [Specific, measurable objectives - derived from Jira + clarifications]

   ## 3. User Stories

   [User narratives from Jira description + additional stories from clarifications]

   Format:
   - As a [type of user], I want to [perform an action] so that [benefit].

   ## 4. Functional Requirements

   [Requirements from Jira acceptance criteria + clarifications]

   1. The system must...
   2. The system must...
   [Number each requirement clearly]

   ## 5. Non-Goals (Out of Scope)

   [Things this feature will NOT include - manage scope creep]

   ## 6. Architecture & Technical Considerations

   ### Affected Services
   [List microservices that need changes based on architecture research]

   ### Shared Libraries to Use
   [Specific shared libraries identified from `/find-library-usage`]
   - `SHARED-LIB-PREFIX.Shared.Queue` - For SQS message processing
   - `SHARED-LIB-PREFIX.Shared.Events` - For publishing domain events
   - [etc.]

   ### Data Storage
   [PostgreSQL tables, DynamoDB tables, S3 buckets - based on architecture patterns]

   ### Integration Points
   [APIs to call, events to publish/consume, queues to process]

   ### Authentication/Authorization
   [JWT, tenant isolation, RBAC requirements]

   ### Anti-Patterns to Avoid
   [Based on shared library documentation and architecture guide]

   ## 7. Design Considerations

   [Link to Jira attachments, describe UI/UX requirements, mention components/styles]

   ## 8. Success Metrics

   [How success will be measured - from Jira + clarifications]
   - Acceptance Criteria from Jira:
     - [List from Jira acceptance criteria]
   - Additional Metrics:
     - [User-provided or inferred metrics]

   ## 9. Implementation Guidance for Junior Developers

   ### Recommended Approach
   [Step-by-step guidance based on architecture research]

   1. **Start with**: [Service/component to modify first]
   2. **Use this pattern**: [Reference to similar implementation found via `/find-library-usage`]
   3. **Test locally**: [Guidance on local testing with K3D/Tilt or Docker]

   ### Code Examples to Reference
   [Specific files/line numbers from `/find-library-usage` results]

   ### Documentation to Read
   [Links to architecture docs, shared library READMEs]

   ## 10. Open Questions

   [Remaining questions or areas needing further clarification]

   ## 11. Related Jira Issues

   [Linked issues, subtasks, dependencies from Jira]

   ## 12. Appendix: Jira Story Details

   **Description** (from Jira):
   ```
   [Full Jira description]
   ```

   **Comments** (from Jira):
   [Relevant comments that provide context]

   **Attachments**: [List Jira attachments with links]
   ```

### Phase 5: Save and Inform

7. **Save PRD**:
   - Filename: `tasks/prd-[jira-key]-[feature-name].md`
   - Example: `tasks/prd-PROJ-1234-user-authentication.md`

8. **Generate Task List** (optional but recommended):
   - After saving PRD, offer to run `/generate-task-list-from-prd tasks/prd-[filename].md`
   - This creates actionable subtasks for the developer

9. **Summary Output**:
   ```
   ✅ PRD Generated: tasks/prd-[jira-key]-[feature-name].md

   **Jira Story**: [JIRA-KEY] - [Title]
   **Architecture Context**:
   - Affects [N] microservices: [list]
   - Uses [N] shared libraries: [list]
   - Integration points: [list]

   **Next Steps**:
   1. Review the PRD in tasks/prd-[filename].md
   2. Run `/generate-task-list-from-prd tasks/prd-[filename].md` to create implementation tasks
   3. Review architecture documentation: Run `/architecture [service-name]` for more details
   ```

## Important Constraints

- **Do NOT start implementing** the PRD or writing code
- **Do NOT make assumptions** - always ask clarifying questions
- **Do NOT skip architecture research** - this is critical for correct implementation guidance
- **Do NOT duplicate shared library functionality** - leverage existing libraries
- **DO reference specific line numbers** from `/find-library-usage` results where helpful
- **DO provide multiple implementation options** if architecture research reveals alternatives

## Error Handling

- **If Jira story not found**: Ask user to verify Jira key and their access permissions
- **If architecture context missing**: Proceed with PRD but note in "Open Questions" that architecture review is needed
- **If Atlassian MCP unavailable**: Ask user to provide Jira story details manually and proceed with reduced automation

## Example MCP Tool Usage

```typescript
// Example Atlassian MCP tool calls (adapt to actual MCP tools available)

// Fetch issue
const issue = await mcp__jira_get_issue({ issueKey: "PROJ-1234" });

// Get issue comments
const comments = await mcp__jira_get_comments({ issueKey: "PROJ-1234" });

// Get linked issues
const links = await mcp__jira_get_issue_links({ issueKey: "PROJ-1234" });

// Get subtasks
const subtasks = await mcp__jira_get_subtasks({ issueKey: "PROJ-1234" });
```

## Integration with Existing Commands

This command integrates seamlessly with:

1. **`/architecture`** - Queries architecture documentation for context
2. **`/find-library-usage`** - Finds shared library usage examples
3. **`/generate-task-list-from-prd`** - Creates implementation tasks from generated PRD
4. **`/check-docs`** - Looks up specific technology documentation if needed

---

## Update PRD Workflow

Use this workflow when `--update` flag is present.

### Phase 1: Load Existing PRD

1. **Locate Existing PRD**:
   - Find file matching `tasks/prd-[jira-key]-*.md`
   - Read current PRD content
   - Parse existing sections and metadata

2. **Extract Current State**:
   - Current requirements list
   - Current architecture decisions
   - Implementation progress notes (if any)
   - Open questions from previous version

### Phase 2: Fetch Updated Jira Data

3. **Fetch Latest Jira Story** using Atlassian MCP:
   - Use `mcp__jira_get_issue` to get current story state
   - Extract: Updated description, acceptance criteria, comments, status
   - Capture: New attachments, new linked issues, new subtasks

4. **Compare Changes**:
   - Identify differences between Jira and existing PRD:
     - ✏️ Changed: Description, acceptance criteria, priority
     - ➕ Added: New comments, new attachments, new linked issues
     - ❌ Removed: Deleted subtasks or links
     - 📊 Status: Story status changes (To Do → In Progress → Done)
   - Flag significant changes that require PRD updates

### Phase 3: Selective Update Strategy

5. **Determine Update Scope**:
   - **Minor changes** (comments, status, minor wording):
     - Update metadata only (Status, Priority, Story Points)
     - Append new comments to Appendix
     - Preserve all existing PRD content

   - **Significant changes** (acceptance criteria, scope, requirements):
     - Update affected sections (Goals, Functional Requirements, Success Metrics)
     - Preserve Architecture & Technical Considerations unless architecture changed
     - Add "Update History" section tracking what changed and when
     - Keep Implementation Guidance unless invalidated by changes

6. **Interactive Confirmation**:
   ```
   📋 **Changes Detected in [JIRA-KEY]**:

   ✏️ Changed:
   - Description updated (3 lines added, 1 removed)
   - Acceptance Criteria #3 modified
   - Priority changed: Medium → High

   ➕ Added:
   - New comment from [User] on [Date]
   - New linked issue: [JIRA-KEY-2]

   📊 Status: In Progress → In Review

   **Recommended Updates**:
   - Section 4 (Functional Requirements) - Update FR-3 based on new acceptance criteria
   - Section 8 (Success Metrics) - Update based on new acceptance criteria
   - Section 12 (Appendix) - Add new comments
   - Metadata - Update status and priority

   **Preserving**:
   - Section 6 (Architecture & Technical Considerations) - No architecture changes detected
   - Section 9 (Implementation Guidance) - Still valid

   Proceed with updates? (y/n)
   ```

### Phase 4: Apply Updates

7. **Update PRD Sections**:
   - **Always Update**:
     - Metadata (Status, Priority, Story Points)
     - Section 12 (Appendix) - Add new Jira comments/attachments

   - **Conditionally Update** (based on changes):
     - Section 1 (Introduction) - If description changed
     - Section 2 (Goals) - If objectives changed
     - Section 4 (Functional Requirements) - If acceptance criteria changed
     - Section 8 (Success Metrics) - If acceptance criteria changed
     - Section 11 (Related Jira Issues) - If links/subtasks changed

   - **Preserve Unless Invalidated**:
     - Section 6 (Architecture & Technical Considerations) - User confirmation required
     - Section 9 (Implementation Guidance) - User confirmation required
     - Section 10 (Open Questions) - Keep existing, can append new ones

8. **Add Update History Section**:
   ```markdown
   ## 13. Update History

   ### Update: [Date]
   **Jira Status**: [Old Status] → [New Status]

   **Changes Applied**:
   - Updated Functional Requirement FR-3 based on modified acceptance criteria
   - Updated Success Metrics to reflect new acceptance criteria
   - Added 2 new comments to Appendix
   - Updated priority: Medium → High

   **Preserved**:
   - Architecture decisions remain valid
   - Implementation guidance still applicable

   **Source**: Jira story [JIRA-KEY] as of [Date]
   ```

### Phase 5: Save and Inform

9. **Save Updated PRD**:
   - Overwrite existing PRD file (preserve filename)
   - Maintain all custom notes/annotations if present

10. **Summary Output**:
    ```
    ✅ PRD Updated: tasks/prd-[jira-key]-[feature-name].md

    **Jira Story**: [JIRA-KEY] - [Title]
    **Status Change**: [Old Status] → [New Status]

    **Updates Applied**:
    - ✏️ Modified: [N] sections
    - ➕ Added: [N] new items
    - 🔒 Preserved: [N] sections unchanged

    **Key Changes**:
    - [Brief summary of most important changes]

    **Next Steps**:
    1. Review updated PRD in tasks/prd-[filename].md
    2. If architecture changed, consider re-running `/architecture [service]`
    3. If implementation in progress, verify guidance still applies
    ```

---

## Tips for Best Results

1. **Complete Jira Stories**: Ensure Jira story has description, acceptance criteria, and context
2. **Run Early**: Use this command during story refinement to identify missing information
3. **Iterate**: After initial PRD generation, refine based on team feedback
4. **Link Back**: Update Jira story with link to generated PRD in `tasks/` directory
5. **Keep Updated**: Use `--update` flag when Jira story changes to refresh the PRD
6. **Update Regularly**: Run updates when story status changes or acceptance criteria evolve
7. **Preserve Progress**: Update mode preserves implementation notes and custom annotations

## Target Audience

The generated PRD is written for **junior developers** with:
- Explicit requirements
- Clear architecture guidance
- Specific library references
- Step-by-step implementation suggestions
- Links to examples and documentation

## Success Criteria

A successful PRD generation includes:
- ✅ All Jira story details captured
- ✅ Architecture context researched and documented
- ✅ Shared libraries identified with usage examples
- ✅ Clear functional requirements numbered
- ✅ Technical considerations with specific service/library names
- ✅ Implementation guidance for junior developers
- ✅ Open questions documented for follow-up