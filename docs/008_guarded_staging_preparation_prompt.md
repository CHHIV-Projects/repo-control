# Milestone 008 — Guarded Staging Preparation

Prompt file:

`008_guarded_staging_preparation_prompt.md`

Required closeout file:

`008_guarded_staging_preparation_closeout.md`

## Objective

Add Repo Control Plane's second bounded Git-write primitive:

    inspect exact unstaged/untracked repository state
        ↓
    prepare immutable staging plan
        ↓
    present exact human-readable file set
        ↓
    require explicit operator approval
        ↓
    revalidate exact repository state
        ↓
    stage exactly the reviewed paths
        ↓
    mechanically verify staged result
        ↓
    record immutable execution evidence

Milestone 008 builds directly on the Milestone 007 safety architecture.

The intended local workflow after this milestone becomes:

    edit files
        ↓
    prepare-stage
        ↓
    review staging plan
        ↓
    explicitly approve staging
        ↓
    staged-only repository
        ↓
    repoctl snapshot
        ↓
    prepare-commit
        ↓
    explicitly approve commit

This milestone does NOT push, fetch, pull, commit automatically, or stage partial hunks.

---

# Scope Decision — Stage All Current Eligible Changes

Milestone 008 intentionally supports one simple staging operation:

    stage all currently visible eligible unstaged and untracked changes

The plan must enumerate the exact individual paths before mutation.

Do NOT implement arbitrary directory staging or broad uncontrolled:

    git add .
    git add -A

against whatever happens to exist at execution time.

Execution must use the exact reviewed path set from the immutable plan after exact state revalidation.

Selective staging of only some files is deferred.

Partial-hunk staging is deferred.

This keeps M008 small enough to prove the staging transaction model before adding richer GUI file-selection behavior.

---

# Architectural Intent

Preserve the existing evidence hierarchy:

    repository source / Git / tests
        ↓
    deterministic Repo Control Plane evidence
        ↓
    immutable snapshots / plans / executions
        ↓
    advisory GPT-OSS

AI must have no authority over staging.

The staging decision must be based only on:

- deterministic local repository state;
- immutable staging plan;
- explicit human approval.

Milestone 008 must reuse the M007 transaction pattern:

    prepare
        ↓
    review
        ↓
    approve
        ↓
    revalidate
        ↓
    execute
        ↓
    verify
        ↓
    audit

Do not invent a separate safety architecture for staging.

---

# Future GUI Compatibility — Hard Requirement

Do not place staging policy exclusively inside CLI handlers.

Implement reusable core services conceptually equivalent to:

    prepare_stage(...)
    execute_prepared_stage(...)

The CLI must remain a thin adapter.

Conceptually:

    Repo Control Plane Core
    
      prepare_stage()
            │
            ▼
      immutable stage plan
            │
            ▼
      execute_prepared_stage()
            │
            ▼
      verified staged state
    
          ▲            ▲
          │            │
        CLI now     Web UI later

Core services must return structured results suitable for eventual browser GUI rendering.

Do not add the browser GUI or HTTP API in this milestone.

---

# Project

Repo Control Plane:

`/home/chuck/projects/repo-control`

Photo Organizer remains explicitly out of scope.

Do not inspect, scan, modify, or otherwise access Photo Organizer.

Do not mutate Vocab App.

All Git-mutation validation must use isolated temporary repositories.

---

# Required Reading

Read and preserve:

- Repo Control Plane architecture / implementation plan
- Milestone 004 prompt and closeout
- Milestone 006 prompt and closeout
- Milestone 006.1 prompt and closeout
- Milestone 007 prompt and closeout

Especially preserve:

- deterministic facts before interpretation;
- immutable external evidence;
- M006 canonical Git-state machinery;
- M007 explicit plan-specific approval;
- M007 stale-plan blocking;
- M007 fail-closed mutation behavior;
- M007 immutable execution evidence;
- M007 rule against automatically undoing a mutation after an uncertain result;
- M006.1 Python-cache hygiene.

Do not broadly reconnoiter the repository.

Inspect only files/services/tests materially required by M008.

---

# Initial Git Preflight

Before coding:

1. confirm branch;
2. confirm HEAD;
3. confirm worktree/index clean;
4. confirm no active Git operation;
5. confirm M007 is committed.

