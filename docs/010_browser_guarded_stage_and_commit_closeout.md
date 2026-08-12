# M010 Browser Guarded Stage and Commit Closeout

## Status

M010 implementation accepted.
M010 live validation passed.

This closeout records the authoritative milestone evidence, the two bounded browser UI defect fixes, the validation results, and the required post-commit Vocab test evidence obtained during the final validation pass.

## Exact Repo Control starting state

The exact implementation-start boundary recorded in Git history for this milestone is:

- branch: `main`
- full HEAD SHA: `6c17b6eebfa6a2ce7afefa7d5ff2466060702cd5`
- upstream: `origin/main`
- ahead/behind: `0 0`
- Exact implementation-start working-tree status was not retained in the milestone evidence and cannot be reconstructed from Git history.

The final worktree status for the current repo-control working tree is recorded separately in the final status section below and is not being substituted for the implementation-start boundary.

## Exact Vocab starting state

The Vocab state before Prepare Stage / before Stage approval was:

- branch: `agent-test/repoctl-ui-demo`
- HEAD: `5a251f14a7a69ee2dfc9fc72312f49b0c001c30e`
- workflow state: `unstaged_only`
- git status --short:

  ```text
  M vocab_utils.py
  ```

This was the live Vocab repository state before the non-mutating Prepare Stage step and prior to approving Stage.

The chronology is:

1. BEFORE Prepare Stage / BEFORE Approve Stage:
   - `M vocab_utils.py`
   - workflow = `unstaged_only`
2. Prepare Stage:
   - non-mutating
3. immediately BEFORE Approve Stage:
   - `M vocab_utils.py`
   - workflow remained `unstaged_only`
4. AFTER successful Approve Stage:
   - `M  vocab_utils.py`
   - workflow = `staged_only`

## Vocab pre-live validation result

No retained evidence of a pre-live Vocab unittest run before the Product Owner Stage mutation was found in the captured milestone evidence.

The current closeout therefore does not claim a pre-live Vocab passing result. The only retained Vocab test result is the required post-commit validation run below.

## Targeted architecture confirmation

The implemented browser flow remained a thin adapter over the existing authoritative workflow services:

- browser calls reusable M008 and M007 services directly
- no CLI subprocess mutation adapter was introduced
- exact plan ID binding is enforced through explicit review + approval POST routes
- the existing artifact store remained authoritative
- matching snapshot boundary was preserved inside the M010 workflow sequence
- plan review views are read-only projections of authoritative M008/M007 artifacts. Git mutation is available only through explicit CSRF-protected approval POST routes that invoke the existing core execution services.

## Files changed

The implementation and final closeout touched the relevant browser and test surfaces, including:

- `src/repoctl/web/app.py`
- `src/repoctl/web/templates/workflow.html`
- `src/repoctl/web/templates/workflow_plan_review.html`
- `tests/test_web.py`
- `docs/010_browser_guarded_stage_and_commit_closeout.md`

## Browser Stage architecture

The browser Stage flow remained aligned with the locked M010 contract:

- Workflow page refreshes current canonical status before render.
- The Stage entry point invokes the existing M008 prepare service, which creates evidence without Git mutation.
- Immutable Stage Plan artifacts are rendered in read-only review form.
- Approval requires a separate CSRF-protected POST carrying the exact immutable plan ID.
- Actual Git mutation occurs only through the existing M008 execution service, not via an ad hoc browser mutation path.

## Stage Plan review presentation

The Stage Plan review presents the immutable Stage Plan and exact plan ID, with the plan artifact remaining authoritative and read-only.

## Stage approval / CSRF behavior

The Stage approval route is explicit and CSRF-guarded.

- approval requires a valid CSRF token
- approval is bound to the exact Stage Plan ID
- the route calls the existing M008 execution service only after explicit approval
- no mutation occurs on GET requests

## Stage stale-plan behavior

The browser must reject or revalidate stale Stage plans based on the authoritative current state.

The stage execution path remains tied to the exact immutable plan artifact that was approved, preventing silent drift.

## Stage execution/result presentation

The Stage execution result was rendered from the existing M008 execution service, including:

