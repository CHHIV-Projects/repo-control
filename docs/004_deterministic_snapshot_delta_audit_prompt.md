# Milestone 004 — Deterministic Snapshot and Structural Delta Audit

Prompt file:

`004_deterministic_snapshot_delta_audit_prompt.md`

Required closeout file:

`004_deterministic_snapshot_delta_audit_closeout.md`

## Objective

Add deterministic repository snapshots and before/after structural comparison to Repo Control Plane.

Milestones 001–003 established:

- deterministic repository facts;
- deterministic internal relationships;
- bounded task-oriented context packs.

Milestone 004 must answer a different question:

    What mechanically changed between two known repository states?

Add:

    repoctl snapshot [--repository <path>]

and:

    repoctl compare <before_snapshot_id> <after_snapshot_id> [--repository <path>]

The result must provide factual structural delta evidence such as:

- files added, removed, or content-changed;
- requirements declarations changed;
- top-level symbols added or removed;
- symbol source-location changes;
- internal dependency relationships added or removed;
- static call relationships added or removed;
- test-reference relationships added or removed;
- parse failures introduced or resolved;
- relevant ambiguity/relationship-resolution changes;
- before/after Git-state metadata.

This milestone does NOT judge whether those changes are good, bad, risky, spaghetti code, architectural improvement, or regression.

It records evidence.

No AI is authorized in Milestone 004.

---

# Controlling Documents

Read and follow:

- `docs/Repo_Control_Plane_v0.1_Architecture_and_Implementation_Plan.md`
- `docs/001_deterministic_repository_scanner_prompt.md`
- `docs/001_deterministic_repository_scanner_closeout.md`
- `docs/002_repository_relationships_prompt.md`
- `docs/002_repository_relationships_closeout.md`
- `docs/003_deterministic_context_pack_generator_prompt.md`
- `docs/003_deterministic_context_pack_generator_closeout.md`

Milestones 001–003 are trusted baselines.

Preserve:

- read-only target-repository behavior;
- deterministic outputs;
- external state storage;
- canonical repository identity;
- transactional publishing;
- conservative AST/relationship resolution;
- no target-code execution;
- no Git writes;
- context-pack behavior.

Do not redesign existing capabilities unless a narrowly necessary integration change is required.

---

# Project and Validation Target

Repo Control Plane:

`/home/chuck/projects/repo-control`

Primary real-repository validation target:

`/home/chuck/ai-agent-tests/vocab-app`

Photo Organizer remains explicitly out of scope.

Do not inspect, scan, snapshot, compare, query, modify, benchmark, or otherwise access Photo Organizer during Milestone 004.

---

# Repo Control Plane Git Preflight

Before coding:

1. confirm Repo Control Plane worktree is completely clean;
2. confirm current branch and HEAD;
3. confirm upstream state if configured;
4. stop and report any unexpected pre-existing changes.

Do not automatically reset, clean, restore, stage, commit, or discard anything.

Do not commit or push unless separately instructed.

---

# Existing Commands

Preserve:

    repoctl scan <repository>
    
    repoctl context "<query>" [--repository <path>]

Add exactly:

    repoctl snapshot [--repository <path>]
    
    repoctl compare <before_snapshot_id> <after_snapshot_id> [--repository <path>]

Do not add additional user-facing commands in this milestone.

---

# Repository Selection

Use the same repository-selection behavior established for `repoctl context`.

When `--repository` is omitted:

- resolve the Git work tree containing the current working directory.

When supplied:

    --repository <path>

the path may identify any location within a Git work tree, and Repo Control Plane must resolve the canonical Git root.

Non-Git targets fail clearly and non-zero.

Snapshot and compare state must remain associated with the existing location-specific `repository_id`.

---

# 1. Snapshot Semantics

`repoctl snapshot` captures the deterministic repository evidence that exists when the command runs.

It must first invoke/reuse the current Milestone 001/002 scan pipeline.