At minimum:

    git branch --show-current
    git rev-parse HEAD
    git status --short

If Repo Control Plane itself is not clean:

    STOP

Do not automatically:

- reset;
- restore;
- stash;
- clean;
- stage;
- discard unexplained state.

Do not commit or push unless separately instructed.

---

# User-Facing Commands

Implement commands equivalent to:

    repoctl milestone prepare-stage \
        --all \
        [--repository <path>]

and:

    repoctl milestone stage <plan_id> \
        --approve \
        [--repository <path>]

`--all` means:

    all currently visible eligible unstaged/untracked paths
    represented in the immutable reviewed plan

It does NOT mean:

    recompute all paths later and stage whatever currently exists

Execution always uses the exact path set captured by the approved plan.

No implicit "latest plan" behavior.

No stage-without-plan behavior.

---

# Gate A — Mechanical Prepare Preconditions

`prepare-stage` must fail closed unless:

    branch_attached == true
    
    staged_changes_present == false
    
    unmerged_entries_present == false
    
    git_operation_in_progress == false

and there is at least one eligible unstaged or untracked change.

The starting index must therefore be clean.

Do not mix existing staged content with an M008 stage transaction.

At least one visible candidate change must exist.

Fail closed for conditions equivalent to:

    detached_head
    staged_changes_present
    conflicts_present
    git_operation_in_progress
    no_stage_candidates

Do not automatically unstage existing content.

Do not resolve conflicts.

Do not alter Git operations.

---

# Gate B — Exact Candidate Enumeration

Build the staging candidate set deterministically from Git.

Do not use filesystem walking alone to decide what Git considers changed.

Use appropriate read-only Git plumbing to identify:

- tracked modified paths;
- tracked deleted paths;
- tracked mode changes;
- untracked non-ignored files.

Disable rename heuristics for canonical plan identity where appropriate.

A rename may therefore be represented conservatively as:

    deletion of old path
        +
    addition of new path

rather than relying on heuristic rename detection.

Ignored files must not be included.

The plan must ultimately contain exact repository-relative individual paths.

Do not store broad directory pathspecs.

Do not infer files outside Git's reported visible change set.

---

# Gate C — Supported Path Types

For M008, support ordinary Git file staging only.

Support:

- regular tracked files;
- regular untracked files;
- tracked file deletions;
- ordinary executable-bit/mode changes where Git supports them.

Fail closed on unsupported or ambiguous path types such as:

- submodule/gitlink changes;
- nested repository boundaries that cannot be safely represented;
- symlink changes if exact behavior is not deliberately implemented and tested;
- special filesystem objects;
- paths whose type cannot be safely classified.

Use a structured condition equivalent to:

    unsupported_path_type

Do not broaden the milestone merely to support an unusual path type.

If symlink support is implemented, it must be exact and separately tested; otherwise block it.

---

# Gate D — Git Filter / Attribute Boundary

`git add` may transform file content through Git attributes and clean filters.

M008 must not silently execute unknown custom content-processing programs.

Before preparing/executing a staging plan, detect whether any candidate path is governed by a custom Git `filter` attribute.

If a custom filter driver would apply:

    BLOCK

with a structured reason equivalent to:

    unsupported_git_filters

This includes environments such as Git LFS or other custom clean/process filters unless explicitly supported in a future milestone.

Do not silently disable filters.

Do not bypass repository attributes.

Built-in Git normalization behavior may be supported if the implementation can deterministically calculate and verify the exact blob Git would stage.

---

# Gate E — Expected Staged Blob Identity

For each regular file candidate, compute the exact object identity Git is expected to stage without mutating the object database.

Prefer Git's own read-only content conversion machinery, for example an approach equivalent to:

    git hash-object --filters --path=<path> <file>

without:

    -w

where appropriate.

The purpose is to bind the plan to Git's expected staged representation rather than merely the raw filesystem bytes.

The plan should capture at least:

- path;
- change classification;
- prior tracked object ID when applicable;
- expected staged object ID;
- prior mode when applicable;
- expected staged mode;
- deletion marker when applicable.

Do not write Git objects during prepare.

Do not store file bodies.

Do not store full textual diffs.

