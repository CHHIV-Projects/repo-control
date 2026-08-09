# Milestone 006 — Read-Only Git Workflow Intelligence

Prompt file:

`006_read_only_git_workflow_intelligence_prompt.md`

Required closeout file:

`006_read_only_git_workflow_intelligence_closeout.md`

## Objective

Add deterministic, read-only Git workflow intelligence to Repo Control Plane.

Milestones 001–005.1 established:

- deterministic repository inventory;
- deterministic repository relationships;
- bounded context packs;
- immutable snapshots;
- deterministic structural comparisons;
- grounded local GPT-OSS advisory analysis.

Milestone 006 adds the Git workflow facts needed to eventually support guarded milestone/commit/push operations.

Add:

    repoctl milestone status [--repository <path>]

The command must answer mechanical workflow questions such as:

- What branch am I on?
- What is HEAD?
- Is HEAD attached or detached?
- Is an upstream configured?
- Based only on locally available refs, is the branch ahead or behind its upstream?
- Is the worktree clean?
- What is staged?
- What is unstaged?
- What is untracked?
- Are unresolved conflicts present?
- Is a merge, rebase, cherry-pick, revert, or bisect operation in progress?
- Is there already an immutable Repo Control Plane snapshot matching the current deterministic repository state?
- Which mechanical conditions would matter before a future guarded commit operation?

This milestone provides evidence.

It does NOT:

- stage files;
- create branches;
- commit;
- push;
- fetch;
- pull;
- merge;
- rebase;
- restore;
- reset;
- clean;
- modify Git configuration.

No AI invocation is required or authorized by `repoctl milestone status`.

---

# Authority Model

The authority hierarchy remains:

    Git repository / source / tests
        ↓
    deterministic Repo Control Plane facts
        ↓
    immutable snapshot/comparison evidence
        ↓
    advisory GPT-OSS analysis

Milestone 006 belongs entirely to the deterministic layer.

Git command output and repository metadata are authoritative for Git workflow facts.

Do not ask GPT-OSS to determine Git state.

---

# Controlling Documents

Read and follow:

- `docs/Repo_Control_Plane_v0.1_Architecture_and_Implementation_Plan.md`
- `docs/001_deterministic_repository_scanner_prompt.md`
- `docs/001_deterministic_repository_scanner_closeout.md`
- `docs/002_repository_relationships_prompt.md`
- `docs/002_repository_relationships_closeout.md`
- `docs/003_deterministic_context_pack_generator_prompt.md`
- `docs/003_deterministic_context_pack_generator_closeout.md`
- `docs/004_deterministic_snapshot_delta_audit_prompt.md`
- `docs/004_deterministic_snapshot_delta_audit_closeout.md`
- `docs/005_gpt_oss_structural_delta_analysis_prompt.md`
- `docs/005_gpt_oss_structural_delta_analysis_closeout.md`
- `docs/005.1_ollama_gpt_oss_structured_output_compatibility_prompt.md`
- `docs/005.1_ollama_gpt_oss_structured_output_compatibility_closeout.md`

Milestones 001–005.1 are trusted baselines.

Do not redesign them.

---

# Project and Validation Boundary

Repo Control Plane:

`/home/chuck/projects/repo-control`

Primary disposable validation repository:

`/home/chuck/ai-agent-tests/vocab-app`

Temporary Git fixture repositories should be used for destructive state scenarios.

Photo Organizer remains explicitly out of scope.

Do not inspect, scan, query, snapshot, compare, analyze, modify, or otherwise access Photo Organizer during Milestone 006.

---

# Git Preflight

Before coding:

1. confirm Repo Control Plane worktree is completely clean;
2. confirm branch and HEAD;
3. confirm upstream state if configured;
4. stop and report unexpected pre-existing changes.

Required evidence:

    git branch --show-current
    git rev-parse HEAD
    git status --short

If worktree status is non-empty:

    STOP

Do not automatically:

- reset;
- restore;
- clean;
- stage;
- commit;
- stash;
- discard changes.

Do not commit or push unless separately instructed.

---

# Existing Commands

Preserve:

    repoctl scan <repository>
    
    repoctl context "<query>" [--repository <path>]
    
    repoctl snapshot [--repository <path>]
    
    repoctl compare <before_snapshot_id> <after_snapshot_id> [--repository <path>]
    
    repoctl analyze <comparison_id> [--repository <path>]

Add exactly:

    repoctl milestone status [--repository <path>]

