# Milestone 006 Read-Only Git Workflow Intelligence Closeout

## 1. Implementation summary

Milestone 006 adds `repoctl milestone status [--repository <path>]` as a deterministic, read-only Git workflow inspection command.

Implementation reuses the Milestone 001 porcelain-v2 entry parser semantics by extracting shared parse logic in `scanner.git_ops`, then layers Milestone 006 branch-header parsing, workflow-state classification, upstream divergence reporting, active Git-operation detection, snapshot-candidate matching, and transactional workflow publication in a focused `repoctl.workflow` package.

The command publishes replaceable current-state artifacts under external Repo Control Plane state without creating snapshots, comparisons, or AI analyses.

## 2. Files added/modified

Added:

- `src/repoctl/workflow/__init__.py`
- `src/repoctl/workflow/git_state.py`
- `src/repoctl/workflow/status.py`
- `tests/test_workflow_status.py`
- `docs/006_read_only_git_workflow_intelligence_closeout.md`

Modified:

- `src/repoctl/cli.py`
- `src/repoctl/scanner/core.py`
- `src/repoctl/scanner/git_ops.py`
- `README.md`

## 3. CLI syntax

```bash
repoctl milestone status [--repository <path>]
```

If `--repository` is omitted, the current working directory is used.

## 4. Read-only Git command boundary

Production status implementation performs read-only Git inspection only.

Used Git behavior is limited to read-only commands such as:

- `git rev-parse --show-toplevel`
- `git rev-parse HEAD`
- `git branch --show-current`
- `git status --porcelain=v2 --branch -z --untracked-files=all`
- `git rev-parse --git-path <marker>`

No fetch, pull, push, commit, reset, restore, switch, checkout-for-mutation, merge completion, rebase continuation, stash, or other Git mutation occurs in the production path.

Automated tests also verify the status path itself does not invoke fetch/pull/push.

## 5. `status.json` schema at a useful high level

`status.json` uses `schema_version = 1` and includes:

- `repository_id`
- `repository_root`
- `head`
- `branch`
- `upstream`
- `remote_refresh_performed`
- `working_tree`
- `workflow_state`
- `git_operation_in_progress`
- `git_operations`
- `mutation_preconditions`
- `current_snapshot_id_candidate`
- `matching_snapshot_exists`
- `matching_snapshot_id`

The `working_tree` object includes deterministic counts and paths for:

- `staged`
- `unstaged`
- `untracked`
- `unmerged`

It also preserves structured porcelain-derived entry evidence.

## 6. Workflow-state enum behavior

Implemented exactly:

- `clean`
- `staged_only`
- `unstaged_only`
- `staged_and_unstaged`
- `conflicted`

Precedence:

- `conflicted` if any unmerged entry exists
- `staged_only` if staged exists and no unstaged/untracked/unmerged exists
- `staged_and_unstaged` if staged exists and any unstaged or untracked exists
- `unstaged_only` if no staged exists and any unstaged or untracked exists
- `clean` otherwise

No policy values such as safe/ready/approved are introduced.

## 7. Staged/unstaged/untracked/unmerged handling

Milestone 006 derives deterministic collections:

- `staged.paths`
- `unstaged.paths`
- `untracked.paths`
- `unmerged.paths`

A path may appear in both staged and unstaged collections when index and worktree changes coexist on the same path.

Rename/copy records remain explicit in the preserved structured entry evidence.

No diffs or source bodies are emitted.

## 8. Branch/detached behavior

Branch reporting remains consistent with existing repository evidence:

- attached: `{ "state": "attached", "name": "<branch>" }`
- detached: `{ "state": "detached", "name": null }`

HEAD commit is reported independently.

## 9. Upstream/divergence behavior

Implemented upstream contract:

- no configured upstream:
  - `configured = false`
  - `divergence_state = "unavailable"`
  - `unavailable_reason = "upstream_not_configured"`
  - `ref = null`, `relation = null`, `ahead = null`, `behind = null`
- configured but locally unavailable upstream ref:
  - `configured = true`
  - `divergence_state = "unavailable"`
  - `unavailable_reason = "upstream_ref_unavailable"`
  - `relation = null`, `ahead = null`, `behind = null`
- configured and locally available upstream relation:
  - `divergence_state = "available"`
  - `unavailable_reason = null`
  - relation derived deterministically as `equal`, `ahead`, `behind`, or `diverged`

No fetch is performed. Ahead/behind reflects only locally available refs.

## 10. Confirmation no fetch/network operation occurs

Confirmed by focused test instrumentation and live validation behavior:

- focused test asserts status path does not invoke `fetch`, `pull`, or `push`
- Vocab App validation produced `remote_refresh_performed = false`
- CLI/Markdown wording states that remote refresh was not performed

No public network hosting is contacted by production status.

## 11. Active Git-operation detection

Detected operations:

- `merge`
- `rebase`
- `cherry_pick`
- `revert`
- `bisect`

Output schema intentionally remains minimal:

- `git_operation_in_progress`
- `git_operations`

Only fixed ordered operation names are published. Internal Git marker paths and metadata file names are not exposed in artifacts.

## 12. Mutation-precondition contract

`mutation_preconditions` exposes facts only:

- `branch_attached`
- `staged_changes_present`
- `unstaged_changes_present`
- `untracked_changes_present`
- `unmerged_entries_present`
- `git_operation_in_progress`
- `upstream_configured`
- `upstream_divergence_available`

No commit/push approval decision is made.

## 13. Snapshot-candidate/matching-snapshot behavior

Milestone 006 performs a fresh deterministic scan in memory/external state, derives the current snapshot candidate using the existing Milestone 004 snapshot ID algorithm, and checks only for exact matching immutable snapshot existence.

If the matching snapshot directory exists, existing snapshot integrity verification is applied before reporting `matching_snapshot_exists = true`.

Status does not create a new snapshot.

## 14. Automated test results

Focused Milestone 006 tests:

- `PYTHONPATH=src python3 -m unittest tests.test_workflow_status -q`
- Result: `Ran 22 tests ... OK`

Full regression:

- `PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q`
- Result: `Ran 99 tests ... OK`

Python syntax validation was also performed earlier with `python3 -m compileall -q src`; repo cache churn created by that validation was cleaned afterward.

## 15. Controlled workflow-state validation

Disposable fixture coverage demonstrated at minimum:

- `clean`
- `staged_only`
- `unstaged_only`
- `staged_and_unstaged`
- `conflicted`

Direct Git evidence and Repo Control Plane status output agreed on counts and classification.

## 16. Local upstream divergence validation

Disposable local repositories plus a local bare remote verified:

- `equal`
- `ahead`
- `behind`
- `diverged`

These validations used only local refs and kept:

- `remote_refresh_performed = false`

inside production status output.

## 17. Vocab App validation

Target:

- `/home/chuck/ai-agent-tests/vocab-app`

Read-only validation sequence:

1. captured `git status --porcelain=v2 -z --untracked-files=all`
2. ran `repoctl milestone status --repository /home/chuck/ai-agent-tests/vocab-app`
3. captured exact porcelain-v2 status again

Result:

- `STATUS_MATCH=1`
- command exit `0`

Observed status facts:

- branch: `agent-test/gpt-oss-synonym-refactor`
- HEAD: `522a1e83e4de876330c018e6f771b77de3b5b011`
- workflow_state: `clean`
- staged/unstaged/untracked/unmerged: all `0`
- upstream configured: `false`
- current snapshot candidate: `snap--c14c64658c4b0066`
- matching snapshot exists: `true`
- matching snapshot id: `snap--c14c64658c4b0066`

## 18. Practical product-check result

Controlled fixture used:

- attached branch
- one staged file
- one additional unstaged modification on same path
- one untracked file
- upstream configured
- no conflict
- no operation in progress

Using only `status.json`, Repo Control Plane reported:

- `workflow_state = staged_and_unstaged`
- `branch_state = attached`
- `staged = 1`
- `unstaged = 1`
- `untracked = 1`
- `upstream_configured = true`
- `upstream_relation = equal`
- `matching_snapshot_exists = false`

This satisfies the product question: Repo Control Plane can tell the operator exactly what Git state exists before a future guarded Git-write milestone without making Git changes.

## 19. Deterministic-output validation

Repeated identical-state status runs were verified byte-identical for:

- `workflow/status.json`
- `workflow/status.md`

No timestamps, durations, random identifiers, or fetched network state are included.

## 20. Target before/after Git status

Validated for disposable fixtures and for Vocab App.

Most important live result:

- Vocab App porcelain-v2 status before/after matched exactly
- `STATUS_MATCH=1`

## 21. Limitations

- no Git fetch is performed
- upstream divergence reflects locally available refs only and may be stale versus the remote server
- no Git mutation is performed
- no commit or push approval decision is made
- status is a current-state projection, not historical workflow history

## 22. Milestone 007 opportunities without implementing them

Potential future guarded-write milestones could build on Milestone 006 facts for:

- policy-gated commit preparation
- explicit approval decisions derived from mutation preconditions
- guarded push readiness checks
- snapshot-required-before-write enforcement
- operator review workflows tied to exact snapshot identity

None of these were implemented in Milestone 006.

## 23. Final Repo Control Plane `git status --short`

At closeout, source changes are limited to Milestone 006 implementation/doc/test files:

- `M README.md`
- `M src/repoctl/cli.py`
- `M src/repoctl/scanner/core.py`
- `M src/repoctl/scanner/git_ops.py`
- `?? src/repoctl/workflow/`
- `?? tests/test_workflow_status.py`
- `?? docs/006_read_only_git_workflow_intelligence_closeout.md`
