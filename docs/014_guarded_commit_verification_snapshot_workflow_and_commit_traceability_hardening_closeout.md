# M014 Guarded Commit Verification, Snapshot Workflow, and Commit Traceability Hardening Closeout

## 1. Executive conclusion

**PASS**

M014 corrects the M013 guarded-Commit defects and adds bounded Workflow Snapshot orchestration and derived Snapshot-to-Commit traceability.

Implemented outcomes:

- recursive post-commit delta verification now matches the staged file-level fingerprint model;
- immutable mutation-success execution evidence is published immediately after Git reports the resulting HEAD;
- immutable audit outcomes distinguish verified Commit from mutation-succeeded/audit-failed Commit;
- Workflow no longer renders `Not executed` after a successful Git mutation;
- Workflow exposes matching-Snapshot readiness before Commit preparation;
- Workflow provides an explicit CSRF-protected Create Matching Snapshot action using the existing Snapshot service;
- Snapshot classification is derived from immutable Plan/execution/audit evidence without modifying Snapshot artifacts.

The canonical Vocab repository was not mutated. Repo Control is ready to return to Vocab M003.

## 2. Starting repository state

The M014 starting gate recorded:

- branch: `main`
- HEAD: `78d3006adc93b690e1f2057313fa557204251a12`
- upstream: `origin/main`
- upstream SHA: `78d3006adc93b690e1f2057313fa557204251a12`
- ahead/behind: `0 0`

Expected pre-existing local state:

```text
 M docs/008_guarded_staging_preparation_prompt.md
 M docs/009_browser_ui_foundation_and_read_only_console_prompt.md
?? .venv/
```

The M014 prompt was committed before implementation. No unexpected source changes were present at the gate.

## 3. M013 requirements implemented

- Recursive verification: `git diff-tree` now traverses file records recursively.
- Mutation persistence: Commit execution evidence is published after successful Git mutation and resulting HEAD discovery, before post-commit audit.
- Audit outcome: separate immutable audit artifacts record `verified` or `mutation_succeeded_audit_failed`.
- Workflow truthfulness: history uses mutation evidence and audit evidence, so a successful mutation cannot appear as `Not executed`.
- Snapshot readiness: Workflow reads the current canonical matching-Snapshot status before exposing Commit preparation.
- Workflow Snapshot creation: explicit POST action reuses `run_scan_with_artifacts` and `create_snapshot`.
- Traceability: Snapshot classifications derive from immutable Commit Plan, execution, and audit evidence.
- Snapshot immutability: existing Snapshot artifacts are not rewritten.

## 4. Recursive post-commit verification

`_verify_post_commit` now invokes recursive `git diff-tree` traversal with `-r`.

This preserves exact file-level comparison of:

- nested paths;
- multiple files;
- add/modify combinations;
- status;
- modes;
- object IDs;
- deterministic path ordering;
- staged-delta fingerprint equality.

The M013 Vocab-shaped failure is fixed without weakening the fingerprint comparison.

## 5. Mutation-success persistence

After `git commit` succeeds and `HEAD` is read, M014 immediately publishes an immutable Commit execution artifact containing:

- Commit Plan ID;
- repository and branch;
- starting and resulting HEAD;
- commit message;
- matching Snapshot ID;
- staged state and delta fingerprints;
- staged scope;
- `mutation_succeeded: true`;
- verification status initially represented as pending.

A separate immutable `commit_audits/<audit_id>/audit.json` and `audit.md` records the later outcome. This avoids mutating the Snapshot or rewriting the mutation-success fact.

## 6. Audit-failure behavior

Post-commit verification failure now publishes an immutable audit outcome with:

- mutation succeeded;
- resulting HEAD;
- execution ID;
- Commit Plan ID;
- outcome `mutation_succeeded_audit_failed`;
- concise failure reason.

A normal verified Commit publishes an audit outcome of `verified`.

The underlying diagnostic distinction remains available between post-verification failure and audit publication failure. The shared operator truth is that Git mutation succeeded.

## 7. Retry/recovery safety

M014 does not add automatic recovery mutation.

After mutation-succeeded/audit-failed:

- no retry is automatic;
- no reset, restore, revert, amend, or replacement Commit is performed;
- resulting HEAD remains visible;
- the Workflow state is distinct from `Not executed`;
- the operator must inspect the resulting evidence before any subsequent action.