Do not add:

    milestone start
    milestone review
    milestone prepare-commit
    milestone commit
    milestone push

in Milestone 006.

Those remain future workflow operations.

---

# 1. Repository Selection

Use the existing canonical repository-selection behavior.

When:

    --repository

is omitted, resolve the Git worktree containing the current working directory.

When supplied:

    --repository <path>

the path may point anywhere inside the target Git worktree.

Resolve the canonical Git repository root and existing Repo Control Plane `repository_id`.

Non-Git targets fail clearly and non-zero.

---

# 2. Strict Read-Only Git Boundary

Milestone 006 may invoke Git only through commands that do not mutate repository state.

Permitted categories include read-only equivalents of:

    git status
    git rev-parse
    git symbolic-ref
    git rev-list
    git config --get
    git diff --name-only / --name-status
    git ls-files

Use the smallest command set necessary.

Explicitly prohibited:

    git add
    git commit
    git push
    git fetch
    git pull
    git merge
    git rebase
    git cherry-pick
    git revert
    git reset
    git restore
    git clean
    git stash
    git switch
    git checkout
    git branch <mutation>
    git config <mutation>
    git remote <mutation>

Do not modify reflogs, refs, index, worktree, configuration, hooks, remotes, or credentials.

Tests may perform Git mutations inside disposable fixture repositories to create states that the production implementation then reads.

---

# 3. No Network Access

`repoctl milestone status` must not contact any remote Git server.

In particular:

    git fetch

is prohibited.

Upstream divergence must be calculated exclusively from locally available refs.

Therefore upstream information may be stale relative to the actual remote server.

The output must explicitly record:

    remote_refresh_performed = false

and must explain in human-readable output that ahead/behind values reflect local Git refs only.

Do not claim that the remote repository itself is current.

---

# 4. Core Git State

Capture deterministic Git facts including at minimum:

- repository root;
- repository ID;
- HEAD commit;
- attached/detached state;
- current branch name when attached;
- upstream configured/not configured;
- upstream ref when configured;
- local ahead count;
- local behind count;
- worktree clean/dirty state;
- staged-entry count;
- unstaged-entry count;
- untracked-entry count;
- unmerged-entry count;
- structured changed-path evidence;
- active Git-operation state;
- remote refresh performed flag.

Do not record timestamps.

Do not record Git command execution duration.

---

# 5. Canonical Status Source

Prefer one canonical porcelain-v2 status source for worktree/index state.

Use the equivalent of:

    git status --porcelain=v2 --branch -z --untracked-files=all

Parse it conservatively.

Support the porcelain-v2 record forms already recognized by Repo Control Plane where applicable.

Do not parse human-readable `git status` prose.

Do not rely on locale-specific output.

Unsupported status forms must fail closed rather than silently disappear.

Reuse existing Milestone 001 Git-status parsing where practical rather than implementing competing semantics.

---

# 6. Working-Tree Entry Model

For every relevant status entry preserve deterministic mechanical evidence.

At minimum distinguish:

    ordinary
    rename_or_copy
    unmerged
    untracked

For tracked entries preserve where available:

- relative path;
- XY status;
- submodule state;
- original path for rename/copy records.

For untracked entries preserve relative path.

Do not read untracked file contents.

Do not infer whether an untracked file is important.

Use established deterministic filesystem-byte path ordering.

---

# 7. Staged / Unstaged Classification

Derive mechanical collections:

    staged_paths
    unstaged_paths
    untracked_paths
    unmerged_paths

A path may legitimately appear in both:

    staged_paths
    unstaged_paths

when it has index changes and additional worktree changes.

Do not collapse that distinction.

Rename/copy evidence must remain explicit.

No diff contents or source snippets are required.

---

# 8. Workflow State Enum

Derive exactly one deterministic:

    workflow_state

from working-tree/index evidence.

Allowed values:

    clean
    staged_only
    unstaged_only
    staged_and_unstaged
    conflicted

Rules:

### clean

No staged, unstaged, untracked, or unmerged entries.

### staged_only

At least one staged entry and:

- no unstaged entries;
- no untracked entries;
- no unmerged entries.

### unstaged_only

No staged entries and at least one:

- unstaged entry; or
- untracked entry;

with no unmerged entries.

### staged_and_unstaged

At least one staged entry and at least one:

- unstaged entry; or
- untracked entry;

with no unmerged entries.

### conflicted