Do not snapshot stale scan artifacts without performing a current scan.

If the current scan fails:

- snapshot creation fails;
- no partial snapshot is published;
- an older successful snapshot is never overwritten.

The snapshot must capture the exact deterministic scan artifacts produced for that state.

Snapshot does not execute target code.

Snapshot does not stage files.

Snapshot does not commit.

Snapshot does not modify Git configuration.

Snapshot does not alter the target repository.

---

# 2. Snapshot Contents

Store snapshots beneath:

    ~/.local/share/repoctl/<repository_id>/snapshots/

Each snapshot directory contains exactly:

    snapshot.json
    repository.json
    files.json
    symbols.json
    tests.json
    dependencies.json
    summary.md

The six scan artifacts must be exact byte copies of the successful deterministic scan artifacts for the captured state.

Do not regenerate or independently reinterpret them while storing the snapshot.

`context.json` and `context.md` are NOT snapshot artifacts in Milestone 004.

Do not snapshot context packs.

---

# 3. Snapshot Identifier

Snapshot identity must be content-derived and deterministic.

Use:

    snapshot_id = "snap--" + first 16 lowercase hex characters of digest

The SHA-256 digest input must be constructed exactly as follows:

Start with:

    b"repoctl-snapshot-v1\0"

Then, in this fixed order:

    repository.json
    files.json
    symbols.json
    tests.json
    dependencies.json
    summary.md

For each artifact append:

    artifact filename encoded as ASCII
    b"\0"
    lowercase hexadecimal SHA-256 digest of the exact artifact bytes encoded as ASCII
    b"\0"

Then SHA-256 the complete byte sequence.

Use the first 16 lowercase hexadecimal characters.

Do not use:

- timestamps;
- random UUIDs;
- PID values;
- sequence counters.

Identical captured repository evidence must produce the same snapshot ID.

---

# 4. Snapshot Idempotence and Immutability

Snapshots are immutable.

If:

    repoctl snapshot

produces a snapshot ID that already exists:

- verify the existing snapshot contents match the newly generated deterministic snapshot exactly;
- if they match, reuse the existing snapshot successfully;
- do not rewrite it merely to update metadata;
- if they do not match, fail closed and report snapshot-state corruption/inconsistency.

Never mutate an existing snapshot into a different repository state.

Transactional publication is required for new snapshots.

---

# 5. `snapshot.json`

Use:

    "schema_version": 1

Include at minimum:

- schema version;
- snapshot ID;
- repository ID;
- canonical repository root;
- branch state/name;
- HEAD;
- working-tree cleanliness;
- structured working-tree status summary;
- scan artifact names;
- SHA-256 digest of each stored scan artifact;
- structural coverage/completeness metadata.

Do not include timestamps.

Do not include user/machine-specific transient metadata beyond information already required by deterministic repository identity/state contracts.

---

# 6. Working-Tree Coverage Contract

The existing scanner remains authoritative for what it analyzes.

Milestone 004 must NOT silently imply that untracked source files were structurally analyzed if the existing scanner does not analyze them.

Snapshots may be taken from clean or dirty repositories.

Tracked modified working-tree files are represented according to the existing scanner behavior.

Git-status evidence must remain visible.

`snapshot.json` must explicitly describe structural coverage.

At minimum expose:

    structural_scope = "tracked_files"

and:

    untracked_entries_present

If untracked entries exist, also record deterministic path evidence from the existing Git-status result.

Define:

    worktree_completeness = "complete_for_tracked_files"

when no untracked entries exist.

Define:

    worktree_completeness = "partial_worktree"

when one or more untracked entries exist.

This means:

- the snapshot remains valid;
- tracked-file structural evidence remains authoritative;
- untracked paths are known to exist;
- their contents must not be represented as structurally audited unless the scanner actually supports them.

Comparison output must preserve this limitation.

Do not expand Milestone 001 scanner scope merely to absorb untracked files in Milestone 004.

---

# 7. Compare Command

