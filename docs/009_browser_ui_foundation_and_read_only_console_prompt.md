# Milestone 009 — Browser UI Foundation and Read-Only Console

Prompt file:

`009_browser_ui_foundation_and_read_only_console_prompt.md`

Required closeout file:

`009_browser_ui_foundation_and_read_only_console_closeout.md`

## Objective

Create the first browser-based Repo Control Plane user interface.

Milestone 009 establishes a human-facing local web console over the deterministic and advisory capabilities already implemented through Milestones 001–008.

The UI should make ordinary Repo Control Plane use understandable without requiring the operator to interpret JSON artifacts or remember CLI syntax.

The first browser console must support, at minimum:

    repository dashboard / Git workflow status
    deterministic context generation
    snapshot creation and history
    snapshot comparison
    GPT-OSS comparison analysis
    human-readable rendering of resulting evidence

Milestone 009 remains:

    TARGET-GIT READ ONLY

The browser must NOT yet execute:

    staging
    commit
    push
    branch mutation
    reset / restore / clean
    any other Git mutation

M007 and M008 mutation primitives remain available through CLI only during this milestone.

The next milestone may expose those already-trusted mutation services through explicit browser approval flows.

---

# Product Direction

The long-term Repo Control Plane user experience is:

    browser GUI = normal operator interface
    CLI         = engineering / diagnostic / automation interface
    core        = single authoritative implementation

The GUI must NOT become a second implementation of Repo Control Plane logic.

Architecture must remain:

                         ┌─────────────┐
                         │ Browser UI  │
                         └──────┬──────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │ Repo Control Plane  │
                    │    Core Services    │
                    └─────────────────────┘
                       ▲               ▲
                       │               │
                     CLI             Web UI

Both interfaces must use the same core services.

Do not duplicate:

- Git status interpretation;
- context generation;
- snapshot logic;
- comparison logic;
- GPT-OSS analysis logic;
- evidence interpretation;
- M007/M008 workflow safety logic.

---

# Project

Repo Control Plane:

`/home/chuck/projects/repo-control`

Photo Organizer remains explicitly out of scope.

Do not inspect, scan, modify, or otherwise access Photo Organizer.

Do not mutate Vocab App.

Use disposable repositories for practical web validation requiring repository changes.

---

# Required Reading

Read and preserve:

- Repo Control Plane architecture / implementation plan
- Milestone 003 prompt and closeout
- Milestone 004 prompt and closeout
- Milestone 005 / 005.1 prompt and closeout
- Milestone 006 prompt and closeout
- Milestone 006.1 prompt and closeout
- Milestone 007 prompt and closeout
- Milestone 008 prompt and closeout

Preserve these architectural principles:

1. repository source / Git / tests remain authoritative;
2. deterministic evidence precedes AI interpretation;
3. GPT-OSS remains advisory;
4. external Repo Control Plane state remains outside target repositories;
5. browser UI is an adapter over core services;
6. Git mutation remains explicitly bounded;
7. M009 browser routes do not perform Git mutation.

Do not perform broad repository reconnaissance.

Inspect only the code and tests necessary to introduce the web adapter cleanly.

---

# Initial Git Preflight

Before coding:

    git branch --show-current
    git rev-parse HEAD
    git status --short

Require:

- branch `main` unless repository evidence establishes otherwise;
- clean worktree/index;
- M008 committed;
- no active Git operation.

If status is not clean:

    STOP

Do not reset, restore, clean, stash, stage, or discard unexplained changes.

Do not commit or push unless separately instructed.

---

# Web Runtime Model

Add a command equivalent to:

    repoctl web \
        --repository <path> \
        [--host 127.0.0.1] \
        [--port 8765]

Exact command organization may follow existing CLI conventions.

For Milestone 009:

    default host = 127.0.0.1

The application must default to loopback-only access.

This milestone does NOT design trusted-LAN authentication.

Do not silently bind to:

    0.0.0.0

or another externally reachable interface.

If non-loopback binding is supplied during M009, either:

- fail closed; or
- require a deliberately explicit unsupported/development override if the architecture already has such a safe mechanism.

Preferred M009 behavior:

    non-loopback binding blocked

