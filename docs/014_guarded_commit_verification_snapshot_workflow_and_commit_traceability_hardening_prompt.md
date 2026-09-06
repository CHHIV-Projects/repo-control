# Repo Control Milestone 014

# Guarded Commit Verification, Snapshot Workflow, and Commit Traceability Hardening

**Prompt file:** `docs/014_guarded_commit_verification_snapshot_workflow_and_commit_traceability_hardening_prompt.md`
**Required closeout:** `docs/014_guarded_commit_verification_snapshot_workflow_and_commit_traceability_hardening_closeout.md`
**Mode:** Bounded implementation
**Reasoning:** High
**Target repository:** `/home/chuck/projects/repo-control`

---

# 1. Objective

Implement the smallest safe set of changes required by the accepted M013 reconnaissance so Repo Control can:

1. correctly verify recursive committed file deltas after a guarded Commit;
2. durably preserve the fact that a Git commit succeeded before later verification/audit can fail;
3. truthfully render mutation-succeeded/audit-failed Commit outcomes;
4. expose the matching-Snapshot prerequisite directly in Workflow;
5. allow explicit creation of the required matching Snapshot from Workflow using the existing authoritative Snapshot service;
6. derive Snapshot-to-Commit traceability without mutating immutable Snapshot artifacts.

After M014 passes, Repo Control should be ready to return to the Vocab App as the next real end-to-end testbed.

Do not broaden this milestone into unrelated Repo Control work.

---

# 2. Controlling Evidence

Treat the accepted M013 closeout as controlling evidence:

`docs/013_guarded_commit_verification_and_snapshot_workflow_reconnaissance_closeout.md`

M013 established the exact guarded Commit defect.

Commit preparation fingerprints recursive staged file records.

Post-commit verification currently invokes:

    git diff-tree --raw --no-renames --abbrev=40 --no-commit-id -z <before_head> <after_head>

without `-r`.

For the real Vocab M002.1 Commit, Git therefore returned a top-level `milestones` directory record rather than the two committed files.

Using recursive traversal produces the exact expected staged-delta fingerprint.

M013 also established that Commit execution currently follows:

    Git mutation
    -> resulting HEAD
    -> post-commit verification
    -> execution artifact creation/publication

Therefore a post-verification exception can occur after Git mutation but before durable execution evidence exists.

That caused the real Vocab Commit to succeed while Workflow later displayed:

`Not executed`

M014 must correct both defects.

---

# 3. Core Safety Invariants

Preserve these invariants.

## 3.1 Git authority

Git repository state remains canonical truth.

Repo Control evidence must accurately describe Git state and must never contradict a Git mutation that already occurred.

## 3.2 Mutation success must survive later audit failure

Once `git commit` succeeds and resulting HEAD is known:

> Repo Control must durably preserve that mutation-success fact before any later verification or audit can erase, obscure, or misrepresent it.

A later audit failure may change the final outcome classification.

It must not change the historical fact that the Commit occurred.

## 3.3 No automatic recovery mutation

For:

`Commit mutation succeeded / audit failed`

Repo Control must not automatically:

- retry the Commit;
- reset;
- restore;
- revert;
- amend;
- create a replacement Commit.

The operator must inspect the resulting state.

## 3.4 Snapshot immutability

Existing Snapshot artifacts remain immutable.

Do not rewrite Snapshot JSON merely to add Commit labels or relationships.

## 3.5 One Snapshot authority

Workflow must reuse the existing Snapshot creation/matching services.

Do not implement a second Workflow-specific Snapshot engine.

---

# 4. Starting-State Gate

Before implementation:

    cd /home/chuck/projects/repo-control
    
    pwd
    git branch --show-current
    git rev-parse HEAD
    git status --short
    git remote -v
    git rev-parse @{upstream} 2>/dev/null || true
    git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null || true
    git log -6 --oneline --decorate

Confirm the M013 prompt and closeout are committed.

Known historical local state may include:

    M docs/008_guarded_staging_preparation_prompt.md
    M docs/009_browser_ui_foundation_and_read_only_console_prompt.md
    ?? .venv/

Observe current reality.

Do not alter those pre-existing items.

STOP if unexpected source changes make M014 attribution unreliable.

---

# 5. Implementation Discipline

This is an implementation milestone, not another broad reconnaissance.

Use M013 findings as the roadmap.

