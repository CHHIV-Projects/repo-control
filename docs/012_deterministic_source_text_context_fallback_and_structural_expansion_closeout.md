# M012 Deterministic Source-Text Context Fallback and Structural Expansion Closeout

## 1. Executive result

**PASS**

M012 materially improves deterministic Context discovery while preserving exact structural-symbol behavior, bounded one-hop expansion, target-repository immutability, and the existing Context artifact contract.

The implementation now uses existing scanner import/attribute metadata, existing `requirements.txt` dependency evidence, and a bounded parser-aware single-line string-literal fallback. Evidence retains provenance, matched tokens, file paths, line locations, and enclosing-symbol/module-scope information where available.

## 2. Starting Repo Control state

The M012 starting-state gate was captured before implementation:

- branch: `main`
- HEAD: `7d8222f7f5f7bb88f226b9524eaccfb59272b51c`
- upstream: `7d8222f7f5f7bb88f226b9524eaccfb59272b51c` (`origin/main`)
- ahead/behind for `HEAD...@{upstream}`: `0 0`

Literal starting `git status --short`:

```text
 M docs/008_guarded_staging_preparation_prompt.md
 M docs/009_browser_ui_foundation_and_read_only_console_prompt.md
?? .venv/
```

These were the expected pre-existing documentation/runtime items. No unexpected Repo Control source changes or evidence-attribution ambiguity was found.

## 3. Prompt lifecycle verification

- prompt: `docs/012_deterministic_source_text_context_fallback_and_structural_expansion_prompt.md`
- prompt commit: `7d8222f7f5f7bb88f226b9524eaccfb59272b51c`
- commit subject: `Add Repo Control M012 deterministic Context discovery prompt`
- prompt was committed before implementation began.

## 4. Pre-change test baseline

Command:

```bash
cd /home/chuck/projects/repo-control
. .venv/bin/activate
PYTHONPATH=src python3 -m unittest tests.test_context tests.test_scanner
```

Literal result:

```text
Ran 30 tests in 0.461s
OK
```

## 5. Implementation summary

Changed implementation/test surfaces:

- `src/repoctl/scanner/python_scan.py`
  - records deterministic import and attribute evidence from the existing Python AST parse;
  - records line ranges and optional enclosing structural symbols;
  - marks module-scope evidence explicitly.
- `src/repoctl/scanner/core.py`
  - persists the parser-derived source evidence in the existing symbols artifact.
- `src/repoctl/context/policy.py`
  - adds named deterministic evidence-ranking weights.
- `src/repoctl/context/generator.py`
  - consumes import/attribute evidence;
  - consumes existing `requirements.txt` declarations;
  - performs bounded single-line non-docstring string matching in safe tracked Python files;
  - applies same-file token-AND ranking;
  - maps source hits to enclosing symbols where available;
  - renders a `Discovery Evidence` section in Context Markdown.
- `tests/test_context.py`
  - adds generalized native coverage for evidence provenance, multiword same-file behavior, enclosing-symbol mapping, and secret-named-file exclusion.

No Vocab file was modified. No unrelated Repo Control subsystem was changed.

## 6. Existing metadata integration

M012 uses the authoritative scanner output rather than creating a second import parser.

Consumed metadata includes:

- parsed import records;
- imported module names/items;
- imported symbols;
- existing `requirements.txt` declarations;
- existing module-resolution and relationship payloads.

`gspread` and `streamlit` are now discoverable through import evidence, and dependency evidence is available from the scanner’s existing `requirements.txt` support.

## 7. Source evidence implementation

The bounded source fallback supports:

- AST attribute evidence, including attribute name, simple receiver/base, dotted expression, line range, and enclosing symbol/module scope;
- single-line, non-docstring string literals up to 256 characters;
- in-memory string matching without storing literal contents in Context artifacts;
- safe tracked Python paths only.

Comments, unrestricted configuration values, arbitrary binary/data files, and broad manifest discovery were not added.

## 8. Evidence provenance

Evidence records retain inspectable fields including:

- `evidence_kind`: `import`, `dependency`, `attribute`, or `string_literal`;
- `matched_tokens`;
- file path;
- source line/end line where available;
- `enclosing_symbol` where unambiguous;
- `scope`, including `module_scope` when no enclosing symbol exists;
- deterministic reason text.

The rendered Context Markdown now includes `Discovery Evidence`. Literal source content is not emitted.

## 9. Enclosing-symbol/module-scope behavior

Source hits inside parsed functions/classes map to the enclosing structural symbol and can participate in existing relationship selection. Module-level hits retain explicit `module_scope` rather than being assigned a fabricated function.

For Vocab’s module-level Streamlit/session-state initialization, the file and attribute evidence are surfaced without requiring a structural symbol named `session_state`.

## 10. Ranking and deduplication

Exact structural behavior remains highest priority. New evidence uses named deterministic weights below exact symbol/path behavior:

1. exact structural symbol;
2. exact path/module component;
3. exact import/dependency evidence;
4. exact attribute evidence;
5. exact/full source evidence;
6. same-file multi-token evidence;
7. existing path/module token evidence;
8. lower-confidence single-token evidence.

Evidence is deduplicated by typed identity and ordered deterministically by score, matched-token count, evidence type, path, line, and name. Existing seed/file/symbol/relationship/test caps remain in force.

## 11. Noise controls

M012 preserves bounded selection limits:

- `MAX_SEEDS = 12`;
- `MAX_FILES = 20`;
- `MAX_SYMBOLS = 40`;
- `MAX_RELATIONSHIPS = 40`;
- `MAX_TEST_REFERENCES = 20`.

Same-file token-AND evidence is higher-confidence than unrelated repository-wide token coincidence. Evidence does not become a semantic architecture claim merely because a common token occurs.

## 12. Security protections

The source fallback:

- uses the scanner’s tracked Python file set;
- excludes conservative secret-bearing Python filename fragments such as `.env`, `credential`, `secret`, `service_account`, `private_key`, and `token`;
- excludes non-Python arbitrary files from the source fallback;
- ignores docstrings and multiline/overlong string literals for the initial string boundary;
- stores no literal content in Context artifacts;
- emits only provenance, tokens, paths, and locations;
- uses synthetic fake secret coverage only;
- leaves target repositories read-only.

## 13. Native fixture coverage

New generalized tests cover:

- import evidence;
- dependency evidence;
- attribute evidence;
- string-literal evidence;
- same-file multiword token-AND across separate evidence records;
- enclosing-symbol mapping;
- secret-named Python-file exclusion;
- provenance and selected-file association.

The native tests do not rely exclusively on Vocab.

### Required 16-case coverage matrix

| Required case | Test method(s) providing coverage |
|---|---|
| 1. import-only match | `ContextTests.test_source_evidence_preserves_import_attribute_string_and_dependency_provenance` |
| 2. dependency-only match | `ContextTests.test_source_evidence_preserves_import_attribute_string_and_dependency_provenance` |
| 3. attribute-only match | `ContextTests.test_source_evidence_preserves_import_attribute_string_and_dependency_provenance` |
| 4. string-literal match | `ContextTests.test_source_evidence_preserves_import_attribute_string_and_dependency_provenance` |
| 5. multiword query | `ContextTests.test_source_evidence_uses_same_file_multiword_matching` |
| 6. source hit inside an enclosing function | `ContextTests.test_source_evidence_maps_to_enclosing_symbol` |
| 7. source hit at module scope | `ContextTests.test_source_evidence_module_scope_priority_bounds_and_line_ranges` |
| 8. ignored/secret-bearing file exclusion | `ContextTests.test_secret_named_python_files_are_excluded_from_source_evidence`; `ContextTests.test_ignored_source_and_incidental_or_database_terms_do_not_claim_implementations` |
| 9. noisy common-term bounds | `ContextTests.test_source_evidence_module_scope_priority_bounds_and_line_ranges` |
| 10. exact-symbol priority over broader source evidence | `ContextTests.test_source_evidence_module_scope_priority_bounds_and_line_ranges` |
| 11. deterministic ordering | `ContextTests.test_deterministic_context_outputs`; `ContextTests.test_source_evidence_module_scope_priority_bounds_and_line_ranges` |
| 12. evidence provenance | `ContextTests.test_source_evidence_preserves_import_attribute_string_and_dependency_provenance` |
| 13. line/range determinism | `ContextTests.test_source_evidence_module_scope_priority_bounds_and_line_ranges` |
| 14. no target mutation | `ContextTests.test_target_repo_unchanged` |
| 15. legitimate no-match | `ContextTests.test_no_match_is_successful` |
| 16. incidental-substring negative control | `ContextTests.test_ignored_source_and_incidental_or_database_terms_do_not_claim_implementations` |

