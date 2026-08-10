# Milestone 007 — Guarded Git Write Foundation

Prompt file:

`007_guarded_git_write_foundation_prompt.md`

Required closeout file:

`007_guarded_git_write_foundation_closeout.md`

## Objective

Introduce Repo Control Plane's first deliberately bounded Git mutation:

    prepare an immutable commit plan
        ↓
    present exact human-readable evidence
        ↓
    require explicit operator approval
        ↓
    revalidate exact repository state
        ↓
    create one ordinary local Git commit
        ↓
    verify the resulting repository state
        ↓
    record immutable execution evidence

Milestone 007 establishes the safety architecture for future Git-write operations.

This milestone is intentionally limited to:

    prepared local commit execution

It does NOT yet automate:

- staging;
- push;
- fetch;
- pull;
- branch creation;
- checkout/switch;
- merge;
- rebase;
- cherry-pick;
- revert;
- reset;
- amend;
- tagging.

The operator remains responsible for deciding what should be staged before preparing the commit.

---

# Architectural Intent

Repo Control Plane has completed its read-only intelligence foundation through Milestones 001–006 and repository hygiene through 006.1.

The current evidence hierarchy remains:

    authoritative repository source/tests
        ↓
    deterministic Repo Control Plane facts
        ↓
    immutable snapshots/comparisons
        ↓
    advisory GPT-OSS interpretation

Git mutation must not reverse that hierarchy.

Repo Control Plane must never allow GPT-OSS, another AI component, or prose interpretation to authorize Git mutation.

The mutation decision must be based on exact deterministic state plus explicit human approval.

---

# Future GUI Compatibility — Hard Design Requirement

Milestone 007 must NOT embed Git-write policy only inside CLI command handlers.

Implement reusable core services representing concepts equivalent to:

    prepare_commit(...)
    execute_prepared_commit(...)

The CLI must remain a thin adapter around those services.

Core services must return structured results suitable for reuse by a future browser-based Repo Control Plane UI.

Do not require interactive terminal prompts inside the core service.

Conceptually:

    Repo Control Plane Core
        ├── deterministic Git state
        ├── prepare commit plan
        ├── validate plan
        ├── execute commit
        └── verify result
    
             ▲               ▲
             │               │
           CLI now        Web UI later

The future GUI must use the same mutation path and safety rules as the CLI.

Do NOT implement the web UI or HTTP API in this milestone.

---

# Project

Repo Control Plane:

`/home/chuck/projects/repo-control`

Photo Organizer remains explicitly out of scope.

Do not inspect, scan, modify, or otherwise access Photo Organizer.

Do not mutate Vocab App for validation.

Any Git-mutation validation must use isolated temporary Git repositories created specifically for tests/validation.

---

# Required Reading

Read and preserve:

- Repo Control Plane architecture / implementation plan
- Milestone 004 prompt and closeout
- Milestone 005 / 005.1 prompt and closeout
- Milestone 006 prompt and closeout
- Milestone 006.1 prompt and closeout

Especially preserve:

- deterministic evidence before AI interpretation;
- immutable external evidence;
- fail-closed Git parsing;
- canonical porcelain-v2 handling;
- M006 workflow-state semantics;
- no network refresh;
- local-ref upstream caveat;
- no generated Python-cache Git noise.

Do not broadly re-reconnoiter the repository.

Inspect only the files/services/tests materially required for this milestone.

---

# Initial Git Preflight

Before coding:

1. confirm branch;
2. confirm HEAD;
3. confirm worktree/index clean;
4. confirm no active Git operation;
5. confirm Milestone 006.1 hygiene is committed.

At minimum establish:

    git branch --show-current
    git rev-parse HEAD
    git status --short

If the Repo Control Plane development repository is not clean:

    STOP

Do not reset, restore, clean, stash, or discard unexplained state.

Do not commit or push unless separately instructed.

---

# User-Facing Commands

Implement commands equivalent to:

    repoctl milestone prepare-commit \
        --message "<commit message>" \
        [--repository <path>]

and:

    repoctl milestone commit <plan_id> \
        --approve \
        [--repository <path>]

Exact argparse organization may follow the existing CLI architecture, but preserve these semantics.

The first command is read-only with respect to the target Git repository.