Inspect only the implementation surfaces necessary to make the named changes safely.

Likely relevant areas include:

- `src/repoctl/workflow/commit_execution.py`
- `src/repoctl/workflow/commit_plan.py`
- Workflow artifact/state helpers
- `src/repoctl/web/views.py`
- Workflow templates
- Snapshot manager/service
- Snapshot browser/detail projection
- existing artifact serialization helpers
- `tests/test_workflow*.py`
- `tests/test_web.py`
- Snapshot tests

Do not perform broad repository spelunking unless a named dependency requires it.

Implement the smallest safe change.

If current architecture contradicts M013 in a material way, STOP and report.

---

# 6. Fix Recursive Post-Commit Verification

Correct post-commit delta inspection so committed records are recursively equivalent to the records fingerprinted during Commit preparation.

The canonical Vocab-shaped failure must be fixed.

At minimum, the resulting behavior must correctly handle:

- files in nested directories;
- multiple committed files;
- add + modify combinations;
- deterministic path ordering;
- modes;
- object IDs;
- status;
- staged-delta fingerprint equality.

The expected conceptual correction is recursive `git diff-tree` traversal.

Do not weaken fingerprint verification merely to make the test pass.

Do not replace exact file-level comparison with directory-level comparison.

---

# 7. Preserve Mutation Success Before Audit

Refactor Commit execution ordering so successful Git mutation becomes durable evidence before later post-commit verification can fail.

Required conceptual lifecycle:

    validate approved pre-commit state
    -> invoke git commit
    -> read resulting HEAD
    -> persist immutable mutation-success evidence
    -> perform post-commit verification
    -> persist/derive verified or audit-failed outcome

Use the smallest additive design compatible with existing artifact architecture.

Possible implementations include:

- an immutable mutation/execution evidence artifact followed by immutable verification/outcome evidence;
- an existing execution artifact safely published at the mutation-success boundary plus separate final audit evidence;
- another existing generalized pattern already present in Repo Control.

Do not create a mutable half-written artifact unless the current architecture explicitly establishes that as safe.

Do not invent a second unrelated workflow state machine if existing `commit_succeeded_audit_failed` semantics can be reused or refined.

---

# 8. Successful Commit Outcome

For a normal verified Commit, preserve current expected behavior.

The final evidence must identify:

- Commit Plan ID;
- starting HEAD;
- resulting Commit SHA;
- matching Snapshot ID;
- committed scope/fingerprint;
- successful verification state.

Workflow must show the Commit as successfully executed.

Snapshot traceability must derive:

`Commit aligned`

for the Snapshot associated with that verified Commit.

---

# 9. Post-Verification Failure Outcome

Create explicit durable behavior for:

`Commit mutation succeeded / post-verification failed`

Required facts:

- Git Commit happened;
- resulting SHA is known;
- mutation evidence exists;
- verification failure remains visible;
- operator is warned not to retry automatically;
- Workflow must not display `Not executed`.

The operator-visible state should clearly communicate:

`Commit mutation succeeded — post-verification failed`

Show where available:

- Commit Plan ID;
- mutation/execution evidence ID;
- starting HEAD;
- resulting HEAD;
- matching Snapshot ID;
- verification status;
- concise failure reason;
- no-retry warning.

Do not classify this as `Commit aligned`.

---

# 10. Existing `commit_succeeded_audit_failed` Semantics

M013 found existing concepts:

- `stage_succeeded_audit_failed`
- `commit_succeeded_audit_failed`
- `post_commit_verification_failed`

Map the implementation carefully.

Prefer to unify operator-visible mutation-succeeded/audit-failed behavior where appropriate while retaining enough detail to distinguish:

- post-commit verification failure;
- artifact/audit publication failure.

Do not collapse useful diagnostic distinctions.

The important common truth is:

`Git mutation succeeded`.

---

# 11. Retry Safety

After any Commit mutation-success/audit-failed outcome:

- do not expose an ordinary “Approve Commit” retry path as though nothing happened;
- do not silently create another Commit;
- do not reset/revert;
- make resulting HEAD visible;
- require operator inspection before subsequent guarded mutation.

Implement the smallest safe guard or unmistakable UI state required by the current architecture.

Do not build a generalized recovery subsystem.

---

# 12. Workflow Matching-Snapshot Readiness

