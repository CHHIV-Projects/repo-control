# Repo Control Plane (Milestone 001)

Repo Control Plane provides a deterministic, read-only repository scanner:

repoctl scan <repository>

Milestone 002 extends scan results with deterministic static relationship analysis for internal Python module dependencies, imported symbols, conservative call relationships, and test-to-symbol static references.

Milestone 003 adds deterministic context-pack generation:

repoctl context "<query>" [--repository <path>]

Milestone 004 adds immutable snapshots and deterministic structural comparison:

repoctl snapshot [--repository <path>]
repoctl compare <before_snapshot_id> <after_snapshot_id> [--repository <path>]

Milestone 005 adds bounded local AI interpretation over immutable comparison evidence:

repoctl analyze <comparison_id> [--repository <path>]

## Development install

```bash
python -m pip install -e .
```

## Usage

```bash
repoctl scan /path/to/git/repo
```

```bash
repoctl context "synonym handling"
repoctl context "get_sheet" --repository /path/to/git/repo
repoctl snapshot --repository /path/to/git/repo
repoctl compare snap--before snap--after --repository /path/to/git/repo
repoctl analyze cmp--abcdef0123456789 --repository /path/to/git/repo
```

## External state location

Default root:

~/.local/share/repoctl/

Outputs are written into a deterministic repository-specific directory and include:

- repository.json
- files.json
- symbols.json
- tests.json
- dependencies.json
- summary.md

Context outputs are written under:

~/.local/share/repoctl/<repository_id>/contexts/<context_id>/

with:

- context.json
- context.md

Snapshots are written under:

~/.local/share/repoctl/<repository_id>/snapshots/<snapshot_id>/

Comparisons are written under:

~/.local/share/repoctl/<repository_id>/comparisons/<comparison_id>/

Analyses are written under:

~/.local/share/repoctl/<repository_id>/analyses/<comparison_id>/<analysis_id>/

with:

- analysis_input.json
- analysis.json
- analysis.md

Snapshots are content-derived and immutable. Running `repoctl snapshot` twice against identical deterministic scan evidence reuses the same snapshot ID.
Comparisons are directional and operate on named snapshots, not the repository's current working state.
Snapshot structural scope remains tracked files; if untracked worktree entries exist, completeness is explicitly reported as partial rather than implying full worktree structural analysis.
Analysis operates only on an existing immutable comparison, sends bounded structural metadata to local Ollama (`gpt-oss:20b`), and keeps deterministic comparison evidence authoritative.
AI output is advisory, immutable, external to target repositories, and does not perform Git writes.
There is no cloud fallback.

Context packs are lexical and deterministic (no AI, embeddings, or semantic search), use a fixed seed-plus-one-hop selection strategy, and enforce fixed bounds for seeds, files, symbols, relationships, and test references.
They are navigation evidence, not source-code authority.

## Read-only target guarantee

Milestone 001 only performs read-only filesystem and Git inspection of the target repository.
It does not write, stage, commit, switch branches, or otherwise mutate the target repository.

## Current limitations

- No call graph or test-to-symbol mapping.
- No dependency resolution.
- No Git write operations.
- No architectural or risk scoring.

Repo Control Plane remains read-only toward target repositories in these milestones. It does not stage, commit, push, switch branches, or otherwise perform Git writes against the target.