with a clear explanation that LAN exposure/authentication is deferred.

The Product Owner may access the browser from Windows through SSH port forwarding during this initial milestone.

Do not create systemd services, Docker containers, reverse proxies, TLS configuration, or permanent server startup behavior yet.

---

# Web Technology Boundary

Use a small, maintainable Python web architecture.

Requirements:

- server-side Python integrates directly with existing Repo Control Plane services;
- no duplicate application backend;
- no Node/npm build requirement unless an existing project dependency makes that clearly preferable;
- no external CDN dependency;
- no externally hosted JavaScript, CSS, fonts, icons, or telemetry;
- no cloud service requirement.

Prefer:

    server-rendered HTML
        +
    minimal local CSS
        +
    minimal JavaScript only where genuinely useful

over a large frontend framework for this first milestone.

If a new Python web dependency is required:

- choose a mature, narrowly scoped package;
- record it explicitly;
- add deterministic dependency declaration;
- document why it is required.

Do not add a large frontend toolchain simply to render the first console.

---

# Single Repository Boundary

Milestone 009 operates against exactly one repository selected when the web process starts:

    repoctl web --repository <path>

Do NOT allow the browser to submit arbitrary filesystem repository paths.

The configured repository root must be canonicalized once at startup and treated as the server's repository boundary.

Every route/action must operate against that bound repository.

This prevents the browser from becoming a generic filesystem navigation surface.

Multi-repository registration/selection is deferred.

The dashboard should prominently show the active repository.

---

# Core Web Service Boundary

Do not have route functions directly implement repository intelligence.

Introduce a small reusable web/view-model adapter layer where useful.

Conceptually:

    web/
        app.py
        views.py
        templates/
        static/

Exact organization may vary.

Route handlers should conceptually perform:

    parse bounded user input
        ↓
    call existing Repo Control Plane core service
        ↓
    receive structured result/artifact
        ↓
    construct human-readable view model
        ↓
    render HTML

Do not parse Git porcelain independently inside web routes.

Do not execute arbitrary Git commands from browser input.

---

# Page 1 — Repository Dashboard

The default page should provide a concise human-readable repository summary.

At minimum show:

    repository name
    canonical repository root
    branch
    HEAD
    workflow state
    staged count
    unstaged count
    untracked count
    conflict count
    active Git operation, if any
    upstream configured/not configured
    locally known upstream relation when available
    explicit "no remote refresh performed" caveat
    current snapshot candidate ID
    exact matching snapshot ID if one exists

Example conceptually:

    Repo Control Plane
    
    Repository
    repo-control
    
    Branch
    main
    
    HEAD
    abc123...
    
    Working Tree
    CLEAN
    
    Staged       0
    Unstaged     0
    Untracked    0
    Conflicts    0
    
    Git operation
    None
    
    Snapshot
    snap--abc...  MATCHING
    
    Upstream
    origin/main
    locally known: equal
    
    No remote refresh was performed.

The page must not claim:

    safe to commit
    architecture approved
    correct
    ready to push

unless a future policy layer explicitly establishes such semantics.

M009 displays deterministic state, not approval judgments.

---

# Workflow Status Refresh

Provide a user control equivalent to:

    Refresh Status

This should call/reuse the existing M006 workflow-status service.

It must not:

- fetch;
- pull;
- update refs;
- stage;
- commit;
- push.

The UI must retain the existing local-ref caveat for upstream status.

---

# Page 2 — Deterministic Context

Provide a human-facing context input.

Conceptually:

    What are you working on?
    
    [ source readiness                         ]
    
    [ Find Relevant Code ]

The submitted query must use the existing M003 deterministic context service.

Do not add semantic search.

Do not call GPT-OSS for context selection.

Display the resulting context in human-readable groups such as:

    Relevant Files
    Relevant Symbols
    Direct Relationships
    Related Tests
    Diagnostics / limitations

Do not require the operator to open `context.json`.

Where useful, show why a file/symbol appeared:

    lexical match
    direct relationship
    related test

Preserve M003 bounds.

Do not turn the web layer into an unbounded source browser.

---

# Context Input Safety

