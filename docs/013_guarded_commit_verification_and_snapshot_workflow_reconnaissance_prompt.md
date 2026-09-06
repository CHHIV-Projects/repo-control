# Repo Control Milestone 013

# Guarded Commit Verification and Snapshot Workflow Reconnaissance

**Prompt file:** `docs/013_guarded_commit_verification_and_snapshot_workflow_reconnaissance_prompt.md`
**Required closeout:** `docs/013_guarded_commit_verification_and_snapshot_workflow_reconnaissance_closeout.md`
**Mode:** Focused reconnaissance
**Reasoning:** High
**Repo Control implementation authority:** None
**Vocab implementation authority:** None
**Git mutation authority:** None except creation of the M013 closeout
**Runtime mutation authority:** None

---

# 1. Objective

Perform a focused reconnaissance of three closely related Repo Control workflow issues exposed by the real Vocab M002.1 testbed:

1. guarded Commit post-verification correctness;
2. matching-Snapshot orchestration inside Workflow;
3. Snapshot-to-Git-commit traceability.

Do not implement fixes in M013.

The purpose is to identify the exact failure mechanism and define the smallest coherent M014 implementation so Vocab development can resume quickly.

---

# 2. Controlling Real-World Evidence

The canonical Vocab repository is:

`/home/chuck/projects/vocab-app`

During Vocab M002.1, Repo Control successfully:

- prepared a guarded Stage plan;
- executed Stage;
- produced the intended staged state;
- required a matching immutable Snapshot before Commit preparation;
- prepared a guarded Commit plan;
- received Product Owner approval.

The approved Git commit then actually succeeded.

Direct Git evidence established:

- resulting HEAD:
  `9b7465deb41a9efa06fc32db7d0723a8c550f1ec`
- commit subject:
  `Close Vocab M002.1 Repo Control integration baseline`
- committed paths exactly:
  - `milestones/002.1_repo_control_integration_baseline_and_m002_evidence_comparison_closeout.md`
  - `milestones/002.1_repo_control_integration_baseline_and_m002_evidence_comparison_prompt.md`
- working tree clean;
- staging/index empty;
- commit diff passed `git diff ... --check`.

However, Repo Control reported a post-commit fingerprint/verification failure.

Afterward, the Workflow UI displayed the corresponding Commit plan as:

`Not executed`

even though Git HEAD had advanced and the approved commit clearly existed.

This is the primary correctness defect to diagnose.

Do not retry, amend, reset, revert, or otherwise alter the Vocab commit.

---

# 3. Additional Workflow Evidence

The same real workflow exposed a usability issue around Snapshots.

After Stage succeeded, `Prepare Commit` was attempted without a matching Snapshot.

Repo Control correctly blocked the operation because a matching immutable Snapshot was required.

The user then had to:

1. leave Workflow;
2. enter Snapshots;
3. create a Snapshot;
4. return to Workflow;
5. retry Prepare Commit.

The underlying safety rule is appropriate.

The workflow orchestration is unnecessarily indirect.

M013 must determine how Workflow can make this prerequisite explicit and actionable.

---

# 4. Snapshot / Git State Model

Preserve the following authority model:

`Git repository state`

is canonical truth.

A Repo Control Snapshot is:

`an immutable deterministic evidence record derived from a particular Git/source state`.

Snapshots may legitimately differ from current Git state because historical/intermediate snapshots are evidence of earlier states.

A matching Snapshot is required only where Repo Control claims or requires that the Snapshot represents the exact current state for a guarded operation.

For guarded Commit:

`current staged Git state`

must be represented by an exact matching immutable Snapshot before the Commit plan is prepared.

---

# 5. Snapshot Traceability Requirement

The Product Owner wants Snapshot history to distinguish clearly between:

- intermediate working/review snapshots;
- snapshots used as Commit evidence;
- snapshots ultimately aligned to a resulting Git commit.

Investigate a conceptual lifecycle such as:

`intermediate`

→ `commit_candidate`

→ successful guarded commit

→ `commit_aligned`

with the resulting Git commit SHA visibly associated.

However:

**do not mutate an existing immutable Snapshot artifact merely to change its label.**

M013 must determine the proper architecture for preserving Snapshot immutability while displaying commit alignment.

Possible designs include:

- a separate immutable Snapshot-to-Commit association artifact;
- execution metadata that references both Snapshot ID and resulting Git SHA;
- derived labels generated from authoritative execution/association evidence;
- another minimal generalized approach.

Do not select a design without inspecting current artifact architecture.

---

# 6. Starting-State Gate

