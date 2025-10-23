# Task List: Fix Bundled Prompts Directory Resolution for Remote Installation

## Relevant Files

- `slash_commands/writer.py` - Contains `_find_package_prompts_dir()` and `_load_prompts()` methods that need to use `importlib.resources` and distinguish between default vs explicit paths
- `tests/test_writer.py` - Tests for writer functionality, needs updates for new behavior
- `slash_commands/cli.py` - CLI interface that needs to change default value for `prompts_dir` parameter and improve error handling
- `tests/test_cli.py` - CLI tests that may need updates for new default behavior

### Notes

- All tests should be run with `pytest tests/` from the project root
- Manual testing should verify the tool works with `uvx` installation
- The package name used for `importlib.resources` is `spec_driven_development_mcp` (from pyproject.toml)

## Tasks

- [ ] 1.0 Update `_find_package_prompts_dir()` to use importlib.resources
  - Demo Criteria: "Run from home directory and verify bundled prompts are located without specifying --prompts-dir"
  - Proof Artifact(s): "Test: `pytest tests/test_writer.py::test_writer_finds_bundled_prompts` shows successful resolution"
  - [ ] 1.1 Import `importlib.resources` module
  - [ ] 1.2 Add strategy using `importlib.resources.files()` to locate bundled prompts
  - [ ] 1.3 Keep existing fallback strategy using `Path(__file__).parent.parent`
  - [ ] 1.4 Add proper error handling for importlib edge cases
  - [ ] 1.5 Write unit test for importlib.resources path resolution

- [ ] 2.0 Update CLI to distinguish default vs explicit prompts directory
  - Demo Criteria: "Running without --prompts-dir shows bundled prompts; explicit --prompts-dir/nonexistent shows clear error"
  - Proof Artifact(s): "Test: Explicit vs default behavior verified in CLI tests; CLI error messages are clear"
  - [ ] 2.1 Change `prompts_dir` default value from `Path("prompts")` to `None` in CLI signature
  - [ ] 2.2 Pass a flag or sentinel value to SlashCommandWriter indicating if path was user-specified
  - [ ] 2.3 Update SlashCommandWriter.__init__ to accept the flag parameter
  - [ ] 2.4 Update error handling in CLI to show different messages for default vs explicit paths

- [ ] 3.0 Update `_load_prompts()` to handle default vs explicit paths differently
  - Demo Criteria: "Default path falls back to bundled prompts; explicit path fails immediately without fallback"
  - Proof Artifact(s): "Test: `test_writer_default_path_fallback` and `test_writer_explicit_path_no_fallback` pass"
  - [ ] 3.1 Modify `_load_prompts()` to check the flag for explicit vs default
  - [ ] 3.2 Only attempt fallback to bundled prompts when using default path
  - [ ] 3.3 Raise clear error for explicit non-existent paths without fallback
  - [ ] 3.4 Write tests for both scenarios (default with fallback, explicit without fallback)

- [ ] 4.0 Improve error messages for better user guidance
  - Demo Criteria: "Error messages clearly distinguish scenarios and provide actionable guidance"
  - Proof Artifact(s): "CLI output showing clear, distinct error messages for each failure scenario"
  - [ ] 4.1 Create different error messages for "default path not found" vs "explicit path not found"
  - [ ] 4.2 Include information about attempted fallback in error messages
  - [ ] 4.3 Show the actual paths that were checked
  - [ ] 4.4 Update existing error handling in CLI to use new messages

- [ ] 5.0 Ensure backward compatibility and verify existing tests pass
  - Demo Criteria: "All existing tests pass; development workflow still works; custom prompts paths still work"
  - Proof Artifact(s): "Test suite: All tests pass; Manual: Run from project root works; Manual: Custom --prompts-dir works"
  - [ ] 5.1 Run full test suite to ensure no regressions
  - [ ] 5.2 Update or remove tests that expected old behavior
  - [ ] 5.3 Test development workflow (running from project root with local prompts)
  - [ ] 5.4 Test custom prompts directory still works when explicitly specified
  - [ ] 5.5 Manual test with uvx installation from GitHub to verify remote install works