Treat context queries as plain bounded text.

Enforce a reasonable maximum input size.

Reject NUL/control characters where appropriate.

HTML-escape all rendered user input and repository-derived strings.

Do not interpolate queries into:

- shell commands;
- filesystem paths;
- templates as executable markup.

Add tests for HTML/script escaping.

---

# Page 3 — Snapshots

Provide a human-readable snapshot view.

Show existing immutable snapshots for the active repository.

At minimum render:

    snapshot ID
    current-state match indicator when applicable
    brief structural summary available from existing artifacts

Provide:

    [ Create Snapshot ]

Creating a snapshot is allowed because it:

- does not mutate target Git;
- writes only Repo Control Plane external evidence.

It must call the existing M004 snapshot service.

Do not duplicate snapshot logic in the web layer.

After creation, display:

    snapshot ID
    whether it matches current repository state
    artifact/evidence summary

Do not automatically stage or commit anything.

---

# Snapshot Immutability

Browser snapshot creation must preserve all M004 guarantees.

The web layer must not:

- overwrite immutable snapshots;
- alter snapshot IDs;
- add UI timestamps into content-derived identity;
- store source bodies differently than the existing snapshot contract.

Repeated identical state should follow the existing deterministic snapshot identity behavior.

---

# Page 4 — Structural Comparison

Allow the operator to select:

    before snapshot
    after snapshot

from known snapshots for the active repository.

Provide:

    [ Compare ]

Use the existing M004 comparison service.

Render comparison results human-readably.

At minimum show counts for:

    files
    requirements
    symbols
    module dependencies
    imported-symbol relationships
    static calls
    test references
    parse failures
    diagnostics

Where non-zero, allow details to be expanded or shown in bounded sections.

Example:

    Structural Comparison
    
    Before: snap--AAA
    After:  snap--BBB
    
    Files
      Added       2
      Removed     0
      Changed     5
    
    Symbols
      Added       3
      Removed     1
    
    Calls
      Added       4
      Removed     1
    
    Tests
      References added    5
      References removed  1
    
    Parse failures
      0

The browser should make structural evidence understandable without replacing the authoritative JSON artifact.

---

# Comparison Input Boundary

The browser must only allow comparison of known immutable snapshot IDs belonging to the active bound repository.

Do not accept arbitrary filesystem locations.

Do not accept another repository's artifact IDs.

Repository mismatch must fail closed.

Use existing artifact integrity checks.

---

# Page 5 — Local GPT-OSS Review

For a known comparison, provide an action equivalent to:

    Analyze with Local GPT-OSS

This must call the existing M005/M005.1 analysis service.

No new AI prompt architecture is authorized.

Preserve:

    exact model
    local Ollama boundary
    structured output validation
    evidence grounding
    fail-closed provider behavior
    advisory-only semantics

Do not send repository source bodies to the model.

Do not call cloud AI.

Do not make AI review a requirement for any Git operation.

---

# GPT-OSS Human-Readable Rendering

Render existing analysis structure in sections such as:

    Local AI Review
    GPT-OSS 20B
    Advisory
    
    Summary
    
    Review Signals
    
      HIGH / MEDIUM / LOW where existing schema supports it
      observation
      interpretation
      evidence IDs
    
    Questions for Human Review

Every rendered signal/question must preserve its deterministic evidence references.

Prominently display:

    AI analysis is advisory.
    Deterministic repository evidence remains authoritative.

Do not expose or render:

- hidden model reasoning;
- `message.thinking`;
- chain-of-thought;
- raw provider internals not intended by M005.1.

Preserve M005.1 rule that model thinking is discarded.

---

# Analysis Failure UX

Provider/model failures must be rendered safely and clearly.

Show stable safe error information derived from existing structured provider errors.

Do not display:

- stack traces to normal browser users;
- secrets;
- credentials;
- full environment dumps;
- Ollama hidden reasoning.

An operator-facing error may conceptually show:

    Local AI analysis failed
    
    invalid_structured_content_json
    
    No repository mutation occurred.

Detailed stack traces may remain server-side for development diagnostics if appropriate.

---

# Page 6 — Git Workflow / Mutation Visibility

