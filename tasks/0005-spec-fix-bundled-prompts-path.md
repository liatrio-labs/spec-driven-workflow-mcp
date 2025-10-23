# Specification: Fix Bundled Prompts Directory Resolution for Remote Installation

## Introduction/Overview

When users install and run `sdd-generate-commands` via `uvx` from a remote Git repository, the tool fails to locate the bundled `prompts` directory. This occurs because the `--prompts-dir` parameter defaults to `Path("prompts")` (a relative path), and the fallback logic in `_find_package_prompts_dir()` doesn't correctly resolve the installed package's prompts location.

**Current Error:**

```text
Error: Prompts directory does not exist: prompts

To fix this:
  - Ensure the prompts directory exists
  - Check that --prompts-dir points to a valid directory (current: prompts)
```

**Goal:** Enable seamless remote installation and execution via `uvx` by correctly resolving the bundled prompts directory, while maintaining backward compatibility for local development and custom prompts directories.

## Goals

1. **Primary Goal:** Fix the prompts directory resolution so `uvx --from git+https://github.com/...` works without requiring `--prompts-dir`
2. **Maintain Backward Compatibility:** Ensure existing users with custom `--prompts-dir` paths continue to work unchanged
3. **Support Development Mode:** Allow developers to use local prompts directories when working from source
4. **Clear Error Messages:** When `--prompts-dir` is explicitly specified but doesn't exist, provide a clear error
5. **Robust Solution:** Implement a comprehensive fix that handles both installed and development scenarios

## User Stories

### Story 1: Remote Installation User

**As a** new user installing via `uvx` from GitHub
**I want to** run `uvx --from git+https://github.com/liatrio-labs/spec-driven-workflow@main sdd-generate-commands generate --agents windsurf`
**So that** I can generate commands without needing to clone the repository or specify a prompts directory

**Acceptance Criteria:**

