# Repo Control Plane v0.1 — Architecture and Implementation Plan

## 1. Purpose

Repo Control Plane is a standalone local development-governance and repository-intelligence system.

Its purpose is to improve AI-assisted software development by:

1. creating a deterministic, inspectable map of a software repository;
2. reducing repeated repository reconnaissance by AI coding agents;
3. detecting structural change and possible architectural degradation over time;
4. simplifying Git and milestone workflow while preserving explicit human control;
5. providing bounded, high-quality context to architects and coding agents;
6. using local AI selectively for interpretation and review without allowing the AI to become the authority for repository facts.

The initial target for development and validation is the disposable Vocab App repository.

Photo Organizer must not be modified or used as the development target until Repo Control Plane has passed its early validation milestones.

---

# 2. Problems Being Solved

## 2.1 Repository Quality and "Spaghetti Code" Risk

AI-assisted development can produce code that works while gradually accumulating:

- redundant implementations;
- duplicate logic;
- unnecessary abstractions;
- oversized files or functions;
- tangled dependencies;
- workarounds for earlier workarounds;
- obsolete or orphaned routines;
- weakly tested surfaces;
- excessive architectural churn;
- multiple paths for accomplishing the same responsibility.

Passing tests alone does not prove that repository architecture remains healthy.

Repo Control Plane will provide deterministic structural evidence and before/after comparison so architectural degradation becomes visible.

It will identify signals and anomalies, not declare architectural truth automatically.

Human architectural judgment remains authoritative.

---

## 2.2 Repeated AI Repository Reconnaissance

Current AI coding agents frequently spend substantial time and token budget rediscovering:

- repository layout;
- relevant files;
- functions and classes;
- dependencies;
- tests;
- Git history;
- related prior changes;
- likely entry points;
- protected areas.

Much of this information is mechanical and can be generated deterministically once and maintained locally.

Repo Control Plane will create a persistent structured repository intelligence layer that can be queried to generate targeted context packs.

Coding agents may use these packs as navigation assistance while remaining required to verify authoritative source code before modification.

---

## 2.3 Git and Milestone Workflow Overhead

Git operations are deterministic but currently require repeated manual bookkeeping and AI explanation.

Repo Control Plane will eventually provide guarded workflow commands that:

- inspect repository state;
- establish milestone baselines;
- identify changed and unexpected files;
- track branch and commit relationships;
- prepare commits;
- prepare pushes;
- generate milestone change packets.

Git-writing operations will be introduced only after read-only behavior is proven.

Dangerous operations will remain outside automated authority unless explicitly approved in a future design.

---

## 2.4 Development Workflow Coordination

The development workflow includes several participants:

- Product Owner / user;
- ChatGPT architect;
- Codex / Copilot coding agents;
- local GPT-OSS;
- Git;
- tests and static-analysis tools.

Repo Control Plane will provide a common evidence layer and handoff format so each participant has a clearly defined responsibility.

---

# 3. Authority Model

The system must maintain strict separation between deterministic evidence and AI interpretation.

## 3.1 Deterministic Repository Intelligence

Authoritative for mechanical facts such as:

- repository path;
- Git branch;
- Git commit;
- Git status;
- files;
- file hashes;
- file sizes;
- line counts;
- functions;
- classes;
- imports;
- declared dependencies;
- module relationships;
- test structures;
- Git differences;
- later, call relationships and repository-history metrics.

Mechanical repository facts must not depend on an LLM.

---

## 3.2 Local GPT-OSS

GPT-OSS may later provide:

- architectural interpretation;
- anomaly explanation;
- bounded code review;
- candidate classification;
- prioritization;
- follow-up questions;
- change-delta interpretation;
- low-risk supervised coding.

GPT-OSS is not authoritative for:

- exhaustive repository inventories;
- exact Git state;
- exact dependency lists;
- exact symbol lists;
- test coverage facts;
- merge decisions;
- architectural approval.

AI interpretation must remain visibly distinct from deterministic evidence.

---

## 3.3 ChatGPT Architect

ChatGPT owns:

- requirements interpretation;
- architectural reasoning;
- milestone design;
- scope definition;
- risk classification;
- coding-agent prompts;
- evaluation of repository evidence against product architecture.

Repo Control Plane should reduce the amount of raw repository reconnaissance ChatGPT needs, but it does not replace architectural judgment.