Syntax:

    repoctl compare <before_snapshot_id> <after_snapshot_id> [--repository <path>]

Comparison direction is significant:

    before -> after

The command must load two immutable snapshots belonging to the selected repository ID.

Fail clearly and non-zero if:

- either snapshot does not exist;
- snapshot integrity validation fails;
- repository IDs differ;
- required snapshot artifacts are missing;
- stored artifact hashes do not match actual snapshot artifact bytes;
- snapshot schema is unsupported.

Do not perform a current repository scan as part of comparison.

`repoctl compare` compares the two named immutable snapshots, regardless of the repository's current working state.

Comparing a snapshot to itself is valid and must produce a zero-delta result.

---

# 8. Comparison Output Location

Store comparison results beneath:

    ~/.local/share/repoctl/<repository_id>/comparisons/<comparison_id>/

Containing exactly:

    comparison.json
    comparison.md

Do not add other generated comparison artifacts.

---

# 9. Comparison Identifier

Use:

    comparison_id = "cmp--" + first 16 lowercase hex characters of SHA-256

Digest input:

    b"repoctl-comparison-v1\0"
    + before_snapshot_id encoded as ASCII
    + b"\0"
    + after_snapshot_id encoded as ASCII
    + b"\0"

Comparison ID must therefore be deterministic and directional.

Swapping before and after normally produces a different comparison ID.

---

# 10. Comparison Publication

Comparison output must be transactional.

If an identical comparison ID already exists:

- verify existing contents are byte-identical to newly generated output;
- reuse it successfully if identical;
- fail closed if the same comparison ID contains different content.

Do not overwrite immutable comparison evidence with different results.

---

# 11. `comparison.json`

Use:

    "schema_version": 1

Include at minimum:

- schema version;
- comparison ID;
- repository ID;
- before snapshot ID;
- after snapshot ID;
- before repository state summary;
- after repository state summary;
- structural coverage/completeness for both snapshots;
- file deltas;
- requirements deltas;
- symbol deltas;
- module dependency deltas;
- imported-symbol relationship deltas;
- static call relationship deltas;
- test-reference deltas;
- parse-failure deltas;
- relevant relationship-diagnostic deltas;
- deterministic aggregate counts.

The JSON is the complete deterministic structural comparison evidence.

`comparison.md` is a bounded human-readable projection of that evidence.

---

# 12. File Delta Contract

Compare tracked file evidence using relative path.

For each path classify mechanically as:

    added
    removed
    content_changed
    unchanged

A path is:

### added

present only in `after`.

### removed

present only in `before`.

### content_changed

present in both and the recorded file SHA-256 differs.

### unchanged

present in both and the recorded SHA-256 matches.

For changed files include where available:

- before SHA-256;
- after SHA-256;
- before/after size;
- before/after line count;
- before/after file type.

Do not infer why content changed.

Do not call delete+add a rename.

Do not use Git history for rename detection in this milestone.

---

# 13. Requirements Delta Contract

Compare the deterministic requirements records already captured by the scanner.

For each recognized requirements file:

- unchanged declaration list;
- added requirements file;
- removed requirements file;
- changed declaration list.

For a changed requirements file, preserve:

    before_declarations
    after_declarations

exactly as recorded by the snapshots.

Do not semantically parse versions.

Do not resolve packages.

Do not say dependency upgrade/downgrade unless exact textual evidence makes that mechanically explicit and such interpretation is already represented structurally.

The safest required output is before/after declaration evidence.

---

# 14. Symbol Delta Contract

Compare top-level recorded symbols only.

Use a stable comparison identity based on:

    relative_path
    symbol_kind
    symbol_name
    occurrence_ordinal

`occurrence_ordinal` is the deterministic source-order occurrence among symbols having the same:

    relative_path
    symbol_kind
    symbol_name

This avoids treating ordinary source-line movement as symbol removal/addition.

Classify symbol evidence as:

    added
    removed
    retained