The second command is the explicitly approved mutation.

---

# Gate A — Mechanical Commit Preconditions

`prepare-commit` must fail closed unless all required mechanical conditions are satisfied.

At minimum require:

    branch_attached == true
    
    staged_changes_present == true
    
    unstaged_changes_present == false
    
    untracked_changes_present == false
    
    unmerged_entries_present == false
    
    git_operation_in_progress == false

This deliberately limits Milestone 007 to a fully staged-only state.

Do not silently stage unstaged files.

Do not silently include untracked files.

Do not ignore conflicts.

Do not allow detached HEAD commits.

Do not allow a commit during:

- merge;
- rebase;
- cherry-pick;
- revert;
- bisect or another M006-recognized operation that makes the state inappropriate.

Reuse the deterministic Git-state machinery from Milestone 006 rather than creating a second incompatible status parser.

---

# Gate B — Matching Snapshot Required

Before a commit plan may be prepared, the exact current repository state must have a matching immutable Repo Control Plane snapshot.

Reuse the M006 current-snapshot-candidate / matching-snapshot logic.

If no exact matching snapshot exists:

    prepare-commit must fail closed

with a structured reason equivalent to:

    matching_snapshot_required

Human-readable output should explain that the operator should first run:

    repoctl snapshot

Do not automatically create the snapshot as part of commit execution.

The purpose is to ensure the state being committed has already been captured as deterministic evidence.

The matching snapshot ID must be recorded in the commit plan.

---

# Gate C — Commit Message

A commit plan must contain the exact intended commit message.

Reject:

- missing message;
- empty message;
- NUL-containing message.

Do not synthesize a message with AI.

Do not rewrite the operator's commit message with GPT-OSS.

Do not infer a commit message from the diff.

The exact approved message must be carried from plan preparation into execution.

---

# Gate D — Exact Staged-State Fingerprint

A commit plan must identify the exact Git index state that the operator reviewed.

Do not rely only on filenames.

The fingerprint must capture the exact staged delta relative to current HEAD using deterministic Git evidence including, as appropriate:

- HEAD object ID;
- path;
- staged status;
- old/new object IDs;
- old/new modes;
- additions;
- modifications;
- deletions.

Disable rename heuristics for the fingerprint if necessary so identity does not depend on heuristic rename detection.

Use deterministic Git plumbing/read-only commands.

Do not use source-text parsing for this purpose.

The fingerprint must change if staged content changes even when the filename does not.

It must also detect:

- added staged file changed after plan preparation;
- modified staged file changed and restaged;
- staged deletion changed;
- staged mode change;
- changed staged file set.

The plan must not contain source-file bodies or a full textual diff.

A bounded human-readable file/status summary is sufficient.

---

# Gate E — Immutable Commit Plan

Store commit plans outside the target repository under the existing Repo Control Plane external state hierarchy, conceptually:

    ~/.local/share/repoctl/<repo-id>/workflow/commit_plans/<plan-id>/

containing:

    plan.json
    plan.md

The plan must be immutable.

The plan should contain at minimum:

- schema version;
- plan ID;
- repository ID;
- canonical repository root;
- branch;
- HEAD before commit;
- exact staged-state fingerprint;
- deterministic staged file/status summary;
- matching snapshot ID;
- exact commit message;
- relevant mechanical precondition facts;
- locally known upstream information where available;
- explicit statement that no remote refresh was performed.

Do not store:

- remote credentials;
- repository source bodies;
- full textual diffs;
- GPT-OSS reasoning;
- hidden model reasoning.

Prefer a content-derived plan ID so repeated preparation of the exact same repository state and exact same message produces the same plan ID.

Do not include incidental timestamps in content-derived identity.

---

# Gate F — Human-Readable Plan

`prepare-commit` must produce concise human-readable output suitable for both terminal use now and eventual GUI rendering.

Conceptually:

    PREPARED COMMIT
    
    Repository: repo-control
    Branch:     main
    HEAD:       abc123...
    
    Snapshot:
    snap--...
    
    Staged files: 4
    
      M src/repoctl/...
      A tests/...
      A docs/...
    
    Unstaged:    0
    Untracked:   0
    Conflicts:   0
    Git op:      none
    
    Commit message:
    
      Complete Milestone 007 ...
    
    Plan:
    commit-plan--...
    
    NO GIT MUTATION PERFORMED
    
    To explicitly approve this exact plan:
    
      repoctl milestone commit <plan-id> --approve

