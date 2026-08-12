# Milestone 010 — Browser Guarded Stage and Commit

Prompt file:

`docs/010_browser_guarded_stage_and_commit_prompt.md`

Required closeout file:

`docs/010_browser_guarded_stage_and_commit_closeout.md`

## Milestone Mode

Implementation milestone.

Reasoning level: High for the initial targeted inspection and safety-boundary confirmation.

After those boundaries are confirmed, implement the smallest safe browser adaptation of the existing M008/M007 authorities.

# Goal

Expose Repo Control Plane’s existing guarded Stage and Commit workflow through the browser.

The browser must support this controlled lifecycle:

```
inspect current repository state
    ↓
Prepare Stage
    ↓
Review immutable Stage Plan
    ↓
Explicitly Approve Stage
    ↓
exact M008 stage execution + verification
    ↓
create/ensure exact matching snapshot
    ↓
Prepare Commit
    ↓
Review immutable Commit Plan
    ↓
Explicitly Approve Commit
    ↓
exact M007 commit execution + verification
```

This milestone does NOT create new Git authority.

It exposes the already-accepted M008 and M007 workflow services through a safe browser interface.

The browser must remain a thin adapter around those core authorities.

# Controlling Prior Work

Read only the material needed for this milestone.

Required:

- `docs/008_guarded_staging_preparation_closeout.md`

- `docs/007_guarded_git_write_foundation_closeout.md`

- `docs/007.1_post_commit_fingerprint_verification_remediation_closeout.md`

- `docs/009.3_read_only_browser_usability_refinement_closeout.md`

Use current source and tests as final implementation authority.

Do not repeat broad repository reconnaissance.

# Repositories

Repo Control Plane:

`/home/chuck/projects/repo-control`

Authorized live integration fixture:

`/home/chuck/ai-agent-tests/vocab-app`

Expected Vocab starting state:

```
branch:
    agent-test/repoctl-ui-demo

HEAD:
    5a251f14a7a69ee2dfc9fc72312f49b0c001c30e

status:
     M vocab_utils.py
```

This is the intentional harmless pending normalization-related change preserved specifically as a natural M010 browser Stage/Commit candidate.

Photo Organizer is out of scope.

Do not access Photo Organizer.

# Gate A — Repo Control Preflight

Before implementation report:

```
cd /home/chuck/projects/repo-control

git branch --show-current
git rev-parse HEAD
git status --short
git rev-parse @{upstream}
git rev-list --left-right --count HEAD...@{upstream}
```

Confirm:

- expected development branch;

- M009.3 is committed;

- working tree clean;

- HEAD/upstream aligned unless explicitly explained;

- no active Git operation.

If Repo Control is unexpectedly dirty:

```
STOP AND REPORT
```

Do not clean unexplained state.

# Gate B — Vocab Fixture Preflight

Read-only:

```
cd /home/chuck/ai-agent-tests/vocab-app

git branch --show-current
git rev-parse HEAD
git status --short
```

Expected:

```
agent-test/repoctl-ui-demo
5a251f14a7a69ee2dfc9fc72312f49b0c001c30e
 M vocab_utils.py
```

Before implementation, the Vocab fixture must remain unchanged.

Do not stage or commit the Vocab fixture during implementation or automated testing.

If its state differs:

```
STOP AND REPORT
```

# Locked Core Safety Contracts

M010 must preserve the existing M008/M007 contracts.

Do not weaken, reinterpret, or duplicate them.

## M008 Stage Authority

Continue using the existing core services responsible for:

```
prepare_stage(...)
execute_prepared_stage(...)
```

The existing authority remains responsible for:

- attached-branch enforcement;

- zero pre-existing staged changes;

- zero conflicts;

- zero active Git operations;

- deterministic eligible candidate enumeration;

- supported path/type enforcement;

- unsupported Git-filter enforcement;

- immutable plan publication;

- exact candidate fingerprint binding;

- exact plan-ID approval;

- stale-plan revalidation;

- exact bounded path staging;

- post-stage exact verification;