For retained symbols, separately report:

    source_location_changed

when recorded start/end line evidence changed.

Do not claim that a symbol body changed merely because:

- its file hash changed;
- its source line changed.

Milestone 004 does not yet have symbol-body semantic fingerprints.

A file may therefore be:

    content_changed

while its recorded symbol inventory is unchanged.

That is valid factual evidence.

---

# 15. Module Dependency Delta Contract

Compare resolved Milestone 002 internal module dependency edges.

Logical edge identity must exclude incidental source-line movement.

Use the stable relationship fields necessary to identify:

- source/importing file;
- target internal file;
- import relationship kind;
- imported module/reference identity.

If the same logical edge exists in both snapshots but its source line changed:

- classify the edge as retained;
- optionally record relationship location change separately;
- do not classify it as removed + added solely because of line movement.

Report:

    added
    removed
    retained

module dependency counts and records.

---

# 16. Imported-Symbol Relationship Delta Contract

Compare resolved imported-symbol relationships using stable logical identity.

At minimum identity should preserve:

- importing file;
- local/imported binding name;
- target/source file;
- target symbol;
- target symbol kind;
- alias/binding identity where applicable.

Exclude source-line position from logical edge identity.

Report:

    added
    removed
    retained

and separately report source-location changes where recorded.

---

# 17. Static Call Relationship Delta Contract

Compare Milestone 002 statically resolved calls.

Stable call-edge identity must include:

- caller file;
- caller symbol kind/name;
- callee file;
- callee symbol kind/name;
- resolution kind.

Do not include call source line in edge identity.

Therefore moving the same proven call to another line does not fabricate architectural churn.

Report:

    added
    removed
    retained

and separately report call-location changes where available.

Do not claim runtime call behavior.

---

# 18. Test-Reference Delta Contract

Compare statically resolved test references.

Stable identity should include:

- test file;
- test class when applicable;
- test function/method;
- target file;
- target symbol;
- target symbol kind;
- reference kind.

Exclude source line from logical identity.

Report:

    added
    removed
    retained

and source-location changes separately where applicable.

Do not claim:

- coverage gained;
- coverage lost;
- test adequacy improved;
- test adequacy regressed.

Only static-reference evidence is authorized.

---

# 19. Parse-Failure Delta Contract

Compare recorded Python parse-failure evidence.

At minimum report:

    introduced_parse_failures
    resolved_parse_failures
    retained_parse_failures

Use deterministic path/error evidence already available from scanner artifacts.

Do not attempt to repair or reinterpret malformed code.

A newly introduced parse failure is factual evidence, not automatically an architectural judgment.

---

# 20. Relationship Diagnostic Delta Contract

Milestone 002 may contain large amounts of unresolved evidence.

Do not make generic external `no_tracked_module_match` noise a major human-readable audit section.

`comparison.json` may preserve deterministic count deltas by diagnostic reason.

For record-level structural audit, prioritize these reasons:

    ambiguous_module
    target_parse_failure
    shadowed_or_rebound
    unresolved_symbol
    wildcard_import

Report mechanically whether such diagnostic records were:

    added
    removed
    retained

when a stable deterministic record identity can be established.

Do not state that newly added diagnostics are necessarily defects.

---

# 21. Git-State Delta

The comparison must include the before/after Git-state facts captured by each snapshot:

- branch attached/detached state;
- branch name;
- HEAD;
- clean/dirty state;
- working-tree status counts/categories;
- worktree completeness.

This is evidence only.

Do not infer authorship, intent, or commit quality.

Do not traverse Git history in Milestone 004.

---

# 22. Structural Delta Summary

Calculate deterministic aggregate counts, at minimum:

## Files

- added;
- removed;
- content changed;
- unchanged.

## Symbols

- added;
- removed;
- retained;
- source-location changed.

## Internal relationships

For each relationship category:

- added;
- removed;
- retained;
- location changed where applicable.

## Tests