M009 should expose the existence of M007/M008 workflow capabilities without executing them.

Show current workflow state and, where useful, existing immutable:

    stage plans
    stage executions
    commit plans
    commit executions

for the active repository.

At minimum the dashboard may display whether the current state is:

    changes available for staging
    staged-only
    clean
    conflicted
    blocked by active Git operation

But do not turn these into policy claims such as "safe."

If existing prepared plans are displayed, show:

- plan ID;
- relevant branch/HEAD;
- exact file count/summary;
- whether current repository state still appears compatible if existing core integrity checks can determine this read-only;
- execution record if one exists.

Do not invent a new plan-validity algorithm in the UI.

---

# HARD M009 MUTATION BOUNDARY

The browser MUST NOT provide routes/buttons/actions that execute:

    prepare-stage + approve
    stage
    prepare-commit + approve
    commit

Clarification:

It is acceptable for M009 to DISPLAY the existing M007/M008 evidence.

Do not expose browser mutation controls yet.

Specifically forbidden browser behavior:

    git add
    git commit
    git push
    git fetch
    git pull
    git checkout
    git switch
    git reset
    git restore
    git clean
    git stash
    git merge
    git rebase
    git cherry-pick
    git revert
    tag creation/deletion

M009 proves the web boundary first.

M010 may expose:

    prepare-stage
    approve-stage
    snapshot
    prepare-commit
    approve-commit

through the same trusted core services.

---

# Route / Action Method Discipline

Use:

    GET

for presentation/read operations where appropriate.

Use:

    POST

for actions that create external Repo Control Plane artifacts, including:

- context generation if represented as an action;
- snapshot creation;
- comparison creation;
- GPT-OSS analysis.

Do not use GET requests to trigger artifact creation.

---

# CSRF / Browser-Origin Safety

Even though M009 defaults to loopback, POST actions must not be trivially triggerable by unrelated browser origins.

Implement a small CSRF/session protection mechanism appropriate to the chosen web stack.

Requirements:

- unpredictable per-session/token value;
- POST actions require valid token;
- invalid/missing token fails without performing the action;
- token is not written into repository artifacts;
- no remote/cloud session service.

Do not introduce user accounts/authentication yet.

This is browser request-integrity protection, not full LAN authentication.

---

# HTML / Output Safety

All repository-derived and user-supplied values must be safely escaped.

Test malicious-looking values such as:

    <script>alert(1)</script>

in:

- context query;
- filenames where practical;
- branch names where practical;
- commit messages/evidence display where practical.

They must render as text, not executable markup.

Do not use unsafe template rendering shortcuts.

---

# Error Boundary

Expected application/repository errors should render as human-readable error pages or inline messages.

Examples:

    repository unavailable
    unsupported repository state
    artifact integrity failure
    comparison not found
    analysis provider unavailable
    invalid input

Normal expected errors must not crash the web server.

The UI should clearly state whether:

    target repository mutation occurred

For every M009 route, expected answer should be:

    NO TARGET GIT MUTATION

---

# External State Boundary

Continue storing Repo Control Plane evidence only under existing external state architecture:

    ~/.local/share/repoctl/<repo-id>/

Do not write:

    web state
    sessions
    context artifacts
    snapshots
    comparisons
    analyses

into the target repository.

Ephemeral browser session/CSRF state may use process memory or an appropriate bounded local mechanism, but must not contaminate target repositories.

---

# No Telemetry

Do not add:

- analytics;
- usage reporting;
- tracking pixels;
- cloud logging;
- error-reporting SaaS;
- remote fonts;
- external CDN calls.

The first Repo Control Plane GUI remains local.

---

# Styling Direction

The first GUI should be functional, calm, and readable rather than visually elaborate.

Priorities:

1. clear hierarchy;
2. obvious repository identity;
3. readable state/status;
4. bounded tables/lists;
5. understandable evidence;
6. explicit advisory versus deterministic distinctions;
7. clear error presentation;
8. responsive layout usable from a normal laptop browser.

Do not spend the milestone on decorative animation.

Use local CSS.

Avoid framework-default diagnostic-looking output where a simple human-readable card/table is appropriate.