Do not describe the plan as:

    safe
    approved
    correct
    architecture-valid

It is a deterministic mutation proposal, not a quality judgment.

---

# Gate G — Prepare Must Be Target-Repository Read Only

`prepare-commit` must not mutate target Git state.

It must not:

- stage;
- unstage;
- commit;
- create branches;
- update refs;
- create tags;
- fetch;
- push;
- pull;
- reset;
- restore;
- stash;
- create synthetic Git-operation markers.

Capture and verify appropriate before/after evidence in tests.

External Repo Control Plane plan artifacts are allowed.

Do not use Git commands that create repository objects merely as a side effect of plan preparation.

---

# Gate H — Explicit Approval

Commit execution requires BOTH:

1. an existing immutable plan ID;
2. an explicit approval signal.

CLI syntax:

    repoctl milestone commit <plan_id> --approve

If `--approve` is absent:

    fail without mutation

with structured reason equivalent to:

    approval_required

The plan ID identifies exactly what was reviewed.

Approval applies only to that exact immutable plan.

There must be no:

    repoctl milestone commit --yes

that recomputes and commits whatever happens to be current.

There must be no implicit "commit latest plan."

The exact plan ID is required.

---

# Gate I — Revalidation Immediately Before Mutation

Before invoking `git commit`, reload and validate the immutable plan and recompute all important deterministic facts.

Require exact equality for at least:

    repository identity
    canonical repository root
    attached branch
    branch name
    HEAD
    staged-state fingerprint
    matching repository state assumptions
    no unstaged changes
    no untracked files
    no conflicts
    no active Git operation

If anything changed after plan preparation:

    FAIL CLOSED

Do not automatically regenerate the plan.

The operator must run `prepare-commit` again and review the new plan.

Examples:

    plan prepared
        ↓
    staged file changed
        ↓
    commit attempted

Result:

    BLOCK

Similarly:

    plan prepared
        ↓
    HEAD changed
        ↓
    BLOCK

and:

    plan prepared
        ↓
    branch changed
        ↓
    BLOCK

---

# Gate J — Git Hooks / External Mutation Boundary

Milestone 007 must not pretend ordinary Git hooks are deterministic Repo Control Plane behavior.

Before commit execution, detect commit-related custom hook conditions sufficiently to avoid silently running unknown repository automation.

For this milestone, fail closed if an active executable/custom commit hook would run, including relevant hooks such as:

- pre-commit;
- prepare-commit-msg;
- commit-msg;
- post-commit;

or if a custom `core.hooksPath` makes safe bounded behavior uncertain.

Do NOT solve this by silently using:

    --no-verify

Repo Control Plane should not bypass repository safeguards without an explicit future design.

Hook-aware commit support may be added later.

Document the limitation clearly.

---

# Gate K — Git Identity

Before mutation, verify Git has sufficient author/committer identity for an ordinary commit.

Do not invent:

    user.name
    user.email

Do not modify Git configuration automatically.

If identity is unavailable:

    fail closed

with a clear structured reason.

---

# Gate L — Exact Commit Execution

After all gates pass and explicit approval is present, create exactly one ordinary local commit using the exact approved commit message.

Do not:

- stage additional files;
- amend;
- sign;
- push;
- fetch;
- merge;
- rebase;
- tag;
- alter author identity;
- change Git configuration.

Prevent interactive editor behavior.

Disable implicit signing if necessary for bounded execution rather than invoking external signing machinery.

Do not use shell-string command construction.

Invoke Git with a structured subprocess argument list.

No shell interpolation of:

- plan ID;
- file path;
- commit message;
- repository path.

---

# Gate M — Post-Commit Verification

Immediately after successful `git commit`, mechanically verify the result.

At minimum verify:

1. HEAD changed;
2. new commit has previous HEAD as its parent;
3. current branch is still the planned branch;
4. the committed delta corresponds to the exact staged delta represented by the approved plan;
5. index no longer contains staged changes;
6. worktree is clean;
7. no conflict appeared;
8. no unexpected Git operation is active.

