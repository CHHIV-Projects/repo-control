# Milestone 002 — Deterministic Repository Relationships

Prompt file:

`002_repository_relationships_prompt.md`

Required closeout file:

`002_repository_relationships_closeout.md`

## Objective

Extend the trusted Milestone 001 deterministic scanner so `repoctl scan <repository>` also derives conservative, statically provable relationships among Python modules, symbols, calls, and tests.

Milestone 002 should answer mechanical questions such as:

- Which tracked Python modules import which other tracked Python modules?
- Which imported symbols can be resolved to tracked repository symbols?
- Which top-level functions make statically resolvable calls to other tracked top-level functions?
- Which test methods/functions statically reference tracked production symbols?

This remains deterministic repository intelligence.

No AI is authorized.

Do not infer runtime behavior that cannot be established statically.

## Controlling Documents

Read and follow:

- `docs/Repo_Control_Plane_v0.1_Architecture_and_Implementation_Plan.md`
- `docs/001_deterministic_repository_scanner_prompt.md`
- `docs/001_deterministic_repository_scanner_closeout.md`

Milestone 001 is the trusted baseline.

Preserve its:

- read-only target-repository guarantee;
- external state model;
- deterministic artifact rules;
- fail-closed Git-status behavior;
- repository identifier contract;
- scan determinism;
- transactional publishing;
- CLI behavior.

Do not redesign Milestone 001 unless a small change is strictly necessary to add the Milestone 002 relationship outputs.

## Project

Repo Control Plane:

`/home/chuck/projects/repo-control`

Primary validation target:

`/home/chuck/ai-agent-tests/vocab-app`

Photo Organizer remains out of scope.

Do not inspect or modify Photo Organizer during this milestone.

## Git Preflight

Before implementation:

1. confirm the Repo Control Plane worktree is clean;
2. confirm the current branch and HEAD;
3. confirm `origin`/upstream state if configured;
4. do not mutate the Vocab App repository.

If the Repo Control Plane worktree is unexpectedly dirty, stop and report before coding.

Do not commit or push unless separately instructed.

## Existing CLI

Do not add a new user-facing command.

Continue using:

    repoctl scan <repository>

Milestone 002 enriches scan output.

## New Artifact

Add exactly one new generated structured artifact:

    dependencies.json

The complete scan output becomes:

    repository.json
    files.json
    symbols.json
    tests.json
    dependencies.json
    summary.md

Do not add additional generated artifacts in this milestone.

`dependencies.json` is new and must use:

    "schema_version": 1

Existing artifact schema versions should remain unchanged unless their actual structure changes.

If `tests.json` must change structure to hold Milestone 002 reference evidence, increment only that artifact's schema version and document the change.

Do not increment unrelated schemas merely because Milestone 002 exists.

## Determinism

All Milestone 001 determinism requirements continue to apply.

Given identical repository state, repeated scans must produce byte-for-byte identical artifacts, including the new `dependencies.json` and updated `summary.md`.

Use the established deterministic path and source-order conventions.

No timestamps, random values, environment-dependent ordering, or locale-dependent sorting.

## 1. Internal Python Module Resolution

Build a deterministic index of tracked Python modules.

Resolve internal modules conservatively.

At minimum support module identities derivable from tracked paths:

    foo.py
        -> foo
    
    package/module.py
        -> package.module
    
    package/__init__.py
        -> package

Also support the conventional top-level `src/` layout:

    src/package/module.py
        -> package.module

when resolution is unambiguous.

Do not execute Python, import target modules, inspect installed packages, modify `sys.path`, or run target application code.

Relative imports may be resolved only when their package context is statically and unambiguously derivable.

If an import could resolve to multiple tracked files, mark it ambiguous rather than choosing one.

If it does not resolve to a tracked repository Python file, treat it as external/unresolved for internal-relationship purposes.

Do not infer that an import is internal merely because its name resembles a repository directory.

## 2. Module Dependency Relationships

`dependencies.json` must record deterministic internal module dependency edges.

At minimum each resolved edge should identify:

- importing file;
- imported module text as written;
- resolved internal target file;
- import kind;
- source line where available.

Required import kinds should distinguish at least:

    import_module
    from_module

Example conceptual evidence:

    app.py
        imports module vocab_utils
        resolved target: vocab_utils.py

Do not label unresolved third-party or standard-library imports as internal dependencies.

Preserve unresolved or ambiguous internal-resolution evidence where useful, but do not turn uncertain resolution into a dependency edge.

