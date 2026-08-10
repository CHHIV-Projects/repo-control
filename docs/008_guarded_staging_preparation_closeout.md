# Milestone 008 — Guarded Staging Preparation Closeout

## 1. Status

PASS

## 2. Initial branch / HEAD / clean preflight

Initial preflight before implementation:

- branch: `main`
- head: `f2261494f3e2b56a530f6365c2e1c87d77549665`
- `git status --short`: clean

## 3. Files changed

Added:

- `src/repoctl/workflow/stage_plan.py`
- `src/repoctl/workflow/stage_execution.py`
- `tests/test_workflow_stage.py`
- `docs/008_guarded_staging_preparation_closeout.md`

Modified:

- `src/repoctl/workflow/__init__.py`
- `src/repoctl/cli.py`
- `README.md`

## 4. Core service architecture

Milestone 008 adds reusable staging core services parallel to M007:

- `prepare_stage(...)` in `workflow/stage_plan.py`
- `execute_prepared_stage(...)` in `workflow/stage_execution.py`

The CLI remains a thin adapter.

Existing M006/M007 workflow architecture is reused:

- `workflow/git_state.py` for canonical Git state
- `WorkflowReasonError` in `workflow/errors.py`
- immutable plan/execution publication patterns aligned with M007

## 5. CLI commands implemented

Implemented command surfaces:

```bash
repoctl milestone prepare-stage --all [--repository <path>]
repoctl milestone stage <plan_id> --approve [--repository <path>]
```

## 6. Mechanical prepare preconditions

`prepare-stage` fails closed unless:

- branch is attached
- existing staged changes count is zero
- unmerged entries count is zero
- no active Git operation exists
- at least one eligible unstaged or untracked change exists

Reason-code coverage includes:

- `detached_head`
- `staged_changes_present`
- `conflicts_present`
- `git_operation_in_progress`
- `no_stage_candidates`

## 7. Candidate enumeration contract

Candidate enumeration is deterministic and Git-derived.

Read-only plumbing used:

- `git diff-files --raw --no-renames --abbrev=40 -z --`
- `git ls-files --others --exclude-standard -z`

The candidate set represents all currently visible eligible unstaged/untracked paths, not a later recomputed broad directory add.

Ignored files are excluded by Git’s own `--exclude-standard` handling.

## 8. Supported path types

Supported:

- regular tracked file modifications
- tracked deletions
- ordinary mode changes for regular files
- regular untracked file additions

Fail-closed unsupported path handling is implemented for:

- symlinks
- submodule/gitlink changes
- non-regular/special filesystem objects

Reason code:

- `unsupported_path_type`

## 9. Git filter/attribute boundary

Before planning/execution, candidate paths are checked with Git attribute inspection.

If a custom `filter` attribute applies to any candidate path, planning blocks with:

- `unsupported_git_filters`

This blocks Git LFS or other custom clean/process filters in Milestone 008.

## 10. Prospective staged-object identity method

For non-deletion regular file candidates, expected staged object identity is computed read-only with Git’s content-conversion machinery using `git hash-object --path=<path> <file>` without `-w`.

The plan records at minimum:

- path
- change classification
- prior object ID when applicable
- expected staged object ID
- prior mode when applicable
- expected staged mode
- deletion state

No file bodies or full textual diffs are stored.

## 11. Stage-candidate fingerprint contract

The immutable plan binds exact candidate state through:

- repository identity/root
- branch
- HEAD
- exact candidate records
- expected staged object IDs
- expected modes/deletion state
- filter-policy evidence

The plan also records an `expected_staged_delta_fingerprint` derived from canonical raw staged records so post-stage verification can reconcile the actual index against the reviewed plan exactly.

Material candidate changes invalidate the plan and cause execution to block with `worktree_state_changed`, `branch_changed`, or `head_changed` as appropriate.

## 12. Immutable plan schema/storage

Stage plans are stored externally under:

- `~/.local/share/repoctl/<repo-id>/workflow/stage_plans/<plan-id>/`

Artifacts:

- `plan.json`
- `plan.md`

Plan IDs are deterministic/content-derived.