- test references added;
- removed;
- retained.

## Parse evidence

- introduced;
- resolved;
- retained failures.

## Requirements

- files added;
- files removed;
- files with changed declaration lists.

These are mechanical counts.

Do not calculate a quality score.

Do not calculate a risk score.

Do not calculate an architecture-health score.

---

# 23. Human-Readable `comparison.md`

Render `comparison.md` entirely from `comparison.json` / the same already-computed comparison result.

Do not perform new comparison logic in the renderer.

Use fixed section ordering:

1. `# Repository Structural Comparison`
2. `## Comparison State`
3. `## Structural Coverage`
4. `## File Changes`
5. `## Requirements Changes`
6. `## Symbol Changes`
7. `## Internal Dependency Changes`
8. `## Imported-Symbol Changes`
9. `## Static Call Changes`
10. `## Test Reference Changes`
11. `## Parse / Resolution Limitations`
12. `## Aggregate Delta Counts`

Sections remain present even when empty.

---

# 24. Bounded Markdown Reporting

`comparison.json` preserves complete deterministic comparison evidence.

`comparison.md` must remain bounded.

Use:

    MAX_MD_ITEMS_PER_SECTION = 50

For each detailed Markdown section:

- render at most 50 records;
- use deterministic ordering;
- record total record count;
- clearly state when additional records were omitted from Markdown.

Do not truncate the underlying `comparison.json` evidence.

Use mechanical ordering rather than relevance ranking.

Prefer:

1. relative path byte order;
2. symbol/relationship identity;
3. source line where needed as final display tie-break.

Do not use AI or heuristic importance ranking.

---

# 25. No Architectural Judgment Yet

Milestone 004 may state:

    4 files changed
    2 top-level symbols were added
    1 internal call edge was removed
    3 test references were added
    1 parse failure was introduced

Milestone 004 must NOT state:

    the change is risky
    complexity increased
    architecture deteriorated
    this is spaghetti code
    test coverage improved
    the refactor is good
    the refactor is bad
    this violates intended architecture

Those interpretations belong to later analysis layers.

---

# 26. Existing Context Command

Do not change Milestone 003 context selection semantics.

Snapshots do not automatically capture context packs.

Comparisons do not automatically execute context queries.

Context-pack versus historical-snapshot analysis is deferred.

Milestone 004 is repository-state comparison, not query-specific comparison.

---

# 27. README

Update README to document:

    repoctl snapshot [--repository <path>]

and:

    repoctl compare <before_snapshot_id> <after_snapshot_id> [--repository <path>]

Document:

- snapshots are content-derived and immutable;
- snapshot output remains outside target repositories;
- compare is directional;
- comparisons operate on named snapshots, not current working state;
- snapshots represent tracked-file structural scope;
- untracked entries make full worktree structural coverage partial;
- comparison is deterministic factual evidence, not architectural judgment;
- no Git writes occur.

Keep README current-state only.

---

# 28. Required Automated Tests

Add focused tests covering at least:

1. snapshot current repository;
2. snapshot explicit repository path;
3. invalid/non-Git repository failure;
4. snapshot performs a fresh scan;
5. deterministic snapshot ID;
6. identical state reuses identical snapshot;
7. immutable existing snapshot verification;
8. transactional snapshot publication;
9. required snapshot artifact set;
10. stored artifact hashes validate;
11. clean-worktree completeness metadata;
12. untracked entry produces `partial_worktree`;
13. snapshot does not mutate target Git state;
14. compare two valid snapshots;
15. compare same snapshot to itself gives zero structural delta;
16. missing snapshot failure;
17. corrupted snapshot failure;
18. deterministic comparison ID;
19. directional comparison ID changes when before/after swap;
20. file added detection;
21. file removed detection;
22. file content-changed detection;
23. requirements declaration-list change detection;
24. top-level symbol addition/removal;
25. symbol line movement is not removal/addition;
26. module dependency addition/removal;
27. imported-symbol relationship addition/removal;
28. static call edge addition/removal;
29. call line movement is not removal/addition;
30. test-reference addition/removal;
31. parse failure introduced/resolved;
32. relevant relationship diagnostic delta;
33. `no_tracked_module_match` does not dominate Markdown audit output;
34. Markdown 50-item section bound;
35. `comparison.json` remains untruncated;
36. repeated comparison produces byte-identical artifacts;
37. compare does not depend on current repository state after snapshots exist;
38. all Milestone 001–003 tests remain passing.

