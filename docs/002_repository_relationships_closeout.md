# Milestone 002 Closeout — Deterministic Repository Relationships

## 1. Implementation Summary

Milestone 002 was implemented by extending the existing `repoctl scan <repository>` pipeline with a deterministic relationship resolver layer.

No new user-facing command was added.

The scan now produces one additional artifact:

- `dependencies.json`

and extends `tests.json` with deterministic per-test resolved repository references.

The implementation preserves Milestone 001 read-only behavior, deterministic output rules, and transactional publishing.

## 2. Repo Control Plane Files Added/Modified

Added:

- `src/repoctl/scanner/relationships.py`
- `tests/test_relationships.py`

Modified:

- `src/repoctl/scanner/core.py`
- `src/repoctl/scanner/summary.py`
- `tests/test_scanner.py`
- `README.md`

## 3. Relationship-Resolution Rules Implemented

Implemented deterministic conservative resolution for:

- internal module dependency edges from `import ...` and `from ... import ...` syntax;
- imported-symbol relationships when module resolution is unique and target top-level symbol is statically recorded;
- static top-level call relationships for:
  - same-module direct function calls;
  - direct imported-symbol calls;
  - imported-module attribute calls;
- test-to-symbol static references for test functions/methods.

Implemented required conservative handling:

- ambiguity never auto-resolves;
- wildcard imports never fabricate symbol relationships;
- shadowed/rebound names block resolution;
- parse-failed target modules may still support module-level dependency evidence but block symbol/call resolution;
- unresolved/ambiguous attempts are recorded deterministically in diagnostics.

## 4. `dependencies.json` Schema (High Level)

`dependencies.json` uses:

- `"schema_version": 1`

High-level sections:

- `module_resolution.file_module_candidates`
- `module_dependencies`
- `imported_symbol_relationships`
- `call_relationships`
- `unresolved_relationships`
- `counts`

Each unresolved/ambiguous record includes required minimal fields:

- `relationship_kind`
- `source_file`
- `source_symbol`
- `source_line`
- `reference`
- `reason`
- `candidates`

## 5. `tests.json` Schema Change / Version Change

`tests.json` changed from `schema_version: 1` to:

- `schema_version: 2`

v2 extension adds deterministic per-test resolved references under:

- `test_files[].classes[].test_methods[].resolved_references`
- `test_files[].top_level_test_functions[].resolved_references`

Each reference includes:

- `target_file`
- `target_symbol`
- `target_symbol_kind`
- `reference_kind`
- `source_line`

Also added aggregate:

- `test_reference_count`

## 6. Supported Static Call-Resolution Cases

Supported:

- same-module direct top-level function call (`same_module`);
- direct imported-symbol call (`imported_symbol`);
- imported-module attribute call (`imported_module_attribute`).

## 7. Explicitly Unsupported / Dynamic Cases

Not resolved (by design):

- runtime/dynamic import behavior;
- full Python runtime name-resolution semantics;
- indirect callback dispatch;
- reflection and dynamic attribute lookup;
- full control-flow-sensitive alias tracking;
- runtime framework routing behavior.

## 8. Automated Test Results

Executed:

- `PYTHONPATH=src python3 -m unittest -v`

Result:

- 22 tests run;
- all passed.

Coverage includes Milestone 001 regression checks plus Milestone 002 cases:

- module import resolution;
- from-import symbol resolution;
- alias handling;
- supported call-resolution modes;
- external import non-internal classification;
- root-vs-src ambiguity with no fabricated edge;
- wildcard import no fabricated symbol edge;
- shadowing/rebinding false-positive prevention;
- parse-failure target constraints;
- test-reference extraction;
- deterministic repeated output including `dependencies.json`.

## 9. Vocab App Validation Results

Executed:

- `PYTHONPATH=src python3 -m repoctl.cli scan /home/chuck/ai-agent-tests/vocab-app`

Observed summary:

- target: `/home/chuck/ai-agent-tests/vocab-app`
- repository_id: `vocab-app--0d568007c8ef`
- branch: `agent-test/gpt-oss-synonym-refactor`
- head: `522a1e83e4de876330c018e6f771b77de3b5b011`
- output: `/home/chuck/.local/share/repoctl/vocab-app--0d568007c8ef`
- parse_errors: `0`

## 10. Representative Verified Relationships From Vocab App

Examples observed in generated artifacts:

- module dependency edge:
  - `app.py` `from vocab_utils import ...` -> `vocab_utils.py`
- imported-symbol relationship:
  - `app.py` local `normalize_synonym_candidates` -> `vocab_utils.py::normalize_synonym_candidates`
- static call relationship:
  - same-module calls in app variants (e.g., `get_mw_data` -> `get_nltk_root`)
- test reference evidence:
  - `test_vocab_utils.py` test methods include static `call`/`import` references to `vocab_utils.py::normalize_synonym_candidates`

## 11. Unresolved / Ambiguous Cases Encountered

Validation run counts from `dependencies.json`:

- `unresolved_relationship_count`: `117`
- `ambiguous_relationship_count`: `0`
- `target_parse_failure_count`: `0`

Representative unresolved reasons in Vocab App:

- `no_tracked_module_match` for non-internal calls/import contexts.

## 12. Deterministic-Output Validation

Determinism was validated in automated tests by consecutive scans over unchanged repositories and byte-for-byte equality checks for:

- `repository.json`
- `files.json`
- `symbols.json`
- `tests.json`
- `dependencies.json`
- `summary.md`

## 13. Vocab App Git Status Before/After

Before/after equality check was performed using porcelain-v2 status bytes.

Result:

- `STATUS_MATCH=1`

This confirms no target-repository mutation from scanning.

## 14. Milestone 003 Opportunities (Not Implemented)

- bounded context-pack generation driven by deterministic relationship artifacts;
- query-oriented projection over deterministic relationship evidence;
- task-specific slicing of module/symbol/test references for agent navigation.

## 15. Final Repo Control Plane `git status --short`

At closeout:

- `M README.md`
- `M src/repoctl/scanner/core.py`
- `M src/repoctl/scanner/summary.py`
- `M tests/test_scanner.py`
- `?? src/repoctl/scanner/relationships.py`
- `?? tests/test_relationships.py`
- `?? docs/002_repository_relationships_closeout.md`

No commit or push was performed during this closeout.
