# Milestone 004 Closeout — Deterministic Snapshot and Structural Delta Audit

## 1. Implementation Summary

Implemented deterministic snapshot capture and immutable structural comparison for Repo Control Plane.

Added commands:

- `repoctl snapshot [--repository <path>]`
- `repoctl compare <before_snapshot_id> <after_snapshot_id> [--repository <path>]`

The implementation reuses the existing deterministic scan pipeline for snapshot creation, stores immutable snapshot artifacts externally, and performs structural before/after comparison exclusively from named snapshots.

No AI, target-code execution, Git writes, rename inference, or Git-history traversal was introduced.

## 2. Files Added/Modified

Added:

- `src/repoctl/snapshot/__init__.py`
- `src/repoctl/snapshot/identity.py`
- `src/repoctl/snapshot/manager.py`
- `src/repoctl/compare/__init__.py`
- `src/repoctl/compare/manager.py`
- `tests/test_snapshot_compare.py`

Modified:

- `src/repoctl/cli.py`
- `src/repoctl/scanner/core.py`
- `README.md`

## 3. Snapshot CLI Behavior

`repoctl snapshot`:

- resolves repository using the same behavior as `repoctl context`;
- performs a fresh deterministic scan first;
- stages the six scan artifacts plus `snapshot.json`;
- integrity-verifies the staged snapshot before first publication;
- derives deterministic `snapshot_id` from exact scan artifact bytes;
- reuses an existing immutable snapshot when identical content already exists.

## 4. Compare CLI Behavior

`repoctl compare <before_snapshot_id> <after_snapshot_id> [--repository <path>]`:

- resolves current repository only to derive `repository_id` and locate the snapshot namespace;
- loads the two immutable snapshots;
- verifies snapshot integrity before use;
- compares snapshot evidence without performing a current scan;
- publishes `comparison.json` and bounded `comparison.md` transactionally;
- reuses an existing identical comparison result when already present.

## 5. Snapshot ID Contract

Implemented:

- `snapshot_id = "snap--" + first 16 lowercase hex chars of SHA-256(...)`

Digest input uses the fixed `repoctl-snapshot-v1\0` prefix plus the ordered scan artifact filenames and exact artifact-byte SHA-256 digests as specified in the prompt.

Identical captured deterministic scan evidence therefore produces the same snapshot ID.

## 6. Comparison ID Contract

Implemented:

- `comparison_id = "cmp--" + first 16 lowercase hex chars of SHA-256(...)`

using the fixed `repoctl-comparison-v1\0` prefix followed by:

- `before_snapshot_id`
- `after_snapshot_id`

Comparison ID is deterministic and directional.

## 7. Snapshot Storage / Artifact Structure

Snapshots are stored beneath:

- `~/.local/share/repoctl/<repository_id>/snapshots/<snapshot_id>/`

Containing exactly:

- `snapshot.json`
- `repository.json`
- `files.json`
- `symbols.json`
- `tests.json`
- `dependencies.json`
- `summary.md`

The six scan artifacts are stored as exact byte copies of the fresh successful scan output.

## 8. `snapshot.json` Schema (High Level)

`snapshot.json` uses:

- `"schema_version": 1`

Includes:

- snapshot ID;
- repository ID and canonical root;
- branch and HEAD;
- working-tree clean/dirty metadata;
- structured working-tree evidence;
- scan artifact names;
- exact stored scan artifact hashes;
- structural coverage/completeness metadata.

## 9. Worktree Coverage / Completeness Behavior

Implemented explicit coverage metadata:

- `structural_scope = "tracked_files"`
- `untracked_entries_present`
- `untracked_paths`
- `worktree_completeness`

Values:

- `complete_for_tracked_files` when no untracked entries exist
- `partial_worktree` when untracked entries exist

Snapshots remain valid for tracked-file structural evidence even when the worktree is partial.

## 10. `comparison.json` Schema (High Level)

`comparison.json` uses:

- `"schema_version": 1`

Includes:

- comparison ID;
- repository ID;
- before/after snapshot IDs;
- before/after repository-state summaries;
- structural coverage for both snapshots;
- file, requirements, symbol, relationship, test-reference, parse-failure, and diagnostic deltas;
- deterministic aggregate counts.

## 11. File-Delta Rules

Implemented file classification by relative path and recorded file SHA-256:

- `added`
- `removed`
- `content_changed`
- `unchanged`

Content changes preserve before/after hash, size, line count, and file type evidence.

No rename inference is performed.

## 12. Symbol-Delta Rules

Implemented canonical normalized top-level symbol stream per file.

Stable symbol identity:

- `relative_path`
- `symbol_kind`
- `symbol_name`
- `occurrence_ordinal`

Ordinals are assigned from one normalized source-order stream, preventing ordinary line movement from becoming false add/remove churn.

Reported:

- `added`
- `removed`
- `retained`
- `source_location_changed`