## 3. Imported-Symbol Resolution

Milestone 001 already records imported-symbol syntax.

Milestone 002 should add relationship resolution where statically provable.

For:

    from vocab_utils import normalize_synonym_candidates

if:

- `vocab_utils` resolves uniquely to a tracked Python module; and
- `normalize_synonym_candidates` is a recorded top-level symbol in that module;

then record a resolved imported-symbol relationship.

At minimum include:

- importing file;
- local/imported name;
- source module;
- source file;
- target symbol name;
- target symbol kind;
- import line;
- alias when present.

Do not claim resolution when:

- the module is ambiguous;
- wildcard import prevents exact determination;
- the target symbol is not statically recorded;
- dynamic export behavior would be required to know the answer.

Wildcard imports may be recorded as syntax but must not generate fabricated symbol relationships.

## 4. Static Internal Call Relationships

Add conservative top-level-function call relationships where resolution is statically provable.

Analyze function bodies using AST only.

Do not execute target code.

Required minimum supported cases:

### Same-module direct function call

Example:

    def a():
        b()

when top-level `b` is uniquely defined in the same file.

Record:

    a -> b

### Direct imported-symbol call

Example:

    from vocab_utils import normalize_synonym_candidates
    
    def get_synonyms_nltk(...):
        return normalize_synonym_candidates(...)

when the imported symbol is uniquely resolved to a tracked top-level function.

Record the caller and resolved repository callee.

### Imported-module attribute call

Example:

    import helper
    
    def run():
        helper.process()

when:

- `helper` resolves uniquely to a tracked internal module; and
- `process` is a known top-level function in that module.

Record the relationship.

## Explicitly Do Not Resolve

Do not attempt Milestone 002 static resolution for:

- instance-method dispatch;
- arbitrary object attributes;
- monkey-patching;
- dynamic imports;
- callbacks passed around indirectly;
- reflection;
- `getattr`;
- runtime registration;
- dependency injection;
- decorators as proof of call behavior;
- framework routing behavior;
- aliases whose target cannot be proven;
- functions returned from other functions.

An omitted relationship is preferable to a false relationship.

The artifact and summary must make clear that call relationships are a conservative static subset, not a complete runtime call graph.

## 5. Call Relationship Schema

For each resolved internal call, record at minimum:

- caller file;
- caller symbol name;
- caller symbol kind;
- callee file;
- callee symbol name;
- callee symbol kind;
- call line;
- resolution kind.

Use a small fixed `resolution_kind` vocabulary such as:

    same_module
    imported_symbol
    imported_module_attribute

If implementation finds a genuinely necessary additional deterministic kind, keep it narrowly defined and document it in the closeout.

Do not create vague values such as `other`.

## 6. Test-to-Symbol Static References

Extend deterministic test evidence.

For each discovered test-like top-level function or test method, determine whether it statically references tracked repository symbols using the same conservative resolution machinery.

At minimum support:

- direct imported production-symbol calls;
- imported internal module + known top-level function calls;
- directly imported production symbols referenced by name within the test body.

The output must distinguish:

    statically references

from:

    behavior is tested

Repo Control Plane may state:

    test_limit_zero statically calls
    vocab_utils.normalize_synonym_candidates

It must NOT state:

    normalize_synonym_candidates is fully tested
    normalize_synonym_candidates has adequate coverage

No coverage or semantic test-quality judgment is authorized.

## 7. `tests.json` Extension

Extend `tests.json` so each discovered test function/method can contain a deterministic collection of resolved repository references.

Each reference should include at minimum:

- target file;
- target symbol;
- target symbol kind;
- reference kind;
- relevant source line.

Reference kinds should remain small and explicit, for example:

    import
    call

If the artifact schema changes, increment `tests.json` schema version and document the exact change.

Do not create a separate test-map artifact.

## 8. `dependencies.json` High-Level Structure

Keep the schema simple.

It should contain conceptually:

- schema version;
- module-resolution metadata;
- resolved internal module dependencies;
- resolved imported-symbol relationships;
- resolved internal function-call relationships;
- ambiguous/unresolved relationship evidence where necessary to prevent false certainty.

Exact internal object layout is an implementation choice, but:

- relationships must be explicit;
- source and target paths must be preserved;
- relationship type must be explicit;
- source lines should be included where known;
- ordering must be deterministic.

Do not build a graph database.

Plain deterministic JSON is sufficient.

## 9. Human-Readable Summary

Update `summary.md` with concise deterministic relationship sections.