- Tool automatically finds bundled prompts in the installed package
- No `--prompts-dir` argument required
- Works from any directory (e.g., user's home directory)

### Story 2: Developer Using Local Source

**As a** developer working on the project
**I want to** run `sdd-generate-commands generate` from the project root
**So that** I can test changes to prompts without reinstalling the package

**Acceptance Criteria:**

- Tool finds `./prompts` directory when run from project root
- Changes to prompt files are immediately reflected
- No need to rebuild/reinstall for prompt changes

### Story 3: User with Custom Prompts

**As a** power user with custom prompts
**I want to** specify `--prompts-dir /path/to/my/prompts`
**So that** I can use my own prompt templates

**Acceptance Criteria:**

- Custom path is respected when specified
- Clear error if specified path doesn't exist
- No fallback to bundled prompts when custom path is explicitly provided

## Demoable Units of Work

### Unit 1: Fix Default Prompts Directory Resolution

**Purpose:** Enable automatic detection of bundled prompts for installed packages
**Users:** Remote installation users (uvx, pip)

**Demo Criteria:**

- Run from home directory: `uvx --from git+https://github.com/liatrio-labs/spec-driven-workflow@BRANCH sdd-generate-commands generate --agents windsurf --dry-run`
- Command succeeds and shows prompts loaded
- No error about missing prompts directory

**Proof Artifacts:**

- Terminal output showing successful execution
- Output includes: `Prompts loaded: N` (where N > 0)
- No error messages about missing directories

### Unit 2: Validate Custom Prompts Directory Behavior

**Purpose:** Ensure explicit `--prompts-dir` works correctly with validation
**Users:** Power users with custom prompts

**Demo Criteria:**

1. Run with valid custom directory: `sdd-generate-commands generate --prompts-dir /tmp/my-prompts --agents cursor --dry-run`
   - Should succeed if directory exists with .md files
2. Run with invalid custom directory: `sdd-generate-commands generate --prompts-dir /nonexistent --agents cursor`
   - Should fail with clear error message
   - Should NOT fall back to bundled prompts

**Proof Artifacts:**

- Terminal output for both scenarios
- Error message clearly states the specified directory doesn't exist
- No fallback behavior when path is explicitly provided

### Unit 3: Verify Development Workflow

**Purpose:** Ensure local development continues to work seamlessly
**Users:** Project contributors and developers

**Demo Criteria:**

- From project root: `sdd-generate-commands generate --agents cursor --dry-run`
- Prompts loaded from `./prompts` directory
- Changes to `./prompts/*.md` are immediately reflected

**Proof Artifacts:**

- Terminal output showing prompts loaded from local directory
- Test run showing modified prompt content is used

## Functional Requirements

### FR1: Default Prompts Directory Resolution

When `--prompts-dir` is NOT specified (uses default `Path("prompts")`), the tool MUST:

1. First check if `./prompts` exists relative to current working directory
2. If not found, attempt to locate bundled prompts using `_find_package_prompts_dir()`
3. Use the first valid prompts directory found
4. Raise a clear error if no valid prompts directory is found

### FR2: Explicit Prompts Directory Validation

When `--prompts-dir` IS specified by the user, the tool MUST:

1. Use ONLY the specified path (no fallback to bundled prompts)
2. Raise a clear error if the specified directory doesn't exist
3. Raise a clear error if the specified directory exists but contains no `.md` files

### FR3: Package Prompts Directory Detection

The `_find_package_prompts_dir()` function MUST:

1. Correctly locate the prompts directory in installed packages (uvx, pip, wheel)
2. Handle both development installs (`pip install -e .`) and production installs
3. Return `None` if prompts directory cannot be found (not raise an exception)
4. Work regardless of the current working directory

### FR4: Error Messages

Error messages MUST:

1. Clearly distinguish between "default path not found" vs "specified path not found"
2. Provide actionable guidance for resolution
3. Indicate whether fallback was attempted
4. Show the actual path that was checked

### FR5: Backward Compatibility

The fix MUST:

1. Not break existing workflows that use `--prompts-dir` with valid paths
2. Not change the CLI interface or parameter names
3. Not require changes to `pyproject.toml` build configuration (prompts already bundled)
4. Maintain the same behavior for local development (running from project root)

## Non-Goals (Out of Scope)

1. **Dynamic Prompt Downloads:** Not downloading prompts from GitHub at runtime
2. **Prompt Caching:** Not implementing local caching of downloaded prompts
3. **Multiple Prompts Directories:** Not supporting multiple prompts directories simultaneously
4. **Prompt Versioning:** Not implementing version-specific prompt selection
5. **Other Installation Methods:** Only focusing on `uvx` (pip support is a side effect)
6. **Configuration Files:** Not adding config file support for default prompts directory

## Design Considerations

### Current Implementation Analysis

**File:** `slash_commands/writer.py`

**Current `_find_package_prompts_dir()` implementation:**

```python
def _find_package_prompts_dir() -> Path | None:
    """Find the prompts directory in the installed package."""
    # Goes up from writer.py to package root
    package_root = Path(__file__).parent.parent
    prompts_dir = package_root / "prompts"

    if prompts_dir.exists():
        return prompts_dir

    return None
```

**Issue:** When installed via uvx/pip, `Path(__file__).parent.parent` may not correctly resolve to the package root where prompts are bundled.

### Proposed Solution

1. **Update `_find_package_prompts_dir()`** to use multiple strategies:
   - Strategy 1: Check relative to `__file__` (current approach)
   - Strategy 2: Use `importlib.resources` to locate bundled data
   - Strategy 3: Check site-packages installation path

2. **Update `_load_prompts()` logic** to:
   - Distinguish between "default path" and "user-specified path"
   - Only attempt fallback for default path
   - Provide different error messages for each case

3. **Update CLI default** to use a sentinel value or None to detect when user hasn't specified a path

### Alternative Approaches Considered

#### Alternative 1: Change CLI default to None

- Pros: Clear distinction between default and user-specified
- Cons: Requires more complex logic in CLI layer

#### Alternative 2: Use importlib.resources exclusively

- Pros: Standard library approach for package data
- Cons: Requires Python 3.9+ (we're on 3.12+, so this is fine)

#### Alternative 3: Environment variable for prompts path

- Pros: Flexible for different environments
- Cons: Adds complexity, not addressing root cause

**Recommended:** Combination of Alternative 1 and Alternative 2

## Technical Considerations

### Package Structure (from pyproject.toml)

```toml
[tool.hatch.build.targets.wheel.force-include]
"prompts/" = "prompts/"
```

The prompts directory is already being bundled at the package root level.

### Installation Paths

- **uvx:** `~/.local/share/uv/cache/...` or similar
- **pip:** `site-packages/` in virtual environment or system Python
- **Development:** Project root directory

### Python Version

- Requires Python 3.12+ (already specified in `pyproject.toml`)
- Can use `importlib.resources.files()` (available in 3.9+)

### Dependencies

- No new dependencies required
- Use standard library `importlib.resources`

## Success Metrics

1. **Installation Success Rate:** 100% of remote installations via uvx succeed without errors
2. **Zero Breaking Changes:** All existing tests pass without modification
3. **Error Clarity:** User feedback indicates error messages are clear and actionable
4. **Development Workflow:** No additional steps required for local development

## Open Questions

None - all requirements are clear based on user responses.

## Implementation Notes

### Files to Modify

1. **`slash_commands/writer.py`**
   - Update `_find_package_prompts_dir()` to use `importlib.resources`
   - Update `_load_prompts()` to handle default vs explicit paths differently
   - Improve error messages

2. **`slash_commands/cli.py`**
   - Change `prompts_dir` default from `Path("prompts")` to `None`
   - Pass information about whether path was user-specified to `SlashCommandWriter`

3. **Tests to Update/Add**
   - `tests/test_writer.py`: Update existing tests for new behavior
   - Add test for `importlib.resources` fallback
   - Add test for explicit path validation
   - Add test for error message clarity

### Key Code Changes

**In `cli.py`:**

```python
prompts_dir: Annotated[
    Path | None,  # Changed from Path
    typer.Option(
        "--prompts-dir",
        "-p",
        help="Directory containing prompt files",
    ),
] = None,  # Changed from Path("prompts")
```

**In `writer.py`:**

```python
def _find_package_prompts_dir() -> Path | None:
    """Find the prompts directory in the installed package."""
    # Try importlib.resources first
    try:
        from importlib.resources import files
        package_files = files("spec_driven_development_mcp")
        prompts_dir = package_files / "prompts"
        if prompts_dir.is_dir():
            return Path(str(prompts_dir))
    except (ImportError, TypeError, FileNotFoundError):
        pass

    # Fallback to relative path from __file__
    package_root = Path(__file__).parent.parent
    prompts_dir = package_root / "prompts"
    if prompts_dir.exists():
        return prompts_dir

    return None
```

### Testing Strategy

1. **Unit Tests:** Test each resolution strategy independently
2. **Integration Tests:** Test full CLI flow with different installation scenarios
3. **Manual Testing:** Verify uvx installation from GitHub works
4. **Regression Testing:** Ensure all existing tests pass

## Definition of Done

- [ ] Code changes implemented and reviewed
- [ ] All existing tests pass
- [ ] New tests added for new behavior
- [ ] Manual testing confirms uvx installation works
- [ ] Error messages are clear and actionable
- [ ] Documentation updated (if needed)
- [ ] No breaking changes to existing workflows
- [ ] PR approved and merged