Before the operator attempts `Prepare Commit`, Workflow should determine whether the current staged Git state has an exact matching immutable Snapshot.

Display concise readiness.

If a matching Snapshot exists:

    Matching Snapshot available
    Snapshot: <snapshot_id>

and allow Commit preparation subject to all other existing gates.

If no exact matching Snapshot exists:

    Matching Snapshot required

and gate Commit preparation.

The user should not first discover this prerequisite through a failed Prepare Commit attempt.

---

# 13. Create Matching Snapshot from Workflow

When the current staged state lacks a matching Snapshot, provide an explicit operator action:

`Create Matching Snapshot`

This action must reuse the authoritative Snapshot service:

`repoctl.snapshot.manager.create_snapshot`

or its established public service boundary.

Required behavior:

    operator explicitly requests Snapshot
    -> re-read current Git state
    -> create/reuse immutable Snapshot through existing service
    -> verify resulting current Snapshot match
    -> return to/update Workflow
    -> show Snapshot ID
    -> enable Commit preparation if other gates pass

Do not create a Snapshot merely by rendering Workflow.

Do not silently create one as a hidden side effect of Prepare Commit.

Do not duplicate Snapshot serialization, ID derivation, hashing, publication, or integrity validation.

---

# 14. Workflow / Snapshot Page Product Boundary

Preserve this product model.

## Workflow

Workflow orchestrates required guarded-operation prerequisites:

- current Git state;
- staging state;
- matching Snapshot readiness;
- Stage/Commit plans;
- mutation execution;
- verification/audit outcome;
- concise traceability.

## Snapshots

Snapshots remains the detailed evidence/history surface:

- Snapshot browsing;
- Snapshot detail;
- historical/intermediate checkpoints;
- derived Commit relationship/status.

A user performing a Commit should not need to leave Workflow merely to satisfy the required matching-Snapshot prerequisite.

---

# 15. Snapshot Classification

Implement derived Snapshot classifications using immutable evidence.

Required semantics:

## Intermediate

Historical Snapshot not tied to a current Commit Plan.

## Matching Snapshot available

Snapshot exactly represents current staged Git state, but no current Commit Plan necessarily references it.

## Commit candidate

Snapshot is explicitly referenced by a prepared/current Commit Plan.

Do not classify every exact matching Snapshot as Commit candidate.

## Commit aligned

A successful verified Commit is associated with the Snapshot and resulting Git SHA.

## Commit mutation succeeded / audit failed

Git Commit occurred and resulting SHA is known, but post-commit verification or audit failed.

Do not promote this state to Commit aligned.

---

# 16. Snapshot-to-Commit Association

Do not mutate the Snapshot artifact.

Use existing immutable execution evidence where sufficient.

If existing execution evidence cannot safely represent the relationship, add the smallest immutable association/outcome artifact required.

The derived relationship should make available, as applicable:

- Snapshot ID;
- Commit Plan ID;
- mutation/execution evidence ID;
- starting HEAD;
- resulting Commit SHA;
- association/outcome type;
- verification state.

Avoid redundant artifacts if the same authoritative facts already exist in an immutable execution artifact.

---

# 17. Snapshot Browsing / Filtering

Add the smallest useful traceability presentation necessary to distinguish Commit-boundary Snapshots from intermediary Snapshots.

Preferred derived categories:

- All
- Matching Snapshot available
- Commit candidate
- Commit aligned
- Commit mutation succeeded / audit failed
- Intermediate / unresolved

Do not redesign the entire Snapshots UI.

The operator should be able to answer quickly:

> Which Snapshots correspond to successful Git Commit boundaries?

and:

> Which Snapshots were only intermediate checkpoints?

---

# 18. Operator-Readable Alignment Facts

Where useful in Workflow and Snapshot detail/history, expose concise facts such as:

- Snapshot ID;
- Snapshot HEAD;
- current Git HEAD;
- exact-current-match state;
- Commit Plan ID;
- resulting Commit SHA;
- alignment classification;
- verification/audit status.

Prefer human-readable states such as:

- `Exact current match`
- `Historical / not current`
- `Matching Snapshot available`
- `Commit candidate`
- `Commit aligned`
- `Commit mutation succeeded / audit failed`

Raw fingerprints may remain available as evidence, but should not be required for ordinary operator interpretation.

---

# 19. Required Native Regression Tests

