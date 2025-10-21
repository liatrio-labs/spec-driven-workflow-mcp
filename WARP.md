# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a **Spec Driven Development (SDD) MCP** project that provides a ubiquitous framework for spec driven development using MCP (Model Context Protocol) technology. The framework consists of structured Markdown prompts and workflows that guide AI agents through specification creation, task list generation, and task management.

## Development Environment

- **Python**: 3.12 (see `.python-version`)
- **Package Manager**: `uv` (modern Python package and project manager)
- **Dependencies**: FastMCP for building MCP servers and clients
- **Release Process**: Semantic Release via GitHub Actions (planned)

## Common Development Commands

### Environment Setup

```bash
# Install dependencies
uv sync

# Activate virtual environment (if needed)
source .venv/bin/activate
```

### Running the Application

```bash
# Run the basic hello script
python hello.py

# Run with uv
uv run hello.py
```

### Development Tools

```bash
# Install development dependencies
uv sync --group dev

# Install pre-commit hooks (when available)
pre-commit install
```

## Architecture and Structure

### Core Framework Components

The project implements a **prompt-driven workflow system** with three main phases:

1. **Specification Generation** (`prompts/generate-spec.md`)
   - Guides creation of detailed feature specifications
   - Uses structured questioning to gather requirements
   - Outputs numbered specs in `/tasks/` directory as `[n]-spec-[feature-name].md`

2. **Task List Generation** (`prompts/generate-task-list-from-spec.md`)
   - Converts specifications into actionable task lists
   - Creates demoable units of work with proof artifacts
   - Outputs task files as `tasks-[spec-file-name].md`

3. **Task Management** (`prompts/manage-tasks.md`)
   - Provides guidelines for executing and tracking tasks
   - Defines task states: `[ ]` (not started), `[~]` (in progress), `[x]` (completed)
   - Enforces one-task-at-a-time completion protocol

### Key Design Principles

- **Simple**: Transparent access to underlying tools and processes
- **Ubiquitous**: Works with any AI agent and model
- **Reliable**: Delivers consistent results through structured workflows
- **Flexible**: Compatible with existing workflows and tools
- **Scalable**: Handles projects of any size

### Workflow States and Transitions

Tasks follow a strict progression:

- Parent tasks contain demoable units of work with demo criteria and proof artifacts
- Subtasks must be completed sequentially (one at a time)
- All subtasks must pass tests before parent task completion
- Each completed parent task requires a commit using conventional commit format

## File Organization

```
/
├── prompts/                    # Core SDD workflow prompts
│   ├── generate-spec.md       # Specification generation workflow
│   ├── generate-task-list-from-spec.md  # Task list creation from specs
│   └── manage-tasks.md        # Task execution and management guidelines
├── tasks/                     # Generated specs and task lists (created as needed)
│   ├── [n]-spec-[name].md    # Feature specifications
│   └── tasks-[spec].md       # Task lists derived from specs
├── hello.py                   # Basic test script
├── pyproject.toml            # Python project configuration
├── uv.lock                   # Dependency lock file
└── README.md                 # Project documentation
```

## Working with the SDD Framework

### Generating a New Feature Spec

Reference the `prompts/generate-spec.md` workflow to create specifications. The process involves:

1. Providing initial feature description
2. Answering structured clarifying questions
3. Generating spec with required sections (goals, user stories, requirements, etc.)
4. Saving as `/tasks/[n]-spec-[feature-name].md`

### Creating Task Lists from Specs

Use `prompts/generate-task-list-from-spec.md` to convert specs into actionable tasks:

1. Analyze existing spec file
2. Generate high-level parent tasks (demoable units)
3. Break down into detailed subtasks
4. Save as `/tasks/tasks-[spec-file-name].md`

### Task Execution Protocol

Follow `prompts/manage-tasks.md` guidelines:

- Work on one subtask at a time
- Mark tasks in progress with `[~]`
- Complete full test suite before marking parent tasks complete
- Use conventional commits for completed parent tasks
- Update relevant files section as you work

## Important Notes

- The `/tasks/` directory is created dynamically as specs and task lists are generated
- Each parent task must include **Demo Criteria** and **Proof Artifact(s)** - these are mandatory
- Task completion requires passing all tests and proper commit messages
- The framework is designed to work with any AI tool and model through MCP technology

## Future Planned Features

- User-defined output formats (Markdown, Jira, GitHub issues)
- Customizable prompts for the SDD workflow
- Integration with project management tools via MCP
