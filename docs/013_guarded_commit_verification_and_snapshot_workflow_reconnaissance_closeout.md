# M013 Guarded Commit Verification and Snapshot Workflow Reconnaissance Closeout

## 1. Executive conclusion

M013 completed focused read-only reconnaissance of the three related workflow issues.

The primary correctness defect is confirmed:

- Commit Plan fingerprinting uses recursive staged file records.
- Post-commit verification invokes `git diff-tree` without `-r`.
- For the real Vocab commit, Git therefore returns one top-level `milestones` directory record instead of the two committed file records.
- The resulting fingerprint differs even though the commit is valid and contains exactly the approved paths.
- Verification raises before the Commit execution payload is built and published.
- Workflow finds no execution artifact and renders the Commit plan as `Not executed`.

The Git mutation succeeded. Repo Control lost the durable execution evidence that should have preserved that fact.

The matching Snapshot prerequisite is correctly enforced by the existing M007 authority, but Workflow exposes it too late. Snapshot creation currently belongs to the dedicated Snapshots route, so the operator must leave Workflow to satisfy a required Commit prerequisite.

Snapshot artifacts are immutable and currently have no commit-alignment association model. The smallest coherent next step is one bounded M014 covering:

1. recursive/correct post-commit verification and mutation-success persistence;
2. explicit matching-Snapshot orchestration from Workflow using the existing Snapshot service;
3. derived Snapshot-to-Commit traceability through immutable execution/association evidence.

No Repo Control implementation change was made during M013. No Vocab, Snapshot, Commit, or runtime mutation was performed.

## 2. Starting Repo Control state

The M013 chronology has four distinct repository states.

### Initial pre-lifecycle repository state

Before the M013 prompt lifecycle commit completed, the captured Repo Control state was:

- branch: `main`
- HEAD: `5ac0f993ff0ff23b2d8e397a1ac6d2a93ada92fe`
- upstream: `origin/main`
- upstream SHA: `5ac0f993ff0ff23b2d8e397a1ac6d2a93ada92fe`
- ahead/behind: `0 0`

The expected pre-existing local state was:

```text
 M docs/008_guarded_staging_preparation_prompt.md
 M docs/009_browser_ui_foundation_and_read_only_console_prompt.md
?? .venv/
```

### Prompt lifecycle commit

The Product Owner then committed the M013 prompt:

- HEAD advanced to: `0c096e90688fad581f35fd120796b2797460b499`
- subject: `Add Repo Control M013 guarded commit and snapshot workflow reconnaissance prompt`
- only added file: `docs/013_guarded_commit_verification_and_snapshot_workflow_reconnaissance_prompt.md`

### Operative M013 reconnaissance baseline

Reconnaissance began only after the prompt lifecycle gate passed. The operative M013 baseline was therefore:

- branch: `main`
- HEAD: `0c096e90688fad581f35fd120796b2797460b499`
- upstream: `origin/main`
- upstream SHA: `0c096e90688fad581f35fd120796b2797460b499`
- ahead/behind: `0 0`
- expected pre-existing local state: the modified `docs/008`, modified `docs/009`, and untracked `.venv/` shown above

No unexpected Repo Control source changes were present at the operative reconnaissance baseline.

The final Repo Control state after reconnaissance is recorded in section 25.

### Repository-history note

Repo Control HEAD advanced between the initial pre-lifecycle capture and the operative reconnaissance baseline through one commit:

- commit: `0c096e90688fad581f35fd120796b2797460b499`
- subject: `Add Repo Control M013 guarded commit and snapshot workflow reconnaissance prompt`
- affected file: `docs/013_guarded_commit_verification_and_snapshot_workflow_reconnaissance_prompt.md` (added)

This was the Product Owner prompt-lifecycle commit performed outside M013 reconnaissance, before the read-only investigation began. It was not an M013 action and did not modify Repo Control implementation, Vocab, workflow artifacts, or the evidence under investigation. The history movement therefore does not affect the validity of the M013 reconnaissance evidence; it explains the difference between the initial pre-lifecycle HEAD and the operative/final HEAD.