---

# Gate F — Exact Worktree / Stage Candidate Fingerprint

Create a deterministic fingerprint representing the exact staging proposal.

It must bind at minimum:

- repository identity;
- canonical repository root;
- branch;
- HEAD;
- exact candidate path set;
- change classification per path;
- old tracked identity where applicable;
- expected staged object identity where applicable;
- expected modes;
- deletion state;
- relevant supported attribute/filter assumptions.

The fingerprint must change if any material proposed staged content changes.

Examples that must invalidate a plan:

    file content changed
    file added
    file removed
    candidate file deleted
    previously deleted file restored
    executable mode changed
    untracked file changed
    candidate path set changed
    Git attribute/filter behavior becomes unsupported

Do not use timestamps as identity.

A file touched without a content/mode change should not necessarily invalidate a plan.

---

# Gate G — Immutable Stage Plan

Store plans outside the target repository under the existing workflow state hierarchy, conceptually:

    ~/.local/share/repoctl/<repo-id>/workflow/stage_plans/<plan-id>/

containing:

    plan.json
    plan.md

The plan must be immutable.

Include at minimum:

- schema version;
- plan ID;
- repository ID;
- canonical repository root;
- branch;
- HEAD;
- exact stage-candidate fingerprint;
- exact candidate file/status summary;
- expected staged identities/modes;
- mechanical preconditions;
- relevant filter-policy evidence;
- explicit statement that no Git mutation occurred;
- explicit statement that no remote refresh occurred.

Prefer a deterministic content-derived plan ID.

Preparing the exact same staging plan twice may reuse the same plan only after integrity verification.

If the same deterministic ID exists with inconsistent content:

    FAIL CLOSED

Do not overwrite it.

---

# Gate H — Human-Readable Plan

`prepare-stage` must produce concise human-readable output suitable for CLI now and GUI rendering later.

Conceptually:

    PREPARED STAGING PLAN
    
    Repository: repo-control
    Branch:     main
    HEAD:       abc123...
    
    Changes proposed for staging: 5
    
      M README.md
      M src/repoctl/cli.py
      A src/repoctl/workflow/stage_plan.py
      A tests/test_workflow_stage.py
      D old_file.py
    
    Existing staged changes: 0
    Conflicts:               0
    Git operation:           none
    
    Plan:
    stage-plan--...
    
    NO TARGET GIT MUTATION PERFORMED
    
    To approve this exact plan:
    
      repoctl milestone stage <plan-id> --approve

Do not describe the plan as:

    safe
    correct
    approved
    architecture-valid

It is an exact deterministic staging proposal.

---

# Gate I — Prepare Must Be Target-Repository Read Only

`prepare-stage` must not mutate target Git state.

It must not:

- stage;
- unstage;
- write the index;
- write Git objects;
- commit;
- change HEAD;
- create refs;
- create branches;
- fetch;
- pull;
- push;
- stash;
- reset;
- restore;
- alter Git config.

External Repo Control Plane plan artifacts are allowed.

Tests must prove target:

- HEAD unchanged;
- index unchanged;
- worktree unchanged.

---

# Gate J — Explicit Plan-Specific Approval

Execution requires BOTH:

1. an exact immutable stage plan ID;
2. explicit approval.

CLI:

    repoctl milestone stage <plan_id> --approve

Without `--approve`:

    no mutation

and return a structured reason equivalent to:

    approval_required

Do not provide:

    stage latest
    --yes against recomputed state
    implicit latest-plan selection

The plan ID must identify exactly what the operator reviewed.

---

# Gate K — Immediate Revalidation Before Mutation

Before invoking Git staging:

1. load immutable plan;
2. verify plan integrity;
3. verify repository binding;
4. recompute current deterministic candidate state;
5. require exact equality with the approved plan.

At minimum require equality for:

    repository identity
    canonical root
    attached branch
    exact branch name
    HEAD
    zero existing staged changes
    exact candidate path set
    exact candidate fingerprint
    expected staged object IDs
    expected modes/deletions
    zero conflicts
    zero active Git operations
    supported filter state

If anything changed:

    BLOCK

Do not regenerate the plan automatically.

The operator must prepare and review a new plan.