Repeated identical prepares reuse an existing plan only after integrity verification.
ID/content mismatch fails closed with `plan_integrity_failed`.

## 13. Prepare read-only evidence

Focused tests verify prepare-stage leaves the target repository unchanged:

- HEAD unchanged
- index unchanged
- worktree unchanged

Practical isolated validation also confirmed:

- `HEAD_BEFORE == HEAD_AFTER_PREPARE`
- `PREPARE_STATUS_UNCHANGED=1`

## 14. Explicit approval behavior

Execution requires both:

- exact immutable `plan_id`
- explicit `--approve`

Without `--approve`:

- no mutation occurs
- `approval_required` is returned

There is no “latest plan” fallback or recomputed stage-on-approve behavior.

## 15. Stale-plan revalidation behavior

Immediately before staging, execution reloads and revalidates:

- plan integrity
- repository binding
- attached branch and exact branch name
- exact HEAD
- zero existing staged changes
- zero conflicts
- zero active Git operations
- exact candidate fingerprint equality

Stale-plan tests cover changed file contents, changed untracked contents, changed path set, changed HEAD, and changed branch.

## 16. Exact staging execution behavior

Execution stages only exact reviewed repository-relative paths from the immutable plan using structured subprocess arguments and `--` path separators.

It does not use uncontrolled `git add .` or `git add -A` over recomputed repository state.

Tracked paths are staged with bounded explicit-path `git add --update -- ...`.
Untracked additions are staged with bounded explicit-path `git add -- ...`.

No commit/fetch/pull/push/reset/restore/stash/branch mutation occurs.

## 17. Index-lock handling

Execution checks `index.lock` via Git-resolved metadata path before mutation.

If present, execution fails closed with:

- `git_index_locked`

No automatic lock deletion or retry occurs.

## 18. Post-stage verification

Execution does not trust `git add` exit code alone. After successful staging it verifies:

- HEAD unchanged
- branch unchanged
- staged changes present
- exact staged path set equals approved plan
- staged raw object/mode records equal approved expected records
- no unstaged changes remain
- no untracked visible changes remain
- no conflicts exist
- no Git operation is active
- resulting workflow state is `staged_only`

## 19. Git-stage failure/partial-mutation behavior

Non-zero `git add` results are inspected against the index before returning.

Implemented distinction:

- `git_stage_failed` when no index mutation occurred
- `git_stage_failed_after_mutation` when the index differs from the pre-execution state

Neither case triggers automatic unstage/reset/retry.

## 20. Execution evidence schema/storage

Successful verified staging writes immutable external execution evidence under:

- `~/.local/share/repoctl/<repo-id>/workflow/stage_executions/<execution-id>/`

Artifacts:

- `execution.json`
- `execution.md`

Recorded facts include at minimum:

- plan ID
- repository ID/root
- branch
- HEAD before/after
- candidate fingerprint
- resulting staged fingerprint
- staged summary
- verification facts
- resulting workflow state
- `remote_refresh_performed=false`
- `commit_performed=false`
- `push_performed=false`

## 21. Audit-failure-after-stage behavior

If staging and verification succeed but execution-audit persistence fails, Milestone 008 returns:

- `stage_succeeded_audit_failed`

The resulting staged state remains preserved. No second staging attempt or automatic unstage occurs.

## 22. Stable reason/error codes

Implemented reason distinctions include:

- `approval_required`
- `detached_head`
- `staged_changes_present`
- `no_stage_candidates`
- `conflicts_present`
- `git_operation_in_progress`
- `unsupported_path_type`
- `unsupported_git_filters`
- `plan_not_found`
- `plan_integrity_failed`
- `repository_mismatch`
- `branch_changed`
- `head_changed`
- `worktree_state_changed`
- `git_index_locked`
- `git_stage_failed`
- `git_stage_failed_after_mutation`
- `post_stage_verification_failed`
- `stage_succeeded_audit_failed`

## 23. Focused test result

Focused Milestone 008 tests:

```bash
PYTHONPATH=src python3 -m unittest tests.test_workflow_stage -q
```

Result:

- `Ran 13 tests ... OK`