## 3. Vocab historical evidence

Canonical repository:

`/home/chuck/projects/vocab-app`

Read-only gate evidence:

- branch: `main`
- resulting HEAD: `9b7465deb41a9efa06fc32db7d0723a8c550f1ec`
- working tree: clean
- latest commit: `9b7465d Close Vocab M002.1 Repo Control integration baseline`

The resulting commit contains exactly:

```text
A milestones/002.1_repo_control_integration_baseline_and_m002_evidence_comparison_closeout.md
M milestones/002.1_repo_control_integration_baseline_and_m002_evidence_comparison_prompt.md
```

Direct Git confirms the approved commit is valid. No Vocab mutation was performed during M013.

## 4. Guarded Commit execution flow

The actual current flow in `src/repoctl/workflow/commit_execution.py` is:

```text
execute_prepared_commit(..., approve=True)
    -> inspect current Git state
    -> locate and load immutable Commit Plan
    -> enforce Git hook and identity boundaries
    -> recompute staged delta/state fingerprints
    -> validate branch, HEAD, worktree, operation, and matching Snapshot
    -> invoke git commit
    -> read resulting HEAD
    -> _verify_post_commit
    -> build execution payload
    -> derive execution ID
    -> publish execution.json/execution.md
    -> return success
```

The browser approval route invokes this same reusable service directly. It does not use a CLI subprocess mutation adapter.

Workflow history in `src/repoctl/web/views.py` indexes Commit plans and separately indexes Commit execution artifacts by `plan_id`. A row is marked Executed only when an execution artifact is present.

## 5. Exact post-verification failure cause

The Vocab Commit Plan was:

- plan: `commit-plan--6e26ba68988d99f2`
- repository: `/home/chuck/projects/vocab-app`
- starting HEAD: `a3fcc8a7bd1e25676d9dbe11de5c644a629a9c1c`
- resulting HEAD: `9b7465deb41a9efa06fc32db7d0723a8c550f1ec`
- commit message: `Close Vocab M002.1 Repo Control integration baseline`
- matching Snapshot: `snap--6a160b81721b5bbd`
- planned staged delta fingerprint: `54197fc117074616f6b09d5e07cd4ac88bc64872b243f679ccb7d543d610b71b`

The planned staged records were:

```text
A milestones/002.1_repo_control_integration_baseline_and_m002_evidence_comparison_closeout.md
M milestones/002.1_repo_control_integration_baseline_and_m002_evidence_comparison_prompt.md
```

The implementation calls:

```text
git diff-tree --raw --no-renames --abbrev=40 --no-commit-id -z <before_head> <after_head>
```

It does not pass `-r`.

Against the real Vocab commit, that command returns one record:

```text
:040000 040000 04456495f3fb8f96f6aa3e07278df976055e13cf 9802f04b87077542c0be6dcfb95ddd5a16fc14eb M milestones
```

The resulting calculated fingerprint is:

```text
48c9c2561490e238729dc3c6f22a49799f6fdfd98f832538099cfd12798a64a3
```

That differs from the planned fingerprint:

```text
54197fc117074616f6b09d5e07cd4ac88bc64872b243f679ccb7d543d610b71b
```

The same Git command with `-r` returns the two intended file records and calculates exactly:

```text
54197fc117074616f6b09d5e07cd4ac88bc64872b243f679ccb7d543d610b71b
```

Therefore the exact failure cause is missing recursive traversal in post-commit `git diff-tree`, not an invalid Vocab commit, path mismatch, mode mismatch, object identity mismatch, line-ending problem, or path-ordering problem.

## 6. Fingerprint model

Commit preparation uses `_staged_delta` in `src/repoctl/workflow/commit_plan.py`:

- `git diff-index --cached --raw --no-renames --abbrev=40 -z HEAD --`
- parse raw records into metadata + path;
- sort by path bytes, then raw metadata bytes;
- hash with the `repoctl-staged-delta-v1` prefix;
- include old/new modes, old/new object IDs, status, and path in the raw record.

Post-commit verification uses `_parse_raw_records` and `_delta_fingerprint_from_records` in `commit_execution.py`, intended to normalize the same record model.

The normalization itself is compatible for this Vocab case. The failure is that non-recursive `git diff-tree` reports the changed directory rather than recursively reporting its changed files.

## 7. Mutation/audit ordering

Current ordering is:

```text
mutate Git
-> read resulting HEAD
-> perform post-commit verification
-> only then build and publish execution artifact
```

This ordering violates the required invariant when post-verification fails. The commit has already happened, but no durable Commit execution artifact is guaranteed to exist.

M014 should preserve mutation success before later verification can fail. The recommended invariant is:

```text
Git mutation succeeds
-> immediately persist immutable mutation-success evidence including resulting HEAD
-> perform post-commit audit
-> persist or derive final verified/audit-failed outcome
```

The exact artifact arrangement should remain additive and immutable.

## 8. Special-state architecture

The implementation already has special error semantics:

- `stage_succeeded_audit_failed` for Stage execution-audit publication failure;
- `commit_succeeded_audit_failed` for Commit execution-audit publication failure;
- `post_commit_verification_failed` for post-commit verification failure, carrying `commit_id`.

The conceptual mutation-succeeded/audit-failed state exists, but the post-verification failure path does not use it to persist an execution artifact. It raises `post_commit_verification_failed` after Git mutation and before execution artifact publication.

M014 should reuse or carefully refine this existing authority rather than inventing a separate unrelated state machine.

## 9. Execution artifact persistence

For the canonical Vocab plan, no Commit execution artifact exists under:

```text
/home/chuck/.local/share/repoctl/vocab-app--0d81efec80ef/workflow/commit_executions/
```

The retained canonical artifact set contains the Commit Plan but no corresponding Commit Execution artifact. Consequently, `summarize_workflow_artifacts` has no execution pair for the plan and sets the row execution to `None`.

The Workflow template then renders:

```text
Not executed
No execution artifact is linked to this plan.
```

This is why the UI misrepresents the real Vocab result.

## 10. Correct recovery semantics

For a commit-succeeded/audit-failed result, the operator behavior must be:

- preserve the resulting commit;
- show the resulting HEAD explicitly;
- preserve the verification/audit failure;
- do not automatically retry;
- do not reset;
- do not restore;
- do not revert;
- require human inspection before any later action;
- ensure the UI never says `Not executed`.

The current exception carries `commit_id`, which is useful, but that fact is not persisted into Workflow history when the execution artifact is absent.

## 11. Workflow rendering findings

Current rendering is binary:

- execution artifact found: `Executed` / `Committed to <head>`;
- execution artifact absent: `Not executed`.

The corrected state should be visibly distinct, for example:

```text
Commit mutation succeeded — post-verification failed
```

The row should expose, where available:

- Commit Plan ID;
- mutation/execution evidence ID;
- starting HEAD;
- resulting HEAD;
- matching Snapshot ID;
- verification status and failure reason;
- explicit no-retry warning.

## 12. Matching Snapshot prerequisite

`prepare_commit` and `_assert_precommit_state` correctly require an exact matching immutable Snapshot for the current staged state. The check uses `_calculate_snapshot_candidate`, which rescans the repository, derives the current Snapshot candidate ID, verifies the existing Snapshot artifact, and compares the exact matching ID to the plan.

The safety rule is correct. The usability issue is orchestration: the Workflow page exposes the Prepare Commit form without first presenting the matching-Snapshot readiness state. A missing Snapshot is discovered only after the operator attempts Commit preparation.

## 13. Proposed Workflow Snapshot orchestration

M014 should reuse the current status and Snapshot services to show:

```text
Current staged state
    -> current Snapshot candidate
    -> exact matching Snapshot exists?

if yes:
    show Snapshot ID and “Matching Snapshot available”
    show Commit readiness

if no:
    show “Matching Snapshot required”
    show explicit Create Matching Snapshot action
    gate Prepare Commit
```

After explicit Snapshot creation:

```text
re-read current Git state
-> create Snapshot through existing create_snapshot service
-> regenerate/verify current matching status
-> expose Snapshot ID
-> enable Prepare Commit
```

Workflow must not silently create a Snapshot during page rendering.

## 14. Snapshot creation service reuse

The authoritative path is `repoctl.snapshot.manager.create_snapshot`, already used by the Snapshots browser route and CLI/service flows.

M014 should invoke or adapt this same service from Workflow orchestration. It should not implement a second Snapshot serializer, ID derivation path, artifact publisher, or integrity verifier.

## 15. Snapshot classification model

Use derived labels based on immutable Snapshot and workflow/execution evidence:

- **Intermediate**: historical Snapshot not tied to a current Commit Plan.
- **Matching Snapshot available**: exact current staged-state match exists, but no Commit Plan is necessarily using it yet.
- **Commit candidate**: Snapshot is explicitly referenced by a prepared/current Commit Plan.
- **Commit aligned**: a successful verified Commit is associated with the Snapshot and resulting Git SHA.
- **Commit mutation succeeded / audit failed**: Git Commit occurred and resulting SHA is known, but post-commit verification or audit failed.

Do not label every exact matching Snapshot as Commit candidate. Do not promote an audit-failed result to Commit aligned.

## 16. Snapshot immutability model

Snapshot artifacts remain immutable.

Commit alignment should be represented by immutable execution or association evidence that references:

- Snapshot ID;
- Commit Plan ID;
- mutation/execution evidence ID;
- starting HEAD;
- resulting Commit SHA;
- alignment/outcome type;
- verification state.

UI labels should be derived from those records. Existing Snapshot JSON should not be edited after publication.

## 17. Snapshot filtering / browsing recommendation

The smallest useful UI change is a derived status/filter presentation, not a Snapshot management redesign:

- All;
- Matching Snapshot available;
- Commit candidate;
- Commit aligned;
- Commit mutation succeeded / audit failed;
- Intermediate/unresolved.

The filter state should be derived from immutable Snapshot and workflow association evidence.

## 18. Git/Snapshot alignment presentation

Workflow and Snapshot detail should show concise operator-readable facts:

- Snapshot ID;
- Snapshot HEAD;
- current Git HEAD;
- exact-match status;
- staged-state fingerprint where useful;
- Commit Plan ID;
- resulting Commit SHA;
- alignment type;
- verification/audit status.

Preferred labels include:

- `Exact current match`;
- `Historical / not current`;
- `Matching Snapshot available`;
- `Commit candidate`;
- `Commit aligned`;
- `Commit mutation succeeded / audit failed`.

## 19. Existing test coverage

Existing tests cover:

- matching Snapshot requirement: `WorkflowCommitTests.test_prepare_blocks_missing_snapshot`;
- successful guarded Commit and execution evidence: `test_successful_commit_and_execution_evidence`;
- multi-file staged commit: `test_successful_commit_with_multi_file_staged_delta`;
- stale branch/HEAD/staged-state blocking: `test_stale_plan_blocks_on_head_branch_and_staged_changes`;
- post-verification failure with HEAD advancement: `test_post_verification_failure_after_successful_commit`;
- genuine fingerprint mismatch with HEAD advancement: `test_genuine_post_commit_mismatch_still_fails_closed`;
- execution-audit failure with HEAD advancement: `test_commit_succeeded_audit_failed`;
- plan integrity, approval, hook, identity, and commit failure boundaries;
- Snapshot creation/reuse and matching behavior in Snapshot/Workflow tests;
- Workflow artifact/history rendering in `tests/test_web.py`.