Examples:

    plan prepared
        ↓
    untracked file changes
        ↓
    BLOCK
    
    plan prepared
        ↓
    another file appears
        ↓
    BLOCK
    
    plan prepared
        ↓
    HEAD changes
        ↓
    BLOCK
    
    plan prepared
        ↓
    branch changes
        ↓
    BLOCK

---

# Gate L — Exact Bounded Staging Execution

After revalidation and explicit approval, stage exactly the reviewed individual paths.

Do not invoke uncontrolled:

    git add .
    git add -A

against a newly recomputed repository state.

Use structured subprocess arguments and an explicit:

    --

path separator.

Pass exact repository-relative paths from the verified immutable plan.

Do not use shell-string command construction.

The operation may stage:

- tracked modifications;
- tracked deletions;
- regular untracked additions;
- supported mode changes.

Do not:

- commit;
- fetch;
- pull;
- push;
- reset;
- clean;
- restore;
- stash;
- change branches;
- create tags;
- change Git configuration.

---

# Gate M — Index Lock / Competing Git Mutation

Before execution, detect an existing Git index lock or equivalent clear evidence that another Git index mutation is active.

Fail closed with a reason equivalent to:

    git_index_locked

Do not delete another process's lock automatically.

Do not retry blindly.

---

# Gate N — Post-Stage Mechanical Verification

Do not trust `git add` exit code alone.

Immediately verify:

1. HEAD is unchanged;
2. branch is unchanged;
3. staged changes now exist;
4. staged path set exactly equals the approved plan's candidate set;
5. staged object identities match the plan's expected identities;
6. staged modes/deletions match the plan;
7. no unstaged changes remain;
8. no visible untracked files remain;
9. no conflicts exist;
10. no Git operation is active.

Expected final workflow state:

    staged_only

The intent of M008 is to move the entire currently visible candidate set into the index so M007 can subsequently operate.

Do not create a commit.

Do not automatically create a snapshot.

---

# Gate O — Verification Failure After Staging

If Git staging occurs but post-stage verification fails:

    DO NOT RESET
    DO NOT RESTORE
    DO NOT UNSTAGE
    DO NOT CLEAN
    DO NOT RETRY

Return:

    post_stage_verification_failed

and report current deterministic repository state.

Once mutation has occurred, Repo Control Plane must not hide it by attempting automatic rollback.

This mirrors M007's post-commit safety rule.

---

# Gate P — Git Stage Command Failure / Partial Mutation

A Git staging command may theoretically fail after changing part of the index.

Therefore, after a non-zero Git staging result, inspect the index before reporting failure.

Distinguish:

    git_stage_failed

when no index mutation occurred

from:

    git_stage_failed_after_mutation

when the index differs from the pre-execution state.

For:

    git_stage_failed_after_mutation

report clearly that staging state changed.

Do NOT:

- unstage automatically;
- reset automatically;
- retry automatically.

Return the current deterministic state and require human review.

This failure mode must be tested through controlled injection where practical.

---

# Gate Q — Immutable Stage Execution Evidence

After successful staging and successful verification, write immutable external execution evidence under a path conceptually equivalent to:

    ~/.local/share/repoctl/<repo-id>/workflow/stage_executions/<execution-id>/

containing:

    execution.json
    execution.md

Record at minimum:

- schema version;
- execution ID;
- plan ID;
- repository ID/root;
- branch;
- HEAD before;
- HEAD after, which should be identical;
- candidate fingerprint;
- resulting staged fingerprint;
- exact staged path/status summary;
- object/mode verification results;
- resulting workflow state;
- remote refresh performed = false;
- commit performed = false;
- push performed = false.

Prefer deterministic/content-derived execution IDs.

Existing identical immutable execution evidence may be reused only after integrity verification.

Never overwrite different content at the same deterministic ID.

---

# Gate R — Audit Failure After Successful Staging

If:

    Git staging succeeds
        ↓
    mechanical verification succeeds
        ↓
    external execution-audit persistence fails

the CLI must clearly report:

    STAGING SUCCEEDED

and preserve the resulting staged state.

Return a distinct condition equivalent to:

    stage_succeeded_audit_failed

Do not imply the staging operation should be retried.

Do not automatically unstage.

This is the staging equivalent of M007:

    commit_succeeded_audit_failed