- index-lock handling;

- execution evidence;

- audit-failure semantics.

Do not implement browser-side substitutes for these checks.

## M007 Commit Authority

Continue using the existing core services responsible for:

```
prepare_commit(...)
execute_prepared_commit(...)
```

The existing authority remains responsible for:

- attached branch;

- staged changes required;

- zero unstaged changes;

- zero untracked changes;

- zero conflicts;

- zero active Git operations;

- exact matching immutable snapshot requirement;

- commit-message validation;

- deterministic staged fingerprint;

- immutable plan;

- exact plan-ID approval;

- stale-plan revalidation;

- Git identity/hook boundaries;

- exact commit execution;

- exact post-commit verification;

- execution evidence;

- audit-failure-after-commit semantics.

The M007.1 canonical fingerprint correction remains authoritative.

Do not reimplement commit verification in the browser.

# Core Architectural Rule

Use:

```
existing M008/M007 workflow service
    ↓
thin browser route/view adapter
    ↓
explicit human review page
    ↓
explicit approval POST
    ↓
existing execution service
```

Do NOT use:

```
browser form
    ↓
ad hoc git subprocess
    ↓
mutation
```

Do not call the CLI from the browser as a subprocess when the reusable core service already exists.

CLI and browser should remain peer adapters over the same core authority.

# Scope A — Browser Workflow Entry Point

Extend the existing Workflow experience so the Product Owner can begin guarded Git promotion.

Provide clear current-state guidance based on existing deterministic workflow facts.

For an eligible unstaged-only repository, expose an action conceptually equivalent to:

```
Prepare Stage — All Eligible Changes
```

The wording must make clear that M008 stages the complete eligible candidate set.

Do not imply selective file or hunk staging exists.

Do not add:

- path checkboxes;

- selective stage controls;

- partial-hunk staging;

- AI-selected staging.

# Scope B — Prepare Stage

Browser Prepare Stage must invoke the existing M008 prepare service.

Preparation is evidence creation, not Git mutation.

After successful prepare, show a human-readable review of the immutable Stage Plan.

At minimum, where existing plan facts support it, show:

```
Action
Repository
Branch
HEAD
Candidate count
Candidate paths
Change classifications
Plan ID
compatibility/current-state information already safely available
```

Machine fingerprints/object IDs/modes may be shown as secondary audit detail where useful.

Do not expose file bodies merely because the browser now performs staging.

Do not silently recompute or alter the candidate set.

# Scope C — Stage Approval

Stage mutation must require a separate explicit approval action.

The approval form must bind the exact immutable:

```
stage plan ID
```

There must be no:

```
latest plan
implicit plan
hidden automatic approval
one-click prepare-and-stage
approval via GET
```

Use POST + existing CSRF protections.

The button/action should clearly communicate that Git staging will occur.

Conceptually:

```
Approve Stage
```

or:

```
Approve Stage — 1 File
```

Use the exact reviewed plan.

Immediately before mutation, the M008 execution service must perform its existing stale-state revalidation.

If stale:

```
fail closed
```

Do not regenerate and execute a replacement plan automatically.

# Scope D — Stage Execution Result

After approved execution, clearly show one of:

```
STAGE SUCCEEDED
STAGE BLOCKED
STAGE FAILED
STAGE SUCCEEDED / AUDIT FAILED
```

Preserve exact workflow reason/error codes as secondary technical evidence.

For successful staging show available facts such as:

```
Stage Plan
Stage Execution
Branch
HEAD unchanged
Files staged
Resulting workflow state
```

Expected normal result:

```
staged_only
```

Do not automatically:

- retry;

- unstage;

- reset;

- restore;

- create a new plan;

- create a commit;

- push.

# Scope E — Partial-Mutation / Audit-Failure Safety

M008 already distinguishes failure before index mutation from failure after index mutation.

The browser must preserve that distinction.

If core authority reports:

```
git_stage_failed_after_mutation
```

the UI must make clear that repository state may have changed and requires human inspection.

Do not automatically repair it.

If core authority reports:

```
stage_succeeded_audit_failed
```

the UI must clearly state:

```
staging succeeded
resulting staged state remains
audit persistence failed
```

Do not offer an automatic retry that could perform another mutation.

Require human inspection.

# Scope F — Snapshot Boundary Between Stage and Commit

Preserve the M007 requirement:

```
exact matching immutable snapshot required before prepare-commit
```

M010 must NOT auto-create that snapshot.

Automatic workflow-boundary snapshots remain deferred architecture.

After successful staging, guide the Product Owner to the existing Snapshot capability.

Conceptually:

```
Stage complete.
A matching snapshot is required before Commit can be prepared.
```

Provide a clear navigation affordance to:

```
Snapshots
```

The existing snapshot creation authority may be used manually.

Once a matching staged-state snapshot exists, the normal commit-preparation flow can proceed.

Do not silently create a snapshot while preparing a commit.

# Scope G — Prepare Commit

When current state satisfies M007 preparation requirements, allow entry of a commit message and:

```
Prepare Commit
```

Commit-message entry belongs to preparation, not approval.

Prepare Commit invokes the existing M007 prepare service.

The browser then displays the immutable Commit Plan for human review.

At minimum show existing authoritative facts such as:

```
Action
Commit message
Repository
Branch
Starting HEAD
staged file/count summary
matching snapshot
Commit Plan ID
```

Where available and useful, show staged paths and fingerprints as secondary details.

Do not modify the index or HEAD during preparation.

# Scope H — Commit Approval

Commit mutation must require a second explicit approval step after the immutable Commit Plan is visible.

The approval form must bind the exact:

```
commit plan ID
```

No:

```
latest plan
implicit approval
prepare-and-commit combination
approval via GET
```

Use POST + CSRF.

Conceptually:

```
Approve Commit
```

Immediately before mutation, existing M007 execution must perform its full revalidation.

If branch, HEAD, staged state, repository binding, snapshot evidence, or another locked condition changed:

```
fail closed
```

Do not automatically prepare and execute a replacement plan.

# Scope I — Commit Execution Result

After execution clearly distinguish:

```
COMMIT SUCCEEDED
COMMIT BLOCKED
COMMIT FAILED
COMMIT SUCCEEDED / AUDIT FAILED
```

Successful result should display existing facts such as:

```
Commit Plan
Commit Execution
Commit message
Previous HEAD
Resulting HEAD
matching snapshot
verification result
```

Do not:

- amend;

- retry automatically;

- create a second commit;

- fetch;

- push.

# Scope J — Commit Audit-Failure Safety

The existing M007 condition:

```
commit_succeeded_audit_failed
```

is safety-critical.

If it occurs, the browser must make unmistakably clear:

```
THE GIT COMMIT SUCCEEDED
THE COMMIT REMAINS
AUDIT PERSISTENCE FAILED
```

If the resulting commit SHA is available, display it.

Do not:

- retry commit;

- amend;

- revert;

- reset;

- automatically execute another plan.

Require human investigation.

# Scope K — Workflow History

Integrate new Stage/Commit browser actions with the human-readable Workflow presentation established in M009.3.

Continue visually pairing related:

```
Stage Plan → Stage Execution
```

and:

```
Commit Plan → Commit Execution
```

for comprehension.

Do NOT merge their immutable identities.

Plan and execution artifacts remain separate evidence objects.

New transactions produced through the browser must be indistinguishable in core audit semantics from equivalent transactions produced through the CLI.

# Scope L — Errors and Fail-Closed Presentation

Catch existing workflow reason errors at the browser adapter boundary and present them safely.

Show:

```
human-readable explanation
stable reason code
```

Examples may include existing codes such as:

```
approval_required
no_stage_candidates
staged_changes_present
conflicts_present
git_operation_in_progress
unsupported_path_type
unsupported_git_filters
plan_not_found
plan_integrity_failed
repository_mismatch
branch_changed
head_changed
worktree_state_changed
git_index_locked
matching_snapshot_required
no_staged_changes
unstaged_changes_present
untracked_changes_present
invalid_commit_message
staged_state_changed
unsupported_git_hooks
git_identity_unavailable
git_commit_failed
post_commit_verification_failed
```

