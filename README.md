# Repo Control Plane (Milestone 001)

Repo Control Plane provides a deterministic, read-only repository scanner:

repoctl scan <repository>

Milestone 002 extends scan results with deterministic static relationship analysis for internal Python module dependencies, imported symbols, conservative call relationships, and test-to-symbol static references.

Milestone 003 adds deterministic context-pack generation:

repoctl context "<query>" [--repository <path>]

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

Context packs are lexical and deterministic (no AI, embeddings, or semantic search), use a fixed seed-plus-one-hop selection strategy, and enforce fixed bounds for seeds, files, symbols, relationships, and test references.
They are navigation evidence, not source-code authority.

## Read-only target guarantee

Milestone 001 only performs read-only filesystem and Git inspection of the target repository.
It does not write, stage, commit, switch branches, or otherwise mutate the target repository.

## Milestone 001 limitations

- No AI integration.
- No call graph or test-to-symbol mapping.
- No dependency resolution.
- No Git write operations.
- No repository delta/snapshot features.
