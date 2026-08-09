# Milestone 001 Closeout — Deterministic Repository Scanner

## 1. Implementation Summary

Implemented production-quality `repoctl scan <repository>` as an installable Python CLI in Repo Control Plane.

The scanner:

- validates the target path and Git work tree;
- uses read-only filesystem and read-only Git inspection;
- derives deterministic repository, file, Python symbol, requirements, and test-structure facts;
- writes only to external state under `~/.local/share/repoctl/<repository_id>/`;
- generates deterministic artifacts:
  - `repository.json`
  - `files.json`
  - `symbols.json`
  - `tests.json`
  - `summary.md`
- uses transactional output publishing to avoid replacing a prior successful artifact set with partial data on failure.

## 2. Files Added/Modified in Repo Control Plane

Added:

- `pyproject.toml`
- `README.md`
- `src/repoctl/__init__.py`
- `src/repoctl/cli.py`
- `src/repoctl/scanner/__init__.py`
- `src/repoctl/scanner/core.py`
- `src/repoctl/scanner/git_ops.py`
- `src/repoctl/scanner/python_scan.py`
- `src/repoctl/scanner/summary.py`
- `src/repoctl/scanner/util.py`
- `tests/__init__.py`
- `tests/test_scanner.py`

## 3. CLI Behavior

Command:

`repoctl scan <repository>`

Behavior:

- exits non-zero on scan failure;
- prints concise completion summary on success including:
  - target repository root;
  - repository identifier;
  - branch state/name;
  - HEAD commit;
  - external output location;
  - parse error count.

## 4. Structured Output Schemas (High Level)

All JSON artifacts include:

`"schema_version": 1`

`repository.json` includes:

- repository root;
- repository identifier (`<slug>--<12-hex-digest>` from canonical path bytes);
- structured branch object (`attached`/`detached`);
- HEAD commit;
- porcelain-v2-derived working-tree status entries;
- working-tree category projection;
- tracked file count;
- repository-level requirements collection with `path` and `declarations`.

`files.json` includes one record per tracked file:

- relative path;
- conservative type classification;
- byte size;
- text line count or null;
- file SHA-256.

`symbols.json` includes one record per tracked Python file:

- parse success/failure;
- parse error text when failure;
- top-level functions/async functions/classes with line spans;
- top-level import structures;
- imported module names;
- imported symbols.

`tests.json` includes conservative structural test evidence:

- discovery convention metadata;
- test-like file/class/method/function counts;
- per-file discovered test classes and test-like functions;
- parse error recording for malformed test files.

`summary.md` is deterministic and rendered strictly from structured scan results.

## 5. Read-Only Safety Mechanism

- Target repository access is read-only:
  - tracked file reads;
  - Python AST parsing without import/execute;
  - read-only Git commands (`rev-parse`, `branch --show-current`, `ls-files`, `status --porcelain=v2 -z`).
- No target file writes, staging, commits, branch changes, or Git configuration changes.
- On unsupported porcelain-v2 records, scan fails closed.

## 6. Automated Test Results

Executed:

`PYTHONPATH=src python3 -m unittest -v`

Result:

- 13 tests run;
- all passed.

Covered areas include:

- valid Git scan;
- invalid/non-Git target;
- tracked-file inventory;
- SHA-256/size/line-count behavior;
- top-level function/class extraction;
- imports and imported-symbol extraction;
- nested function exclusion from top-level;
- malformed Python parse failure without aborting scan;
- test class/method discovery;
- requirements extraction with empty declarations behavior;
- dirty working-tree reporting;
- deterministic artifact output;
- external output location;
- proof of unchanged target Git state before/after scan.

## 7. Vocab App Validation Results

Executed:

`PYTHONPATH=src python3 -m repoctl.cli scan /home/chuck/ai-agent-tests/vocab-app`

Observed runtime summary:

- target: `/home/chuck/ai-agent-tests/vocab-app`
- repository_id: `vocab-app--0d568007c8ef`
- branch: `agent-test/gpt-oss-synonym-refactor`
- head: `522a1e83e4de876330c018e6f771b77de3b5b011`
- output: `/home/chuck/.local/share/repoctl/vocab-app--0d568007c8ef`
- parse_errors: `0`

Validation principle applied:

- no volatile target facts were hardcoded;
- scan reports actual repository state observed at runtime.

## 8. Exact External Output Location Used During Validation

`/home/chuck/.local/share/repoctl/vocab-app--0d568007c8ef`

## 9. Parse Errors or Limitations Encountered

- no parse errors in Vocab App during this validation run;
- implementation currently assumes UTF-8 decode for Python/requirements text parsing and records parse failure where decoding/parsing fails.

## 10. Milestone 002 Follow-Up Opportunities (Not Implemented)

- deterministic internal module dependency graph;
- deterministic static test-to-symbol references;
- expanded imported-symbol relationship analysis.

## 11. Final Repo Control Plane `git status --short`

At closeout:

- `?? README.md`
- `?? pyproject.toml`
- `?? src/`
- `?? tests/`
- `?? docs/001_deterministic_repository_scanner_closeout.md`

## Vocab App Git Status Before/After Validation

Explicit verification run captured porcelain-v2 status bytes before and after scan execution:

- `STATUS_MATCH=1`

This indicates exact equality of:

- `git -C /home/chuck/ai-agent-tests/vocab-app status --porcelain=v2 -z --untracked-files=all`

before versus after `repoctl scan`.

No target-repository mutation was observed during validation.