The database branch of `ContextTests.test_ignored_source_and_incidental_or_database_terms_do_not_claim_implementations` additionally verifies that incidental lexical/string evidence does not become a structural database implementation claim.

## 14. Existing regression evidence

The existing exact-symbol and Context behavior remained passing. The final focused Context/scanner result was:

```text
Ran 36 tests in 0.589s
OK
```

This includes the original 30-test baseline coverage plus six M012 behavior/security tests.

## 15. Vocab benchmark — exact symbols

Canonical acceptance repository:

`/home/chuck/projects/vocab-app`

Canonical Vocab scan:

- HEAD: `a3fcc8a7bd1e25676d9dbe11de5c644a629a9c1c`
- Python parse errors: `0`

Results:

- `get_sheet`: matched; `app.py` surfaced; structural symbol and relationship context preserved.
- `update_score`: matched; `app.py` surfaced.
- `get_synonyms_nltk`: matched; `app.py` surfaced.

## 16. Vocab benchmark — source/import

- `gspread`: matched; `app.py` import evidence and `requirements.txt` dependency evidence surfaced; `get_sheet`/related context remained available.
- `streamlit`: matched; `app.py` import evidence and `requirements.txt` dependency evidence surfaced.
- `session_state`: matched; `app.py` attribute evidence surfaced with `session` and `state` tokens and module-scope handling; no `session_state` structural symbol was required.

## 17. Vocab benchmark — product language

- `practice`: matched through bounded string-literal evidence in `app.py`; no architectural interpretation was fabricated.
- `google sheets`: matched through same-file deterministic evidence in `app.py`; `google` and `sheets` remained separately inspectable, and no claim was made that the exact phrase occurs in source.

The canonical evidence includes Google-related URL text and sheet-related source evidence in the same file, which is sufficient for deterministic navigation but not semantic architectural certainty.

## 18. Vocab benchmark — semantic boundary

- `worksheet`: `no_matches`; the literal was absent from inspected source/dependency evidence.
- `quiz`: `no_matches`; the literal was absent from the current implementation terminology.

M012 does not add aliases or semantic inference to force these queries to match.

## 19. Vocab benchmark — negative controls

- `container`: `no_matches`; incidental `use_container_width` did not produce a false container-infrastructure result.
- `database`: bounded string evidence was found in incidental application text, but no structural symbols or database implementation evidence were produced. This remains an honest lexical result, not a database claim.

## 20. Before/after benchmark comparison

M011 baseline:

- exact structural symbols matched;
- `gspread`, `streamlit`, `session_state`, `practice`, and `google sheets` returned `no_matches`;
- `container` and `database` returned `no_matches`.

M012 result:

- exact structural controls remain matched;
- `gspread` and `streamlit` now produce import/dependency evidence;
- `session_state` now produces attribute evidence;
- `practice` now produces bounded string evidence;
- `google sheets` now produces same-file multi-token evidence;
- `container` remains `no_matches`;
- `database` produces only explicitly labeled incidental string evidence and no implementation claim;
- `worksheet` and `quiz` remain honest no-match semantic-boundary cases.

## 21. CLI/browser compatibility

CLI and browser Context generation continue to call the same `run_scan_with_artifacts` and `build_and_publish_context` core services. No browser-only discovery algorithm was added.

The generated Context Markdown exposes discovery provenance through the shared artifact renderer. Existing browser Context views continue to consume the same Context artifact.