Do not rely only on the process exit code.

The exact committed file/content footprint must be mechanically reconciled against the prepared plan.

If the Git command succeeds but verification fails:

    DO NOT RESET
    DO NOT REVERT
    DO NOT RETRY

Report:

    ESCALATION REQUIRED

and provide:

- old HEAD;
- resulting HEAD;
- failed verification fact;
- current deterministic status.

Once a commit has occurred, Repo Control Plane must never hide or silently undo it because post-verification failed.

---

# Gate N — Immutable Execution Evidence

After successful commit and successful verification, write external immutable execution evidence, conceptually:

    ~/.local/share/repoctl/<repo-id>/workflow/commit_executions/<execution-id>/

with:

    execution.json
    execution.md

Record at minimum:

- plan ID;
- repository ID;
- branch;
- HEAD before;
- HEAD after;
- commit message;
- matching snapshot ID used by the plan;
- staged-state fingerprint;
- deterministic committed file/status summary;
- verification results;
- remote refresh performed = false;
- push performed = false.

Do not store full source bodies or full diffs.

A content-derived execution ID based on the resulting commit identity is preferred.

---

# Gate O — Audit Failure After Successful Commit

A particularly important failure case:

    Git commit succeeds
        ↓
    external Repo Control Plane audit write fails

The CLI must clearly report that:

    THE COMMIT SUCCEEDED

and expose the resulting commit ID.

Do not return an ambiguous message that encourages the operator to retry the commit.

Do not automatically create another commit.

Use a distinct structured condition equivalent to:

    commit_succeeded_audit_failed

This condition should be tested.

---

# Structured Error / Result Codes

Provide stable machine-readable reason codes suitable for a future GUI.

At minimum support distinctions equivalent to:

    approval_required
    detached_head
    no_staged_changes
    unstaged_changes_present
    untracked_changes_present
    conflicts_present
    git_operation_in_progress
    matching_snapshot_required
    invalid_commit_message
    plan_not_found
    plan_integrity_failed
    repository_mismatch
    branch_changed
    head_changed
    staged_state_changed
    unsupported_git_hooks
    git_identity_unavailable
    git_commit_failed
    post_commit_verification_failed
    commit_succeeded_audit_failed

Exact internal exception organization is implementation-specific.

Do not collapse materially different safety failures into generic:

    commit failed

when the exact deterministic reason is known.

---

# Upstream / Remote Semantics

Milestone 007 remains local-only.

Do not:

    fetch
    pull
    push

during prepare or commit execution.

If upstream information is available through M006 local refs, display it with the existing caveat:

    no remote refresh performed

Do not claim the local divergence information reflects the current remote server.

Upstream state is not an authorization mechanism for this first local commit milestone.

No remote URL should be written into human-readable evidence.

---

# No AI Authorization

GPT-OSS must not participate in commit authorization.

Do not call Ollama during:

    prepare-commit
    commit

Do not require an AI analysis to approve or deny the operation.

A prior GPT-OSS analysis may exist as advisory evidence elsewhere, but it has no authority over Git mutation.

The commit plan must be fully derivable from deterministic local Git/Repo Control Plane state.

---

# Test Fixture Isolation — Hard Requirement

Milestone 006 exposed why Git-state tests must be isolated.

Never create synthetic files such as:

    .git/MERGE_HEAD
    .git/REBASE_HEAD
    .git/CHERRY_PICK_HEAD

inside the actual Repo Control Plane development repository for testing.

All destructive or synthetic Git-state fixtures must live in isolated temporary repositories.

Automated tests must clean them up through fixture lifecycle.

The full test suite must not leave Repo Control Plane itself with:

- fake Git-operation markers;
- staged files;
- unstaged files;
- untracked test artifacts;
- changed HEAD;
- changed branch.

Capture Repo Control Plane development-repository status before and after practical validation where useful.

---

# Required Automated Tests

Add focused tests covering at minimum:

## Prepare success

- attached branch;
- staged-only changes;
- matching snapshot exists;
- no conflicts;
- no Git operation;
- valid commit message;
- plan created;
- target HEAD unchanged;
- target index unchanged;
- target worktree unchanged.

## Prepare blocks