Capture current Repo Control state:

    cd /home/chuck/projects/repo-control
    
    pwd
    git branch --show-current
    git rev-parse HEAD
    git status --short
    git remote -v
    git rev-parse @{upstream} 2>/dev/null || true
    git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null || true
    git log -8 --oneline --decorate

Known historical local items may include:

- modified `docs/008_guarded_staging_preparation_prompt.md`;
- modified `docs/009_browser_ui_foundation_and_read_only_console_prompt.md`;
- untracked `.venv/`.

Observe current reality.

Do not clean, restore, stage, commit, or alter pre-existing local state.

STOP if unexpected Repo Control source changes make evidence attribution unreliable.

---

# 7. Vocab Evidence Gate

Read-only inspect:

    cd /home/chuck/projects/vocab-app
    
    git branch --show-current
    git rev-parse HEAD
    git status --short
    git log -3 --oneline --decorate
    git show --stat --oneline 9b7465deb41a9efa06fc32db7d0723a8c550f1ec
    git diff-tree --no-commit-id --name-status -r 9b7465deb41a9efa06fc32db7d0723a8c550f1ec

Confirm the real commit remains intact.

Do not mutate Vocab.

If the SHA is no longer present in canonical Vocab history, STOP and report.

---

# 8. Reconstruct the Guarded Commit Execution Path

Trace the actual Repo Control implementation from:

`Commit Plan approval`

through:

`Git commit execution`

through:

`post-commit verification`

through:

`execution artifact publication`

through:

`Workflow history rendering`.

Identify exact:

- services/functions;
- state transitions;
- fingerprint inputs;
- expected pre-commit fingerprint;
- resulting commit inspection;
- post-commit verification rules;
- execution artifact creation;
- audit artifact creation;
- error handling;
- persistence ordering;
- UI/history interpretation.

Produce an explicit execution sequence.

---

# 9. Determine Why Post-Commit Verification Failed

Identify the exact technical reason the Vocab M002.1 commit failed post-verification.

Do not assume the commit was wrong.

Direct Git already establishes that the intended files were committed.

Investigate possible classes such as:

- fingerprint ordering;
- file-mode representation;
- line-ending normalization;
- staged-vs-committed blob identity;
- add/modify status representation;
- path ordering;
- index fingerprint vs resulting-tree fingerprint;
- prompt CRLF cleanup history;
- metadata included in one fingerprint but not the other;
- another implementation-specific cause.

Determine the actual cause from code/artifacts.

Do not patch it in M013.

---

# 10. Inspect Existing Special-State Design

Determine whether Repo Control already defines or intends states such as:

- `commit_succeeded`;
- `commit_succeeded_audit_failed`;
- `stage_succeeded_audit_failed`;
- equivalent mutation-succeeded/verifier-failed states.

Inspect:

- source;
- tests;
- milestone documents;
- architecture documentation;
- UI rendering logic.

Determine whether:

A. the special state exists but this path failed to use it;

B. the state exists conceptually but is incompletely implemented;

C. the state does not exist in implementation;

D. another state model is authoritative.

Do not invent a new state machine if an intended one already exists.

---

# 11. Mutation-Before-Audit Ordering

This is a critical safety question.

Once Git mutation succeeds:

Repo Control must never represent the operation as though it did not execute merely because later audit verification failed.

Evaluate the required invariant:

> After a Git mutation succeeds, execution evidence must preserve that fact before or regardless of subsequent verification success.

Investigate whether current ordering is effectively:

    mutate Git
    -> verify
    -> publish execution

and whether it should instead become something like:

    mutate Git
    -> immediately persist mutation-success evidence
    -> perform post-verification
    -> enrich/finalize outcome

or another safer atomic ordering.

The exact implementation recommendation must come from evidence.

---

# 12. Retry / Recovery Semantics

Define the correct operator behavior for:

`commit succeeded but audit failed`.

The expected safety principle is:

- preserve the resulting commit;
- do not automatically retry;
- do not automatically reset/revert;
- make resulting HEAD explicit;
- require human inspection;
- preserve the verification failure;
- make the UI unmistakably different from `Not executed`.

Determine how current code supports or violates this principle.

---

# 13. Workflow UI Correctness

Inspect how Workflow decides to render:

- Not executed;
- Executed;
- Failed;
- incompatible;
- current workflow state;
- resulting HEAD.

Determine why the real Vocab execution appeared as `Not executed`.

Recommend the smallest UI/state correction so the operator sees something equivalent to:

`Commit mutation succeeded — post-verification failed`

with:

- starting HEAD;
- resulting HEAD;
- Commit Plan ID;
- execution ID;
- Snapshot ID;
- verification status;
- explicit warning not to retry.

Do not implement in M013.

---