## 22. Artifact compatibility

The Context artifact remains `schema_version: 1`. New provenance is additive within existing seed records and scanner payloads. No strict schema consumer or existing test required a version increment.

Existing Context identity remains based on canonical query and repository state. Repeated scans and deterministic selection continue to use the existing publication and identity contracts.

## 23. Performance findings

The final focused Context/scanner suite ran in `0.589s` for 36 tests. The full Repo Control suite ran in `6.509s` for 160 tests.

The canonical Vocab benchmark completed within a single bounded read-only command across all twelve queries. M012 uses query-time parsing of the scanner’s tracked Python file set and does not introduce a persistent full-text index.

## 24. Target repository immutability

The canonical Vocab benchmark captured before/after Git state:

- `VOCAB_HEAD_UNCHANGED True`
- `VOCAB_STATUS_UNCHANGED True`

Vocab remained at HEAD `a3fcc8a7bd1e25676d9dbe11de5c644a629a9c1c`. Its pre-existing documentation-only status remained:

```text
 M milestones/002.1_repo_control_integration_baseline_and_m002_evidence_comparison_prompt.md
?? milestones/002.1_repo_control_integration_baseline_and_m002_evidence_comparison_closeout.md
```

No Vocab application source file was modified. Photo Organizer was not accessed.

## 25. Coder burden/result assessment

M012 materially reduces mechanical discovery work for ordinary terminology that has repository evidence. A coder can now start with `gspread`, `streamlit`, `session_state`, `practice`, or `google sheets` and reach relevant files and inspectable evidence without first knowing the exact function name.

The coder still owns architectural interpretation, ambiguity resolution, and broader semantic query planning.

## 26. Remaining product-language gap

Deterministic Context now bridges product terminology as far as supported repository tokens and evidence permit. It does not infer that a set of lexical hits constitutes an architecture, and it does not answer broad questions requiring semantic interpretation such as “where does the application remember whether I knew a word?”

That boundary is intentional and remains outside M012.

## 27. Scope deviations

No authorized scope deviation occurred.

The implementation did not add embeddings, semantic retrieval, arbitrary synonyms, broad manifest support, unrestricted comments/configuration search, persistent indexing, Git mutation, target-code execution, or Vocab-specific rules.

## 28. Test summary

Pre-change baseline:

```text
Ran 30 tests in 0.461s
OK
```

Final focused Context/scanner regression:

```text
Ran 36 tests in 0.589s
OK
```

Final full Repo Control regression:

```text
Ran 160 tests in 6.509s
OK
```

Compilation validation:

```text
PYTHONPATH=src python3 -m compileall -q src tests
```

Completed successfully.

## 29. Recommended next Repo Control step

No additional milestone is required by the M012 evidence. The next useful step is to exercise this Context capability in the next real Vocab implementation workflow and observe whether further concrete gaps emerge.

## 30. Vocab readiness recommendation

The improved Context is ready to be exercised in the next real Vocab implementation milestone. It provides useful deterministic evidence from product/source terminology while preserving explicit semantic and architectural boundaries.

## 31. Final Repo Control state

Captured after implementation and validation:

- branch: `main`
- HEAD: `7d8222f7f5f7bb88f226b9524eaccfb59272b51c`
- upstream: `7d8222f7f5f7bb88f226b9524eaccfb59272b51c` (`origin/main`)
- ahead/behind: `0 0`

Literal final `git status --short`:

```text
 M docs/008_guarded_staging_preparation_prompt.md
 M docs/009_browser_ui_foundation_and_read_only_console_prompt.md
 M src/repoctl/context/generator.py
 M src/repoctl/context/policy.py
 M src/repoctl/scanner/core.py
 M src/repoctl/scanner/python_scan.py
 M tests/test_context.py
?? .venv/
?? docs/012_deterministic_source_text_context_fallback_and_structural_expansion_closeout.md
```

M012 implementation changes and tests are intentionally uncommitted. The M012 closeout is also intentionally untracked until separately authorized. No staging, commit, push, cleanup, restore, reset, or Vocab mutation was performed.
