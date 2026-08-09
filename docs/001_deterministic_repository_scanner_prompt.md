# Milestone 001 — Deterministic Repository Scanner

Prompt file:

`001_deterministic_repository_scanner_prompt.md`

Required closeout file:

`001_deterministic_repository_scanner_closeout.md`

## Objective

Build the first production-quality Repo Control Plane capability:

    repoctl scan <repository>

This milestone establishes the deterministic, read-only repository-intelligence foundation.

It must inspect a target Git repository, derive mechanical repository facts without AI, and write versioned structured outputs plus a human-readable summary to Repo Control Plane's external state directory.

This milestone is intentionally narrow.

Do not implement context generation, architectural analysis, local AI, repository-change comparison, Git workflow automation, or any target-repository mutation.

## Controlling Architecture

Read and follow:

`docs/Repo_Control_Plane_v0.1_Architecture_and_Implementation_Plan.md`

Treat that document as controlling for:

- authority boundaries;
- read-only target-repository behavior;
- state location;
- deterministic-vs-AI separation;
- Milestone 001 scope and non-goals.

Do not broaden this milestone beyond that plan.

## Project

Repo Control Plane repository:

`/home/chuck/projects/repo-control`

Initial validation target:

`/home/chuck/ai-agent-tests/vocab-app`

The Vocab App is a disposable validation target.

Do not modify it.

Photo Organizer is explicitly out of scope for Milestone 001.

Do not inspect, modify, benchmark, or otherwise operate on the Photo Organizer repository in this milestone.

## Existing Experimental Reference

An earlier disposable scanner prototype exists at:

`/home/chuck/ai-agent-tests/repo-audit-tools/repo_inventory.py`

You may inspect it for lessons learned.

It is not authoritative architecture and should not simply be copied wholesale. Build the production implementation within Repo Control Plane according to the controlling architecture and this prompt.

## Required CLI

Implement an installable CLI exposing:

    repoctl scan <repository>

Use a normal Python package structure under:

`src/repoctl/`

A simple standard-library CLI is preferred unless an existing project dependency clearly justifies otherwise.

Do not introduce dependencies merely for convenience.

The command must:

1. resolve and validate the supplied repository path;
2. verify that it is a Git work tree;
3. inspect the repository using read-only filesystem and Git operations;
4. derive the required deterministic facts;
5. write outputs only beneath Repo Control Plane's external state directory;
6. print a concise completion summary containing the target repository, Git identity, output location, and any parse errors.

## Read-Only Safety Boundary

The target repository may be read but must never be mutated.

Allowed examples:

- reading tracked files;
- parsing source;
- `git status`;
- `git branch --show-current`;
- `git rev-parse`;
- `git ls-files`;
- other demonstrably read-only Git inspection.

Forbidden against the target repository:

- file creation or modification;
- staging;
- commit;
- push;
- branch creation or switching;
- reset;
- clean;
- checkout/restore;
- merge/rebase;
- Git configuration changes;
- hooks;
- application execution that writes state;
- migrations;
- package installation into the target;
- any attempt to "repair" the target.

If a required behavior cannot be implemented without target-repository mutation, stop and report rather than expanding authority.

## External State

Default state root:

`~/.local/share/repoctl/`

Create a deterministic repository-specific directory beneath that root.

The repository identifier must safely distinguish repositories that happen to share the same basename.

Keep the scheme simple, stable, filesystem-safe, and documented.

The scan must produce:

    repository.json
    files.json
    symbols.json
    tests.json
    summary.md

These are generated Repo Control Plane state and must not be written into the target repository.

All JSON outputs must include a simple schema/version identifier sufficient for later evolution.

Use stable ordering so repeated scans of unchanged repository state produce semantically equivalent results.

Do not introduce volatile timestamps into authoritative scan content unless there is a compelling reason; repeatability is more important.

## Required Repository Facts

`repository.json` must include at minimum:

- schema version;
- resolved repository root;
- repository identifier;
- current branch, including safe representation of detached HEAD if encountered;
- HEAD commit;
- working-tree status in a structured form;
- tracked-file count.

Working-tree reporting must distinguish, where Git permits:

- modified;
- added/staged;
- deleted;
- renamed;
- untracked;
- other relevant porcelain states.

Do not mutate the repository to determine status.

## Required File Facts

`files.json` must contain one deterministic record for every Git-tracked file.

At minimum:

- relative path;
- conservative extension/type classification;
- byte size;
- line count when safely text-decodable;
- `null` or equivalent when a meaningful text line count cannot be determined;
- SHA-256 of the file bytes.

Do not infer semantic purpose from filenames.

Examples:

- `.py` may be classified as Python;
- `.txt` as text;
- `.bat` as batch script;
- `.vbs` as VBScript;

but a filename such as `test_foo.py` must not by itself be declared authoritative evidence that a particular behavior is tested.

Handle unusual but valid Git filenames safely.

## Required Python Symbol Facts

For every tracked `.py` file, parse with Python's AST without importing or executing the target module.

`symbols.json` must include:

- parse success/failure;
- parse error text in a safe deterministic form when parsing fails;
- top-level functions;
- top-level async functions;
- top-level classes;
- start and end lines where available;
- top-level imports;
- imported module names;
- imported symbols where directly represented by the AST.

Do not report nested functions as top-level functions.

Do not execute application code to discover symbols.

One malformed Python file must not abort the entire repository scan.

## Requirements Extraction

Recognize ordinary requirements text files conservatively, including at minimum `requirements.txt`.

Capture nonblank, non-comment declarations as recorded text.

Do not resolve packages, contact package indexes, install dependencies, or infer actual runtime use.

Store the extracted declarations in the most appropriate structured output without adding another milestone-001 output file unless clearly necessary.

Document the chosen schema.

## Required Test Structure

`tests.json` must conservatively report structural testing evidence derivable from AST and paths.

At minimum include:

- Python files recognized as test-like using an explicitly documented filename/path convention;
- top-level classes in those files;
- methods in those classes whose names satisfy the chosen conservative test naming convention;
- top-level test-like functions if present.

For each discovered test method/function include:

- name;
- file;
- start/end lines where available.

Important evidence rule:

The scanner may say:

    test_vocab_utils.py contains class TestVocabUtils
    TestVocabUtils contains method test_limit_zero

It must NOT conclude:

    normalize_synonym_candidates is tested

unless a later milestone adds deterministic reference/call analysis capable of supporting that claim.

Test-to-symbol mapping is Milestone 002 work.

## Human-Readable Summary

Generate `summary.md` entirely from the structured deterministic scan results.

At minimum summarize:

- repository root;
- repository identifier;
- branch;
- HEAD;
- working-tree state;
- tracked-file count;
- tracked files;
- Python files and parse status;
- top-level functions/classes/imports;
- test-like files/classes/method counts;
- requirements declarations;
- parse errors.

The summary is a projection of the structured data, not a second independently derived source of truth.

It should be concise and navigable rather than an architectural interpretation.

Do not include AI commentary, architecture scores, or speculative conclusions.

## Error Handling

Fail clearly and without target mutation when:

- the supplied path does not exist;
- the supplied path is not a Git work tree;
- Git inspection itself cannot be completed;
- the external state directory cannot safely be written.

Individual source parse failures should normally be recorded and the scan should continue.

Errors must be useful to a human and must not expose secrets unnecessarily.

## Tests

Add focused automated tests for the scanner and CLI.

Tests should use temporary repositories/fixtures wherever practical rather than depending solely on the live Vocab App.

Required coverage should include at least:

1. valid Git repository scan;
2. invalid/non-Git target;
3. tracked-file inventory;
4. SHA-256/size/line-count behavior;
5. Python top-level function/class extraction;
6. imports and imported-symbol extraction;
7. nested function not classified as top-level;
8. malformed Python captured as a parse failure without aborting the scan;
9. test class and test-method discovery;
10. requirements extraction;
11. dirty working-tree reporting;
12. stable/deterministic ordering;
13. external output location;
14. proof that normal scanning leaves the target repository unchanged.

For read-only validation, compare target-repository Git state before and after scanning rather than merely assuming that no mutation occurred.

## Vocab App Validation

After automated tests pass, run the production command against:

`/home/chuck/ai-agent-tests/vocab-app`

Validate the generated facts against direct read-only Git/source evidence.

Do not hardcode volatile facts such as:

- current branch;
- current commit;
- working-tree state;
- tracked-file count.

The Vocab App may evolve during these experiments.

The validation should prove that `repoctl` reports whatever state actually exists at scan time.

Do not modify or commit anything in the Vocab App.

## Documentation

Provide concise README/use documentation sufficient to show:

- installation/development invocation;
- `repoctl scan` syntax;
- default external state location;
- output files;
- read-only target guarantee;
- current Milestone 001 limitations.

Avoid speculative documentation for future commands not yet implemented.

## Explicit Non-Goals

Do not implement:

- GPT-OSS;
- Ollama/Aider integration;
- Codex/Copilot integration;
- context packs;
- semantic search;
- function call graphs;
- test-to-production-symbol mapping;
- architectural health scoring;
- complexity scoring;
- duplicate-code detection;
- snapshots;
- repository-delta comparison;
- Git-history analytics beyond what is strictly required for current repository identity;
- Git writes;
- milestone branch management;
- commits/pushes;
- web UI;
- background daemon/service;
- CI integration;
- Photo Organizer integration.

## Future M012 Benchmark Note

The Photo Organizer Milestone 12.65.0 reconnaissance is an ongoing project artifact and must NOT be treated as a frozen benchmark document.

It is informational only for the future direction of Repo Control Plane.

When a future benchmark is explicitly authorized, use immutable/bounded Git evidence such as the relevant historical Git range and/or an explicitly captured benchmark snapshot.

Do not assume that the current 12.65.0 closeout text will remain unchanged.

Do not access Photo Organizer for this milestone.

## Implementation Discipline

Implement the smallest clean structure that supports Milestone 001 and credible extension into Milestone 002.

Avoid premature frameworks, databases, services, plugin systems, or abstraction layers.

Prefer:

- plain Python;
- typed data where useful;
- clear separation between Git inspection, filesystem inspection, Python parsing, output models, and CLI orchestration;
- deterministic serialization;
- focused tests.

Do not build generalized infrastructure for hypothetical languages or repository types beyond what this milestone requires.

## Validation Before Closeout

Run at minimum:

- the project's full Milestone 001 automated test suite;
- Python syntax/compile checks as appropriate;
- `repoctl scan` against the Vocab App;
- direct comparison of key scan results to read-only Git evidence;
- `git diff --check`;
- `git status --short`.

Also verify that scanning Vocab App did not alter its Git state.

## Stop / Escalation Conditions

Stop and report before implementation expansion if any of the following appears necessary:

- target-repository writes;
- Git mutation;
- Photo Organizer access;
- AI/LLM use;
- database/service infrastructure;
- execution/import of target application code;
- dependency installation into the target repository;
- substantial architecture beyond the controlling v0.1 plan;
- ambiguity that would make mechanical scan results non-deterministic or misleading.

Do not solve a stop condition by quietly broadening scope.

## Required Closeout

Create:

`001_deterministic_repository_scanner_closeout.md`

The closeout should be concise but evidence-based and include:

1. implementation summary;
2. files added/modified in Repo Control Plane;
3. CLI behavior;
4. structured output schemas at a useful high level;
5. read-only safety mechanism;
6. automated test results;
7. Vocab App validation results;
8. exact external output location used during validation;
9. any parse/errors or limitations encountered;
10. known Milestone 002 follow-up opportunities without implementing them;
11. final Repo Control Plane `git status --short`.

Also report the Vocab App Git status before and after validation to demonstrate that the target repository was not mutated.

Do not commit or push unless separately instructed.

## Acceptance Criteria

Milestone 001 passes only if:

- `repoctl scan <repository>` works from the Repo Control Plane project;
- target access is read-only;
- required structured artifacts are generated externally;
- Python/file/test facts are derived without AI or target-code execution;
- malformed source is handled safely;
- outputs are deterministically ordered;
- automated tests pass;
- Vocab App validation agrees with direct repository evidence;
- Vocab App remains unmodified;
- no Photo Organizer access occurs;
- Git writes and all later-phase features remain absent.