## 8. Workflow rendering

Workflow history now reads immutable Commit execution and audit evidence together.

Verified outcome:

```text
Executed
Committed to <resulting HEAD>
```

Audit-failed outcome:

```text
Mutation succeeded / audit failed
Commit mutation succeeded; post-verification failed: <reason>
```

The execution ID and resulting HEAD remain displayed. The audit-failed row is not rendered as `Not executed`.

## 9. Matching Snapshot readiness

The Workflow route refreshes canonical status before rendering and receives:

- current workflow state;
- `matching_snapshot_exists`;
- `matching_snapshot_id`.

When staged state exists without an exact Snapshot, Workflow shows:

```text
Matching Snapshot required
Snapshot: none
```

and does not show an active Prepare Commit form.

When the exact match exists, Workflow shows the Snapshot ID and exposes Prepare Commit subject to the existing core gates.

## 10. In-Workflow Snapshot creation

Workflow provides `POST /workflow/snapshot/create`, protected by the existing CSRF mechanism.

The route:

1. re-runs the authoritative scan;
2. calls the existing `create_snapshot` service;
3. redirects to Workflow;
4. causes current matching status to be regenerated and displayed.

No Snapshot is created during Workflow GET rendering, and no second Snapshot engine was introduced.

## 11. Snapshot classification

The existing Snapshot list now derives a classification from immutable workflow evidence:

- `Intermediate`: historical Snapshot without a Commit Plan association;
- `Matching Snapshot available`: exact current candidate without a Commit Plan association;
- `Commit candidate`: referenced by a Commit Plan;
- `Commit aligned`: referenced by a verified Commit execution/audit outcome;
- `Commit mutation succeeded / audit failed`: referenced by mutation evidence whose audit outcome failed.

An exact matching Snapshot is not automatically labeled Commit candidate.

## 12. Snapshot-to-Commit association

No Snapshot JSON is changed.

The derived relationship uses existing immutable references:

- Commit Plan `matching_snapshot_id`;
- Commit execution `execution_id`, `head_before`, `head_after`, and mutation evidence;
- Commit audit outcome and verification state.

These references are sufficient for the current bounded UI projection without adding a second association artifact.

## 13. Snapshot immutability

Snapshot creation and verification code remains authoritative and unchanged in its artifact identity and publication model.

M014 only reads Snapshot IDs and joins them to immutable workflow evidence. Existing Snapshot bytes are not edited after creation.

## 14. Snapshot browsing/filtering

The existing Snapshot table now displays the derived classification alongside its existing immutable state label, Snapshot ID, HEAD, cleanliness, and current-match status.

No broad Snapshot-management redesign or filter subsystem was added.

## 15. Files changed

Implementation and tests:

- `src/repoctl/workflow/commit_execution.py`
- `src/repoctl/web/app.py`
- `src/repoctl/web/views.py`
- `src/repoctl/web/templates/workflow.html`
- `src/repoctl/web/templates/snapshots.html`
- `tests/test_workflow_commit.py`
- `tests/test_web.py`

Closeout:

- `docs/014_guarded_commit_verification_snapshot_workflow_and_commit_traceability_hardening_closeout.md`

Pre-existing `docs/008`, `docs/009`, and `.venv/` were not modified or staged.

## 16. Tests added/changed

Native Commit coverage now includes:

- recursive nested-path verification;
- Vocab-shaped multi-file fingerprint equality;
- mutation evidence after post-verification failure;
- audit outcome persistence;
- resulting HEAD preservation;
- Workflow history not showing `Not executed`;
- `WorkflowCommitTests.test_post_verification_failure_after_successful_commit` verifies the browser page has no ordinary `/workflow/commit/prepare` form after mutation success/audit failure;
- the same test verifies the explicit `Do not retry automatically` warning;
- audit-failed status rendering;
- no rollback behavior.

Browser coverage now includes:

- staged-only Snapshot prerequisite gating;
- explicit Workflow Snapshot creation;
- readiness transition after Snapshot creation;
- Commit action availability only after exact matching Snapshot exists.

Snapshot byte immutability is verified by `WorkflowCommitTests.test_nested_paths_match_staged_fingerprint_after_commit`, which captures every Snapshot artifact file before verified Commit association and compares the complete byte map afterward.

## 17. Focused test results

Command:

```bash
cd /home/chuck/projects/repo-control
. .venv/bin/activate
PYTHONPATH=src python3 -m unittest tests.test_workflow_commit tests.test_web
```

Literal result:

```text
Ran 44 tests in 3.790s
OK
```

The combined Commit/Snapshot/Web validation also passed:

```text
Ran 57 tests in 3.964s
OK
```

## 18. Full suite results

Command:

```bash
cd /home/chuck/projects/repo-control
. .venv/bin/activate
PYTHONPATH=src python3 -m unittest
```

Literal result:

```text
Ran 162 tests in 6.851s
OK
```

## 19. Compile/static validation

Command:

```bash
PYTHONPATH=src python3 -m compileall -q src tests
```

Completed successfully.

`git diff --check -- src tests` also completed without findings.

## 20. Browser validation

A temporary native Git repository was used; Vocab was not used for mutation testing.

Missing Snapshot case:

```text
MISSING_SNAPSHOT_GATE True True False
```

This confirmed:

- matching Snapshot required was visible;
- Create Matching Snapshot was visible;
- Prepare Commit was not visible.

After explicit Snapshot creation:

```text
SNAPSHOT_CREATED_READINESS True True
SNAPSHOT_PAGE_CLASSIFICATION True
```

Controlled audit-failure case:

```text
AUDIT_FAILURE_CODE post_commit_verification_failed
AUDIT_UI_STATE True False True True
HEAD_ADVANCED True
```

This confirmed:

- Git mutation occurred;
- resulting HEAD advanced;
- Workflow showed mutation succeeded/audit failed;
- Workflow did not show `Not executed`;
- execution evidence remained visible.

## 21. Native successful Commit fixture

The existing successful Commit controls continued to pass, including ordinary single-file Commit, multi-file Commit, staged fingerprint validation, clean post-Commit state, and execution evidence publication.

The recursive nested-path success fixture also passed and produced a `verified` audit outcome.

## 22. Native mutation-succeeded/audit-failed fixture

The native forced post-verification failure fixture passed:

- temporary repository Commit advanced HEAD;
- `post_commit_verification_failed` remained the diagnostic exception;
- mutation execution evidence was persisted;
- audit outcome was persisted as `mutation_succeeded_audit_failed`;
- Workflow history showed `Mutation succeeded / audit failed`;
- no `Not executed` state was rendered;
- no ordinary Commit approval form was rendered;
- the explicit `Do not retry automatically` warning was rendered;
- no rollback or retry mutation occurred.

## 23. Vocab status

Canonical Vocab was not used as a mutation fixture and was not modified, staged, committed, reset, restored, reverted, or pushed during M014.

The historical Vocab repository remains outside the M014 mutation path. No Photo Organizer access occurred.

## 24. Remaining limitations

- The mutation evidence artifact remains the immutable record of Commit success, while the audit artifact carries final verification state; consumers must join both records for complete status.
- Snapshot classification is currently presented in the existing Snapshot table rather than a broader filter/search experience.
- No automatic recovery workflow was added by design.
- Vocab M003 has not yet been run and is the next real-world validation.

## 25. Recommendation

Repo Control is ready to return to Vocab M003.

The next project milestone should be Vocab M003 using the improved Context, matching-Snapshot Workflow, guarded Stage/Commit, and Commit traceability surfaces from the start.

No M015 should be created merely for additional Repo Control polishing unless Vocab M003 exposes a genuine new control-plane gap.

## 26. Final repository state

- branch: `main`
- HEAD: `78d3006adc93b690e1f2057313fa557204251a12`
- upstream: `78d3006adc93b690e1f2057313fa557204251a12` (`origin/main`)
- ahead/behind: `0 0`

Literal final `git status --short`:

```text
 M docs/008_guarded_staging_preparation_prompt.md
 M docs/009_browser_ui_foundation_and_read_only_console_prompt.md
 M src/repoctl/web/app.py
 M src/repoctl/web/templates/snapshots.html
 M src/repoctl/web/templates/workflow.html
 M src/repoctl/web/views.py
 M src/repoctl/workflow/commit_execution.py
 M tests/test_web.py
 M tests/test_workflow_commit.py
?? .venv/
?? docs/014_guarded_commit_verification_snapshot_workflow_and_commit_traceability_hardening_closeout.md
```

No staging, commit, push, cleanup, restore, reset, or Vocab mutation was performed during M014.