Use temporary Git repository fixtures for before/after mutations.

It is acceptable and expected for tests to perform Git writes inside disposable test fixture repositories.

Repo Control Plane itself must remain read-only toward user target repositories.

---

# 29. Vocab App Validation

After automated tests pass, validate read-only snapshot behavior against:

`/home/chuck/ai-agent-tests/vocab-app`

Do not assume its branch, HEAD, or current status.

Capture the actual state at validation time.

Run:

    repoctl snapshot --repository /home/chuck/ai-agent-tests/vocab-app

Run it twice without changing Vocab App.

Verify:

- both runs resolve to the same snapshot ID;
- stored snapshot artifacts are unchanged;
- artifact hashes validate;
- Vocab App Git porcelain-v2 status is byte-identical before and after;
- no target files are created.

Then run:

    repoctl compare <snapshot_id> <snapshot_id> \
      --repository /home/chuck/ai-agent-tests/vocab-app

Verify:

- zero structural delta;
- deterministic comparison ID;
- complete/partial worktree status matches the actual captured state;
- no target mutation occurs.

Do not modify Vocab App merely to create a delta example.

---

# 30. Controlled Structural Delta Validation

Use a temporary/disposable Git repository fixture to demonstrate a non-zero before/after comparison.

The controlled change should exercise several structural categories, for example:

Before:

    module_a.py
    module_b.py
    test_module_a.py

After a controlled fixture change:

- modify one tracked file;
- add one tracked Python file;
- add/remove a top-level function;
- add/remove an internal import or call edge;
- add or remove a static test reference;
- optionally introduce then resolve a parse-failure case in a separate fixture test.

Create:

    before snapshot
        ->
    controlled fixture mutation
        ->
    after snapshot
        ->
    comparison

Verify the generated structural delta directly against the fixture source.

Do not use AI for the verification.

---

# 31. Practical Product Check

Milestone 004 must include one small factual audit demonstration answering:

    "What structurally changed between these two fixture states?"

Using only `comparison.json` / `comparison.md`, demonstrate that Repo Control Plane can identify the initial mechanical change footprint without broad manual repository reconnaissance.

Closeout should state:

- file changes detected;
- symbol changes detected;
- relationship changes detected;
- test-reference changes detected;
- any parse/coverage limitations;
- whether direct source inspection confirmed the comparison evidence.

Do not make quality judgments.

---

# Explicit Non-Goals

Do not implement:

- GPT-OSS;
- Ollama;
- Aider;
- Codex/Copilot integration;
- architecture scoring;
- risk scoring;
- spaghetti-code detection;
- complexity metrics;
- duplicate-code detection;
- semantic change interpretation;
- Git-history traversal;
- commit-range reconstruction;
- rename inference;
- blame analysis;
- author analysis;
- branch creation;
- staging;
- committing;
- pushing;
- snapshot labels/timestamps;
- snapshot deletion;
- retention policies;
- context-pack historical comparison;
- source-code execution;
- runtime tracing;
- web UI;
- daemon/background service;
- Docker/containerization;
- Photo Organizer access.

---

# Implementation Discipline

Extend the existing application.

Preferred flow:

    target repository
        ↓
    existing deterministic scan
        ↓
    six current scan artifacts
        ↓
    deterministic content-derived snapshot
        ↓
    immutable snapshot storage

and:

    before snapshot
        +
    after snapshot
        ↓
    deterministic structural comparator
        ↓
    comparison.json
        ↓
    bounded comparison.md