# 14. Matching Snapshot Workflow Orchestration

Inspect current Prepare Commit prerequisite handling.

Determine:

- where matching-Snapshot eligibility is checked;
- how exact matching is established;
- why the operator only learns of the missing Snapshot after attempting Prepare Commit;
- whether Workflow already has enough information to expose the prerequisite before the attempt.

Recommend a Workflow experience such as:

    Current staged state
        ↓
    Matching Snapshot check
    
    if exact match exists:
        display Snapshot ID
        enable Prepare Commit
    
    if no exact match:
        display "Matching Snapshot required"
        offer [Create Matching Snapshot]
        disable or gate Prepare Commit

After Snapshot creation:

- re-read Git state;
- create immutable Snapshot;
- verify exact match;
- expose Snapshot ID;
- enable Prepare Commit.

Do not silently create the Snapshot without operator visibility.

---

# 15. Workflow vs Snapshot Tab Responsibility

Evaluate this product boundary:

## Workflow

Orchestrates prerequisites and guarded mutation lifecycle.

Examples:

- Git state;
- Stage;
- matching Snapshot requirement;
- Commit;
- post-verification.

## Snapshots

Provides detailed inspection/history/browsing of Snapshot artifacts.

A user performing a Commit should not need to navigate away from Workflow merely to satisfy a required workflow prerequisite.

Determine whether this can be implemented by reusing the existing Snapshot service rather than creating a Workflow-specific Snapshot implementation.

There must remain one authoritative Snapshot creation path.

---

# 16. Snapshot Classification / Labels

Determine how the UI should identify Snapshot roles.

Desired operator-visible categories include:

- `Intermediate`
- `Commit candidate`
- `Commit aligned`

Potential additional status where appropriate:

- `Commit attempted / audit failed`

Do not make labels imply facts that have not occurred.

Before Commit:

a matching staged Snapshot may be displayed as:

`Commit candidate`

After a verified successful Commit:

it may be displayed as:

`Commit aligned`
`Commit SHA: <sha>`

After mutation succeeds but audit fails:

the UI must truthfully show both facts rather than falsely promoting the Snapshot to fully verified alignment.

---

# 17. Preserve Snapshot Immutability

A Snapshot must remain immutable.

Investigate how commit alignment can be represented without editing historical Snapshot contents.

Preferred architectural direction is likely:

`Snapshot artifact`

plus:

`separate immutable relationship/execution evidence`

from which UI labels are derived.

But verify current artifact architecture before recommending the exact design.

Do not introduce mutable tags on immutable evidence unless existing architecture explicitly supports safe annotations.

---

# 18. Snapshot Browsing / Filtering

Determine the smallest useful UI support for traceability.

Potential filters:

- All;
- Commit aligned;
- Intermediate;
- Commit candidates / unresolved;
- Audit failed.

Do not build a broad Snapshot management redesign.

The objective is to make it easy to answer:

> Which snapshots correspond to Git commit boundaries?

and:

> Which snapshots were merely intermediate checkpoints?

---

# 19. Git / Snapshot Alignment Display

Recommend whether Workflow and/or Snapshot detail should explicitly show:

- Snapshot ID;
- Snapshot HEAD;
- current Git HEAD;
- staged-state fingerprint;
- match status;
- associated Commit SHA;
- alignment type.

Prefer a simple operator-readable status such as:

`Exact current match`

`Historical / not current`

`Commit aligned`

`Commit mutation succeeded / audit failed`

rather than requiring interpretation of raw fingerprints.

---

# 20. Existing Tests

Inspect existing guarded Commit, Snapshot, Workflow, and browser tests.

Map coverage for:

- matching Snapshot requirement;
- successful guarded Commit;
- post-commit verification;
- verification failure after Git mutation;
- execution artifact persistence;
- resulting HEAD;
- retry prevention;
- Workflow history rendering;
- Snapshot immutability;
- Snapshot creation;
- Snapshot reuse;
- Snapshot/Git-state matching.

Identify exact missing tests.

Do not add tests in M013.

---

# 21. Required Future Regression Fixture

Define a native Repo Control fixture reproducing the real defect without relying on Vocab.

The future implementation test must prove:

1. stage approved files;
2. create matching Snapshot;
3. prepare Commit;
4. execute Git commit;
5. simulate or trigger post-verification failure;
6. confirm HEAD advanced;
7. confirm execution artifact says mutation succeeded;
8. confirm UI/history does not say `Not executed`;
9. confirm retry is blocked or clearly unsafe;
10. confirm no automatic rollback occurred.

Also define a successful control case.

---

# 22. Vocab as Read-Only Historical Reproduction