Add focused tests proving the M013 failures are corrected.

At minimum cover:

1. recursive post-commit diff verification for nested paths;
2. Vocab-shaped multi-file add/modify commit fingerprint equality;
3. successful Commit still produces correct execution evidence;
4. mutation-success evidence persists when post-verification fails;
5. resulting HEAD is preserved after verification failure;
6. Workflow does not render `Not executed` after Git mutation;
7. Workflow shows explicit mutation-succeeded/audit-failed state;
8. no automatic retry/reset/restore/revert occurs;
9. retry path is blocked or unmistakably unsafe after mutation success;
10. matching-Snapshot readiness is visible before Prepare Commit;
11. missing matching Snapshot gates Commit preparation;
12. explicit Workflow Snapshot creation uses the existing Snapshot authority;
13. Snapshot creation/reuse remains deterministic;
14. merely matching Snapshot != Commit candidate;
15. prepared/current Commit Plan can derive Commit candidate;
16. verified Commit derives Commit aligned;
17. audit-failed Commit does not derive Commit aligned;
18. Snapshot artifact bytes remain unchanged after Commit association evidence exists.

Use temporary native Git repositories.

Do not use the canonical Vocab repository as the mutation fixture.

---

# 20. Required Mutation-Succeeded / Audit-Failed Fixture

Create a native test case reproducing the important safety boundary.

Conceptually:

    create temporary Git repository
    -> create nested tracked path(s)
    -> modify/add approved files
    -> stage exact files
    -> create matching Snapshot
    -> prepare Commit Plan
    -> execute Commit
    -> force controlled post-verification failure
    -> assert HEAD advanced
    -> assert Commit exists
    -> assert durable mutation-success evidence exists
    -> assert audit failure remains explicit
    -> assert Workflow does not say Not executed
    -> assert no automatic rollback/retry
    -> assert Snapshot bytes unchanged

Also retain a successful control case using the recursive verification path.

---

# 21. Existing Regression Suite

Run focused affected tests first.

Then run the full Repo Control test suite.

Also run:

    python -m compileall src tests

or the repository's established equivalent.

Record exact command, counts, failures, and runtime in the closeout.

Do not claim success from partial tests if the full suite fails.

---

# 22. Manual Browser Validation

After automated tests pass, perform a bounded browser validation against a safe temporary/test repository, not Vocab.

Validate the operator experience:

## Matching Snapshot missing

Workflow should show:

- matching Snapshot required;
- explicit Create Matching Snapshot action;
- Commit preparation gated.

## Snapshot created

After explicit creation:

- matching Snapshot ID appears;
- readiness becomes satisfied;
- Commit preparation becomes available.

## Successful Commit

After approved Commit:

- resulting SHA visible;
- execution shown accurately;
- Snapshot classified `Commit aligned`.

## Controlled audit-failure case

Where safely testable:

- mutation-success state is visible;
- resulting SHA shown;
- UI does not say `Not executed`;
- no-retry warning visible;
- Snapshot not classified `Commit aligned`.

Do not mutate Vocab during this validation.

---

# 23. Vocab Boundary

Canonical Vocab remains:

`/home/chuck/projects/vocab-app`

M014 may inspect the historical M002.1 evidence read-only if necessary.

Do not:

- create another Vocab Commit;
- retry the historical Commit;
- reset/revert/amend Vocab;
- create Vocab Snapshots for M014 testing;
- modify Vocab source;
- start Vocab M003 work.

After M014 is accepted, Vocab M003 becomes the next real end-to-end project milestone.

---

# 24. Scope Boundaries

Do not include:

- semantic Context changes;
- deployment/runtime work;
- generalized workflow-session tracking;
- new AI features;
- unrelated Git mutation functionality;
- broad UI redesign;
- Snapshot artifact mutation;
- second Snapshot engine;
- Vocab implementation;
- Photo Organizer access.

Do not “clean up” unrelated code merely because it is nearby.

---

# 25. Escalation / Stop Conditions

STOP and report before broadening scope if:

- fixing mutation-success persistence requires changing the fundamental Git mutation authority;
- Snapshot immutability cannot be preserved;
- Workflow would require a second Snapshot implementation;
- a safe immutable mutation-success record cannot be created within current artifact architecture without a materially larger redesign;
- retry safety cannot be enforced without broad mutation changes;
- existing source behavior materially contradicts the accepted M013 findings;
- tests expose unrelated architectural breakage that would turn M014 into a broader redesign;
- unexpected repository state makes attribution unsafe.

