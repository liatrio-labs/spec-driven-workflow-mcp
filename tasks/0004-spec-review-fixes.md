# 0004-spec-review-fixes.md

## Introduction/Overview

This specification addresses code review findings from the `feat/install-slash-commands` branch review. The review identified 15 issues across High, Medium, and Low priority categories. This spec focuses on implementing fixes for all issues not explicitly marked as "Won't Do", ensuring the slash command generator CLI is production-ready.

**Important Context**: After checking documentation and reviewing the codebase, we discovered:

- Project requires Python 3.12+ (`requires-python = ">=3.12"`)
- `tomllib` is always available in Python 3.12+ standard library
- No need for `tomli` dependency or version detection logic
- Current TOML reading implementation is already correct

The main goals are to fix critical packaging issues, add validation mechanisms, improve version management, and strengthen documentation.

## Goals

1. Fix package discovery configuration to include the `slash_commands` module in the distribution
2. Document that TOML reading uses stdlib `tomllib` (always available in Python 3.12+)
3. Add content validation tests for generated YAML and TOML files
4. Centralize version management to reduce coupling between modules
5. Enhance documentation with troubleshooting section
6. Maintain existing test coverage while adding new validation tests

## User Stories

- **As a maintainer**, I want the package to install correctly so that users can use the CLI tool immediately after installation
- **As a developer**, I want proper version management so that refactoring modules doesn't break version references
- **As a user**, I want compatibility documentation so I know what Python versions are supported
- **As a developer**, I want validation tests so that generated content is always valid
- **As a user**, I want troubleshooting guidance so I can resolve common issues independently

## Demoable Units of Work

### Slice 1: Fix Package Discovery Configuration

**Purpose**: Ensure the `slash_commands` module is included in package installation

**Demo Criteria**:

- Run `uv pip install -e .` successfully
- Execute `uv run sdd-generate-commands --list-agents` without import errors
- Verify installed package includes `slash_commands` directory

**Proof Artifacts**:

- `pyproject.toml` with updated packages configuration
- Terminal output showing successful installation
- Terminal output showing successful CLI execution

### Slice 2: Document TOML Reading Approach

**Purpose**: Clarify that tomllib is always available since Python 3.12+ is required

**Demo Criteria**:

- Verify `tomllib` import works in `slash_commands/writer.py`
- Documentation clearly states Python 3.12+ requirement
- No runtime errors from TOML reading

**Proof Artifacts**:

- Current `slash_commands/writer.py` already uses `tomllib` correctly
- Documentation update clarifying Python version requirement
- Terminal output showing successful TOML parsing

### Slice 3: Add Generated Content Validation Tests

**Purpose**: Verify generated YAML and TOML files are parseable

**Demo Criteria**:

- New tests validate TOML round-trip parsing
- New tests validate YAML parsing
- Tests catch invalid content before file writing

**Proof Artifacts**:

- Test file `tests/test_validation.py` with validation tests
- pytest output showing all validation tests passing
- Example of test catching invalid content

### Slice 4: Centralize Version Management

**Purpose**: Create single source of truth for version information

**Demo Criteria**:

- Version read from `pyproject.toml` via shared `__version__.py` module
- No imports from `mcp_server` module for version
- Version displayed correctly in generated metadata

**Proof Artifacts**:

- New `__version__.py` module in project root
- Updated imports in `slash_commands/generators.py` (change from `mcp_server.__version__`)
- Terminal output showing correct version in generated files

### Slice 5: Add Troubleshooting Documentation

**Purpose**: Help users resolve common issues

**Demo Criteria**:

- Troubleshooting section added to `docs/slash-command-generator.md`
- FAQ covers common error scenarios
- Documentation includes Python version requirements

**Proof Artifacts**:

- Updated documentation file
- Table mapping error messages to solutions
- Python version compatibility matrix

## Functional Requirements

1. **FR1**: The `pyproject.toml` packages configuration must include `"slash_commands"` in the list
2. **FR2**: TOML reading approach documented (Python 3.12+ required, `tomllib` in stdlib)
3. **FR3**: ~~`tomli` dependency added~~ Not needed since Python 3.12+ required
4. **FR4**: Validation tests must verify TOML round-trip parsing (generate and parse back)
5. **FR5**: Validation tests must verify YAML parsing for markdown frontmatter
6. **FR6**: Version management centralized using shared module pattern (matches existing approach)
7. **FR7**: Version reading must not depend on importing from `mcp_server` module
8. **FR8**: Troubleshooting section must include at least 5 common issues with solutions
9. **FR9**: Documentation must clearly state Python 3.12+ requirement
10. **FR10**: All existing tests must continue to pass after changes

## Non-Goals (Out of Scope)