## 13. Relationship / Test-Reference Delta Rules

Implemented stable logical identities excluding incidental source-line movement for:

- module dependencies;
- imported-symbol relationships;
- static call relationships;
- test references.

Reported:

- `added`
- `removed`
- `retained`
- `location_changed` or `source_location_changed` where applicable.

## 14. Parse / Diagnostic Delta Rules

Parse failures are compared deterministically as:

- `introduced_parse_failures`
- `resolved_parse_failures`
- `retained_parse_failures`

Relationship-diagnostic record deltas are focused on:

- `ambiguous_module`
- `target_parse_failure`
- `shadowed_or_rebound`
- `unresolved_symbol`
- `wildcard_import`

Stable diagnostic identity uses:

- `reason`
- `relationship_kind`
- `source_file`
- `source_symbol`
- `reference`
- ordered `candidates`

`source_line` is excluded from logical identity and treated separately as location-change evidence.

## 15. Bounded Markdown Behavior

`comparison.md` is rendered only from already-computed deterministic comparison results.

Fixed bound implemented:

- `MAX_MD_ITEMS_PER_SECTION = 50`

The bound applies per complete top-level Markdown section, not per subsection/category.

Changed categories are prioritized before retained categories when truncation occurs.

`comparison.json` remains complete and untruncated.

## 16. Automated Test Results

Executed:

- `PYTHONPATH=src python3 -m unittest -q`
- `PYTHONPATH=src python3 -m compileall src tests`

Result:

- 53 tests run;
- all passed.

Coverage includes snapshot freshness, deterministic IDs, reuse/idempotence, integrity verification, completeness metadata, self-comparison retained evidence, structural delta fixture cases, corruption detection, markdown bounds, and independence from current repository state after snapshot capture.

## 17. Vocab App Repeated-Snapshot Validation

Executed twice without modifying Vocab App:

- `repoctl snapshot --repository /home/chuck/ai-agent-tests/vocab-app`

Observed:

- first run: `snapshot_id = snap--c14c64658c4b0066`
- second run: same `snapshot_id = snap--c14c64658c4b0066`
- second run reused existing immutable snapshot
- stored artifact hashes validated successfully

## 18. Vocab App Self-Comparison Result

Executed:

- `repoctl compare snap--c14c64658c4b0066 snap--c14c64658c4b0066 --repository /home/chuck/ai-agent-tests/vocab-app`

Observed:

- `comparison_id = cmp--3123f9c78943d442`
- zero additions/removals/content changes/location changes
- retained evidence preserved, for example:
  - files unchanged: 12
  - symbols retained: 27
  - module dependencies retained: 2
  - calls retained: 13
  - test references retained: 20

## 19. Controlled Fixture Before/After Comparison Result

Controlled fixture validation demonstrated non-zero structural delta with direct source confirmation.

Verified categories included:

- one tracked file addition (`module_c.py`)
- tracked file content changes
- requirements declaration-list change
- top-level symbol addition (`new_func`)
- internal dependency addition
- static call addition
- test-reference addition
- separate parse-failure fixture case

Comparison evidence matched the fixture source changes mechanically.

## 20. Practical Product-Check Result

Using only `comparison.json` / `comparison.md`, Repo Control Plane identified the initial mechanical change footprint for the controlled fixture without broad manual repository reconnaissance.

The generated comparison surfaced:

- file additions/content changes;
- symbol additions;
- internal relationship changes;
- test-reference changes;
- parse-failure evidence where introduced.

Direct source inspection confirmed the comparison evidence.

## 21. Deterministic-Output Validation

Validated through automated tests and runtime checks:

- identical deterministic scan evidence yields identical snapshot IDs;
- repeated compare of the same named snapshots yields byte-identical comparison artifacts;
- changing the current repository after snapshot capture does not alter comparison results for the same snapshot pair.

## 22. Target-Repository Before/After Git Status

Exact Vocab App porcelain-v2 before/after equality check around repeated snapshot and self-compare validation:

- `STATUS_MATCH=1`

No target mutation was observed.

## 23. Limitations

- tracked-file structural scope only;
- no rename inference;
- no semantic interpretation, quality judgment, or risk scoring;
- no source-body semantic comparison beyond deterministic inventories and relationships.

## 24. Milestone 005 Opportunities (Not Implemented)

- bounded local analysis layer over structural delta evidence;
- deterministic-to-AI handoff using explicit before/after structural packets;
- anomaly prioritization on top of immutable deterministic comparison artifacts.

## 25. Final Repo Control Plane `git status --short`

At closeout:

- `M README.md`
- `M src/repoctl/cli.py`
- `M src/repoctl/scanner/core.py`
- `?? src/repoctl/compare/`
- `?? src/repoctl/snapshot/`
- `?? tests/test_snapshot_compare.py`
- `?? docs/004_deterministic_snapshot_delta_audit_closeout.md`

No commit or push was performed during this closeout.