The console should feel like an operator dashboard, not raw debug output.

---

# Navigation

Provide a small stable navigation structure conceptually:

    Dashboard
    Context
    Snapshots
    Comparisons
    AI Review
    Workflow

Exact presentation is flexible.

Current repository identity should remain visible throughout the UI.

---

# Browser Refresh Semantics

Refreshing a page must not accidentally repeat a POST action.

Use normal Post/Redirect/Get behavior or equivalent.

Examples:

    Create Snapshot
        ↓
    POST
        ↓
    redirect
        ↓
    snapshot result page

Browser refresh should render the existing result rather than create another action unnecessarily.

Existing deterministic artifact reuse semantics remain authoritative.

---

# Concurrency Scope

M009 is a single-user local development console.

Do not build:

- multi-user permissions;
- collaborative sessions;
- websocket orchestration;
- distributed locking;
- job queues;
- background workers.

However, avoid obviously unsafe global mutable request state.

If GPT-OSS analysis is synchronous for M009, that is acceptable.

Display an understandable in-progress/loading state where practical, but do not add a job system merely for this milestone.

---

# CLI Preservation

All existing CLI commands must continue working unchanged unless a tiny compatible refactor is required to share core services.

At minimum preserve:

    repoctl scan
    repoctl context
    repoctl snapshot
    repoctl compare
    repoctl analyze
    repoctl milestone status
    repoctl milestone prepare-stage
    repoctl milestone stage
    repoctl milestone prepare-commit
    repoctl milestone commit

M009 must not make CLI usage depend on running the web server.

---

# Web Server Shutdown

Normal Ctrl+C / process termination must stop the web server cleanly.

Do not daemonize in this milestone.

Do not leave background processes after automated validation.

---

# Required Automated Tests

Add focused web tests covering at minimum:

## Server/application initialization

- valid repository binding;
- invalid/non-Git repository rejected safely;
- canonical repository root established;
- default loopback host behavior;
- non-loopback binding blocked under M009 policy.

## Dashboard

- clean repository rendering;
- staged-only rendering;
- unstaged/untracked rendering;
- conflict/operation rendering where practical;
- snapshot match rendering;
- upstream local-ref caveat visible;
- no remote refresh.

## Context

- valid context query;
- bounded human-readable results;
- empty/invalid query handling;
- HTML escaping;
- target repository unchanged.

## Snapshot

- existing snapshot listing;
- create snapshot through POST;
- CSRF required;
- repeated current-state snapshot follows deterministic identity;
- target Git state unchanged.

## Comparison

- valid known snapshot comparison;
- repository mismatch/unknown snapshot blocked;
- structural counts/details rendered;
- target Git state unchanged.

## GPT-OSS analysis

Use controlled/fake provider behavior for automated tests.

Verify:

- known comparison can invoke existing analysis service;
- analysis renders grounded evidence IDs;
- advisory warning visible;
- provider failure rendered safely;
- hidden thinking never rendered;
- target Git unchanged.

Do not require live Ollama for normal unit tests.

## Workflow visibility

- M006 state rendered;
- existing stage/commit plan/execution metadata may be rendered;
- NO mutation controls/routes execute Git mutation.

## CSRF

- valid POST token succeeds;
- missing token blocked;
- invalid token blocked;
- blocked request performs no artifact-producing action.

## HTML safety

Verify browser rendering escapes:

    <script>
    <img onerror=...>
    HTML-like filenames/messages

where applicable.

## Git mutation prohibition

Have tests explicitly establish that browser request handling never invokes:

    git add
    git commit
    git push
    git fetch
    git pull

or M007/M008 execution services.

---

# Practical Validation

Use a disposable repository.

Do not use Photo Organizer or mutate Vocab App.

Demonstrate:

    start repoctl web against disposable repo
        ↓
    open dashboard
        ↓
    verify repository / branch / HEAD / state
        ↓
    generate deterministic context
        ↓
    create snapshot
        ↓
    make controlled repository change outside UI
        ↓
    create second snapshot as appropriate
        ↓
    compare snapshots
        ↓
    render structural comparison
        ↓
    perform local GPT-OSS analysis if live provider is available
        ↓
    render grounded advisory review
        ↓
    verify browser never mutated Git