---

# Snapshot Semantics

M008 does NOT require a matching snapshot before staging.

This is intentional.

Before staging, the repository may contain:

- unstaged modifications;
- untracked files;

which are precisely what M008 is preparing to place into Git's index.

After successful M008 execution, the intended next evidence step is:

    repoctl snapshot

That snapshot captures the exact staged repository state used by M007's:

    matching_snapshot_required

gate.

Do not automatically snapshot from M008.

The separation remains:

    stage
        ↓
    inspect / snapshot
        ↓
    prepare commit

---

# No AI Authorization

Do not call GPT-OSS during:

    prepare-stage
    stage

AI must not:

- select files;
- exclude files;
- approve files;
- determine whether staging is allowed;
- rewrite plan evidence.

GPT-OSS remains advisory only.

---

# Stable Reason / Error Codes

Provide machine-readable distinctions suitable for a future GUI.

At minimum support conditions equivalent to:

    approval_required
    detached_head
    staged_changes_present
    no_stage_candidates
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
    git_stage_failed
    git_stage_failed_after_mutation
    post_stage_verification_failed
    stage_succeeded_audit_failed

Use more specific codes where useful, but do not collapse materially different mutation states into a generic:

    stage failed

when deterministic facts distinguish them.

---

# Test Isolation — Hard Requirement

All staging mutation tests must use disposable temporary repositories.

Never perform M008 staging tests against:

- Repo Control Plane development repository;
- Vocab App;
- Photo Organizer.

Never create synthetic conflict/Git-operation markers inside the actual development repository.

Automated tests must leave Repo Control Plane's own repository untouched except for intentional milestone source/test/doc changes created by the coder.

---

# Required Automated Tests

Add focused tests covering at minimum:

## Prepare success

Starting state:

- attached branch;
- no staged changes;
- unstaged and/or untracked eligible changes;
- no conflicts;
- no active Git operation.

Verify:

- exact candidate enumeration;
- deterministic expected staged identities;
- immutable plan creation;
- target HEAD unchanged;
- target index unchanged;
- target worktree unchanged.

## Prepare blocks

- detached HEAD;
- existing staged changes;
- no changes;
- conflict;
- active Git operation;
- unsupported path type;
- custom Git filter.

## Plan determinism / integrity

- repeated identical prepare => identical plan ID;
- existing valid plan reused after integrity verification;
- corrupted plan JSON blocked;
- tampered plan content blocked;
- plan ID/content mismatch blocked.

## Approval

- stage without `--approve` => no mutation;
- correct plan + approval => eligible for execution.

## Stale plan

Prepare a valid plan and then independently change:

- file contents;
- untracked file contents;
- candidate path set;
- deletion/restoration state;
- mode where practical;
- branch;
- HEAD.

Each must block before staging.

## Exact successful staging

Verify:

- HEAD unchanged;
- exact approved paths staged;
- expected object IDs match actual staged IDs;
- expected modes/deletions match;
- no unstaged changes;
- no visible untracked files;
- final state `staged_only`;
- no commit created;
- execution evidence created.

## Ignored files

Confirm ordinary ignored files are not accidentally included or staged.

## Git stage failure

Inject controlled failure before index mutation and verify:

    git_stage_failed

with unchanged index.

## Failure after partial mutation

Inject or simulate a controlled partial-index mutation failure where practical and verify:

    git_stage_failed_after_mutation

with:

- no automatic reset;
- no automatic unstage;
- current staged state reported.

## Post-stage verification failure

Inject controlled verification failure after successful staging.

Verify:

- staging remains;
- no automatic rollback;
- `post_stage_verification_failed`;
- current index state reported.

## Audit failure

Inject external audit-write failure after successful verified staging.

Verify:

- staged state remains;
- `stage_succeeded_audit_failed`;
- no second staging attempt;
- no automatic unstage.

## CLI

Validate:

    prepare-stage --all
    stage <plan_id> --approve

as thin adapters over reusable services.

---

# Practical Validation

Use a disposable isolated Git repository.

