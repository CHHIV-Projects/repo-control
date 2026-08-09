# Milestone 003 — Deterministic Context Pack Generator

Prompt file:

`003_deterministic_context_pack_generator_prompt.md`

Required closeout file:

`003_deterministic_context_pack_generator_closeout.md`

## Objective

Build the first task-oriented Repo Control Plane capability:

    repoctl context "<query>" [--repository <path>]

Milestones 001 and 002 established deterministic repository facts and relationships.

Milestone 003 must convert those facts into a bounded, deterministic navigation context pack that helps an architect or coding agent answer:

- Where should I start looking?
- Which files and symbols are most directly related to this topic?
- Which internal modules are connected?
- Which tests statically reference the relevant code?
- What deterministic limitations or ambiguities should I know about?

The purpose is to reduce repeated broad repository reconnaissance.

This is still deterministic repository intelligence.

No AI is authorized in Milestone 003.

The context pack is a navigation aid, not source-code authority and not architectural analysis.

---

# Controlling Documents

Read and follow:

- `docs/Repo_Control_Plane_v0.1_Architecture_and_Implementation_Plan.md`
- `docs/001_deterministic_repository_scanner_prompt.md`
- `docs/001_deterministic_repository_scanner_closeout.md`
- `docs/002_repository_relationships_prompt.md`
- `docs/002_repository_relationships_closeout.md`

Milestones 001 and 002 are trusted baselines.

Preserve:

- read-only target-repository access;
- deterministic output;
- canonical repository identification;
- external state;
- transactional publishing;
- conservative relationship resolution;
- ambiguity preservation;
- parse-failure behavior;
- no target-code execution;
- no Git writes.

Do not redesign those capabilities.

---

# Project and Validation Target

Repo Control Plane:

`/home/chuck/projects/repo-control`

Primary validation target:

`/home/chuck/ai-agent-tests/vocab-app`

Photo Organizer remains explicitly out of scope.

Do not inspect, scan, query, modify, benchmark, or otherwise access Photo Organizer during Milestone 003.

---

# Git Preflight

Before coding:

1. confirm Repo Control Plane worktree is completely clean;
2. confirm current branch and HEAD;
3. confirm upstream state if configured;
4. stop and report if unexpected pre-existing worktree changes exist.

Do not automatically repair, clean, stage, reset, or discard repository state.

Do not commit or push unless separately instructed.

---

# Existing Commands

Preserve:

    repoctl scan <repository>

Add:

    repoctl context "<query>" [--repository <path>]

Do not add other user-facing commands.

---

# Repository Selection

For:

    repoctl context "<query>"

the target repository defaults to the Git work tree containing the current working directory.

The command must resolve the actual Git repository root before analysis.

An explicit target may be supplied with:

    repoctl context "<query>" --repository <path>

The explicit path may point anywhere inside the target Git work tree; Repo Control Plane must resolve the canonical Git root.

If:

- the current directory is not inside a Git work tree; or
- an explicit repository path does not resolve to a Git work tree;

fail clearly and non-zero.

Do not search parent directories beyond ordinary Git work-tree resolution semantics.

---

# Freshness Contract

A context pack must describe the repository state that exists when the context command runs.

Do not blindly consume potentially stale Milestone 001/002 artifacts.

`repoctl context` must invoke/reuse the existing deterministic scan pipeline for the selected repository before generating context.

The implementation may reuse the in-memory scan result and/or the newly published canonical scan artifacts.

Do not create a second scanner.

If the scan fails, context generation must fail.

Do not generate context from stale prior scan data after a current scan failure.

Target-repository access remains read-only.

---

# Query Contract

The query is navigation text supplied by the user.

Examples:

    "synonym"
    "synonym handling"
    "get_sheet"
    "source readiness"

Milestone 003 does not implement semantic search.

Query matching is lexical and deterministic.

## Canonical query

Derive:

    canonical_query

by:

1. stripping leading/trailing whitespace;
2. collapsing every run of whitespace to one ASCII space.