Do not turn a fail-closed core error into a browser workaround.

# Browser Security Requirements

Preserve all accepted browser security properties.

Required:

- loopback-only server enforcement;

- repository remains bound at startup;

- no arbitrary browser repository-path input;

- CSRF protection on every mutation-capable POST;

- no mutation on GET;

- POST/Redirect/GET where appropriate;

- HTML escaping;

- no Node/CDN dependency;

- no external browser service;

- no hidden approval default;

- exact plan-ID binding.

Browser mutation authority is limited to the two existing operations authorized by this milestone:

```
M008 Stage
M007 Commit
```

# Explicitly Out of Scope

Do NOT add:

- Git fetch;

- Git pull;

- Git push;

- upstream refresh;

- remote branch creation;

- repository chooser;

- repository registry;

- branch creation/switching;

- selective staging;

- partial-hunk staging;

- commit amend;

- revert;

- reset;

- restore;

- stash;

- cleanup;

- automatic snapshot creation;

- persistent snapshot labels;

- code lineage;

- task model;

- Milestone Record;

- strict coder-context freshness authority;

- Architect Packet;

- whitespace diagnostics;

- whitespace normalization;

- service/systemd startup;

- tunnel automation;

- Photo Organizer integration.

# Targeted Implementation Boundary

Inspect only directly relevant files.

Likely browser files include:

```
src/repoctl/web/app.py
src/repoctl/web/views.py
src/repoctl/web/templates/workflow.html
src/repoctl/web/static/app.css
tests/test_web.py
```

Existing core authorities likely include:

```
src/repoctl/workflow/stage_plan.py
src/repoctl/workflow/stage_execution.py
src/repoctl/workflow/commit_plan.py
src/repoctl/workflow/commit_execution.py
src/repoctl/workflow/git_state.py
src/repoctl/workflow/status.py
src/repoctl/workflow/errors.py
```

Existing snapshot support may be inspected only as required to guide the manual matching-snapshot step.

Do not alter M007/M008 core files merely to simplify browser integration unless a concrete incompatibility is discovered.

If core changes appear necessary:

```
STOP AND REPORT
```

before modifying them.

# Gate C — Targeted Architecture Confirmation Before Coding

Before implementation, confirm:

1. Browser routes can call M008/M007 reusable core services directly.

2. No CLI subprocess adapter is required.

3. Existing plan objects contain enough information for safe human review.

4. Exact `plan_id` can be carried through CSRF-protected approval forms.

5. Existing M008/M007 exceptions/reason codes can be presented without changing core semantics.

6. Existing snapshot browser capability can satisfy the manual staged-snapshot boundary.

7. M010 can be implemented without modifying fundamental M007/M008 authority.

If any answer is materially no:

```
STOP AND REPORT
```

with the exact blocker.

# Automated Validation Strategy

All automated Git-mutation tests must use isolated disposable temporary repositories.

Do NOT use the Vocab fixture for automated mutation tests.

At minimum test:

## Stage Browser Success

```
create eligible working-tree change
browser Prepare Stage
verify prepare is non-mutating
review exact plan
browser Approve Stage
verify exact paths staged
verify HEAD unchanged
verify staged_only
verify execution evidence
```

## Stage Approval Required

Attempt execution path without valid explicit browser approval.

Confirm:

```
no mutation
```

## Stage Stale Plan

```
prepare stage
mutate candidate state
approve old plan
```

Confirm:

```
core refuses
HEAD unchanged
index unchanged
```

## Stage Error/Audit Semantics

Cover browser rendering for:

```
normal block
failure after mutation where feasible through controlled test double
stage_succeeded_audit_failed
```

Confirm no automatic recovery/retry.

## Commit Preparation Snapshot Gate

From staged-only state without matching snapshot:

```
Prepare Commit
```

Confirm:

```
matching_snapshot_required
no commit
```