Use Vocab only as read-only evidence.

Do not create another Vocab commit to test M013.

The future M014 fix should first be proven with Repo Control-native fixtures.

Vocab M003 will become the next real end-to-end test after M014 passes.

---

# 23. Scope Decision for M014

Conclude whether M014 should implement all three related improvements together:

A. post-commit verification/state correctness;

B. matching-Snapshot Workflow orchestration;

C. Snapshot commit-alignment traceability;

or whether safety requires splitting them.

Prefer one bounded M014 if they share the same workflow/artifact surfaces and can be implemented coherently without broadening scope.

Do not split merely for ceremony.

Do split if one change requires materially different architecture or risk.

---

# 24. Required Closeout

Create exactly:

`docs/013_guarded_commit_verification_and_snapshot_workflow_reconnaissance_closeout.md`

Include:

## 1. Executive conclusion

Root cause and recommended M014 scope.

## 2. Starting Repo Control state

Exact Git evidence.

## 3. Vocab historical evidence

Confirm commit SHA and exact committed paths.

## 4. Guarded Commit execution flow

Plan approval through UI history.

## 5. Exact post-verification failure cause

Evidence-based diagnosis.

## 6. Fingerprint model

What was compared and why it differed.

## 7. Mutation/audit ordering

Current ordering and recommended invariant.

## 8. Special-state architecture

Existing or missing `commit_succeeded_audit_failed` equivalent.

## 9. Execution artifact persistence

Why Workflow displayed `Not executed`.

## 10. Correct recovery semantics

No retry/reset/revert behavior.

## 11. Workflow rendering findings

Required operator-visible state.

## 12. Matching Snapshot prerequisite

Current behavior.

## 13. Proposed Workflow Snapshot orchestration

Exact intended flow.

## 14. Snapshot creation service reuse

How one authoritative path is preserved.

## 15. Snapshot classification model

Intermediate / candidate / aligned / audit-failed semantics.

## 16. Snapshot immutability model

How labels/associations are derived without mutating Snapshot artifacts.

## 17. Snapshot filtering / browsing recommendation

Smallest useful UI change.

## 18. Git/Snapshot alignment presentation

What the user should see.

## 19. Existing test coverage

Exact mapped tests.

## 20. Missing regression coverage

Tests required for M014.

## 21. Native failure fixture

How to reproduce mutation-succeeded/audit-failed safely.

## 22. Vocab role

Read-only historical evidence and next future end-to-end test.

## 23. Recommended M014 scope

One milestone or justified split.

## 24. Explicit non-goals

No semantic Context work, deployment work, Vocab implementation, or unrelated UI redesign.

## 25. Final Repo Control state

Capture:

    cd /home/chuck/projects/repo-control
    
    git branch --show-current
    git rev-parse HEAD
    git status --short
    git rev-parse @{upstream} 2>/dev/null || true
    git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null || true

---

# 25. Stop Conditions

STOP and report if:

- Vocab historical evidence contradicts the recorded successful commit;
- the failure cannot be reproduced or traced from existing Repo Control artifacts/code;
- fixing the issue would require redesigning unrelated Git mutation authorities;
- Snapshot immutability would need to be weakened;
- Workflow would require a second independent Snapshot implementation;
- the implementation direction requires automatic retry/reset/revert;
- unrelated Repo Control source changes make attribution unreliable.

Do not implement during M013.

---

# 26. Expected Outcome

M013 must answer:

1. Why did the real Vocab commit succeed while Repo Control post-verification failed?
2. Why did Workflow later say `Not executed`?
3. What state should Repo Control preserve when Git mutation succeeds but audit fails?
4. At what point must mutation-success evidence be persisted?
5. How should retry/recovery behave?
6. How can Workflow show the matching-Snapshot prerequisite before Prepare Commit?
7. How can the user create the required matching Snapshot without leaving Workflow?
8. How can Snapshot history distinguish intermediate from commit-aligned evidence?
9. How can that traceability be implemented without mutating immutable Snapshot artifacts?
10. Can all three fixes be implemented safely in one bounded M014?
11. What exact native tests prove the fix before returning to Vocab?

---

# 27. Working Principle

> Git is canonical truth. Repo Control must never lose or misrepresent a Git mutation that already happened.

And:

> Required evidence artifacts should be orchestrated by Workflow, while dedicated artifact pages remain available for inspection and history.

And:

> Snapshot traceability must improve without compromising Snapshot immutability.

Complete this reconnaissance quickly and narrowly so the resulting M014 implementation can be validated and Vocab M003 can resume.

---

**End of `013_guarded_commit_verification_and_snapshot_workflow_reconnaissance_prompt.md`**