---

## 3.4 Codex / Copilot

Coding agents own implementation within explicitly approved scope.

They may consume Repo Control Plane context packs to reduce reconnaissance.

They must still verify relevant source and tests before modifying code.

Coding agents do not own:

- product architecture;
- merge authority;
- repository truth;
- unapproved scope expansion.

---

## 3.5 Product Owner

The Product Owner retains final authority for:

- milestone scope;
- architecture approval;
- unexpected changes;
- commits;
- pushes;
- merges;
- releases;
- destructive operations.

---

# 4. Physical Architecture

Repo Control Plane is a standalone project.

Initial project location:

    /home/chuck/projects/repo-control

It must not live inside Photo Organizer.

Conceptual structure:

    repo-control/
    ├── pyproject.toml
    ├── README.md
    ├── docs/
    │   └── Repo_Control_Plane_v0.1_Architecture_and_Implementation_Plan.md
    ├── src/
    │   └── repoctl/
    │       ├── __init__.py
    │       ├── cli.py
    │       ├── scanner/
    │       ├── context/
    │       ├── audit/
    │       ├── git/
    │       ├── ai/
    │       └── reporting/
    └── tests/

The user-facing application will ultimately expose one command:

    repoctl

Internal capabilities will be implemented as modules beneath that command.

The user should not need to operate independent Python scripts for each capability.

---

# 5. Initial Interaction Model

Version 0.1 will be CLI-first.

Examples of eventual commands:

    repoctl scan <repository>
    repoctl context <topic>
    repoctl snapshot <name>
    repoctl compare <snapshot>
    repoctl milestone status
    repoctl milestone start
    repoctl milestone review
    repoctl milestone prepare-commit
    repoctl milestone commit
    repoctl milestone push

Only `repoctl scan` is authorized for Milestone 001.

A web dashboard may be added later using the same backend.

The CLI is deliberately first because it is:

- easy to validate;
- transparent;
- scriptable;
- deterministic;
- suitable for Linux;
- easy to integrate with VS Code and SSH.

---

# 6. Execution Model

Initial operations are explicitly user-invoked.

The system must not silently modify or inspect unrelated repositories.

Initial flow:

    user command
        ->
    repoctl states what it is analyzing
        ->
    deterministic operation
        ->
    explicit result
        ->
    generated artifacts

Automatic execution may be added later for safe operations such as post-merge scans or CI validation.

Git writes, merge operations, branch deletion, resets, and other destructive operations remain explicitly human-controlled.

---

# 7. Input Model

Repo Control Plane has three categories of input.

## 7.1 Repository-Derived Input

Automatically obtained from the target repository:

- Git metadata;
- files;
- source structure;
- imports;
- tests;
- dependencies;
- history;
- differences.

The user should not manually supply data that can be derived mechanically.

---

## 7.2 Workflow Input

Later milestones may consume milestone metadata such as:

- milestone number;
- intent;
- expected files or subsystems;
- protected areas;
- allowed areas;
- baseline commit;
- target commit.

This metadata may eventually be generated as part of architect-created milestone prompts.

---

## 7.3 Human Decisions

Human input should primarily consist of decisions:

- run operation;
- approve scope;
- accept warning;
- commit;
- push;
- merge.

The system should minimize repetitive manual data entry.

---

# 8. Output and State Model

Initial generated state must remain outside the analyzed repository.

Default state root:

    ~/.local/share/repoctl/

Example:

    ~/.local/share/repoctl/
    └── vocab-app/
        ├── repository.json
        ├── files.json
        ├── symbols.json
        ├── dependencies.json
        ├── tests.json
        └── summary.md

Machine-generated state is regeneratable and is not part of the target repository.

Later durable project records may be deliberately exported into project documentation, for example:

    docs/change_packets/<milestone>_change_packet.md

Machine cache and durable project records must remain conceptually separate.

---

# 9. Safety Model

## 9.1 Initial Target Repository Access

Milestones 001 through the early repository-intelligence arc are read-only with respect to the target repository.

Repo Control Plane may:

- read files;
- inspect Git metadata;
- execute read-only Git commands;
- parse source;
- write only to its external Repo Control Plane state directory.

It may not:

- edit target files;
- stage files;
- commit;
- push;
- switch target branches;
- reset;
- clean;
- delete;
- merge;
- modify configuration;
- execute application migrations;
- modify runtime services.