## Commit Browser Success

```
create controlled change
Stage using guarded flow or equivalent controlled setup
create exact matching snapshot
browser Prepare Commit
verify prepare is non-mutating
review exact immutable Commit Plan
browser Approve Commit
verify exactly one commit
verify exact message
verify parent
verify exact committed delta
verify execution evidence
```

## Commit Stale Plan

```
prepare valid Commit Plan
alter bound staged state or other locked state
approve old plan
```

Confirm:

```
refusal
no unintended commit
```

## Commit Audit-Failure Semantics

Exercise browser handling of:

```
commit_succeeded_audit_failed
```

Confirm:

```
browser reports that commit succeeded
no second commit is attempted
no reset/revert/amend occurs
```

## Browser Security

Confirm:

- mutation endpoints reject GET where applicable;

- CSRF remains required;

- repository cannot be supplied/rebound through browser form;

- exact plan ID is required;

- no browser fetch/push/pull route exists.

# Regression Validation

Run at minimum:

```
tests.test_web
tests.test_workflow_stage
tests.test_workflow_commit
```

Then run the full Repo Control suite.

M007.1 multi-file post-commit fingerprint regression must remain passing.

No existing deterministic evidence artifacts should be rewritten merely by loading browser pages.

# Gate D — Vocab Pre-Mutation Validation

After implementation and automated tests pass, return to the preserved Vocab fixture read-only.

Confirm again:

```
branch:
    agent-test/repoctl-ui-demo

HEAD:
    5a251f14a7a69ee2dfc9fc72312f49b0c001c30e

status:
     M vocab_utils.py
```

Run the existing Vocab test suite before mutation.

Expected healthy baseline:

```
14 tests passing
```

If Vocab tests fail unexpectedly:

```
STOP AND REPORT
```

Do not stage or commit.

# Gate E — Product Owner Live Browser Validation

This is intentionally a Product Owner-controlled live mutation gate.

The coder must NOT perform the Vocab Stage/Commit approval clicks on behalf of the Product Owner.

After all automated validation passes:

1. launch Repo Control against:
   
   ```
   /home/chuck/ai-agent-tests/vocab-app
   ```

2. provide the browser URL/tunnel instructions;

3. report that M010 is ready for Product Owner live validation;

4. STOP before Vocab mutation.

The Product Owner will exercise the actual browser approval workflow.

# Expected Product Owner Live Sequence

The intended live validation is:

```
Dashboard / Workflow
    ↓
inspect the one pending vocab_utils.py change
    ↓
Prepare Stage — All Eligible Changes
    ↓
review immutable Stage Plan
    ↓
Approve Stage
    ↓
confirm staged_only
    ↓
create matching Snapshot using existing browser Snapshot capability
    ↓
Prepare Commit
```

Recommended live commit message:

```
Complete pending synonym normalization refinement
```

Then:

```
review immutable Commit Plan
    ↓
Approve Commit
    ↓
verify exactly one local commit
    ↓
verify clean Vocab working tree
```

No push.

# Expected Vocab State Transition

Before live test:

```
HEAD:
    5a251f14a7a69ee2dfc9fc72312f49b0c001c30e

status:
     M vocab_utils.py
```

After successful Stage:

```
HEAD remains:
    5a251f14a7a69ee2dfc9fc72312f49b0c001c30e

expected status:
    M  vocab_utils.py
```

After successful Commit:

```
HEAD:
    exactly one new local commit

status:
    clean
```

The resulting SHA must be recorded in the closeout.

Do not push the Vocab branch.

# Gate F — Post-Live Validation

After Product Owner approval succeeds:

1. verify Vocab branch and new HEAD;

2. verify exact parent is the original fixture HEAD;

3. verify commit message;

4. verify working tree clean;

5. rerun Vocab tests;

6. verify browser Workflow shows the new:  
   Stage Plan  
   Stage Execution  
   Commit Plan  
   Commit Execution

7. verify Dashboard reflects clean state;

8. verify no remote operation occurred.

If Stage succeeds but audit fails, or Commit succeeds but audit fails:

```
STOP AND PRESERVE CURRENT STATE
```

Do not retry.

Record exact evidence and escalate.

# Product Owner Review Requirements

The Product Owner should be able to answer yes to:

- I can tell what will be staged before approving it.

- Preparing a plan does not mutate Git.

- Stage requires a separate explicit approval.

- After Stage I can see that the repository is staged-only.

- I understand why a matching Snapshot is required before Commit.

- I can review the exact Commit Plan and message before approval.

- Commit requires a separate explicit approval.

- I can clearly see the resulting commit.

- Errors tell me what was blocked and why.

- I never see Push implied as part of Commit.

- Plan IDs remain available but do not dominate the human workflow.

# Closeout

Create:

`docs/010_browser_guarded_stage_and_commit_closeout.md`

Include:

1. status;

2. exact Repo Control starting branch/HEAD/upstream/status;

3. exact Vocab starting branch/HEAD/status;

4. targeted architecture confirmation;

5. files changed;

6. browser Stage architecture;

7. Stage Plan review presentation;

8. Stage approval/CSRF behavior;

9. Stage stale-plan behavior;

10. Stage execution/result presentation;

11. stage partial-mutation/audit-failure handling;

12. browser Commit architecture;

13. matching-snapshot boundary;

14. Commit Plan review presentation;

15. Commit approval/CSRF behavior;

16. Commit stale-plan behavior;

17. Commit execution/result presentation;

18. `commit_succeeded_audit_failed` browser behavior;

19. confirmation M008 core authority was preserved;

20. confirmation M007/M007.1 core authority was preserved;

21. confirmation no CLI subprocess mutation adapter was introduced;

22. browser security validation;

23. targeted test commands and literal results;

24. full Repo Control regression result;

25. Vocab pre-live test result;

26. Product Owner live Stage evidence:  
    plan ID  
    execution ID  
    resulting status;

27. matching staged snapshot ID;

28. Product Owner live Commit evidence:  
    plan ID  
    execution ID  
    resulting commit SHA;

29. post-commit Vocab test result;

30. final Vocab branch/HEAD/status;

31. confirmation Vocab was not pushed;

32. confirmation no fetch/pull/push capability was added;

33. confirmation no automatic snapshot was added;

34. confirmation no selective/partial staging was added;

35. confirmation no other Git mutation capability was added;

36. confirmation no Photo Organizer access occurred;

37. known limitations/deferred items;

38. exact final Repo Control `git status --short`;

39. exact final Vocab `git status --short`.

# Explicit Escalation Protocol

STOP AND REPORT if:

- Repo Control is unexpectedly dirty at start;

- Vocab fixture differs from the known pending state before live validation;

- browser integration requires redesign of M007 or M008;

- browser would need to call Git directly instead of existing workflow authority;

- exact plan identity cannot be bound through approval;

- CSRF cannot be preserved;

- plan review lacks enough existing information for meaningful human approval;

- stale plan execution is not rejected by existing authority;

- matching snapshot requirement would need to be bypassed;

- automatic snapshot creation appears necessary;

- Stage produces unexpected partial mutation;

- Commit succeeds but audit persistence fails;

- Stage succeeds but audit persistence fails;

- any remote Git operation would be required;

- any reset/revert/restore/cleanup would be required;

- Photo Organizer access would be required.

Do not improvise around a locked safety boundary.

# Definition of Done

Milestone 010 is complete only when:

- existing M008 Stage authority is safely accessible through browser Prepare → Review → Approve;

- existing M007 Commit authority is safely accessible through browser Prepare → Review → Approve;

- preparation remains non-mutating;

- exact immutable plan IDs bind approvals;

- stale plans fail closed;

- existing core post-mutation verification remains authoritative;

- audit-failure-after-mutation states are clearly and safely surfaced;

- matching snapshot remains explicitly required between Stage and Commit;

- no snapshot is created automatically;

- no selective staging is introduced;

- no direct browser Git implementation bypasses M007/M008;

- no fetch/pull/push capability is introduced;