At least one unmerged entry.

`conflicted` takes precedence over the other values.

Git-operation state and detached HEAD are represented separately and do not create additional `workflow_state` enum values.

Do not introduce:

    ready
    safe
    unsafe
    approved

into this enum.

---

# 9. Branch / Detached HEAD

Represent branch state consistently with existing repository evidence:

Attached:

    {
      "state": "attached",
      "name": "main"
    }

Detached:

    {
      "state": "detached",
      "name": null
    }

Do not invent a branch name for detached HEAD.

HEAD commit remains recorded independently.

---

# 10. Upstream Contract

If no upstream is configured:

    upstream.configured = false

and:

    upstream.ref = null
    upstream.ahead = null
    upstream.behind = null

If upstream is configured and resolvable from local refs:

    upstream.configured = true

record:

- upstream ref;
- ahead count;
- behind count.

Use local commit graph evidence only.

Do not fetch.

If upstream configuration exists but the corresponding local ref is unavailable:

- retain configured upstream identity;
- classify local divergence as unavailable;
- do not fabricate zero counts.

Use an explicit state such as:

    divergence_state = "available"
    
    divergence_state = "unavailable"

When available, derive:

    relation = "equal"
    relation = "ahead"
    relation = "behind"
    relation = "diverged"

according to local ahead/behind counts.

When unavailable:

    relation = null

---

# 11. Remote Privacy

Do not publish remote URLs in Milestone 006 status artifacts.

Do not record:

- HTTPS credentials;
- embedded access tokens;
- SSH private-key paths;
- credential-helper output.

The upstream ref name is sufficient.

Repo Control Plane does not need the remote URL for this milestone.

---

# 12. Active Git Operations

Detect read-only evidence for these in-progress Git operations:

    merge
    rebase
    cherry_pick
    revert
    bisect

Use Git-aware repository metadata paths that work with normal repositories and linked worktrees.

Do not assume `.git` is always a directory directly under repository root.

Prefer Git-resolved metadata locations.

Output:

    git_operations

as a deterministic ordered collection.

Use fixed ordering:

    merge
    rebase
    cherry_pick
    revert
    bisect

Also expose:

    git_operation_in_progress = true|false

Do not alter or complete any operation.

Do not interpret whether an active operation was intentional.

---

# 13. Mechanical Future-Action Preconditions

Milestone 006 should expose deterministic booleans useful to future guarded Git-write milestones.

Add:

    mutation_preconditions

with exactly:

    branch_attached
    staged_changes_present
    unstaged_changes_present
    untracked_changes_present
    unmerged_entries_present
    git_operation_in_progress
    upstream_configured
    upstream_divergence_available

These are facts only.

Do not create a derived field named:

    safe_to_commit
    safe_to_push
    approved_to_commit
    ready_to_push

Milestone 006 must not make the final mutation decision.

Future guarded-write milestones may define those policies explicitly.

---

# 14. Current Deterministic Snapshot Identity

Milestone 006 should connect live Git workflow state to the existing deterministic repository evidence without automatically creating a new immutable snapshot.

Perform/reuse a fresh deterministic scan in memory.

Using the established Milestone 004 snapshot-ID algorithm, calculate:

    current_snapshot_id_candidate

for the exact current deterministic tracked-file evidence.

Do NOT publish a new snapshot merely because `milestone status` was run.

Then determine:

    matching_snapshot_exists = true|false

by checking whether the immutable snapshot namespace already contains that exact candidate ID.

If an exact snapshot exists:

    matching_snapshot_id = <candidate id>

Otherwise:

    matching_snapshot_id = null

This gives future workflow logic a mechanical answer to:

    "Has this exact deterministic repository state already been snapshotted?"

Do not choose a "latest" snapshot.

Snapshot IDs are content-derived, not chronological.

Do not infer chronology from directory ordering.

---

# 15. Snapshot Integrity

If an exact matching snapshot directory exists, verify it using the existing Milestone 004 snapshot-integrity logic before reporting:

    matching_snapshot_exists = true

If the expected candidate directory exists but fails integrity verification:

- fail status clearly;
- do not pretend a valid matching snapshot exists;
- do not repair or overwrite it.

Do not create a snapshot during status.

---

# 16. No Automatic Comparison or AI Analysis

`repoctl milestone status` must not automatically:

- create a snapshot;
- create a comparison;
- invoke GPT-OSS;
- run `repoctl analyze`;
- select an earlier baseline;
- infer which comparison the user intends.

