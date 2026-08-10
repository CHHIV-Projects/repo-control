# Milestone 007 — Guarded Git Write Foundation Closeout

## 1. Status

PASS

## 2. Initial branch / HEAD / clean preflight

Initial preflight evidence before implementation:

- branch: `main`
- head: `85faf2948dff3914ccafa11d1e5f3d7a97eb712b`
- `git status --short`: clean

## 3. Files changed

Added:

- `src/repoctl/workflow/errors.py`
- `src/repoctl/workflow/commit_plan.py`
- `src/repoctl/workflow/commit_execution.py`
- `tests/test_workflow_commit.py`
- `docs/007_guarded_git_write_foundation_closeout.md`

Modified:

- `src/repoctl/workflow/__init__.py`
- `src/repoctl/cli.py`
- `README.md`

## 4. Core service architecture

Milestone 007 is implemented with reusable workflow services (CLI remains a thin adapter):

- `prepare_commit(...)` in `workflow/commit_plan.py`
- `execute_prepared_commit(...)` in `workflow/commit_execution.py`

Shared deterministic Git-state semantics are reused from Milestone 006:

- `workflow/git_state.py`
- `workflow/status.py` snapshot-candidate/matching logic

Stable reason-code carrying error type:

- `WorkflowReasonError` in `workflow/errors.py`

## 5. CLI commands implemented

Implemented command surfaces:

```bash
repoctl milestone prepare-commit --message "<commit message>" [--repository <path>]
repoctl milestone commit <plan_id> --approve [--repository <path>]
```

## 6. Mechanical commit preconditions

`prepare-commit` enforces fail-closed preconditions:

- attached branch required (`detached_head` on failure)
- staged changes required (`no_staged_changes`)
- zero unstaged changes (`unstaged_changes_present`)
- zero untracked files (`untracked_changes_present`)
- zero unmerged entries (`conflicts_present`)
- zero active Git operations (`git_operation_in_progress`)

No auto-staging or auto-cleanup is performed.

## 7. Snapshot requirement

Preparation requires exact matching immutable snapshot:

- uses existing M006 snapshot candidate/matching check
- fails closed with `matching_snapshot_required` when missing
- does not auto-create snapshots

## 8. Staged fingerprint contract

Plan binding uses deterministic staged fingerprinting from canonicalized Git plumbing records with rename heuristics disabled:

- command basis: `git diff-index --cached --raw --no-renames --abbrev=40 -z HEAD --`
- canonical metadata included: path, status, old/new object IDs, old/new modes
- fingerprint changes for material staged-index changes, including content replacement under same path, set changes, deletions, and mode changes
- no source bodies or full textual diff stored

## 9. Immutable plan schema/storage

External immutable plan storage:

- `~/.local/share/repoctl/<repo-id>/workflow/commit_plans/<plan-id>/`
- artifacts: `plan.json`, `plan.md`

Plan ID is deterministic/content-derived from canonical plan content.

If same deterministic plan exists, it is reused after integrity verification.
If deterministic ID exists with inconsistent content, operation fails closed (`plan_integrity_failed`).

## 10. Explicit approval behavior

Commit execution requires both:

- exact `plan_id`
- explicit `--approve`

Without `--approve`:

- no mutation
- `approval_required`

No "latest plan" or implicit approval behavior exists.

## 11. Stale-plan revalidation behavior

Immediately before mutation, execution reloads plan and revalidates:

- repository identity/root
- branch attached + exact branch name
- exact HEAD before
- exact staged-state fingerprint
- no unstaged/untracked/conflicts/active operation
- matching immutable snapshot still satisfied

Mismatches fail closed with specific reasons, e.g.:

- `repository_mismatch`
- `branch_changed`
- `head_changed`
- `staged_state_changed`

## 12. Hook boundary

Strict hook boundary implemented per addendum:

- block if any executable commit hook is present (`pre-commit`, `prepare-commit-msg`, `commit-msg`, `post-commit`)
- block if `core.hooksPath` is custom-configured
- return `unsupported_git_hooks`
- no use of `--no-verify`

## 13. Git identity behavior

Execution verifies author/committer identity using Git-provided identity resolution.

If unavailable:

- fail closed with `git_identity_unavailable`
- no automatic config mutation (`user.name`/`user.email`) is performed

## 14. Exact commit execution behavior

After all gates pass:

- exactly one ordinary local commit is executed
- exact approved message is used
- command runs non-interactively (`GIT_EDITOR=:`)
- implicit signing suppressed (`--no-gpg-sign`) for bounded behavior
- no fetch/pull/push/staging/amend/tag/branch mutation

## 15. Post-commit verification

Execution does not trust Git exit code alone. It verifies:

- HEAD changed
- new commit parent equals planned previous HEAD
- branch unchanged
- committed delta fingerprint equals approved staged delta fingerprint
- index clean (no staged entries)
- worktree clean (no unstaged/untracked)
- no conflicts
- no active git operation

On verification failure after commit:

- returns `post_commit_verification_failed`
- includes resulting commit ID
- does not reset/revert/retry

