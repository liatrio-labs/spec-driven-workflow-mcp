# Task List: Code Review Fixes

Based on: `0004-spec-review-fixes.md`

## Relevant Files

- `pyproject.toml` - Package configuration; needs `slash_commands` added to packages list
- `slash_commands/writer.py` - TOML reading logic using `tomllib` (no changes needed, already correct)
- `slash_commands/generators.py` - Version import needs update from `mcp_server.__version__` to shared module
- `mcp_server/__init__.py` - Current version implementation (may optionally be updated to use shared module)
- `__version__.py` - New module to create at project root for centralized version management
- `tests/test_validation.py` - New test file for generated content validation tests
- `docs/slash-command-generator.md` - Documentation that needs troubleshooting section and Python version clarification
- `tests/conftest.py` - Test fixtures (may need updates if new fixtures are required)

### Notes

- The project requires Python 3.12+ (`requires-python = ">=3.12"` in pyproject.toml), so `tomllib` is always available in stdlib
- No need for `tomli` dependency since `tomllib` is available in Python 3.12+
- Current TOML reading implementation in `slash_commands/writer.py` is already correct
- All existing tests must continue to pass after changes
- Use `pytest` to run tests: `pytest tests/test_validation.py` for new tests or `pytest` for all tests

## Tasks

- [x] 1.0 Fix Package Discovery Configuration
  - Demo Criteria: "Run `uv pip install -e .` successfully; execute `uv run sdd-generate-commands --list-agents` without import errors; verify installed package includes `slash_commands` directory"
  - Proof Artifact(s): "Updated `pyproject.toml` with packages configuration; terminal output showing successful installation; terminal output showing successful CLI execution"
  - [x] 1.1 Update `pyproject.toml` line 39 to include `"slash_commands"` in the packages list: `packages = ["mcp_server", "prompts", "slash_commands"]`
  - [x] 1.2 Run `uv pip install -e .` to verify package installs successfully without errors
  - [x] 1.3 Execute `uv run sdd-generate-commands --list-agents` to verify CLI works without import errors
  - [x] 1.4 Verify that the installed package includes the `slash_commands` directory using: `python -c "import slash_commands; print(slash_commands.__file__)"`

- [x] 2.0 Document TOML Reading Approach
  - Demo Criteria: "Verify `tomllib` import works in `slash_commands/writer.py`; documentation clearly states Python 3.12+ requirement; no runtime errors from TOML reading"
  - Proof Artifact(s): "Documentation update clarifying Python version requirement; terminal output showing successful TOML parsing"
  - [x] 2.1 Add note to `docs/slash-command-generator.md` documentation section clarifying that Python 3.12+ is required and `tomllib` is available in standard library
  - [x] 2.2 Add a comment in `slash_commands/writer.py` near the `tomllib` import explaining it's from stdlib (Python 3.12+)
  - [x] 2.3 Verify `tomllib` import works by running `python -c "import tomllib; print('OK')"` in Python 3.12+
  - [x] 2.4 Test TOML reading by running existing tests: `pytest tests/test_writer.py -v`

- [x] 3.0 Add Generated Content Validation Tests
  - Demo Criteria: "New tests validate TOML round-trip parsing; new tests validate YAML parsing; tests catch invalid content before file writing"
  - Proof Artifact(s): "Test file `tests/test_validation.py` with validation tests; pytest output showing all validation tests passing; example of test catching invalid content"
  - [x] 3.1 Create new test file `tests/test_validation.py` for validation tests
  - [x] 3.2 Add test function `test_toml_round_trip_parsing()` that generates TOML content, parses it back, and verifies equivalence
  - [x] 3.3 Add test function `test_yaml_frontmatter_parsing()` that validates YAML frontmatter is parseable and structurally correct
  - [x] 3.4 Add test function `test_invalid_toml_content_caught()` that attempts to generate invalid TOML and verifies it's caught
  - [x] 3.5 Add test function `test_invalid_yaml_content_caught()` that attempts to generate invalid YAML and verifies it's caught
  - [x] 3.6 Run tests with `pytest tests/test_validation.py -v` to verify all validation tests pass
  - [x] 3.7 Run full test suite with `pytest` to ensure no regressions

- [ ] 4.0 Centralize Version Management
  - Demo Criteria: "Version read from `pyproject.toml` via shared `__version__.py` module; no imports from `mcp_server` module for version; version displayed correctly in generated metadata"
  - Proof Artifact(s): "New `__version__.py` module in project root; updated imports in `slash_commands/generators.py`; terminal output showing correct version in generated files"
  - [ ] 4.1 Create new file `__version__.py` at project root with version reading logic using `tomllib` to read from `pyproject.toml`
  - [ ] 4.2 Update `slash_commands/generators.py` line 11 to import from `__version__` instead of `mcp_server`: change `from mcp_server import __version__` to `from __version__ import __version__`
  - [ ] 4.3 Verify version is correctly imported by running `python -c "from __version__ import __version__; print(__version__)"`
  - [ ] 4.4 Test that generated files contain correct version by running `uv run sdd-generate-commands --dry-run` and checking metadata
  - [ ] 4.5 Optionally update `mcp_server/__init__.py` to import from shared `__version__.py` module for consistency
  - [ ] 4.6 Run all tests with `pytest` to ensure version changes don't break existing functionality

- [ ] 5.0 Add Troubleshooting Documentation
  - Demo Criteria: "Troubleshooting section added to `docs/slash-command-generator.md`; FAQ covers common error scenarios; documentation includes Python version requirements"
  - Proof Artifact(s): "Updated documentation file; table mapping error messages to solutions; Python version compatibility matrix"
  - [ ] 5.1 Add a "Python Version Requirements" section near the beginning of `docs/slash-command-generator.md` stating Python 3.12+ is required
  - [ ] 5.2 Expand the existing "Troubleshooting" section with at least 5 common error scenarios and their solutions
  - [ ] 5.3 Add troubleshooting entries for: "No Agents Detected", "Invalid Agent Key", "Permission Denied", "I/O Error", "Prompts Directory Not Found"
  - [ ] 5.4 Add a Python version compatibility note explaining why `tomllib` is available and no additional dependencies are needed
  - [ ] 5.5 Review documentation for clarity and completeness
  - [ ] 5.6 Verify the documentation renders correctly when viewed as markdown
