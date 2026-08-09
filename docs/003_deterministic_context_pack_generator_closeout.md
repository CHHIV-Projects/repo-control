# Milestone 003 Closeout — Deterministic Context Pack Generator

## 1. Implementation Summary

Implemented deterministic context-pack generation as a new CLI capability:

- `repoctl context "<query>" [--repository <path>]`

The implementation reuses a fresh Milestone 001/002 scan on each context command, then performs deterministic lexical seed selection plus one-hop bounded relationship expansion to produce:

- `context.json`
- `context.md`

No AI, semantic search, embeddings, target-code execution, or Git writes were introduced.

## 2. Files Added/Modified

Added:

- `src/repoctl/context/__init__.py`
- `src/repoctl/context/policy.py`
- `src/repoctl/context/generator.py`
- `tests/test_context.py`

Modified:

- `src/repoctl/cli.py`
- `src/repoctl/scanner/core.py`
- `README.md`

## 3. CLI Syntax and Repository Selection Behavior

Added command:

- `repoctl context "<query>" [--repository <path>]`

Behavior:

- when `--repository` is omitted, target defaults to current working directory Git worktree resolution;
- when `--repository` is provided, any path within the target worktree is accepted and canonical Git root is resolved;
- non-Git targets fail clearly and non-zero;
- context generation first invokes current deterministic scan; if scan fails, context fails.

## 4. Query Canonicalization / Tokenization Contract

Implemented:

- canonical query = trim + collapse whitespace runs via Python whitespace semantics;
- empty canonical query is rejected;
- matching/tokenization uses casefolded lexical rules only;
- token boundaries: whitespace, `_`, `-`, `.`, `/`, `\`;
- no camelCase/PascalCase splitting;
- no Unicode normalization/transliteration;
- duplicate tokens collapse to first occurrence order.

## 5. Ranking / Seed-Selection Rules

Implemented deterministic lexical ranking with named constants and fixed priority strengths:

1. exact symbol-name match
2. exact path/module component match
3. full-query substring match
4. multiple token matches
5. single token match

Tie-breaking:

1. higher score
2. more matched query tokens
3. symbol before file for otherwise equivalent symbol/file seed records
4. deterministic path byte order
5. source line
6. symbol name

Seed identity and dedup:

- file seed key: `("file", relative_path)`
- symbol seed key: `("symbol", relative_path, symbol_kind, symbol_name, start_line)`

`MAX_SEEDS = 12` applies to seed records, not unique files.

## 6. One-Hop Expansion Rules

Implemented one-hop only expansion (no recursion) across deterministic Milestone 002 relationships:

- module dependency
- imported symbol
- call
- test reference

Eligible edges are constrained to those connected to selected seed file/symbol context under the Milestone 003 contract.

## 7. Fixed Context Limits

Implemented named constants and deterministic truncation metadata:

- `MAX_SEEDS = 12`
- `MAX_FILES = 20`
- `MAX_SYMBOLS = 40`
- `MAX_RELATIONSHIPS = 40`
- `MAX_TEST_REFERENCES = 20`

Each bounded collection records total qualifying count, selected count, and truncation flag.

## 8. `context.json` Schema (High Level)

`context.json` uses:

- `"schema_version": 1`

Includes:

- repository identity/state metadata;
- original/canonical query and query tokens;
- deterministic `context_id`;
- `selection_contract_version`;
- `match_status` (`matched` or `no_matches`);
- selected seed records;
- selected files;
- selected symbols;
- selected internal relationships;
- selected related tests/references;
- projected limitations/ambiguities;
- parse-failure limitations;
- selection/truncation metadata.

## 9. Deterministic `context.md` Structure

Rendered from deterministic structured context result only (no re-selection).

Fixed section order implemented:

1. `# Repository Context`
2. `## Repository State`
3. `## Query`
4. `## Suggested Source Inspection`
5. `## Relevant Symbols`
6. `## Internal Relationships`
7. `## Related Tests`
8. `## Limitations / Ambiguities`
9. `## Selection Metadata`