---

## 9.2 Failure Behavior

If repository state is ambiguous or an operation cannot be proven read-only, stop and report.

Do not invent alternate mutation methods.

Do not silently repair the target repository.

---

# 10. Repository Intelligence Model

The repository map is not intended to be one large prose document.

The authoritative representation is structured machine-readable data.

Initial data products should evolve toward:

    repository.json
    files.json
    symbols.json
    dependencies.json
    tests.json
    git_history.json

Human-readable Markdown summaries are projections of that structured data.

This allows:

- deterministic regeneration;
- querying;
- targeted context generation;
- model independence;
- later use by ChatGPT, Codex, Copilot, GPT-OSS, CI, and human reviewers.

---

# 11. Context Pack Model

A later `repoctl context` capability will convert repository intelligence into bounded task-specific context.

Example:

    repoctl context "source readiness"

Potential output:

    Relevant files
    Relevant functions/classes
    Internal dependency relationships
    Relevant tests
    Recent related Git changes
    Suggested source locations to inspect
    Protected areas

Context packs are navigation aids.

They do not supersede source code.

Coding agents must verify relevant source before implementation.

---

# 12. Repository Change Auditing

A later before/after audit will compare repository structure across a milestone.

Potential deterministic changes include:

- files added/removed/modified;
- functions/classes added or removed;
- dependencies added or removed;
- tests added or removed;
- new circular dependencies;
- large file/function growth;
- duplicate-code signals;
- Git churn changes;
- unexpected files touched.

This provides evidence for architectural QA beyond ordinary test success.

Structural signals indicate areas requiring review; they are not automatic declarations that code is defective.

---

# 13. Local AI Integration

GPT-OSS will not be part of Milestone 001.

When introduced, GPT-OSS should receive bounded deterministic evidence and relevant source/diffs only when necessary.

Preferred task:

    deterministic evidence
        ->
    GPT-OSS interpretation
        ->
    architect/human review

Avoid:

    GPT-OSS searches entire repository
        ->
    GPT-OSS reconstructs mechanical facts
        ->
    GPT-OSS becomes factual authority

The successful local configuration established during experimentation is:

    Aider
    +
    ollama_chat/gpt-oss:20b
    +
    diff editing for existing substantial files
    +
    explicit Git/test review

GPT-OSS remains supervised.

---

# 14. Git Workflow Direction

Git support will be introduced in stages.

## Stage A — Read-only

    repoctl milestone status

May report:

- branch;
- HEAD;
- upstream;
- cleanliness;
- commits ahead/behind;
- changed files;
- untracked files;
- baseline relationships.

## Stage B — Guarded Writes

Later commands may include:

    repoctl milestone start
    repoctl milestone prepare-commit
    repoctl milestone commit
    repoctl milestone push

Before any write:

- show exact proposed operation;
- show exact files affected;
- require explicit approval;
- fail closed on unexpected state.

## Explicitly excluded unless separately approved

- force push;
- reset --hard;
- automatic merge to main;
- branch deletion;
- history rewriting;
- automatic conflict resolution;
- silent file discard.

---

# 15. Change Packet Direction

The eventual common milestone artifact should combine:

    intent
    Git state
    changed files
    test results
    static checks
    repository structural delta
    architecture-health signals
    local AI observations
    coder closeout
    unresolved questions
    readiness status

This becomes a common handoff artifact among:

- Product Owner;
- ChatGPT architect;
- coding agent;
- GPT-OSS reviewer;
- Git/GitHub history.

---

# 16. Implementation Milestones

## Milestone 001 — Deterministic Repository Scanner

Build production-quality:

    repoctl scan <repository>

Read-only.

No AI.

No Git writes.

Test only against Vocab App initially.

---

## Milestone 002 — Repository Relationships

Add deterministic:

- imported-symbol extraction;
- internal module dependency graph;
- top-level call relationships where statically knowable;
- test classes;
- test methods;
- test-to-symbol references where statically knowable.

---

## Milestone 003 — Context Pack Generator

Build:

    repoctl context <topic>

Generate bounded navigation context from deterministic repository intelligence.

Test whether a coding agent can locate relevant implementation areas with materially less broad reconnaissance.

---

## Milestone 004 — Snapshot and Repository Delta Audit

Build:

    repoctl snapshot <name>
    repoctl compare <name>