Milestone 006 reports state only.

The operator remains responsible for explicitly invoking existing commands when desired.

---

# 17. Output Location

Store the current workflow projection externally:

    ~/.local/share/repoctl/<repository_id>/workflow/

Containing exactly:

    status.json
    status.md

These are current-state projection artifacts, not immutable historical records.

Each successful status invocation may replace the previous:

    status.json
    status.md

using transactional publication.

Do not generate a history of workflow statuses in Milestone 006.

Snapshots already provide immutable repository-state history.

---

# 18. Deterministic Output

For identical:

- repository state;
- local Git refs;
- existing matching-snapshot state;

repeated status commands must produce byte-for-byte identical:

    status.json
    status.md

Do not include:

- timestamps;
- durations;
- random values;
- network data.

Changes in local upstream refs may legitimately change status output.

---

# 19. `status.json`

Use:

    "schema_version": 1

Include at minimum:

    schema_version
    repository_id
    repository_root
    head
    branch
    upstream
    remote_refresh_performed
    working_tree
    workflow_state
    git_operation_in_progress
    git_operations
    mutation_preconditions
    current_snapshot_id_candidate
    matching_snapshot_exists
    matching_snapshot_id

The structured working-tree evidence must include deterministic counts and paths for:

    staged
    unstaged
    untracked
    unmerged

Do not add AI interpretation fields.

---

# 20. `status.md`

Render only from the already-computed `status.json`/structured result.

Do not independently query Git from the renderer.

Use fixed section order:

    # Milestone Git Status
    
    ## Repository
    
    ## Branch and HEAD
    
    ## Upstream
    
    ## Working Tree
    
    ## Active Git Operations
    
    ## Mutation Preconditions
    
    ## Repo Control Plane Evidence
    
    ## Limitations

The limitations section must state at minimum:

- no Git fetch was performed;
- upstream divergence reflects locally available refs only;
- no Git mutation was performed;
- no commit/push approval decision is made by this command.

Do not include source-code bodies or diff snippets.

---

# 21. CLI Summary

After successful execution, print a concise operator summary.

Example shape:

    Repository: /path/to/repo
    Branch: main
    HEAD: abc123...
    Workflow state: staged_and_unstaged
    Staged: 4
    Unstaged: 2
    Untracked: 1
    Unmerged: 0
    Upstream: origin/main
    Local relation: ahead 1 / behind 0
    Git operation: none
    Matching snapshot: snap--...

Do not print remote URLs.

Do not claim that upstream information is freshly fetched.

---

# 22. README

Update README to document:

    repoctl milestone status [--repository <path>]

Document:

- command is read-only toward Git;
- no fetch occurs;
- ahead/behind reflects local refs only;
- workflow-state enum;
- active-operation detection;
- staged/unstaged/untracked distinction;
- exact snapshot-match reporting;
- output location;
- no commit/push decision or Git mutation occurs.

Do not document future mutation commands as implemented.

---

# 23. Automated Tests

Add focused tests covering at least:

1. clean repository;
2. staged-only repository;
3. unstaged tracked change;
4. untracked-only change;
5. staged + unstaged same path;
6. staged + untracked;
7. conflicted/unmerged state;
8. attached branch;
9. detached HEAD;
10. upstream absent;
11. upstream configured and equal;
12. locally ahead;
13. locally behind;
14. locally diverged;
15. configured upstream ref unavailable;
16. no fetch/network operation occurs;
17. rename/copy status handling;
18. merge-operation detection;
19. rebase-operation detection;
20. cherry-pick-operation detection;
21. revert-operation detection;
22. bisect-operation detection;
23. deterministic Git-operation ordering;
24. paths containing spaces;
25. deterministic staged/unstaged/untracked ordering;
26. exact workflow-state enum behavior;
27. exact mutation-precondition booleans;
28. fresh deterministic snapshot-candidate calculation;
29. no matching snapshot case;
30. valid matching snapshot case;
31. corrupt matching snapshot fails closed;
32. status does not create a snapshot;
33. status does not create comparison/analysis artifacts;
34. remote URLs are absent from status artifacts;
35. no source/diff contents appear in output;
36. transactional status publication;
37. repeated identical state produces byte-identical artifacts;
38. target Git status is byte-identical before/after execution;
39. all Milestone 001–005.1 tests remain passing.