Demonstrate:

    init temporary repo
        ↓
    initial commit
        ↓
    modify tracked file
        ↓
    add regular untracked file
        ↓
    optionally delete a tracked file
        ↓
    repoctl milestone prepare-stage --all
        ↓
    inspect exact plan
        ↓
    verify HEAD/index unchanged
        ↓
    repoctl milestone stage <plan-id> --approve
        ↓
    verify HEAD unchanged
        ↓
    verify exact planned paths staged
        ↓
    verify no unstaged/untracked visible changes
        ↓
    verify workflow state staged_only
        ↓
    verify execution evidence

Then demonstrate stale-plan refusal:

    create new unstaged change
        ↓
    prepare valid plan
        ↓
    modify one candidate after preparation
        ↓
    attempt approved stage
        ↓
    BLOCK
        ↓
    verify index unchanged

---

# M007 Integration Validation

In a disposable repository, demonstrate the intended combined local workflow:

    create working-tree changes
        ↓
    prepare-stage --all
        ↓
    approve stage
        ↓
    verify staged_only
        ↓
    repoctl snapshot
        ↓
    repoctl milestone prepare-commit --message "..."
        ↓
    verify commit plan can now be prepared

A full M007 commit execution may also be demonstrated if useful, but is not required solely to prove M008.

The important integration requirement is that successful M008 output is directly compatible with M007's staged-only and matching-snapshot model.

---

# Full Regression Validation

Run focused M008 tests.

Then:

    PYTHONPATH=src python3 -m unittest -q

under ordinary Python bytecode behavior.

Do NOT use:

    PYTHONDONTWRITEBYTECODE=1

M006.1 hygiene must remain effective.

After tests verify:

- no `.pyc` / `__pycache__` Git noise;
- no synthetic Git operation marker;
- no changed development-repository HEAD;
- no staged test artifacts in Repo Control Plane itself.

---

# Expected Source Shape

Prefer adding purpose-specific workflow services alongside M007.

Conceptually:

    workflow/
        git_state.py
        status.py
        errors.py
        commit_plan.py
        commit_execution.py
        stage_plan.py
        stage_execution.py

Exact filenames may vary if a smaller clean design is appropriate.

Reuse `WorkflowReasonError` if it remains the correct abstraction.

Do not create a second incompatible workflow error system.

Do not duplicate the M006 Git-state parser.

Do not create a generic arbitrary Git command runner.

---

# Human-Readable Output Direction

The CLI remains an engineering interface, but output should be deliberately usable by a human and structured for eventual GUI rendering.

Prefer output that communicates:

- repository;
- branch;
- HEAD;
- exact file count;
- exact path/status list;
- plan ID;
- whether mutation occurred;
- exact next operator action.

Do not make the operator interpret raw JSON for ordinary use.

Keep structured JSON artifacts authoritative underneath.

---

# Explicit Non-Goals

Do not implement:

- selective path staging;
- partial-hunk staging;
- interactive staging;
- automatic file selection;
- AI file selection;
- commit execution as part of staging;
- automatic snapshot creation;
- push;
- fetch;
- pull;
- remote refresh;
- branch creation/deletion;
- switch/checkout;
- merge;
- rebase;
- cherry-pick;
- revert;
- reset;
- restore;
- stash;
- clean;
- Git LFS/custom filter support;
- submodule staging;
- broad symlink support unless explicitly proven;
- GUI;
- REST API;
- GitHub API integration;
- credential handling;
- Photo Organizer validation.

---

# No Generic Git Escape Hatch

Do not add:

    repoctl git <args>

or:

    repoctl exec-git

All mutations must remain purpose-specific.

After M008, the only supported target Git mutation primitives should remain conceptually:

    execute prepared staging plan
    execute prepared commit plan

---

# Implementation Discipline

The expected M008 implementation is:

    inspect deterministic Git state
        ↓
    require clean index
        ↓
    enumerate all eligible visible changes
        ↓
    calculate exact expected staged identities
        ↓
    create immutable stage plan
        ↓
    operator reviews exact file list
        ↓
    explicit plan-specific approval
        ↓
    revalidate exact state
        ↓
    stage exact path set
        ↓
    mechanically verify exact index result
        ↓
    record immutable execution evidence

Do not broaden the milestone into general Git workflow automation.

---

# Escalation Protocol

STOP and report rather than broadening scope if:

- exact prospective staged identity cannot be computed read-only;
- Git clean/filter behavior makes staging nondeterministic or externally executable;
- candidate enumeration cannot safely distinguish exact paths;
- M006 state parsing would need broad redesign;
- staging can only be implemented using uncontrolled directory-wide pathspecs;
- exact post-stage object verification cannot be established;
- a test contaminates the Repo Control Plane development repository;
- partial index mutation occurs unexpectedly during practical validation;
- any requirement would force Photo Organizer access.

Report:

1. exact gate;
2. observed state;
3. expected state;
4. mutations already performed;
5. whether index mutation occurred;
6. rollback performed or not;
7. current HEAD/status;
8. smallest next decision required.

Never automatically repair an ambiguous staging state.

---

# Required Closeout

Create:

`docs/008_guarded_staging_preparation_closeout.md`

Include:

1. status — PASS or ESCALATION;
2. initial branch / HEAD / clean preflight;
3. files changed;
4. core service architecture;
5. CLI commands implemented;
6. mechanical prepare preconditions;
7. candidate enumeration contract;
8. supported path types;
9. Git filter/attribute boundary;
10. prospective staged-object identity method;
11. stage-candidate fingerprint contract;
12. immutable plan schema/storage;
13. prepare read-only evidence;
14. explicit approval behavior;
15. stale-plan revalidation behavior;
16. exact staging execution behavior;
17. index-lock handling;
18. post-stage verification;
19. Git-stage failure/partial-mutation behavior;
20. execution evidence schema/storage;
21. audit-failure-after-stage behavior;
22. stable reason/error codes;
23. focused test result;
24. full regression result;
25. Python-cache hygiene result;
26. practical isolated-repository success validation;
27. stale-plan practical validation;
28. M007 integration validation;
29. confirmation no network mutation occurred;
30. confirmation no commit occurred during M008 staging path;
31. confirmation no Vocab App mutation occurred;
32. confirmation no Photo Organizer access occurred;
33. limitations/deferred items;
34. recommendation for next milestone;
35. literal final `git status --short`.

Do not commit or push unless separately instructed.

---

# Acceptance Criteria

Milestone 008 passes only if:

- `prepare-stage` is target-repository read-only;
- starting index must contain zero staged changes;
- conflicts and active Git operations block;
- candidate set is exact and deterministic;
- ignored files are excluded;
- unsupported path types fail closed;
- custom Git content filters fail closed;
- prospective staged blob identities are calculated without writing Git objects;
- immutable stage plans are integrity checked;
- repeated identical plans have deterministic identity;
- explicit exact-plan approval is required;
- missing approval performs no mutation;
- branch changes invalidate the plan;
- HEAD changes invalidate the plan;
- candidate content changes invalidate the plan;
- candidate path-set changes invalidate the plan;
- execution stages only exact reviewed paths;
- no broad recomputed `git add .` / uncontrolled `git add -A` occurs;
- no commit occurs;
- no network mutation occurs;
- post-stage HEAD is unchanged;
- actual staged object identities match approved expected identities;
- actual staged path set matches the approved plan;
- successful result is `staged_only`;
- no visible unstaged/untracked candidate changes remain;
- index-lock conditions fail closed;
- stage failure without mutation is distinguished from failure after index mutation;
- no automatic reset/restore/unstage occurs after uncertain mutation;
- post-stage verification failure preserves staged evidence;
- audit failure after successful staging clearly reports that staging succeeded;
- immutable stage execution evidence is created after successful verification;
- M008 staged output is compatible with M007 after an explicit snapshot;
- all mutation tests use disposable repositories;
- full regression suite passes;
- Python cache hygiene remains effective;
- Repo Control Plane development repository is not contaminated by test state;
- no Vocab App mutation occurs;
- no Photo Organizer access occurs;
- CLI remains a thin adapter over reusable core services suitable for a future GUI.

Successful M008 establishes the complete bounded local pre-commit mutation chain:

    prepare-stage
        ↓
    approve stage
        ↓
    snapshot
        ↓
    prepare-commit
        ↓
    approve commit

After this foundation is proven, the next milestone can decide between adding controlled remote/push workflow or beginning the first browser-based Repo Control Plane user interface without weakening the M007/M008 transaction model.