- Interactive prompt timeout handling (marked "Won't Do")
- Backup file collision prevention (marked "Won't Do")
- Detection logic directory verification (marked "Won't Do")
- Automatic cleanup of old backup files (marked "Won't Do")
- Enhanced error messages with shell commands (marked "Won't Do")
- Microsecond precision for backup timestamps
- Command preview before generation
- Custom prompt templates support
- Plugin architecture for new agent formats

## Design Considerations

### Version Management Best Practices

Based on Python packaging best practices (PEP 566):

- Use `importlib.metadata.version()` for reading version from installed package
- Fallback to reading `pyproject.toml` file system path only during development
- Current implementation in `mcp_server/__init__.py` reads from file system
- Better approach: try installed package metadata first, then fallback to file system
- Single source of truth: version lives in `pyproject.toml`

### TOML Compatibility Strategy

- Python 3.12+: Use `tomllib` from standard library (always available)
- Project requires Python 3.12+ (`requires-python = ">=3.12"` in pyproject.toml)
- No need for conditional logic or fallback libraries
- Current implementation in `slash_commands/writer.py` already correct

### Validation Testing Approach

- Round-trip test: generate content → parse it back → verify equivalence
- Parser validation: ensure generated TOML/YAML is syntactically valid
- Content validation: verify metadata structure matches expected format

## Technical Considerations

### Dependencies

**Note**: Project requires Python 3.12+ (`requires-python = ">=3.12"`), so `tomllib` is always available in stdlib.

- Add `tomli>=2.0.0` to dependencies ONLY if we want broader compatibility
- For Python 3.12+: `tomllib` available in stdlib, no additional dependency needed
- Ensure `pyyaml` already present for YAML validation (already in dependencies)
- **Simplest approach**: Keep Python 3.12+ requirement, don't add `tomli` dependency

### Version Management Implementation

**Approach**: Extend current pattern in `mcp_server/__init__.py`:

- Create shared `__version__.py` module at project root that exports version
- Module reads from `pyproject.toml` using existing `_get_version()` pattern
- Update `slash_commands/generators.py` to import from shared module instead of `mcp_server`
- Reduces coupling: `slash_commands` no longer depends on `mcp_server` for version

**Implementation**:
Create `__version__.py` in project root:

```python
"""Version information for spec-driven-development-mcp."""

from pathlib import Path
import tomllib


def _get_version() -> str:
    """Get the version from pyproject.toml."""
    pyproject_path = Path(__file__).parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)
    return data["project"]["version"]


__version__ = _get_version()
```

Update imports in:

- `slash_commands/generators.py`: Change `from mcp_server import __version__` to `from __version__ import __version__`
- Optionally update `mcp_server/__init__.py` to import from shared module

### TOML Reading Compatibility

**Approach**: Keep current implementation as-is

- Project requires Python 3.12+ (`requires-python = ">=3.12"`)
- `tomllib` is always available in Python 3.12+ standard library
- Current implementation in `slash_commands/writer.py` is correct
- No code changes needed

**Documentation**: Add note to documentation clarifying Python 3.12+ requirement

### Package Configuration Fix

Update `pyproject.toml` line 39:

```toml
packages = ["mcp_server", "prompts", "slash_commands"]
```

## Success Metrics

1. **Installation Success**: 100% successful installations via `uv pip install -e .`
2. **Test Coverage**: All existing tests pass + new validation tests added
3. **Python Compatibility**: Works on Python 3.12+ (required version)
4. **Documentation Completeness**: Troubleshooting section covers all High priority error scenarios
5. **Zero Import Errors**: No module import failures at runtime
6. **Package Completeness**: `slash_commands` module included in distribution

## Decisions Made

1. **Python Version Check**: No runtime check needed - pip handles version enforcement during installation
2. **Validation Tests**: Run only in CI/test suite, not during generation
3. **Troubleshooting Location**: Add to `docs/slash-command-generator.md` under troubleshooting section
4. **CHANGELOG**: Automatic via semantic-release, no manual update needed
5. **Version Management**: Use Option 1 - shared `__version__.py` module pattern
6. **TOML Compatibility**: Use Option 1 - keep current implementation, no changes needed

## Related Files

- `pyproject.toml` - Package configuration
- `slash_commands/writer.py` - TOML reading logic (no changes needed)
- `slash_commands/generators.py` - Version import (needs update)
- `tests/test_generators.py` - Validation test location
- `docs/slash-command-generator.md` - Documentation updates
- `mcp_server/__init__.py` - Current version implementation
- `__version__.py` - New module to create at project root

## Summary

This spec addresses code review findings for the `feat/install-slash-commands` branch. The main fixes are:

1. **Critical**: Fix package discovery by adding `slash_commands` to wheel packages
2. **Documentation**: Clarify TOML approach and Python 3.12+ requirement
3. **Testing**: Add validation tests for generated content
4. **Architecture**: Centralize version management to reduce coupling
5. **User Experience**: Add troubleshooting documentation

All changes follow Python packaging best practices and maintain compatibility with the existing codebase. The spec is ready for implementation.