At minimum include:

- internal Python module dependency count;
- resolved imported-symbol relationship count;
- resolved static internal call count;
- test-to-symbol static reference count;
- per-file internal module relationships;
- per-test resolved references where present;
- unresolved/ambiguous relationship counts.

Do not turn the summary into architecture commentary.

Avoid statements such as:

    module X is overly coupled
    function Y is risky
    architecture is healthy

Those belong to later audit/AI milestones.

## 10. Existing Artifact Integrity

Preserve Milestone 001 meaning.

Do not degrade:

- file inventory;
- hashes;
- requirements extraction;
- Python parse handling;
- branch/status reporting;
- external-state behavior;
- transactional output publishing.

A relationship-analysis failure caused by malformed Python should respect the existing parse-failure evidence rather than aborting an otherwise valid scan unless the new relationship result would become misleading.

Do not manufacture relationships for files that failed AST parsing.

## 11. Tests

Add focused automated tests for the relationship engine.

Required coverage should include at minimum:

1. internal `import module` resolution;
2. internal `from module import symbol` resolution;
3. alias handling;
4. same-module direct call resolution;
5. imported-symbol call resolution;
6. imported-module attribute call resolution;
7. external import not classified as internal;
8. ambiguous internal resolution does not create a false edge;
9. wildcard import does not fabricate symbol relationships;
10. nested/local functions are not misrepresented as repository top-level callees;
11. test-method static reference to a production symbol;
12. distinction between static reference evidence and semantic test-coverage claims;
13. deterministic ordering;
14. byte-for-byte repeated-scan determinism including `dependencies.json`;
15. existing Milestone 001 tests remain passing;
16. target-repository Git state remains exactly unchanged before/after scan.

Use temporary Git repositories/fixtures for focused edge cases wherever practical.

Do not rely only on Vocab App.

## 12. Vocab App Validation

After automated tests pass, run:

    repoctl scan /home/chuck/ai-agent-tests/vocab-app

Validate Milestone 002 relationships against direct read-only source evidence.

At minimum determine from the actual current repository state whether relationships such as the following exist and, if they do, are represented correctly:

- an application module importing an internal utility module;
- a production function calling a resolved utility function;
- a test module importing an internal utility;
- test methods statically calling/resolving a tracked utility symbol.

These are examples of the kinds of relationships to verify.

Do not hardcode assumptions if the Vocab App has changed.

Verify the current source at validation time.

Capture Vocab App Git status before and after scanning and prove equality.

Do not modify or commit anything in Vocab App.

## 13. README

Update README only as necessary to document that `repoctl scan` now includes deterministic repository relationship analysis and the new `dependencies.json` artifact.

Keep documentation current-state only.

Do not document future AI/context/Git commands as implemented.

## Explicit Non-Goals

Do not implement:

- GPT-OSS;
- Ollama;
- Aider integration;
- Codex/Copilot integration;
- semantic search;
- context packs;
- architecture scoring;
- complexity metrics;
- duplicate-code detection;
- circular-dependency quality judgments;
- runtime call tracing;
- code execution;
- import execution;
- framework-specific route discovery;
- database-model relationship analysis;
- Git-history analytics;
- snapshots;
- before/after delta auditing;
- Git writes;
- Git branch management;
- commit/push support;
- web UI;
- daemon/background service;
- Docker/containerization;
- Photo Organizer access.

## Implementation Discipline

Extend the existing scanner rather than creating a second scan engine.

Prefer a small relationship-analysis module layered on Milestone 001 AST results.

Reuse existing parsed structure where practical rather than reparsing files through separate competing logic.

Keep responsibilities clear:

    Git/filesystem facts
        -> existing Milestone 001 scanner
    
    AST symbol facts
        -> existing Python scan layer
    
    relationship resolution
        -> Milestone 002 deterministic relationship layer
    
    artifact rendering
        -> structured outputs / summary

Avoid premature generic graph frameworks.

Do not introduce third-party dependencies unless strictly necessary and explicitly justified before use.

## Stop / Escalation Conditions

Stop and report rather than broadening scope if implementation appears to require:

- executing/importing target application code;
- modifying the target repository;
- Git mutation;
- runtime tracing;
- framework-specific inference;
- package installation into the target;
- AI/LLM use;
- Docker/containerization;
- Photo Organizer access;
- a database/graph service;
- dynamic Python resolution that cannot remain deterministic;
- a materially broader module-resolution architecture than described here.