Generate deterministic before/after structural changes.

Begin QA use for architectural-churn detection.

---

## Milestone 005 — GPT-OSS Analysis Layer

Feed bounded deterministic evidence to local GPT-OSS.

Use AI only for:

- interpretation;
- anomaly prioritization;
- architectural questions;
- candidate review.

Mechanical facts remain deterministic authority.

---

## Milestone 006 — Git Workflow Intelligence

Add read-only milestone/Git reporting.

No Git mutation yet.

---

## Milestone 007+ — Guarded Git Operations

Introduce carefully bounded Git writes with explicit approval gates.

---

# 17. Milestone 001 Required Capability

The first production capability must be:

    repoctl scan <repository>

It should deterministically capture at minimum:

## Repository

- resolved repository path;
- repository identifier;
- branch;
- HEAD commit;
- working-tree status;
- tracked-file count.

## Files

For every tracked file:

- relative path;
- extension/type;
- byte size;
- line count when text-decodable;
- SHA-256.

## Python Structure

For every tracked Python file:

- parse success/failure;
- top-level functions;
- function start/end lines;
- top-level classes;
- class start/end lines;
- top-level imports.

## Requirements

For recognized requirements files:

- non-comment requirement declarations.

## Tests

At minimum:

- test-like Python files identified conservatively;
- top-level test classes;
- test methods inside those classes.

Test discovery must not claim that a behavior is tested merely because of naming.

## Outputs

Write structured results beneath external Repo Control Plane state.

Produce:

    repository.json
    files.json
    symbols.json
    tests.json
    summary.md

The exact schema should be simple, versioned, and deterministic.

---

# 18. Milestone 001 Explicit Non-Goals

Do not implement:

- GPT-OSS;
- Aider integration;
- Codex integration;
- context generation;
- architectural scoring;
- complexity scoring;
- duplicate detection;
- call graphs;
- change snapshots;
- Git writes;
- Git branch creation;
- commit/push support;
- web UI;
- daemon/background service;
- Photo Organizer integration.

The purpose of Milestone 001 is trustworthy repository fact extraction.

---

# 19. Initial Validation Target

Primary target:

    /home/chuck/ai-agent-tests/vocab-app

The existing experimental repository inventory provides known facts that can be used for comparison.

The production scanner should reproduce the known repository structure without requiring AI interpretation.

---

# 20. Future Benchmark — Photo Organizer M012 Reconnaissance

The completed Photo Organizer reconnaissance:

    Milestone 12.65.0 — Bounded M012 Delta Classification Reconnaissance

should be retained as a future benchmark.

Relevant bounded range:

    461653e..453032b

Known characteristics include:

- 8 commits;
- 48 changed paths;
- mixed implementation and correction commits;
- backend Source identity changes;
- backend test changes;
- frontend changes;
- development runtime/operator assets;
- historical milestone documentation;
- protected subsystems confirmed unchanged;
- KEEP / REVISE / RESTORE / DISCARD classification;
- reconstruction roadmap.

A future Repo Control Plane benchmark should measure how much of the mechanical reconnaissance can be reproduced deterministically and how much architectural work can be reduced before involving a high-cost coding agent.

The objective is not necessarily to reproduce the prose closeout.

The objective is to minimize expensive AI repository archaeology while improving factual certainty.

---

# 21. Success Criteria

Repo Control Plane should be considered successful only if it demonstrates measurable value.

Key measures:

## Accuracy

Mechanical repository facts match direct Git/source inspection.

## Repeatability

Repeated scans of the same commit produce equivalent structured facts.

## Safety

Scanning does not modify the target repository.

## Reconnaissance Reduction

Coding agents can begin from targeted repository context instead of broad repository discovery.

## QA Visibility

Structural changes become visible across milestones.

## Cost Reduction

Expensive cloud coding-agent usage spent on repository reconnaissance is materially reduced.

## Transparency

The Product Owner can determine:

- what was inspected;
- what changed;
- what checks ran;
- what AI concluded;
- what remains uncertain.

## Model Independence

Replacing GPT-OSS or a coding agent does not invalidate the deterministic repository intelligence layer.

---

# 22. Governing Principle

Use deterministic tools for facts.

Use AI for interpretation.

Use tests and source code for validation.

Use Git for history.

Use humans for architectural and irreversible decisions.