Do not improvise around a stop condition.

---

# 26. Required Closeout

Create exactly:

`docs/014_guarded_commit_verification_snapshot_workflow_and_commit_traceability_hardening_closeout.md`

Include:

## 1. Executive conclusion

PASS / PARTIAL / STOP and concise reason.

## 2. Starting repository state

Branch, HEAD, upstream, parity, status.

## 3. M013 requirements implemented

Map each accepted requirement to implementation.

## 4. Recursive post-commit verification

Exact change and why it fixes the Vocab-shaped defect.

## 5. Mutation-success persistence

Exact artifact/state design and persistence ordering.

## 6. Audit-failure behavior

How post-verification failure is represented.

## 7. Retry/recovery safety

Proof that no automatic retry/reset/revert occurs.

## 8. Workflow rendering

Successful and mutation-succeeded/audit-failed states.

## 9. Matching Snapshot readiness

How Workflow determines and displays readiness.

## 10. In-Workflow Snapshot creation

How the existing Snapshot service is reused.

## 11. Snapshot classification

Exact derived semantics implemented.

## 12. Snapshot-to-Commit association

Artifact/evidence model and immutable references.

## 13. Snapshot immutability

Proof Snapshot artifacts remain unchanged.

## 14. Snapshot browsing/filtering

What was added and why it remains bounded.

## 15. Files changed

Exact list.

## 16. Tests added/changed

Map tests to requirements.

## 17. Focused test results

Exact command/results.

## 18. Full suite results

Exact command/results.

## 19. Compile/static validation

Exact command/results.

## 20. Browser validation

Observed Workflow/Snapshot behavior.

## 21. Native successful Commit fixture

Evidence.

## 22. Native mutation-succeeded/audit-failed fixture

Evidence.

## 23. Vocab status

Confirm canonical Vocab remained unchanged.

## 24. Remaining limitations

Only genuine known limitations.

## 25. Recommendation

Explicitly state whether Repo Control is ready to return to Vocab M003.

## 26. Final repository state

Capture:

    git branch --show-current
    git rev-parse HEAD
    git status --short
    git rev-parse @{upstream} 2>/dev/null || true
    git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null || true

---

# 27. Acceptance Criteria

M014 is PASS only if all of the following are true:

- recursive Commit verification is correct;
- the Vocab-shaped nested-file fingerprint defect has a regression test;
- successful Git mutation is durably evidenced before later audit failure can erase it;
- Workflow never says `Not executed` when the Commit actually occurred;
- resulting Commit SHA remains visible after audit failure;
- no automatic retry/reset/restore/revert occurs;
- matching-Snapshot readiness is visible before Commit preparation;
- an explicit matching Snapshot can be created from Workflow;
- the existing Snapshot service remains authoritative;
- Snapshot artifacts remain immutable;
- `Matching Snapshot available`, `Commit candidate`, `Commit aligned`, and audit-failed semantics are correctly distinguished;
- Commit-aligned traceability includes resulting Git SHA;
- affected focused tests pass;
- full Repo Control suite passes;
- browser validation passes;
- Vocab is not mutated.

---

# 28. Post-M014 Direction

If M014 passes:

**stop Repo Control feature work and return to the Vocab App.**

The next project milestone should be:

`Vocab M003 — bounded refactor and characterization tests`

using the improved Repo Control workflow from the start.

Vocab M003 should serve as the next real-world end-to-end validation of:

- Context discovery;
- Snapshot workflow;
- guarded Stage;
- matching-Snapshot readiness;
- guarded Commit;
- Commit traceability.

Do not create M015 merely for additional Repo Control polishing unless Vocab M003 exposes a genuine new control-plane gap.

---

# 29. Working Principles

> Git is canonical truth.

> Once Git mutation succeeds, Repo Control must never represent that mutation as though it did not happen.

> Required evidence prerequisites belong in Workflow orchestration.

> Snapshot history remains immutable, while Commit alignment is derived from immutable relationship/execution evidence.

> Fix the real control-plane defects, prove them natively, and return to the product work.

---

**End of `014_guarded_commit_verification_snapshot_workflow_and_commit_traceability_hardening_prompt.md`**