- Product Owner successfully exercises the full flow against the intentional Vocab pending change;

- the Vocab fixture ends at exactly one new local commit with a clean working tree and passing tests;

- the Vocab branch is not pushed;

- Repo Control full regression passes;

- Photo Organizer remains untouched.

M010 clarification decisions confirmed.

The coder’s architectural reading is correct: M010 is a browser adaptation of the existing M008/M007 authorities, not a redesign of Git workflow safety.

Use the following locked browser interaction contract.

1. FLOW OWNER

The Workflow page owns the guided Stage → Snapshot → Commit lifecycle.

Use route-level actions and read-only plan review views.

Preferred interaction:

    Workflow
        ↓
    POST Prepare Stage
        ↓
    redirect to Stage Plan Review
        ↓
    POST Approve Stage
        ↓
    redirect to execution result / Workflow state
        ↓
    user creates matching Snapshot through existing Snapshot UI
        ↓
    Workflow
        ↓
    enter commit message + POST Prepare Commit
        ↓
    redirect to Commit Plan Review
        ↓
    POST Approve Commit
        ↓
    redirect to execution result / Workflow state

Do not use a modal as the primary plan-review surface.

A dedicated read-only review view is preferred because the immutable plan should be clearly inspectable before mutation and normal POST/Redirect/GET behavior should remain explicit.

Exact route naming is an implementation detail and may follow current Flask conventions.

2. GENERIC REPOSITORY BEHAVIOR

The feature must work for any repository safely bound to the running Repo Control browser instance.

Do not special-case Vocab App in production implementation.

Testing boundary:

    automated mutation tests:
        isolated disposable temporary repositories

    live Product Owner acceptance:
        Vocab App fixture only

The Vocab fixture is the milestone safety harness, not application-specific behavior.

3. IMMUTABLE PLAN REVIEW CONTENT

The browser review page should present a human-readable projection of the existing immutable core plan.

For Stage, show existing facts such as:

    action
    repository
    branch
    starting HEAD
    candidate count
    exact candidate paths
    change classifications
    exact immutable Stage Plan ID
    compatibility/current-state information if already available safely

For Commit, show existing facts such as:

    action
    repository
    branch
    starting HEAD
    commit message
    staged scope/count
    matching snapshot
    exact immutable Commit Plan ID

Machine fingerprints/object IDs/modes may be secondary audit detail.

Do NOT add a new browser review timestamp or other metadata merely for presentation unless that fact already exists authoritatively in the plan artifact.

The underlying immutable plan artifact remains authoritative.

The browser summary is not a new approval object.

4. PLAN ID FLOW

The plan ID returned by the existing prepare service is the exact identity carried into the review page and approval POST.

Approval must bind that exact immutable ID.

The user must not be able to:

    type a replacement plan ID
    select a different plan during approval
    approve “latest”
    approve an implicitly regenerated plan

Conceptually:

    prepare service
        → returns exact plan_id
        → review exact plan_id
        → approval POST carries exact plan_id
        → core execution reloads and revalidates exact plan_id

The browser must never substitute a newer plan automatically if the reviewed plan becomes stale.

5. APPROVAL UX

Use one explicit approval action per immutable plan.

Stage:

    Approve Stage

Commit:

    Approve Commit

Do not add an additional browser-created confirmation model or multi-step approval ceremony.

The security contract remains:

    exact plan ID
    +
    explicit user approval
    +
    CSRF-protected POST
    +
    existing core revalidation

The approval button should exist on the corresponding plan-review view so the user is approving the plan they are currently looking at.

6. PREPARE AND APPROVE MUST REMAIN SEPARATE

Do not combine:

    Prepare + Stage

or:

    Prepare + Commit

into one browser operation.

Preparation remains non-mutating.

The user must see the resulting immutable plan before the separate mutation approval is available.

7. CORE SERVICE AUTHORITY