Use disposable Git repositories and local bare repositories for branch/upstream/divergence testing.

Tests may mutate fixture repositories in order to construct states.

Production status implementation remains read-only.

---

# 24. Vocab App Validation

After automated tests pass, validate against:

`/home/chuck/ai-agent-tests/vocab-app`

Treat the actual current repository state as authoritative.

Before running status capture:

    git status --porcelain=v2 -z --untracked-files=all

Then run:

    repoctl milestone status \
        --repository /home/chuck/ai-agent-tests/vocab-app

Verify directly:

- branch and HEAD;
- attached/detached state;
- current workflow state;
- staged/unstaged/untracked/unmerged counts;
- active Git-operation state;
- upstream configuration;
- local ahead/behind evidence if available;
- current snapshot candidate;
- matching-snapshot status.

Afterward capture exact porcelain-v2 status again.

Require:

    STATUS_MATCH=1

Do not modify Vocab App.

---

# 25. Controlled Workflow-State Validation

Use disposable temporary Git repositories to demonstrate important non-clean states.

At minimum demonstrate:

    staged_only
    unstaged_only
    staged_and_unstaged
    conflicted

Also demonstrate at least one active Git operation.

Direct Git evidence must agree with Repo Control Plane output.

Do not perform these destructive state constructions in Vocab App.

---

# 26. Local Upstream Validation

Use disposable local repositories and a local bare remote to prove:

    equal
    ahead
    behind
    diverged

without contacting the public network.

Verify the reported counts mechanically against Git.

Confirm:

    remote_refresh_performed = false

throughout.

---

# 27. Practical Product Check

Milestone 006 must answer:

    "Can Repo Control Plane tell the operator exactly what Git state
     exists before a future guarded milestone/commit operation without
     making any Git changes?"

Using a controlled fixture, demonstrate a state such as:

- attached branch;
- staged files present;
- one additional unstaged modification;
- upstream configured;
- local branch ahead or behind;
- no conflict;
- no operation in progress.

Using only `status.json` / `status.md`, report:

- branch/HEAD;
- staged versus unstaged footprint;
- local upstream relationship;
- mutation-precondition facts;
- whether an exact Repo Control Plane snapshot already exists.

Verify against direct read-only Git evidence.

Do not make an approval/commit decision.

---

# Explicit Non-Goals

Do not implement:

- `milestone start`;
- `milestone review`;
- `milestone prepare-commit`;
- `milestone commit`;
- `milestone push`;
- branch creation;
- branch switching;
- Git staging;
- commit creation;
- push;
- fetch;
- pull;
- merge;
- rebase;
- reset;
- restore;
- clean;
- stash;
- tag creation;
- Git configuration changes;
- remote changes;
- automatic snapshot creation;
- automatic comparison;
- automatic GPT-OSS analysis;
- commit-message generation;
- GitHub API integration;
- pull-request creation;
- CI integration;
- protected-branch policy management;
- source-code editing;
- Docker changes;
- Photo Organizer access.

---

# Implementation Discipline

Extend existing Repo Control Plane infrastructure.

Preferred architecture:

    selected repository
        ↓
    canonical read-only Git inspection
        +
    fresh deterministic scanner evidence
        ↓
    workflow state classifier
        ↓
    current snapshot candidate calculation
        ↓
    exact immutable snapshot existence/integrity check
        ↓
    status.json
        ↓
    status.md

Prefer a focused package such as:

    src/repoctl/workflow/
        __init__.py
        git_state.py
        status.py

or an equivalently small organization.

Reuse existing:

- Git status parser;
- canonical repository resolution;
- deterministic path ordering;
- scanner;
- snapshot identity;
- snapshot integrity validation.

Do not duplicate these contracts.

No new third-party dependencies should be required.

---

# Stop / Escalation Conditions

Stop and report rather than broadening scope if implementation appears to require:

- Git mutation;
- network fetch;
- GitHub/cloud API access;
- remote credentials;
- new persistent database infrastructure;
- automatic baseline selection;
- AI interpretation;
- modifying existing snapshot identity;
- modifying Milestone 001 Git-status semantics incompatibly;
- source-code execution;
- Docker;
- Photo Organizer access.

If Git state cannot be established deterministically, report the limitation rather than guessing.

Once the contracts in this prompt are satisfied, make ordinary implementation decisions locally without another broad reconnaissance cycle.

---

# Validation Before Closeout

Run at minimum:

- full Repo Control Plane automated suite;
- Milestone 006 focused tests;
- Python syntax/compile validation;
- clean/staged/unstaged/mixed/conflicted fixture validation;
- active Git-operation fixture validation;
- local upstream equal/ahead/behind/diverged validation;
- matching-snapshot validation;
- Vocab App read-only status validation;
- exact target Git-status before/after equality;
- repeated deterministic output validation;
- `git diff --check`;
- final `git status --short`.

---

# Required Closeout

Create:

`docs/006_read_only_git_workflow_intelligence_closeout.md`

Include:

1. implementation summary;
2. files added/modified;
3. CLI syntax;
4. read-only Git command boundary;
5. `status.json` schema at a useful high level;
6. workflow-state enum behavior;
7. staged/unstaged/untracked/unmerged handling;
8. branch/detached behavior;
9. upstream/divergence behavior;
10. confirmation no fetch/network operation occurs;
11. active Git-operation detection;
12. mutation-precondition contract;
13. snapshot-candidate/matching-snapshot behavior;
14. automated test results;
15. controlled workflow-state validation;
16. local upstream divergence validation;
17. Vocab App validation;
18. practical product-check result;
19. deterministic-output validation;
20. target before/after Git status;
21. limitations;
22. Milestone 007 opportunities without implementing them;
23. final Repo Control Plane `git status --short`.

Do not commit or push unless separately instructed.

---

# Acceptance Criteria

Milestone 006 passes only if:

- Milestones 001–005.1 remain intact;
- `repoctl milestone status` works;
- Git inspection is strictly read-only;
- no Git fetch/network request occurs;
- branch and HEAD evidence is correct;
- staged, unstaged, untracked, and unmerged states are distinguished;
- workflow-state classification is deterministic;
- detached HEAD is represented correctly;
- local upstream equal/ahead/behind/diverged states are correct;
- unavailable local upstream refs are not treated as zero divergence;
- active Git operations are detected without mutation;
- mutation-precondition fields contain facts rather than approval decisions;
- current deterministic snapshot candidate is calculated without publishing a snapshot;
- an existing matching snapshot is integrity-verified before being reported;
- status output is deterministic;
- target repositories are not modified;
- remote URLs/credentials are not exposed;
- Vocab App validation matches direct Git evidence;
- all automated tests pass;
- no AI, Git writes, Docker changes, or Photo Organizer access is introduced.



# Product Owner / Architect Clarification Addendum — Milestone 006 Git-State Contract

This addendum resolves the remaining pre-coding implementation questions.

It does not broaden Milestone 006 scope.

## 1. Upstream Divergence Unavailable Reason

When an upstream is configured but its corresponding locally available ref cannot support divergence calculation, report:

    upstream.configured = true
    upstream.divergence_state = "unavailable"
    upstream.relation = null
    upstream.ahead = null
    upstream.behind = null

Also include:

    upstream.unavailable_reason = "upstream_ref_unavailable"

For an available divergence result:

    upstream.divergence_state = "available"
    upstream.unavailable_reason = null

For no configured upstream:

    upstream.configured = false
    upstream.ref = null
    upstream.divergence_state = "unavailable"
    upstream.unavailable_reason = "upstream_not_configured"
    upstream.relation = null
    upstream.ahead = null
    upstream.behind = null

Use exactly these two unavailable-reason values for schema version 1:

    upstream_not_configured
    upstream_ref_unavailable

Do not create arbitrary human prose as machine-readable reason values.

Human-readable Markdown may explain the corresponding condition.

## 2. Active Git Operation Representation

Keep Git-operation evidence intentionally minimal.

`status.json` must contain:

    git_operation_in_progress = true|false

and:

    git_operations = [...]

using only the fixed ordered operation names:

    merge
    rebase
    cherry_pick
    revert
    bisect

Do not add per-operation Git metadata paths, marker-file names, internal repository paths, or operation payload details to `status.json`.

The deterministic presence of an operation name is sufficient workflow evidence for Milestone 006.

Detection implementation may inspect Git-resolved metadata internally, but those implementation details are not part of the output schema.

## 3. Unsupported Porcelain-v2 Record Failure

Unsupported porcelain-v2 record forms must fail closed.

Use a stable failure classification:

    unsupported_porcelain_v2_record

The safe operator message may include only the unrecognized record type/prefix needed to identify the parser issue.

Conceptually:

    git status error [unsupported_porcelain_v2_record]:
    unsupported porcelain-v2 record prefix: X