- detached HEAD;
- no staged changes;
- unstaged change present;
- untracked file present;
- conflict;
- active merge;
- active rebase or other supported operation;
- missing matching snapshot;
- invalid commit message.

## Plan integrity

- corrupted plan JSON;
- tampered plan content;
- plan ID/content mismatch;
- wrong repository.

## Stale plan

Prepare a valid plan, then independently change:

- branch;
- HEAD;
- staged content;
- staged file set;
- staged mode where practical.

Each must block without commit.

## Approval

- commit without `--approve` => no mutation;
- commit with correct plan + approval => allowed.

## Hook boundary

- executable relevant hook => blocked;
- custom hooksPath uncertainty => blocked according to the implemented contract.

## Successful commit

Verify:

- exactly one new commit;
- correct parent;
- exact approved message;
- exact staged delta committed;
- no push/fetch;
- clean final worktree;
- execution evidence written.

## Git commit failure

Simulate a controlled commit failure and verify no false success record is written.

## Post-verification failure

Where practical, inject a controlled verification failure after commit and verify:

- no reset;
- no revert;
- no retry;
- resulting commit ID clearly reported;
- escalation state preserved.

## Audit failure

Inject an external evidence-write failure after successful Git commit and verify:

- commit remains;
- resulting commit ID returned;
- condition is clearly `commit_succeeded_audit_failed`;
- no retry/second commit occurs.

---

# Practical Validation

Use an isolated temporary repository.

Do not mutate Vocab App or Photo Organizer.

Demonstrate this exact lifecycle:

    create temporary Git repo
        ↓
    initial commit
        ↓
    make controlled source change
        ↓
    stage it manually
        ↓
    create matching repoctl snapshot
        ↓
    repoctl milestone prepare-commit
        ↓
    inspect plan
        ↓
    verify target HEAD unchanged
        ↓
    repoctl milestone commit <plan-id> --approve
        ↓
    verify exactly one commit
        ↓
    verify exact message/content
        ↓
    verify clean repository
        ↓
    verify immutable execution evidence

Also demonstrate at least one stale-plan refusal:

    prepare valid plan
        ↓
    change staged content
        ↓
    attempt approved execution
        ↓
    BLOCK
        ↓
    HEAD unchanged

---

# Regression Validation

Run the focused Milestone 007 tests.

Then run the full Repo Control Plane suite under ordinary Python behavior:

    PYTHONPATH=src python3 -m unittest -q

Do not use `PYTHONDONTWRITEBYTECODE=1`.

Milestone 006.1 hygiene must remain effective.

After the test suite, confirm there is no generated `.pyc` / `__pycache__` Git noise.

Confirm no synthetic Git-operation marker remains in the Repo Control Plane development repository.

---

# Expected Source Shape

Prefer a small dedicated workflow mutation/service area that composes existing M006 Git-state functionality.

Do not put all mutation logic directly in:

    cli.py

Do not duplicate the M006 porcelain parser.

Do not create a generic "run arbitrary Git command" abstraction exposed to the user.

The core API should remain purpose-specific and bounded.

Conceptually acceptable:

    workflow/
        status.py
        git_state.py
        commit_plan.py
        commit_execution.py

Exact filenames may differ if the existing architecture suggests a cleaner minimal organization.

---

# No Generic Git Escape Hatch

Do NOT add functionality equivalent to:

    repoctl git <arbitrary args>

or:

    repoctl exec-git

Repo Control Plane mutation surfaces must be named and purpose-specific.

For Milestone 007, the only permitted target mutation is:

    one ordinary prepared local commit

---

# Explicit Non-Goals

Do not implement:

- automatic staging;
- file-selection UI;
- web GUI;
- REST API;
- push;
- fetch;
- pull;
- branch creation;
- branch deletion;
- checkout;
- switch;
- merge;
- rebase;
- cherry-pick;
- revert;
- reset;
- amend;
- commit signing;
- hook execution support;
- AI commit-message generation;
- AI mutation approval;
- milestone-number inference;
- closeout parsing;
- test-result gating;
- CI integration;
- GitHub API integration;
- credential handling;
- remote mutation;
- Photo Organizer validation.

These belong to later milestones.

---

# Implementation Discipline