Add this wording as a locked M010 rule:

    The browser may render plan/execution state and collect approval
    intent, but all mutation authority remains in the existing M008/M007
    core services.

    The browser must not reimplement eligibility checks, candidate
    enumeration, snapshot validation, fingerprint logic, stale-plan
    detection, Git-operation checks, execution verification, or
    post-mutation verification.

No browser-side branch/HEAD/staged-state/fingerprint logic may become an independent authority.

Display-only derivation is acceptable where already supported by existing deterministic facts.

8. FAILURE PRESENTATION

Existing core WorkflowReasonError reason codes remain authoritative.

The browser adapter may translate them into readable explanatory text, but must also retain/display the stable reason code.

Example:

    Stage blocked

    Repository state changed after this Stage Plan was prepared.
    Review the current repository state and prepare a new plan.

    Reason:
        worktree_state_changed

Do not catch a fail-closed error and automatically repair, regenerate, retry, restage, or recommit.

9. STALE PLAN UX

A review page may display compatibility/current-state information if that information can be safely obtained using existing read-only services.

However:

    browser compatibility display is informational
    core execution-time revalidation is authoritative

Even if the browser thinks a plan appears compatible, M008/M007 must revalidate immediately before mutation.

If execution reports stale:

    show the failure
    preserve repository state
    require the user to return and explicitly prepare a new plan

10. EXECUTION EVIDENCE / AUDIT TRAIL

The existing external M008/M007 execution artifacts remain the source of truth.

Do NOT introduce:

    browser-only audit records
    duplicate plan records
    duplicate execution records
    separate approval persistence model

The browser should render summaries of the existing plan/execution artifacts in the Workflow UI.

Plan and execution identities remain distinct immutable evidence objects even when visually paired.

11. SNAPSHOT BOUNDARY

Keep the M007 matching-snapshot requirement exactly as designed.

After Stage succeeds:

    show that the repository is staged_only
    explain that Commit preparation requires an exact matching Snapshot
    provide navigation to the existing Snapshot page

Do NOT automatically create the snapshot in M010.

After the user creates the matching snapshot, they return to Workflow and prepare Commit.

12. LIVE VOCAB APPROVAL

The coder may implement and fully validate M010 using disposable repositories.

The coder must STOP before performing the real Vocab mutation.

The Product Owner will personally perform:

    Prepare Stage
    Review Stage Plan
    Approve Stage
    create matching Snapshot
    Prepare Commit
    Review Commit Plan
    Approve Commit

against the preserved:

    M vocab_utils.py

Vocab fixture.

No push.

13. AUDIT-FAILURE CONDITIONS

Preserve the existing special conditions exactly.

If:

    stage_succeeded_audit_failed

then staging already happened.

Do not retry or unstage.

If:

    commit_succeeded_audit_failed

then the Git commit already happened.

Do not retry, amend, revert, or reset.

The browser must make these conditions visually unmistakable.

14. NO NEW MODEL

The existing artifact store is authoritative.

M010 introduces no new persistent:

    browser audit model
    approval record model
    task model
    lineage model
    milestone model

A browser approval is an invocation of the existing execution authority against an existing exact immutable plan.

15. IMPLEMENTATION DIRECTION

Your recommended implementation direction is approved:

    route-level POST actions
    +
    dedicated read-only plan review views
    +
    thin adapters over existing core services

Proceed with the Gate C targeted architecture confirmation first.

If that inspection shows this contract can be implemented without modifying fundamental M008/M007 authority:

    proceed with implementation.

If a core authority redesign appears necessary:

    STOP AND REPORT.

STATUS:

    M010 CLARIFICATIONS CONFIRMED
    WORKFLOW PAGE OWNS GUIDED FLOW
    DEDICATED READ-ONLY PLAN REVIEW
    EXACT PLAN-ID APPROVAL
    SINGLE EXPLICIT APPROVAL PER PLAN
    CORE ARTIFACT STORE REMAINS AUTHORITATIVE
    GENERIC BOUND-REPOSITORY FEATURE
    VOCAB IS LIVE ACCEPTANCE FIXTURE ONLY
    NO M008/M007 SAFETY REDESIGN AUTHORIZED