Sections remain present even when empty.

## 10. Unresolved / Ambiguous Filtering Behavior

Implemented strict allowlist projection for context limitation diagnostics:

- `ambiguous_module`
- `target_parse_failure`
- `shadowed_or_rebound`
- `unresolved_symbol`
- `wildcard_import`

Diagnostic inclusion additionally requires intersection with selected context.

`no_tracked_module_match` is never projected into context packs.

## 11. Automated Test Results

Executed:

- `PYTHONPATH=src python3 -m unittest -v`
- `PYTHONPATH=src python3 -m compileall src tests`

Result:

- 39 tests run, all passing.

Coverage includes context command routing, query normalization/tokenization, deterministic ranking/selection behaviors, limits/truncation metadata, no-match success, one-hop boundary, diagnostic filtering, deterministic output, and target read-only verification.

## 12. Vocab App Validation Results

Executed:

- `repoctl context "synonym" --repository /home/chuck/ai-agent-tests/vocab-app`
- `repoctl context "get_sheet" --repository /home/chuck/ai-agent-tests/vocab-app`

Observed:

- both commands succeeded;
- context artifacts written to deterministic context directories;
- output counts respected fixed limit contract.

## 13. Representative `synonym` / `get_sheet` Results

`synonym` context:

- context_id: `synonym--ee6b5af5c217`
- selected files: `vocab_utils.py`, `app - stable.py`, `app v-1.py`, `app v-2.py`, `app.py`, `test_vocab_utils.py`
- selected symbols include `vocab_utils.py::normalize_synonym_candidates` and related `get_synonyms*` functions
- selected relationships: 33
- selected test references: 20 (truncated from 24)

`get_sheet` context:

- context_id: `get-sheet--ceb0833c7fe1`
- selected files: app variants plus `vocab_utils.py`
- selected relationships: 12
- selected test references: 0

## 14. Practical Reconnaissance-Reduction Result

Mechanical question:

- "Which files and symbols should a coding agent inspect first for synonym handling?"

Using only generated context (`synonym` pack), top suggested files were:

1. `vocab_utils.py`
2. `app - stable.py`
3. `app v-1.py`
4. `app v-2.py`
5. `app.py`
6. `test_vocab_utils.py`

Top symbols included:

- `vocab_utils.py::normalize_synonym_candidates`
- `app.py::get_synonyms_nltk` (and app variant equivalents)
- `test_vocab_utils.py::TestNormalizeSynonyms`

Direct repository evidence matched these suggestions: context included production symbol relationships and test references to synonym normalization without broad unrelated file dumping.

## 15. Determinism Validation

Validated by repeated generation tests and runtime checks:

- repeated context generation for unchanged repo/query produced byte-identical `context.json` and `context.md`;
- deterministic ids and sorting applied under fixed policy constants;
- markdown layout remained fixed.

## 16. Vocab App Before/After Git Status

Porcelain-v2 byte equality check around validation commands:

- `STATUS_MATCH=1`

No target repository mutation observed.

## 17. Limitations

- lexical matching only (no semantic interpretation);
- one-hop bounded projection by design;
- context packs are navigation evidence, not authoritative source or architecture conclusions.

## 18. Milestone 004 Opportunities (Not Implemented)

- snapshot capture command and deterministic comparison flow;
- bounded before/after structural delta reporting;
- context-pack comparison against prior snapshot state.

## 19. Final Repo Control Plane `git status --short`

At closeout:

- `M README.md`
- `M src/repoctl/cli.py`
- `M src/repoctl/scanner/core.py`
- `?? src/repoctl/context/`
- `?? tests/test_context.py`
- `?? docs/003_deterministic_context_pack_generator_closeout.md`

No commit/push was performed during this closeout.