## 20. Missing regression coverage

M014 must add native tests for:

- recursive post-commit diff verification across nested paths;
- canonical Vocab-shaped add/modify multi-file commit fingerprint equality;
- mutation-success evidence persisted when post-verification fails;
- Workflow row not rendered as `Not executed` after mutation success;
- resulting HEAD and commit ID retained after audit failure;
- explicit retry warning or retry blocking;
- no automatic rollback/reset/revert;
- matching Snapshot readiness shown before Prepare Commit;
- explicit Workflow Snapshot creation using the existing Snapshot service;
- Snapshot classification from immutable associations;
- Commit candidate versus merely matching Snapshot available;
- Commit aligned versus mutation-succeeded/audit-failed;
- Snapshot artifacts remain byte-identical after alignment evidence is created.

## 21. Native failure fixture

The future M014 fixture should use a temporary native Repo Control Git repository:

1. create a tracked nested path and a modified tracked path;
2. stage exact approved files;
3. create a matching Snapshot with the existing Snapshot service;
4. prepare a Commit Plan;
5. execute the Commit with a controlled post-verification failure or a real recursive-diff verification path;
6. assert HEAD advanced and the commit exists;
7. assert mutation-success evidence records the resulting SHA;
8. assert audit failure remains explicit;
9. assert Workflow history does not say `Not executed`;
10. assert retry is blocked or unmistakably unsafe;
11. assert no rollback/reset/revert occurred;
12. assert Snapshot bytes remain unchanged.

A successful control fixture must prove the same nested-path commit produces a verified execution artifact and Commit aligned traceability.

## 22. Vocab role

Vocab is read-only historical evidence for M013. The canonical Vocab commit remains intact at `9b7465deb41a9efa06fc32db7d0723a8c550f1ec`, with the exact approved paths and a clean worktree.

No additional Vocab Commit, retry, reset, revert, Snapshot, or other Git mutation was performed.

Vocab M003 should become the next real end-to-end test after M014 passes its native fixtures.

## 23. Recommended M014 scope

One bounded M014 remains appropriate because all three issues share the same lifecycle and artifact surfaces:

```text
staged Git state
-> matching Snapshot
-> Commit Plan
-> Commit mutation
-> post-commit audit
-> immutable Snapshot/Commit traceability
```

M014 should implement:

- correct recursive post-commit verification;
- durable mutation-success-before-audit evidence;
- truthful Workflow rendering and recovery semantics;
- explicit matching-Snapshot readiness and creation orchestration from Workflow;
- immutable derived Snapshot-to-Commit association/labels.

No split is required by the M013 evidence. Split only if implementation design proves that persistence ordering and Snapshot association require materially incompatible artifact changes.

## 24. Explicit non-goals

M013 and recommended M014 do not include:

- semantic Context work;
- deployment/runtime work;
- Vocab implementation changes;
- Vocab mutation or retry;
- automatic retry/reset/restore/revert;
- mutable Snapshot artifacts;
- a second Snapshot implementation;
- unrelated UI redesign;
- fetch, pull, or push;
- Photo Organizer access.

## 25. Final Repo Control state

Captured after read-only reconnaissance and closeout creation:

- branch: `main`
- HEAD: `0c096e90688fad581f35fd120796b2797460b499`
- upstream: `0c096e90688fad581f35fd120796b2797460b499` (`origin/main`)
- ahead/behind: `0 0`

Literal final `git status --short`:

```text
 M docs/008_guarded_staging_preparation_prompt.md
 M docs/009_browser_ui_foundation_and_read_only_console_prompt.md
?? .venv/
?? docs/013_guarded_commit_verification_and_snapshot_workflow_reconnaissance_closeout.md
```

Expected pre-existing items remain unchanged. The only M013-authored project output is this closeout. Canonical Vocab final `git status --short` was empty; its HEAD remained `9b7465deb41a9efa06fc32db7d0723a8c550f1ec`.