## 16. Execution evidence schema/storage

Immutable execution evidence path:

- `~/.local/share/repoctl/<repo-id>/workflow/commit_executions/<execution-id>/`
- artifacts: `execution.json`, `execution.md`

Execution includes at minimum:

- plan ID
- repository ID/root
- branch
- HEAD before/after
- commit message
- matching snapshot ID
- staged fingerprints/summary
- verification facts
- `remote_refresh_performed=false`
- `push_performed=false`

Execution IDs are deterministic/content-derived.
Existing deterministic execution IDs are reused only after integrity verification.

## 17. Audit-failure-after-commit behavior

Implemented explicit condition:

- `commit_succeeded_audit_failed`

When commit succeeds but external execution-audit write fails:

- commit remains
- resulting commit ID is reported
- no retry/second commit performed

## 18. Stable reason/error codes

Implemented reason distinctions include:

- `approval_required`
- `detached_head`
- `no_staged_changes`
- `unstaged_changes_present`
- `untracked_changes_present`
- `conflicts_present`
- `git_operation_in_progress`
- `matching_snapshot_required`
- `invalid_commit_message`
- `plan_not_found`
- `plan_integrity_failed`
- `repository_mismatch`
- `branch_changed`
- `head_changed`
- `staged_state_changed`
- `unsupported_git_hooks`
- `git_identity_unavailable`
- `git_commit_failed`
- `post_commit_verification_failed`
- `commit_succeeded_audit_failed`

## 19. Focused test result

Focused Milestone 007 tests:

```bash
PYTHONPATH=src python3 -m unittest tests.test_workflow_commit -q
```

Result:

- `Ran 16 tests ... OK`

Coverage includes prepare/commit success, blocking gates, stale-plan refusal, hook boundary, identity boundary, plan integrity, commit failure, post-verify failure, audit failure, and CLI behavior.

## 20. Full regression result

Full suite under ordinary Python behavior:

```bash
PYTHONPATH=src python3 -m unittest -q
```

Result:

- `Ran 115 tests ... OK`

## 21. Python-cache hygiene result

Milestone 006.1 hygiene remained effective:

- no tracked `*.pyc` / `*.pyo` / `__pycache__` paths were introduced by ordinary test execution

## 22. Practical isolated-repository validation

Practical success lifecycle demonstrated in an isolated temporary repo:

1. init repo + initial commit
2. make controlled source change
3. stage manually
4. create matching `repoctl snapshot`
5. `repoctl milestone prepare-commit --message 'M007 practical commit'`
6. verify HEAD unchanged before commit execution
7. `repoctl milestone commit <plan-id> --approve`
8. verify exactly one new commit
9. verify parent equals previous HEAD
10. verify exact commit message
11. verify clean repository
12. verify execution evidence path emitted

Observed evidence:

- `PLAN_ID=commit-plan--775c114a0e7bd9c5`
- `HEAD_BEFORE=43ec1877a3d746a4a76cb53514f8a8ea1bb6a28e`
- `HEAD_AFTER=b57abb0ba236c1088608d3d178eeb43e3a8faae1`
- `PARENT=43ec1877a3d746a4a76cb53514f8a8ea1bb6a28e`
- `COMMIT_MSG=M007 practical commit`
- `STATUS_EMPTY=1`

## 23. Stale-plan practical validation

Practical stale-plan refusal demonstrated in isolated repo:

1. prepare valid plan
2. modify staged content and restage
3. attempt approved execution with original plan
4. block with stale-state reason
5. HEAD unchanged

Observed evidence:

- commit exit code: `2`
- `HEAD_UNCHANGED=1`
- error: `workflow error [staged_state_changed]: staged index state changed since plan preparation`

## 24. Confirmation no network mutation occurred

Confirmed by implementation and validation:

- no fetch/pull/push in prepare or commit path
- CLI success output states remote refresh not performed and push performed false

## 25. Confirmation no Vocab App mutation occurred

Confirmed.

Milestone 007 mutation validation used only disposable temporary repositories.

## 26. Confirmation no Photo Organizer access occurred

Confirmed.

No Photo Organizer paths were accessed, scanned, or mutated.

## 27. Limitations/deferred items

Deferred by design:

- hook-aware deterministic commit support with custom hook environments
- staging automation
- push/fetch/pull
- branch/switch orchestration
- amend/signing workflows
- GUI/API integration

Current milestone intentionally provides a bounded local prepared-commit primitive only.

## 28. Recommendation for next milestone

Build Milestone 008 on the same immutable plan + explicit approval + revalidation architecture, adding carefully scoped higher-level workflow operations (for example, deterministic staging preparation) without weakening M007 safety boundaries.

## 29. Final `git status --short`

```text
 M README.md
 M src/repoctl/cli.py
 M src/repoctl/workflow/__init__.py
?? docs/007_guarded_git_write_foundation_closeout.md
?? src/repoctl/workflow/commit_execution.py
?? src/repoctl/workflow/commit_plan.py
?? src/repoctl/workflow/errors.py
?? tests/test_workflow_commit.py
```