For live GPT-OSS validation, use the existing configured local model:

    gpt-oss:20b

Preserve M005.1 settings and safety contract.

Do not broaden live validation if Ollama is temporarily unavailable; report that condition separately while automated provider tests remain authoritative.

---

# Windows Browser Access Validation

M009 should document the development access method from the Product Owner's Windows laptop.

Because the web server defaults to server loopback, expected access is conceptually:

    Windows
        ↓
    SSH port forward
        ↓
    henderson-server1:127.0.0.1:<web-port>

For example, documentation may show an SSH command equivalent to:

    ssh -N -L 8765:127.0.0.1:8765 chuck@192.168.1.173

and then browser access to:

    http://127.0.0.1:8765

Do not hard-code this specific IP into application logic.

The documentation may use the current development environment as an example.

LAN-native browser access without SSH tunneling is deferred until an authentication/exposure milestone deliberately addresses it.

---

# Documentation

Update README with a concise Browser UI section.

Include:

- startup command;
- default loopback-only behavior;
- Windows SSH tunnel example;
- browser URL;
- pages/capabilities;
- explicit M009 no-Git-mutation boundary;
- how to stop server.

Do not turn README into a deployment manual yet.

---

# Regression Validation

Run focused M009 tests.

Then run:

    PYTHONPATH=src python3 -m unittest -q

under ordinary Python bytecode behavior.

Do NOT use:

    PYTHONDONTWRITEBYTECODE=1

M006.1 hygiene must remain effective.

After validation confirm:

- no generated cache Git noise;
- no synthetic Git-operation marker;
- Repo Control Plane development HEAD unchanged;
- no staged test artifacts;
- no left-running test web process.

---

# Dependency Validation

If M009 adds web dependencies:

- verify installation/declaration is reproducible;
- ensure tests run from the documented environment;
- document exact newly introduced dependency names;
- do not upgrade unrelated dependencies.

Do not change Ollama/model dependencies unless required by existing M005 compatibility.

---

# Expected Source Shape

Conceptually:

    src/repoctl/
        web/
            __init__.py
            app.py
            views.py
            templates/
                base.html
                dashboard.html
                context.html
                snapshots.html
                comparison.html
                analysis.html
                workflow.html
                error.html
            static/
                app.css
    
        cli.py
    
    tests/
        test_web.py

Exact organization may differ if the existing package architecture supports a smaller clean implementation.

Do not place large HTML strings directly in CLI code.

Do not mix CSS into Git workflow services.

---

# Stable Web/View Models

Prefer explicit human-facing view models over passing arbitrary core dictionaries directly into templates.

For example, conceptually:

    DashboardView
    ContextView
    SnapshotView
    ComparisonView
    AnalysisView
    WorkflowView

These do not need to be formal classes if a simpler typed structure works.

The important rule is:

    core evidence
        ↓
    bounded presentation mapping
        ↓
    template

Do not let templates redefine repository semantics.

---

# Explicit Non-Goals

Do not implement:

- browser Git staging execution;
- browser commit execution;
- browser push;
- browser fetch/pull;
- selective staging;
- partial-hunk staging;
- branch management;
- repository cloning;
- GitHub API;
- GitHub authentication;
- user accounts;
- LAN authentication;
- TLS;
- reverse proxy;
- Docker deployment;
- systemd service;
- automatic startup;
- multi-repository management;
- arbitrary filesystem browsing;
- source-code editor;
- browser shell/terminal;
- generic Git command execution;
- WebSockets;
- background task queue;
- cloud AI;
- telemetry;
- Photo Organizer validation.

---

# No Generic Execution Escape Hatch

Do not expose routes equivalent to:

    /shell
    /exec
    /git?args=...
    /run-command

The browser may invoke only explicitly supported Repo Control Plane core operations.

No user-controlled shell command construction.

---

# Security / Escalation Protocol

STOP and report rather than broadening scope if:

- existing core services cannot be invoked cleanly without CLI parsing;
- web implementation would require duplicating Git/state logic;
- repository path cannot be safely bound at server startup;
- a browser route can mutate Git unexpectedly;
- HTML/template escaping cannot be established;
- custom input can escape repository/artifact boundaries;
- CSRF protection cannot be implemented cleanly;
- a new dependency materially changes project packaging/deployment architecture;
- live GPT-OSS integration exposes thinking or raw provider internals;
- validation would require Photo Organizer access.

Report:

1. exact gate;
2. observed state;
3. expected state;
4. target repository mutations already performed, if any;
5. external Repo Control Plane artifacts created;
6. web process state;
7. current development-repository HEAD/status;
8. smallest next decision required.

Do not automatically broaden the architecture.

---

# Required Closeout

Create:

`docs/009_browser_ui_foundation_and_read_only_console_closeout.md`

Include:

1. status — PASS or ESCALATION;
2. initial branch / HEAD / clean preflight;
3. files changed;
4. web framework/dependencies selected and rationale;
5. web/core architecture;
6. CLI `repoctl web` command;
7. repository startup-binding contract;
8. loopback/non-loopback behavior;
9. dashboard implementation;
10. context UI implementation;
11. snapshot UI implementation;
12. comparison UI implementation;
13. GPT-OSS analysis UI implementation;
14. workflow visibility implementation;
15. explicit browser Git-mutation prohibition;
16. CSRF implementation;
17. HTML/output escaping evidence;
18. external-state boundary;
19. no-telemetry/offline asset behavior;
20. CLI preservation result;
21. focused web test result;
22. full regression result;
23. Python-cache hygiene result;
24. practical isolated-repository browser validation;
25. live GPT-OSS browser validation result or bounded provider-unavailable report;
26. Windows SSH-tunnel access validation/documentation;
27. confirmation no browser Git mutation occurred;
28. confirmation no network Git mutation occurred;
29. confirmation no Vocab App mutation occurred;
30. confirmation no Photo Organizer access occurred;
31. dependency additions;
32. limitations/deferred items;
33. recommendation for M010;
34. literal final `git status --short`.

Do not commit or push unless separately instructed.

---

# Acceptance Criteria

Milestone 009 passes only if:

- browser UI starts through an explicit Repo Control Plane command;
- default server binding is loopback-only;
- browser is bound to one startup-selected repository;
- browser cannot browse arbitrary filesystem repositories;
- UI uses existing Repo Control Plane core services;
- CLI remains functional independently;
- dashboard renders current deterministic Git/workflow state;
- upstream information retains the no-remote-refresh caveat;
- deterministic context can be generated and rendered human-readably;
- snapshots can be created through existing M004 logic;
- known snapshots can be compared;
- structural comparisons render human-readably;
- known comparisons can be analyzed through existing local GPT-OSS service;
- AI output preserves grounded evidence IDs;
- AI output is explicitly labeled advisory;
- hidden model thinking is never rendered;
- workflow plan/execution evidence can be displayed where implemented;
- browser routes do NOT stage files;
- browser routes do NOT commit;
- browser routes do NOT push/fetch/pull;
- target Git state remains unchanged by all M009 browser actions;
- artifact-producing browser actions require POST;
- POST actions require CSRF protection;
- user/repository-derived HTML is safely escaped;
- expected application errors render safely;
- no arbitrary command execution surface exists;
- no telemetry/cloud UI dependency exists;
- external CSS/assets are not required;
- target-repository evidence remains stored externally;
- focused browser tests pass;
- full Repo Control Plane regression suite passes;
- M006.1 cache hygiene remains effective;
- practical browser validation succeeds against a disposable repository;
- Windows access method is documented;
- no Vocab App mutation occurs;
- no Photo Organizer access occurs;
- final development repository status contains only intended M009 changes.

Successful completion establishes the first trusted human-facing Repo Control Plane console.

The intended M010 direction is then:

    browser review of exact stage plan
        ↓
    explicit Approve Stage
        ↓
    verified staged state
        ↓
    snapshot
        ↓
    browser review of exact commit plan
        ↓
    explicit Approve Commit
        ↓
    verified local commit

using the existing M007/M008 core services rather than introducing new mutation logic into the UI.