The intended safety flow is:

    inspect exact deterministic state
        ↓
    require staged-only repository
        ↓
    require exact matching snapshot
        ↓
    fingerprint exact staged delta
        ↓
    create immutable plan
        ↓
    human reviews plan
        ↓
    explicit plan-specific approval
        ↓
    reload plan
        ↓
    revalidate everything
        ↓
    one local Git commit
        ↓
    mechanically verify commit
        ↓
    write immutable execution evidence

Do not compress:

    prepare
    approve
    execute

into a single command.

The separation is fundamental to the future GUI and human-control model.

---

# Escalation Protocol

STOP and report rather than broadening scope if:

- M006 Git-state machinery cannot safely support exact preconditions;
- deterministic staged fingerprinting cannot be implemented without target mutation;
- matching-snapshot semantics prove incompatible with staged-only state;
- ordinary Git commit behavior cannot be bounded because of hooks/configuration;
- post-commit verification cannot establish exact staged-delta correspondence;
- implementation would require broad scanner/snapshot redesign;
- tests reveal mutation of the Repo Control Plane development repository itself;
- any requirement would force Photo Organizer access;
- a successful commit occurs but post-verification or audit persistence fails unexpectedly.

Report:

1. exact gate;
2. observed state;
3. expected state;
4. mutations already performed;
5. rollback performed or not;
6. repository HEAD/status;
7. smallest next decision required.

Never automatically repair an ambiguous Git mutation state.

---

# Required Closeout

Create:

`docs/007_guarded_git_write_foundation_closeout.md`

Include:

1. status — PASS or ESCALATION;
2. initial branch / HEAD / clean preflight;
3. files changed;
4. core service architecture;
5. CLI commands implemented;
6. mechanical commit preconditions;
7. snapshot requirement;
8. staged fingerprint contract;
9. immutable plan schema/storage;
10. explicit approval behavior;
11. stale-plan revalidation behavior;
12. hook boundary;
13. Git identity behavior;
14. exact commit execution behavior;
15. post-commit verification;
16. execution evidence schema/storage;
17. audit-failure-after-commit behavior;
18. stable reason/error codes;
19. focused test result;
20. full regression result;
21. Python-cache hygiene result;
22. practical isolated-repository validation;
23. stale-plan practical validation;
24. confirmation no network mutation occurred;
25. confirmation no Vocab App mutation occurred;
26. confirmation no Photo Organizer access occurred;
27. limitations/deferred items;
28. recommendation for next milestone;
29. final `git status --short`.

Do not commit or push unless separately instructed.

---

# Acceptance Criteria

Milestone 007 passes only if:

- `prepare-commit` is target-repository read-only;
- commit plans are immutable and integrity-checked;
- plans describe an exact staged repository state;
- staged content changes invalidate a plan;
- branch changes invalidate a plan;
- HEAD changes invalidate a plan;
- repository mismatch invalidates a plan;
- a matching Repo Control Plane snapshot is required;
- no unstaged/untracked/conflicted state is accepted;
- active Git operations block preparation/execution;
- explicit approval is required;
- missing approval performs no mutation;
- custom/active commit hooks fail closed under the M007 contract;
- Git identity is verified without automatic configuration;
- approved execution creates exactly one ordinary local commit;
- no automatic staging occurs;
- no fetch/pull/push occurs;
- no amend occurs;
- no signing occurs;
- no AI participates in authorization;
- resulting commit is mechanically verified against the plan;
- failed post-verification never triggers automatic reset/revert/retry;
- successful commit plus audit failure is unambiguously reported as commit succeeded;
- immutable execution evidence is created after successful verification;
- all Git-mutation tests use isolated temporary repositories;
- the full regression suite passes;
- ordinary Python validation creates no Git cache noise;
- Repo Control Plane's own development repository is not contaminated by test Git-operation markers;
- no Vocab App mutation occurs;
- no Photo Organizer access occurs;
- CLI logic remains a thin adapter over reusable core services suitable for the future browser GUI.

Successful completion establishes the first trusted human-approved Git-write primitive for Repo Control Plane.

The next milestones may then build higher-level workflow operations—such as controlled staging, richer milestone review, push preparation/execution, and the initial browser-based UI—on top of this same prepare/revalidate/approve/execute/verify architecture.