Keep responsibilities separate:

    scanner
        -> current repository facts
    
    snapshot layer
        -> immutable capture/integrity
    
    comparison layer
        -> before/after deterministic structural delta
    
    renderer
        -> human-readable projection only

Do not create duplicate scanner or relationship-analysis logic.

Prefer narrowly scoped modules such as:

    src/repoctl/snapshot/
    src/repoctl/compare/

or an equivalently clean existing-package organization.

Exact module decomposition is an ordinary implementation choice.

No third-party dependency should be introduced unless strictly necessary and explicitly justified before use.

---

# Stop / Escalation Conditions

Stop and report rather than broadening scope if implementation appears to require:

- target-repository Git writes;
- AI/semantic interpretation;
- Git-history traversal;
- executing/importing target code;
- modifying Milestone 001 tracked-file semantics;
- scanning untracked file contents;
- rename inference;
- architecture/risk scoring;
- database infrastructure;
- Docker;
- Photo Organizer access;
- major incompatible redesign of existing artifact schemas.

If current deterministic artifacts cannot prove a claimed structural delta, do not claim it.

Prefer explicit limitation evidence to inference.

Once the contracts in this prompt are satisfied, make ordinary implementation decisions locally rather than extending pre-coding reconnaissance.

---

# Validation Before Closeout

Run at minimum:

- full Repo Control Plane automated test suite;
- Python compile/syntax validation as appropriate;
- deterministic snapshot repeat tests;
- deterministic comparison repeat tests;
- snapshot integrity/corruption tests;
- controlled temporary-repository structural delta test;
- Vocab App repeated snapshot/idempotence validation;
- Vocab App self-comparison zero-delta validation;
- direct evidence verification;
- Vocab App exact Git-status before/after equality;
- Repo Control Plane `git diff --check`;
- Repo Control Plane `git status --short`.

---

# Required Closeout

Create:

`docs/004_deterministic_snapshot_delta_audit_closeout.md`

Include:

1. implementation summary;
2. files added/modified;
3. snapshot CLI behavior;
4. compare CLI behavior;
5. snapshot ID contract;
6. comparison ID contract;
7. snapshot storage/artifact structure;
8. `snapshot.json` schema at useful high level;
9. worktree coverage/completeness behavior;
10. `comparison.json` schema at useful high level;
11. file-delta rules;
12. symbol-delta rules;
13. relationship/test-reference delta rules;
14. parse/diagnostic delta rules;
15. bounded Markdown behavior;
16. automated test results;
17. Vocab App repeated-snapshot validation;
18. Vocab App self-comparison result;
19. controlled fixture before/after comparison result;
20. practical product-check result;
21. deterministic-output validation;
22. target-repository before/after Git status;
23. limitations;
24. Milestone 005 opportunities without implementing them;
25. final Repo Control Plane `git status --short`.

Do not commit or push unless separately instructed.

---

# Acceptance Criteria

Milestone 004 passes only if:

- Milestones 001–003 remain intact;
- `repoctl snapshot` captures a fresh deterministic scan;
- snapshot IDs are deterministic and content-derived;
- snapshots are immutable and integrity-verifiable;
- snapshot storage remains external to the target repository;
- worktree structural coverage is explicit;
- untracked entries cannot create false claims of complete worktree analysis;
- `repoctl compare` compares named immutable snapshots;
- comparison direction is explicit;
- file, requirements, symbol, relationship, test-reference, and parse deltas are mechanically correct;
- ordinary line movement does not fabricate relationship removal/addition;
- `comparison.json` preserves complete deterministic evidence;
- `comparison.md` is bounded and deterministic;
- identical snapshots produce zero structural delta;
- controlled fixture comparison matches direct source evidence;
- Vocab App is not modified;
- all automated tests pass;
- no AI, semantic judgment, Git writes, Docker, or Photo Organizer access is introduced.