The original supplied query may be preserved for display, but matching and context identity must use the canonical query.

An empty canonical query must fail clearly.

## Query tokens

Derive deterministic search tokens from the canonical query.

Required rules:

- case-insensitive matching using `casefold()`;
- split words on whitespace and common path/symbol separators;
- `_`, `-`, `.`, `/`, and `\` act as token boundaries;
- discard empty tokens;
- preserve token order;
- duplicate tokens collapse to their first occurrence;
- do not perform stemming;
- do not use synonyms;
- do not use embeddings;
- do not use AI;
- do not contact external services.

For example:

    "source readiness"

produces tokens conceptually equivalent to:

    source
    readiness

and:

    "get_synonyms_nltk"

must allow matching both the exact symbol text and its component tokens.

Document the exact tokenization rule in code/tests.

---

# Context Identity and External Location

Context output must remain outside the target repository.

Use the existing repository state root:

    ~/.local/share/repoctl/<repository_id>/

Add:

    contexts/

Each distinct canonical query gets a deterministic context identifier:

    <query-slug>--<12-hex-digest>

The digest must be the first 12 lowercase hexadecimal characters of SHA-256 over UTF-8 bytes of the canonical casefolded query.

The readable query slug must:

- be derived from the canonical casefolded query;
- use lowercase ASCII letters/digits and `-`;
- replace runs of unsupported characters/separators with `-`;
- strip leading/trailing `-`;
- use `query` if the slug would otherwise be empty.

Example shape only:

    synonym-handling--1a2b3c4d5e6f

The example digest is not normative.

Output:

    ~/.local/share/repoctl/<repository_id>/
        contexts/
            <context_id>/
                context.json
                context.md

Do not create additional context artifacts in Milestone 003.

Publishing must be transactional so a failed generation does not replace a previously successful pack with partial output.

---

# Schema

`context.json` must use:

    "schema_version": 1

It must contain at minimum:

- schema version;
- repository identifier;
- repository root;
- branch;
- HEAD;
- working-tree cleanliness/status summary;
- original query;
- canonical query;
- query tokens;
- context identifier;
- selection/ranking contract identifier or version;
- match status;
- seed matches;
- selected files;
- selected symbols;
- relevant internal relationships;
- relevant tests/test references;
- relevant ambiguity/parse limitations;
- selection counts/truncation evidence.

`context.md` must be rendered solely from `context.json`/the same deterministic structured result.

Do not derive independent facts while rendering Markdown.

---

# Core Principle — Evidence, Not Guessing

The context generator must select from facts already deterministically established by the scan and relationship layers.

It may use:

- tracked paths;
- module identities;
- top-level symbol names;
- imports;
- internal module dependencies;
- resolved imported-symbol relationships;
- resolved static calls;
- resolved test references;
- parse failures;
- ambiguity diagnostics.

It may not infer:

- architectural responsibility;
- semantic intent;
- runtime behavior;
- business meaning;
- code quality;
- whether a test is sufficient;
- whether a file should be changed.

The context pack says:

    "these repository facts are related to the lexical query"

not:

    "these are definitely the files that must be modified."

Source code remains authoritative.

---

# Deterministic Seed Matching

Milestone 003 needs a transparent deterministic relevance mechanism.

Do not implement opaque search ranking.

For each tracked Python file and recorded top-level symbol, calculate query evidence from the following fields only:

## File evidence

- relative path;
- logical module identity when available.

## Symbol evidence

- symbol name;
- containing file path;
- containing logical module identity.

## Matching

A field may provide:

### Exact canonical-query match

The full canonical casefolded query equals the casefolded field value.

### Full-query substring match

The full canonical casefolded query occurs within the casefolded field value.

### Token matches

Individual query tokens occur as complete components or substrings within the supported field.

Use one documented scoring function.

Required weighting order from strongest to weakest:

1. exact symbol-name match;
2. exact path/module component match;
3. full-query substring match;
4. multiple query-token matches;
5. individual query-token match.

The exact small integer weights are an implementation choice, but they must:

- be defined as named constants;
- be documented;
- be deterministic;
- be covered by exact tests;
- not depend on repository iteration order.

Tie-breaking must use:

1. higher score;
2. more distinct query tokens matched;
3. symbol before file only when comparing otherwise equivalent symbol/file seed records;
4. deterministic repository path byte order;
5. source line;
6. symbol name.

Do not use AI to rank.

Do not use Git history to rank.

Do not use file size or code complexity to rank.

---

# Seed Selection

A seed is a directly lexical-matching file or top-level symbol.

Select at most:

    12 seed records

for Milestone 003.

This limit is fixed for schema version 1.

If more than 12 candidates qualify:

- keep the highest-ranked 12;
- record total candidate count;
- record that truncation occurred.

Do not silently discard the existence of truncation.

If no seed candidates exist:

    match_status = "no_matches"

Generate a valid deterministic context pack containing repository/query metadata and zero selected repository items.

A no-match result is not a system error and should exit successfully.

Do not broaden matching automatically when no result exists.

---

# Relationship Expansion

After seed selection, perform at most one deterministic relationship hop.

The purpose is to add directly connected navigation evidence without allowing the context to expand into the entire repository.

Eligible one-hop relationships:

- internal module dependency involving a seed file;
- resolved imported-symbol relationship involving a seed file/symbol;
- resolved static call where the caller or callee is a seed symbol;
- resolved test reference whose target is a seed file/symbol.

Do not recursively expand relationships from newly added neighbors.

Milestone 003 is exactly:

    lexical seed
        +
    one relationship hop

not:

    graph traversal until exhausted

---

# Selected File Limit

A context pack may contain at most:

    20 selected files

Selection order:

1. files containing selected seed symbols;
2. directly matched seed files;
3. one-hop production-code neighbors;
4. one-hop test files.

Within each priority class, use deterministic relevance score/evidence and path ordering.

If more than 20 files qualify:

- retain the first 20 under the deterministic policy;
- record total qualifying count;
- record truncation.

Do not dynamically increase the limit.

---

# Selected Symbol Limit

Include at most:

    40 selected/relevant top-level symbols

Priority:

1. seed symbols;
2. symbols directly participating in a one-hop relationship with seed symbols;
3. top-level symbols in a selected seed file that themselves match at least one query token.

Do not dump every symbol from every selected file into the context pack.

Record truncation if applicable.

---

# Relationship Limit

Include at most:

    40 resolved relationship records

limited to relationships involving selected files/symbols.

Priority:

1. relationships directly involving a seed symbol;
2. relationships directly involving a seed file;
3. resolved test references to seed symbols/files;
4. other eligible one-hop relationships.

Use deterministic tie-breaking.

Record total qualifying count and truncation.

---

# Test Evidence

Include test evidence when Milestone 002 statically resolves a test reference to a selected production symbol/file.

The context may state:

    test_limit_zero
    statically calls
    vocab_utils.py::normalize_synonym_candidates

It must not say:

    normalize_synonym_candidates is adequately tested
    this test covers all synonym behavior
    test coverage is sufficient

Include:

- test file;
- test class when applicable;
- test function/method;
- target symbol/file;
- reference kind;
- source line.

Include at most:

    20 test references

using deterministic ordering/priority.

Record truncation if needed.

---

# Unresolved and Ambiguous Evidence Filtering

Milestone 002 intentionally records comprehensive unresolved relationship evidence.

Milestone 003 must NOT dump all unresolved relationships into context packs.

In particular, ordinary:

    no_tracked_module_match

records for standard-library or third-party imports/calls should not be included merely because they exist.

Include diagnostic relationship evidence only when it materially limits interpretation of a selected seed or selected internal relationship.

Include:

- ambiguous internal module resolution involving a selected file/reference;
- `target_parse_failure` affecting a selected relationship;
- `shadowed_or_rebound` where it prevented an otherwise relevant supported resolution;
- `unresolved_symbol` involving a selected internal module/reference;
- wildcard-import uncertainty involving a selected internal module.

Do not include generic unrelated external/unresolved noise.

The complete Milestone 002 evidence remains available in `dependencies.json`.

The context pack is a bounded navigation projection, not an exhaustive diagnostics dump.

---

# Parse Failures

If a selected or directly related Python file has an AST parse failure:

- include the file;
- include the parse-failure limitation;
- do not fabricate symbols or relationships;
- do not fail the context command if the underlying scan itself successfully records the parse failure.

The context pack must make the limitation visible.

---

# Context Markdown

`context.md` must be concise and optimized for human/coding-agent navigation.

Use fixed section ordering:

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

## Suggested Source Inspection

This section is deterministic.

It should list selected files in the exact selected-file priority order.

For each file include short mechanical reasons such as:

    exact symbol match: get_sheet
    path token match: synonym
    imports seed module: vocab_utils
    called by seed symbol
    referenced by test

Do not generate prose explaining what the file "does."

Do not include source-code bodies or arbitrary snippets in Milestone 003.

The coding agent is expected to inspect authoritative source after receiving the navigation context.

---

# Determinism

Given:

- the same canonical repository location;
- same repository state;
- same canonical query;

two consecutive context commands must produce byte-for-byte identical:

    context.json
    context.md

No timestamps.

No runtime duration.

No random identifiers.

No locale-dependent output.

No nondeterministic dictionary/set iteration.

Markdown layout is part of the deterministic contract.

Add exact repeated-generation tests.

---

# README

Update README to document:

    repoctl context "<query>" [--repository <path>]

Document:

- default current-working-directory repository behavior;
- explicit repository option;
- external context location;
- lexical/deterministic nature;
- seed + one-hop behavior;
- fixed bounded limits;
- no AI/semantic search;
- context is navigation evidence, not source authority.

Keep documentation current-state only.

---

# Required Automated Tests

Add focused tests for at least:

1. context command using current repository;
2. context command using explicit `--repository`;
3. invalid/non-Git repository;
4. empty query rejection;
5. canonical whitespace normalization;
6. deterministic tokenization;
7. exact symbol match ranking;
8. file/path token matching;
9. deterministic tie-breaking;
10. 12-seed truncation;
11. one-hop dependency expansion;
12. one-hop imported-symbol expansion;
13. one-hop call expansion;
14. related-test inclusion;
15. no recursive second-hop expansion;
16. 20-file bound;
17. 40-symbol bound;
18. 40-relationship bound;
19. 20-test-reference bound;
20. truncation metadata;
21. no-match successful context pack;
22. generic `no_tracked_module_match` noise excluded;
23. relevant ambiguity retained;
24. relevant parse-failure limitation retained;
25. no source-code bodies/snippets emitted;
26. context output stored outside target repository;
27. byte-for-byte repeated context determinism;
28. context invokes current scan rather than trusting stale state;
29. target Git state unchanged before/after context generation;
30. all Milestone 001 and 002 tests remain passing.

Use temporary repositories/fixtures for ranking and graph-boundary cases.

Do not rely solely on Vocab App.

---

# Vocab App Validation

After automated tests pass, validate against:

`/home/chuck/ai-agent-tests/vocab-app`

Do not assume its branch, HEAD, or contents remain static.

Capture its actual current state at validation time.

At minimum run context queries that exercise different navigation patterns.

Recommended examples, subject to current repository contents:

    repoctl context "synonym" \
      --repository /home/chuck/ai-agent-tests/vocab-app

and:

    repoctl context "get_sheet" \
      --repository /home/chuck/ai-agent-tests/vocab-app

Verify against direct read-only source evidence that:

- the strongest obvious matching files/symbols are included;
- one-hop internal production relationships are included when present;
- related tests are included when statically proven;
- unrelated repository files are not broadly dumped into the pack;
- generic external unresolved evidence is not dumped into the pack;
- selected file/symbol/relationship limits are respected;
- no speculative architectural descriptions appear.

Record exact Vocab App Git porcelain-v2 status before and after validation and prove equality.

Do not modify Vocab App.

---

# Practical Reconnaissance-Reduction Check

Milestone 003 should include one small manual validation of the original product goal.

Using the generated Vocab App context pack, answer only this mechanical question from the pack:

    "Which files and symbols should a coding agent inspect first for synonym handling?"

Then compare that recommendation to direct read-only repository evidence.

The closeout should report:

- how many files the context pack suggested;
- which files were top-ranked;
- whether those files actually contain the relevant source/test relationships;
- whether broad repository discovery would still have been necessary to locate the initial code area.

This is not a Codex token/cost benchmark yet.

Do not invoke a second paid coding agent merely to perform the check.

The purpose is to establish whether deterministic context is already useful enough to justify Milestone 004.

---

# Explicit Non-Goals

Do not implement:

- GPT-OSS;
- Ollama;
- Aider;
- Codex/Copilot integration;
- embeddings;
- vector databases;
- semantic search;
- fuzzy ML ranking;
- source-code summarization;
- architectural interpretation;
- code-quality scoring;
- complexity metrics;
- duplicate detection;
- Git-history relevance ranking;
- snapshot comparison;
- milestone change auditing;
- protected-area workflow metadata;
- source-code snippets/context-body extraction;
- Git writes;
- branch management;
- commit/push operations;
- web UI;
- daemon/background service;
- Docker/containerization;
- Photo Organizer access.

---

# Implementation Discipline

Extend the existing Repo Control Plane architecture.

Do not create a second repository-intelligence engine.

Preferred flow:

    current target repository
        ↓
    existing scan pipeline
        ↓
    Milestone 001 facts
        +
    Milestone 002 relationships
        ↓
    deterministic query matcher
        ↓
    seed selection
        ↓
    one-hop bounded expansion
        ↓
    context.json
        ↓
    context.md

Keep query selection/ranking in a focused module.

Keep rendering separate from selection.

Use named constants for:

    MAX_SEEDS = 12
    MAX_FILES = 20
    MAX_SYMBOLS = 40
    MAX_RELATIONSHIPS = 40
    MAX_TEST_REFERENCES = 20

Do not hide limits in scattered literals.

Prefer small typed data structures where they improve clarity.

No third-party dependency should be introduced unless strictly necessary and explicitly justified before use.

---

# Stop / Escalation Conditions

Stop and report rather than expanding scope if implementation appears to require:

- AI or semantic inference;
- embeddings/vector search;
- execution/import of target code;
- target-repository writes;
- Git mutation;
- Photo Organizer access;
- runtime dependency resolution;
- recursive/unbounded graph traversal;
- Git-history indexing;
- database/search-service infrastructure;
- Docker;
- source-code summarization;
- major redesign of Milestone 001/002 schemas.

If lexical matching cannot establish relevance, return no match rather than guessing.

If relationship expansion cannot be proven, omit it rather than guessing.

After the contracts in this prompt are satisfied, ordinary implementation choices should be made using the smallest clean solution rather than extending pre-coding reconnaissance.

---

# Validation Before Closeout

Run at minimum:

- full Repo Control Plane automated test suite;
- Python syntax/compile checks as appropriate;
- repeated context-generation determinism checks;
- Vocab App validation queries;
- direct source comparison for representative results;
- practical reconnaissance-reduction check;
- Vocab App Git-status before/after equality;
- Repo Control Plane `git diff --check`;
- Repo Control Plane `git status --short`.

---

# Required Closeout

Create:

`docs/003_deterministic_context_pack_generator_closeout.md`

Include:

1. implementation summary;
2. files added/modified;
3. CLI syntax and repository selection behavior;
4. query canonicalization/tokenization contract;
5. ranking/seed-selection rules;
6. one-hop expansion rules;
7. fixed context limits;
8. `context.json` schema at a useful high level;
9. deterministic `context.md` structure;
10. unresolved/ambiguous filtering behavior;
11. automated test results;
12. Vocab App validation results;
13. representative `synonym` and/or `get_sheet` context results;
14. practical reconnaissance-reduction result;
15. determinism validation;
16. Vocab App before/after Git status;
17. limitations;
18. Milestone 004 opportunities without implementing them;
19. final Repo Control Plane `git status --short`.

Do not commit or push unless separately instructed.

---

# Acceptance Criteria

Milestone 003 passes only if:

- existing `repoctl scan` behavior remains intact;
- `repoctl context "<query>"` works from inside a Git repository;
- explicit `--repository` works;
- context always reflects a current deterministic scan;
- lexical seed matching is deterministic and transparent;
- one-hop relationship expansion is bounded and non-recursive;
- context packs remain within fixed limits;
- generic unresolved external noise is excluded;
- relevant ambiguity/parse limitations remain visible;
- `context.json` and `context.md` are byte-for-byte deterministic;
- no source code is executed;
- no target repository is modified;
- Vocab App validation matches direct source evidence;
- the context pack materially narrows the initial source-inspection area for the Vocab App example;
- no AI, semantic search, Git writes, Docker, or Photo Organizer access is introduced.





# Product Owner / Architect Clarification Addendum — Milestone 003 Selection Contract

This addendum resolves the remaining pre-coding determinism questions.

It does not broaden Milestone 003 scope.

## 1. Exact Tokenization Contract

Milestone 003 must NOT perform camelCase or PascalCase splitting.

Examples:

    HTTPServer
        -> httpserver

    getHTTPServer
        -> gethttpserver

Do not infer:

    http
    server

or:

    get
    http
    server

unless those components are separately present through one of the explicitly supported separators.

### Token separators

The following ASCII characters are explicit token boundaries:

    _
    -
    .
    /
    \

Whitespace is also a token boundary.

Use Python string whitespace semantics consistently for canonical whitespace handling and tokenization.

Do not perform Unicode normalization.

Do not strip accents or transliterate characters.

Do not treat arbitrary Unicode punctuation as a separator.

Examples:

    get_synonyms_nltk
        -> get
           synonyms
           nltk

    naïve-path
        -> naïve
           path

    HTTPServer
        -> httpserver

    source—readiness

where the middle character is a Unicode em dash, remains one token after casefolding because the em dash is not an authorized v1 separator.

Matching uses `casefold()` but no additional normalization.

The same tokenizer must be used for query tokens and token/component matching against supported repository fields.

Document and test these exact rules.

## 2. Diagnostic / Limitation Filtering

Milestone 003 must use a strict deterministic allowlist.

There is no discretionary "materially limits interpretation" judgment in implementation.

Only diagnostics having one of these reasons are eligible for context inclusion:

    ambiguous_module
    target_parse_failure
    shadowed_or_rebound
    unresolved_symbol
    wildcard_import

A diagnostic is included only when BOTH conditions are true:

1. its `reason` is in the allowlist above; and
2. its relationship evidence intersects the selected context.

For condition 2, intersection means at least one of:

- `source_file` is a selected file;
- a candidate tracked path is a selected file;
- `source_symbol` identifies a selected symbol.

Do not include diagnostics solely because they exist in `dependencies.json`.

In particular:

    no_tracked_module_match

must never be included in a Milestone 003 context pack.

Do not add implementation-specific discretionary inclusion rules.

Preserve the complete diagnostic evidence in `dependencies.json`; context is only a bounded projection.

## 3. Seed Identity and Deduplication

Seed records remain typed and distinct.

A file seed and a symbol seed are NOT collapsed merely because the symbol resides in that file.

### File seed identity

A file seed is uniquely identified by:

    ("file", relative_path)

Only one file seed with that identity may exist.

### Symbol seed identity

A symbol seed is uniquely identified by:

    (
        "symbol",
        relative_path,
        symbol_kind,
        symbol_name,
        start_line
    )

Only one symbol seed with that identity may exist.

Therefore a file may legitimately contribute:

- one file seed; and
- one or more distinct symbol seeds.

All such seed records compete independently under the existing deterministic ranking and:

    MAX_SEEDS = 12

The 12-seed limit applies to seed records, not unique files.

After seed selection, downstream `selected_files` MUST deduplicate by relative path.

A file therefore appears at most once in the selected-file collection even if several seed records point to it.

Selected symbols likewise deduplicate by their canonical symbol identity.

Do not introduce diversity quotas or per-file seed caps in Milestone 003.

## 4. Fixed `match_status` Vocabulary

For `context.json` schema version 1, `match_status` has exactly two allowed values:

    matched
    no_matches

Use:

    matched

when at least one seed record survives seed selection.

Use:

    no_matches

when zero seed candidates qualify.

Do not introduce alternate strings such as:

    success
    partial
    empty
    found
    truncated

Truncation is represented separately in selection metadata and does not change `match_status`.

## 5. Relationship Selection and Cross-Type Ordering

The existing relationship priority buckets remain controlling:

    Priority 1:
    relationship directly involving a seed symbol

    Priority 2:
    relationship directly involving a seed file

    Priority 3:
    resolved test reference to a seed symbol/file

    Priority 4:
    other eligible one-hop relationship involving selected context

Every qualifying relationship must be assigned exactly one priority bucket: the strongest applicable bucket.

Within the same priority bucket, apply this fixed relationship-type order:

    1. imported_symbol
    2. call
    3. module_dependency
    4. test_reference

Use these type labels consistently in context selection even if the underlying Milestone 002 artifact uses more detailed resolution-kind fields.

Within equal priority bucket and relationship type, sort deterministically by:

1. source file using established filesystem-byte path ordering;
2. source line, with missing line sorted after known lines;
3. source symbol name, using case-sensitive encoded ordering without locale rules;
4. target file using established filesystem-byte path ordering;
5. target symbol name, using case-sensitive encoded ordering;
6. underlying deterministic relationship/resolution kind as final tie-breaker.

Then apply:

    MAX_RELATIONSHIPS = 40

Record:

- total qualifying relationships;
- selected relationship count;
- whether truncation occurred.

Do not rely on source artifact iteration order when selecting at the relationship limit.

## 6. Single Selection Policy

Implement one canonical Milestone 003 selection-policy layer containing:

- tokenization rules;
- match scoring constants;
- seed identity rules;
- seed ranking;
- fixed limits;
- relationship priority/type ordering;
- diagnostic allowlist/filtering;
- deterministic sort keys.

Do not duplicate these policies independently between JSON generation, Markdown rendering, CLI behavior, or tests.

`context.md` must render the already-selected structured result rather than re-performing selection.

## 7. Required Clarification Tests

In addition to the original Milestone 003 requirements, explicitly test:

- camelCase is not split;
- PascalCase is not split;
- the five authorized ASCII separators split tokens;
- Unicode punctuation not explicitly authorized does not split tokens;
- non-ASCII characters are preserved except for normal `casefold()` behavior;
- file and symbol seeds for the same file remain distinct seed records;
- duplicate file seeds collapse by file identity;
- duplicate symbol seeds collapse by canonical symbol identity;
- selected files deduplicate by path after seed selection;
- `match_status` accepts only `matched` and `no_matches`;
- `no_tracked_module_match` diagnostics are never projected into context;
- allowlisted diagnostics are included only when they intersect selected context;
- mixed relationship types obey the fixed priority/type sort contract before the 40-record cap.

These are refinements of existing Milestone 003 requirements, not new feature scope.

## 8. Scope Lock

These clarifications do not authorize:

- camelCase semantic parsing;
- Unicode normalization/transliteration;
- fuzzy matching;
- semantic search;
- dynamic ranking;
- seed diversity heuristics;
- AI judgment of diagnostic relevance;
- recursive relationship traversal;
- new generated artifacts;
- source-code execution;
- Git writes;
- Docker;
- Photo Organizer access.

Proceed with the smallest implementation satisfying the original Milestone 003 prompt plus this addendum.