If a relationship cannot be proven statically under the supported rules, record it as unresolved/ambiguous or omit the claimed edge.

Do not guess.

## Validation Before Closeout

Run at minimum:

- full Repo Control Plane automated test suite;
- Python syntax/compile validation as appropriate;
- `repoctl scan` against Vocab App;
- direct read-only verification of representative module/symbol/call/test relationships;
- repeated-scan byte-for-byte determinism validation;
- Repo Control Plane `git diff --check`;
- Repo Control Plane `git status --short`;
- exact Vocab App Git-status equality before/after validation.

## Required Closeout

Create:

`docs/002_repository_relationships_closeout.md`

Include:

1. implementation summary;
2. Repo Control Plane files added/modified;
3. relationship-resolution rules implemented;
4. `dependencies.json` schema at a useful high level;
5. any `tests.json` schema change/version change;
6. supported static call-resolution cases;
7. explicitly unsupported/dynamic cases;
8. automated test results;
9. Vocab App validation results;
10. representative verified relationships from Vocab App;
11. unresolved/ambiguous cases encountered;
12. deterministic-output validation;
13. Vocab App Git status before/after;
14. Milestone 003 opportunities without implementing them;
15. final Repo Control Plane `git status --short`.

Do not commit or push unless separately instructed.

## Acceptance Criteria

Milestone 002 passes only if:

- Milestone 001 behavior remains intact;
- `repoctl scan` produces `dependencies.json`;
- internal module dependencies are resolved conservatively;
- imported production symbols are resolved only when provable;
- supported top-level static calls are resolved correctly;
- test-to-symbol references are reported as static evidence, not coverage claims;
- ambiguity never becomes fabricated certainty;
- all output remains deterministic;
- automated tests pass;
- Vocab App validation matches direct source evidence;
- scanning does not mutate Vocab App;
- no AI, Git writes, Docker, context generation, or Photo Organizer access is introduced.



# Product Owner / Architect Clarification Addendum — Milestone 002 Relationship Contract

This addendum resolves the final pre-coding ambiguities identified during Milestone 002 review.

It does not broaden Milestone 002 scope.

## 1. Initial Git Preflight

At the initial start of Milestone 002 implementation, the Repo Control Plane worktree must be completely clean.

Use read-only Git status inspection equivalent to:

    git status --porcelain=v2 -z --untracked-files=all

If any tracked or untracked worktree entry exists at initial implementation start:

- stop;
- report the exact status;
- do not automatically restore, clean, stage, commit, or otherwise repair the repository.

There is no concept of an implicit or operator-approved dirty baseline for the initial Milestone 002 start.

If work is later resumed after Milestone 002 implementation has already intentionally begun, do not treat the milestone's own known work-in-progress files as an initial-preflight violation. Preserve and report that state rather than resetting it.

This clarification applies only to process preflight and does not change target-repository read-only behavior.

## 2. `tests.json` Schema Version

Milestone 002 intentionally changes the structure and meaning of `tests.json` by adding deterministic resolved repository references to discovered tests.

Therefore:

    tests.json
    schema_version = 2

is mandatory for Milestone 002.

Do not leave this conditional.

Unrelated Milestone 001 JSON artifacts retain their existing schema versions unless their structures actually change.

The new:

    dependencies.json

uses:

    schema_version = 1

Document the exact `tests.json` v1 -> v2 structural change in the closeout.

## 3. Ambiguous Module Resolution

Internal module resolution must never use a precedence rule or tie-break to choose among multiple valid tracked candidates.

If the same import identity maps to more than one tracked candidate under the supported Milestone 002 resolution rules:

    classification = ambiguous

and:

- record the ambiguity;
- record all candidate tracked paths in deterministic path order;
- create no resolved module edge;
- create no imported-symbol edge dependent on that module;
- create no call edge dependent on that module;
- create no test-reference edge dependent on that module.

Examples include mixed repository layouts where both root and `src/` mappings would produce the same logical module name.

Do not prefer:

- root over `src/`;
- `src/` over root;
- shortest path;
- first lexical path;
- first discovered path.

Ambiguity must remain ambiguity.

## 4. Mandatory Unresolved / Ambiguous Evidence

`dependencies.json` must contain deterministic diagnostic evidence for supported relationship-resolution attempts that cannot be resolved.

At minimum distinguish:

    unresolved
    ambiguous

Do not silently omit a relationship attempt when its syntax matches a Milestone 002 supported resolution form but resolution fails.

A minimal diagnostic record must include:

- `relationship_kind`;
- `source_file`;
- `source_symbol`, or null when the relationship occurs at module scope;
- `source_line`;
- `reference`;
- `reason`;
- `candidates`.

`candidates` must be:

- an empty list when no tracked candidate can be established;
- a deterministically ordered list of candidate tracked paths/symbols when ambiguity exists.

Required `relationship_kind` values should remain narrowly defined, for example:

    module_import
    imported_symbol
    call
    test_reference

Required reason vocabulary should remain small and explicit, for example:

    no_tracked_module_match
    ambiguous_module
    unresolved_symbol
    wildcard_import
    shadowed_or_rebound
    target_parse_failure

If one additional reason is genuinely necessary, define it narrowly and document it in the closeout.

Do not store arbitrary raw source-code lines merely for diagnostics.

### Scope of unresolved import evidence

For ordinary import syntax:

- imports that resolve uniquely to tracked Python modules become internal dependency edges;
- imports with multiple tracked candidates become ambiguous records;
- imports with no tracked module match may be recorded as unresolved/external evidence but must not become internal dependency edges.

For call/reference analysis, create unresolved diagnostic records only when the call/reference syntax otherwise matches a supported Milestone 002 resolution form.

Do not attempt to diagnose every arbitrary Python expression.

## 5. Shadowing and Rebinding

Static call/reference resolution must fail conservatively when the apparent imported or module-level name is shadowed or rebound.

If a candidate identifier is locally bound in the caller's relevant Python scope, do not resolve a use of that identifier to an imported or repository-level symbol merely because the same name exists there.

Relevant local bindings include, where statically observable:

- function parameters;
- assignment targets;
- annotated assignment targets;
- augmented assignment targets;
- loop targets;
- `with ... as` targets;
- exception `as` targets;
- assignment expressions;
- local imports;
- nested function/class definitions that bind the name in that scope.

Likewise, if a module-level imported binding is statically rebound in the module such that exact call identity cannot be proven, do not claim a resolved repository call from that binding.

When shadowing/rebinding prevents an otherwise supported resolution:

    reason = shadowed_or_rebound

and no resolved call/reference edge is created.

Do not implement full Python control-flow or runtime name-resolution analysis in Milestone 002.

Conservative omission is preferred to a false edge.

## 6. AST Parse-Failure Policy

A Python AST parse failure must NOT fail the overall repository scan.

Preserve Milestone 001 behavior:

- record the parse failure;
- skip AST-dependent relationship extraction originating from that file;
- continue scanning other files.

If another successfully parsed file imports a tracked Python file whose AST failed:

- the tracked module path may still establish a module-level dependency when module resolution itself is unambiguous;
- imported-symbol resolution into the failed target must not be claimed;
- function-call resolution into the failed target must not be claimed;
- record `target_parse_failure` where an otherwise supported relationship attempt depends on unavailable target symbol evidence.

The relationship output and summary must expose the existence/count of relationship-analysis limitations caused by parse failures.

Do not fabricate an empty symbol table for a file that failed parsing.

Do not fail the global scan merely because one tracked Python file cannot be parsed.

## 7. Canonical Resolver

Use one canonical deterministic relationship resolver for:

- module dependency resolution;
- imported-symbol resolution;
- production call resolution;
- test-reference resolution.

Do not implement separate competing resolution rules for production code and tests.

The same ambiguity, parse-failure, shadowing, and unresolved rules must apply consistently wherever relevant.

## 8. Required Negative Tests

In addition to the original Milestone 002 test requirements, explicitly cover:

- root-versus-`src/` ambiguous module identity produces no edge;
- locally shadowed imported function produces no call edge;
- locally shadowed imported module produces no attribute-call edge;
- module-level rebinding prevents false imported-name resolution;
- wildcard import produces no fabricated symbol edge;
- target AST parse failure preserves module evidence where provable but prevents symbol/call resolution;
- unresolved and ambiguous diagnostic records use the required deterministic minimal structure.

These are refinements of already-required Milestone 002 behavior, not new feature scope.

## 9. Scope Lock

These clarifications do not authorize:

- runtime import resolution;
- Python execution;
- full control-flow analysis;
- a custom Python symbol-table engine beyond what is needed for conservative Milestone 002 resolution;
- package installation;
- new user-facing commands;
- additional generated artifacts;
- AI integration;
- Docker;
- Git writes;
- Photo Organizer access.

Proceed with the smallest deterministic implementation satisfying the original Milestone 002 prompt plus this addendum.