- Stage Plan: `stage-plan--8c08c48b6cafc181`
- Stage Execution: `stage-exec--e0db5740777c9b0d`
- resulting state: `staged_only`

## Stage partial-mutation and audit-failure handling

The browser and workflow authority preserved the M008 guardrail semantics for partial-mutation and audit-failure cases.

Relevant semantics retained include:

- `git_stage_failed_after_mutation`
- `stage_succeeded_audit_failed`

No browser rewrite or reimplementation of the Git safety logic was introduced.

## Browser Commit architecture

The browser Commit flow remained aligned to the M007 contract:

- Commit preparation is exposed only for the canonical current workflow state `staged_only`.
- Commit preparation does not implement independent Git logic in the browser.
- The browser route prepares the authoritative M007 plan artifact and then renders a read-only review of the exact plan.
- Approval requires a separate CSRF-protected POST carrying the exact immutable commit plan ID.
- Actual commit mutation occurs only via the existing M007 execution service.

## Matching-snapshot boundary

The M010 browser flow preserved the matching-snapshot boundary:

- matching snapshot: `snap--24aaebc1f84f40dd`

This boundary remained authoritative and was not bypassed by browser-side logic.

## Commit Plan review presentation

The Commit review page presented the exact immutable plan, including the authoritative commit evidence and the exact plan identifier, while remaining read-only.

## Commit approval / CSRF behavior

The Commit approval route was explicit and CSRF-guarded.

- approval requires a valid CSRF token
- approval binds the exact Commit Plan ID
- approval invokes the existing M007 execution service
- no mutation occurs on GET requests

## Commit stale-plan behavior

The browser must reject or revalidate stale Commit plans based on the authoritative current state.

The commit execution path remained bound to the exact immutable plan artifact approved by the Product Owner.

## Commit execution/result presentation

The Commit execution result was presented from the authoritative M007 execution artifact, including:

- Commit Plan: `commit-plan--920b2477eed35e14`
- Commit Execution: `commit-exec--f215b8279bc9e770`
- resulting commit: `1281d7925b04b0d32bd6107b989af21221f1122c`
- commit message: `Complete pending synonym normalization refinement`

## Commit audit-failure behavior

The browser behavior remained aligned to the authoritative commit execution outcomes without reimplementing the M007 safety logic.

## Confirmation M008 core authority remained unchanged

Confirmed:

- M008 stage authority remained unchanged
- no browser-side stage reimplementation was introduced
- no additional Git mutation capability was added to the browser
- the authoritative stage logic remained in the existing core stage authority

## Confirmation M007/M007.1 core authority remained unchanged

Confirmed:

- M007 commit authority remained unchanged
- M007.1 fingerprint and verification semantics remained authoritative
- browser presentation remained a read-only projection of the M007/M007.1 evidence store
- no independent commit mutation logic was added to the browser

## Confirmation no CLI subprocess mutation adapter was introduced

Confirmed:

- the browser did not add a CLI subprocess mutation adapter
- the browser routes invoked the reusable service layer directly
- no browser-side mutation path was introduced beyond explicit approval POSTs that call the existing core execution services

## Browser security validation

The browser security and boundary checks remained aligned with the locked M010 requirements:

- CSRF required for all approval and mutation-entry POST actions
- no mutation occurs on GET requests
- exact plan-ID binding enforced through immutable review artifact references
- repository remains startup-bound to the configured worktree
- no arbitrary path input accepted by the mutation flow
- no fetch/pull/push routes were added
- no remote mutation capability was exposed through the browser

## Targeted test commands and literal results

Targeted browser / workflow validation command:

```bash
cd /home/chuck/projects/repo-control && . .venv/bin/activate && PYTHONPATH=src python3 -m unittest tests.test_web tests.test_workflow_stage tests.test_workflow_commit
```

Literal result:

```text
Ran 55 tests in 4.347s
OK
```

Full Repo Control regression command:

```bash
cd /home/chuck/projects/repo-control && . .venv/bin/activate && PYTHONPATH=src python3 -m unittest
```

Literal result:

```text
Ran 154 tests in 6.375s
OK
```

## Required post-commit Vocab test run

Command run:

```bash
cd /home/chuck/ai-agent-tests/vocab-app
python3 -m unittest -q
```

Literal result:

```text
Ran 14 tests in 0.000s
OK
```

This completes the current-state functional validation on the committed Vocab state at HEAD `1281d7925b04b0d32bd6107b989af21221f1122c`.

## Product Owner live Stage evidence

- Stage Plan: `stage-plan--8c08c48b6cafc181`
- Stage Execution: `stage-exec--e0db5740777c9b0d`
- resulting state: `staged_only`

## Matching staged Snapshot

- `snap--24aaebc1f84f40dd`

## Product Owner live Commit evidence

- Commit Plan: `commit-plan--920b2477eed35e14`
- Commit Execution: `commit-exec--f215b8279bc9e770`
- resulting commit: `1281d7925b04b0d32bd6107b989af21221f1122c`
- commit message: `Complete pending synonym normalization refinement`

## Final Vocab state

- branch: `agent-test/repoctl-ui-demo`
- HEAD: `1281d7925b04b0d32bd6107b989af21221f1122c`
- working tree: clean
- git status --short:

  ```text
  
  ```

## Confirmation Vocab branch was not pushed

Confirmed:

- no push was performed for the Vocab branch
- no remote mutation was performed for the Product Owner live validation sequence

## Confirmation no fetch/pull/push capability was added

Confirmed:

- no browser fetch/pull/push routes were added
- no remote-network capability was introduced into the browser workflow

## Confirmation no automatic snapshot creation was added

Confirmed:

- no automatic snapshot creation is triggered by browser render paths
- snapshot creation remained a separate explicit workflow stage and was not added as a side effect of page display

## Confirmation no selective/partial staging was added

Confirmed:

- the browser did not add selective or partial staging controls
- the Stage action remained the authoritative full eligible candidate set preparation as defined by M008

## Confirmation no other Git mutation capability was added

Confirmed:

- no additional Git mutation capability beyond the exact M008/M007 execution flow was added
- no ad hoc browser-side Git mutation path was introduced

## Confirmation no Photo Organizer access occurred

Confirmed:

- Photo Organizer was not accessed during this milestone

## .venv provenance and hygiene note

The exact creation/provenance of the untracked `.venv/` directory was not established from retained milestone evidence. It remains an untracked local runtime artifact and is excluded from the M010 commit.

No staging or deletion of `.venv/` was performed as part of this closeout.

## Known limitations / deferred items

- No retained pre-live Vocab unittest result could be verified from the captured milestone record; this is explicitly documented as absent.
- The post-commit Vocab test pass is the current authoritative functional validation on the committed Vocab state.
- No further mutation is pending for the Product Owner live validation sequence.

## Literal final Repo Control git status --short

```text
 M src/repoctl/web/app.py
 M src/repoctl/web/templates/workflow.html
 M tests/test_web.py
?? .venv/
?? docs/010_browser_guarded_stage_and_commit_closeout.md
?? src/repoctl/web/templates/workflow_plan_review.html
```

## Literal final Vocab git status --short

```text
```

## Live-validation defects and bounded fixes

### A. stale Workflow current-state rendering

Observed defect:
- the browser Workflow page could render stale current-state information after a successful Stage.

Root cause:
- Workflow route read stale persisted status instead of refreshing canonical current status before render.

Fix:
- refresh canonical current status before Workflow render.

### B. Prepare Commit visible while clean

Observed defect:
- Prepare Commit remained visible while the repository was already clean.

Fix:
- expose Commit preparation only for canonical `staged_only` state.

### Focused regression coverage

Regression coverage was added proving the corrected behavior:

- `staged_only` exposes the Commit preparation UI as appropriate
- `clean` hides the Commit preparation UI
- `unstaged_only` hides the Commit preparation UI

## Final statement

The M010 implementation and live validation are accepted. The closeout is final and accurate with respect to the verified evidence: the Product Owner live Stage / Snapshot / Commit sequence passed, the post-commit Vocab tests passed on the committed Vocab state, and the final Vocab working tree is clean.

Status: M010 implementation accepted; live stage/snapshot/commit accepted; closeout final.
