# Repo Control Plane (Milestone 001)

Repo Control Plane provides a deterministic, read-only repository scanner:

repoctl scan <repository>

## Development install

```bash
python -m pip install -e .
```

## Usage

```bash
repoctl scan /path/to/git/repo
```

## External state location

Default root:

~/.local/share/repoctl/

Outputs are written into a deterministic repository-specific directory and include:

- repository.json
- files.json
- symbols.json
- tests.json
- summary.md

## Read-only target guarantee

Milestone 001 only performs read-only filesystem and Git inspection of the target repository.
It does not write, stage, commit, switch branches, or otherwise mutate the target repository.

## Milestone 001 limitations

- No AI integration.
- No call graph or test-to-symbol mapping.
- No dependency resolution.
- No Git write operations.
- No repository delta/snapshot features.