Do not include the complete raw porcelain record merely for diagnostics.

In particular, do not expose an arbitrary path or other record payload when the prefix alone is sufficient to identify the unsupported form.

Automated tests should prove that unsupported records cannot be silently skipped.

## 4. Canonical Porcelain-v2 Parser Reuse

The Milestone 001 porcelain-v2 parser is the controlling implementation for status-record semantics.

Milestone 006 must reuse it wherever applicable.

Do not create a second competing parser for:

    ordinary
    rename_or_copy
    unmerged
    untracked

records.

A narrowly necessary extension for Milestone 006 branch/header evidence is permitted, but:

- existing record semantics must remain unchanged;
- the same fail-closed philosophy applies;
- existing Milestone 001 scanner behavior must continue to pass regression tests.

If implementation appears to require materially incompatible duplicate status parsing:

    STOP — ESCALATION REQUIRED

Prefer extending shared Git-status infrastructure over forking the contract.

## 5. Transactional Workflow Publication

`workflow/status.json` and `workflow/status.md` form one successful workflow-status publication.

Required publication semantics:

1. compute the complete structured status;
2. render both artifacts;
3. stage both outside the final published pair;
4. validate both;
5. publish only after both are complete;
6. on a controlled publication failure, preserve the previous successful status pair.

Do not leave a new `status.json` paired with an old `status.md`, or vice versa.

Reuse existing transactional publication helpers/patterns where practical.

The exact filesystem swap/rename implementation is an ordinary engineering choice.

Because workflow status is a replaceable current-state projection rather than immutable history, the contract requires transactional pair behavior but does not mandate the exact immutable-directory algorithm used by snapshots/comparisons.

No temporary publication files may remain in the target repository.

All workflow state remains under Repo Control Plane external state.

## 6. Local-Ref Staleness Warning

README and `status.md` must place the local-ref limitation directly alongside upstream ahead/behind reporting.

Use wording equivalent to:

    No Git fetch is performed.
    Ahead/behind values describe locally available Git refs and may not
    reflect the current state of the remote server.

Do not describe:

    ahead = 0
    behind = 0

as proof that the local branch is current with the actual remote server.

It proves equality only against the locally available upstream ref.

The CLI summary should likewise avoid wording such as:

    remote is current
    fully synchronized with GitHub

Use factual wording such as:

    Local upstream relation: equal
    Ahead: 0
    Behind: 0
    Remote refresh: not performed

## 7. Network Boundary Applies to Implementation and Validation

Production `repoctl milestone status` must perform no network operation.

Tests may create and manipulate local bare repositories as fixtures.

Those fixture setup operations are test preparation and must remain clearly separate from the production status path.

Tests should prove that the status implementation itself does not invoke:

    fetch
    pull
    push

or another remote-refresh operation.

Do not use public Git hosting for automated divergence tests.

## 8. Required Clarification Tests

In addition to the original Milestone 006 test requirements, explicitly verify:

- no configured upstream produces `upstream_not_configured`;
- configured but unavailable local upstream ref produces `upstream_ref_unavailable`;
- available divergence has `unavailable_reason = null`;
- active Git operations are represented only by the fixed ordered operation names;
- Git-internal operation metadata paths are not published;
- unsupported porcelain-v2 records fail with `unsupported_porcelain_v2_record`;
- safe unsupported-record diagnostics do not expose the full raw record;
- existing Milestone 001 porcelain-v2 semantics remain authoritative;
- workflow publication cannot leave mismatched `status.json` / `status.md` after a controlled failure;
- previous successful workflow artifacts survive a controlled replacement failure;
- README/status Markdown explicitly state that no fetch occurs and locally available upstream refs may be stale.

These are refinements of existing Milestone 006 requirements, not additional feature scope.

## 9. Proceed Instruction

No further pre-coding clarification is required if the initial Git preflight passes.

Proceed with:

    clean preflight
        ↓
    shared read-only Git-state inspection
        ↓
    workflow-state classification
        ↓
    active-operation detection
        ↓
    local upstream divergence
        ↓
    current snapshot-candidate calculation
        ↓
    exact snapshot integrity check
        ↓
    transactional status publication
        ↓
    fixture and Vocab App validation

Make ordinary implementation choices locally after these contracts are satisfied.

Ask for Product Owner input only if a genuine scope, read-only safety, parser-compatibility, or architecture conflict is encountered.