Coverage includes prepare success, block conditions, unsupported filters/path types, plan determinism/integrity, approval, stale-plan refusal, index-lock handling, exact successful staging, stage failure before mutation, failure after mutation, post-stage verification failure, audit failure, and CLI adapters.

## 24. Full regression result

Full suite under ordinary Python behavior:

```bash
PYTHONPATH=src python3 -m unittest -q
```

Result:

- `Ran 128 tests ... OK`

## 25. Python-cache hygiene result

Milestone 006.1 hygiene remained effective:

- no tracked `*.pyc` / `*.pyo` / `__pycache__` paths were introduced during ordinary test execution

## 26. Practical isolated-repository success validation

Isolated practical lifecycle demonstrated:

1. initial commit
2. modify tracked file
3. add untracked file
4. delete tracked file
5. `prepare-stage --all`
6. verify HEAD and visible status unchanged after prepare
7. `stage <plan-id> --approve`
8. verify HEAD unchanged
9. verify exact staged path set
10. verify execution evidence

Observed evidence:

- `PLAN_ID=stage-plan--f5bd708d0c7e45d2`
- `HEAD_BEFORE=aef2a25bb8142b2b91bf8d2cb9e8e7d675d3670e`
- `HEAD_AFTER_PREPARE=aef2a25bb8142b2b91bf8d2cb9e8e7d675d3670e`
- `HEAD_AFTER_STAGE=aef2a25bb8142b2b91bf8d2cb9e8e7d675d3670e`
- `PREPARE_STATUS_UNCHANGED=1`
- final staged status:
  - `M  app.py`
  - `A  new.txt`
  - `D  old.txt`

## 27. Stale-plan practical validation

Isolated stale-plan refusal demonstrated:

1. prepare valid stage plan
2. modify candidate file after preparation
3. attempt approved execution
4. block before staging
5. verify HEAD unchanged
6. verify index unchanged

Observed evidence:

- `PLAN_ID=stage-plan--bcbd593c6f4482b3`
- `STAGE_EXIT=2`
- `HEAD_UNCHANGED=1`
- `INDEX_UNCHANGED=1`
- error: `workflow error [worktree_state_changed]: worktree candidate state changed since stage plan preparation`

## 28. M007 integration validation

In an isolated repository, the intended combined workflow was demonstrated:

1. create working-tree changes
2. `prepare-stage --all`
3. approve stage
4. verify staged result
5. `repoctl snapshot`
6. `repoctl milestone prepare-commit --message 'Integration path'`

Observed result:

- `PREPARE_COMMIT_EXIT=0`
- commit plan was prepared successfully against the staged-only + snapshotted state

This confirms successful M008 output is directly compatible with M007 after an explicit snapshot.

## 29. Confirmation no network mutation occurred

Confirmed.

No fetch/pull/push or remote refresh occurs in the M008 staging path.

## 30. Confirmation no commit occurred during M008 staging path

Confirmed.

Practical validation showed `HEAD_AFTER_STAGE == HEAD_BEFORE` and no commit command is invoked by the M008 path.

## 31. Confirmation no Vocab App mutation occurred

Confirmed.

All M008 mutation validation used disposable temporary repositories only.

## 32. Confirmation no Photo Organizer access occurred

Confirmed.

No Photo Organizer paths were accessed, scanned, or mutated.

## 33. Limitations/deferred items

Deferred by design:

- selective path staging
- partial-hunk staging
- AI-assisted file selection
- custom Git filter driver support
- broad symlink support
- submodule staging
- remote workflow / push
- GUI/API integration

## 34. Recommendation for next milestone

Build the next milestone on top of the complete bounded local mutation chain now available:

`prepare-stage -> approve stage -> snapshot -> prepare-commit -> approve commit`

The most natural next step is either a guarded local push/remote workflow or initial GUI composition over these existing immutable plan/execution services.

## 35. Literal final `git status --short`

```text
 M README.md
 M src/repoctl/cli.py
 M src/repoctl/workflow/__init__.py
?? docs/008_guarded_staging_preparation_closeout.md
?? src/repoctl/workflow/stage_execution.py
?? src/repoctl/workflow/stage_plan.py
?? tests/test_workflow_stage.py
```