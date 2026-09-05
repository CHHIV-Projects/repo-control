# M011 Context Source-Text and Product-Language Discovery Reconnaissance Closeout

## 1. Executive conclusion

M011 confirms that the current Context engine is a bounded lexical selector over scanner metadata and parsed structural symbols. It is effective for known implementation symbols such as `get_sheet`, `update_score`, and `get_synonyms_nltk`, but it does not currently use several already-persisted scanner fields as seed candidates and does not search raw source text.

The gap is therefore narrower than a full indexing redesign:

- existing import/module metadata is already sufficient to improve import discovery;
- attribute references, string literals, and module-scope source hits are not currently indexed for Context selection;
- deterministic product-language bridging is feasible where query tokens have repository evidence, without claiming semantic understanding;
- broader questions such as “where does the application remember whether I knew a word?” remain a separate semantic interpretation problem.

Recommended classification: **B — small deterministic source-text fallback required**, with an initial sub-step that uses existing scanner import metadata before adding broader source scanning.

Recommended next milestone: **M012 — Deterministic Source-Text Context Fallback and Structural Expansion**.

No Repo Control implementation change was made during M011. The only authored project output is this closeout.

## 2. Starting Repo Control state

The required starting-state gate was captured before reconnaissance:

- working directory: `/home/chuck/projects/repo-control`
- branch: `main`
- HEAD: `859f9a651aee429fe20d55b8e5d236673480e7ff`
- upstream: `859f9a651aee429fe20d55b8e5d236673480e7ff` (`origin/main`)
- ahead/behind for `HEAD...@{upstream}`: `0 0`

Literal starting `git status --short`:

```text
 M docs/008_guarded_staging_preparation_prompt.md
 M docs/009_browser_ui_foundation_and_read_only_console_prompt.md
?? .venv/
?? docs/011_context_source_text_and_product_language_discovery_reconnaissance_prompt.md
```

The modified documentation and `.venv/` were the known dirty state permitted by the M011 prompt. The M011 prompt itself was present as the untracked reconnaissance input. No unexpected source-code changes were found, and no cleanup, staging, restore, reset, commit, or push was performed.

### Prompt-start process deviation

The M011 prompt was untracked and uncommitted at reconnaissance start. This was a process deviation from the normal immutable-prompt workflow:

```text
Architect prompt -> Product Owner saves/reviews -> prompt is committed -> coder begins milestone work
```

The technical reconnaissance remains valid because the prompt content used by the coder was the controlling input throughout the run. Future milestones should restore the normal rule that the prompt is committed before coder execution begins. The prompt is not being retroactively described as committed.

## 3. Existing Context architecture

The actual query-to-result flow is:

```text
CLI repoctl context or browser Context POST
    -> run_scan_with_artifacts
    -> validate Git worktree and read current repository state
    -> enumerate tracked files
    -> parse Python files and imports
    -> discover test structure
    -> build deterministic relationships
    -> publish scan artifacts externally
    -> build_query_info
    -> build lexical seeds from paths/modules/top-level symbols
    -> select bounded files and symbols
    -> expand one hop over stored relationships
    -> select related tests and allowlisted diagnostics
    -> publish context.json and context.md externally
```

Entry points observed:

- CLI: `repoctl context "<query>" [--repository <path>]` in `src/repoctl/cli.py`.
- Browser: Context generation POST in `src/repoctl/web/app.py`, which calls the same reusable `run_scan_with_artifacts` and `build_and_publish_context` services directly.
- Browser Context viewing: `src/repoctl/web/views.py` loads and evaluates stored Context artifacts for freshness; it does not perform a second discovery algorithm.

The target repository remains read-only. Scan and Context artifacts are stored outside the target repository under the configured Repo Control state root.

## 4. Current symbol model

The current Python scanner structurally records:

- top-level functions;
- top-level async functions;
- top-level classes;
- import records;
- imported module names;
- imported symbols;
- test classes, test methods, and top-level test functions.

Context seed selection currently treats the following as direct searchable seed fields:

- tracked file paths;
- derived module candidates for files;
- names of top-level functions;
- names of top-level async functions;
- names of top-level classes.

Imported names are not currently treated as Context symbols. Attribute names, local variables, constants, string literals, comments, dependency declarations, and arbitrary test names are not direct Context seed fields. Test structure is used primarily for relationship/test-reference expansion after a seed exists.

`get_sheet`, `update_score`, and `get_synonyms_nltk` work because they are top-level function definitions in `app.py` and are included in the parsed structural symbol payload.

## 5. Current query semantics

The current query contract is deterministic and lexical:

- trim and collapse whitespace runs;
- casefold for matching;
- split tokens on whitespace, `_`, `-`, `.`, `/`, and `\\`;
- preserve first-occurrence token order and remove duplicates;
- no stemming, synonyms, embeddings, semantic inference, or AI.

Seed matching checks file paths, module candidates, and structural symbol names. It supports:

- exact structural symbol-name matching;
- exact path/module component matching;
- full-query substring matching over those fields;
- multiple-token matches over those fields;
- single-token matches over those fields.

It does not currently search:

- raw source text;
- import metadata as independent seed records;
- attribute names;
- string literals;
- comments;
- dependency manifests;
- configuration keys;
- arbitrary test names.

Current deterministic ranking is:

1. exact symbol name;
2. exact path/module component;
3. full-query substring;
4. multiple-token match;
5. single-token match.

Current bounds are `MAX_SEEDS=12`, `MAX_FILES=20`, `MAX_SYMBOLS=40`, `MAX_RELATIONSHIPS=40`, and `MAX_TEST_REFERENCES=20`.

## 6. Reproduced Vocab benchmark

Canonical benchmark repository used:

`/home/chuck/projects/vocab-app`

The historical frozen testbed `/home/chuck/ai-agent-tests/vocab-app` was not used for the M011 benchmark.

Canonical Vocab scan evidence:

- HEAD: `a3fcc8a7bd1e25676d9dbe11de5c644a629a9c1c`
- tracked files: `14`
- Python parse errors: `0`

The benchmark was run against a temporary external artifact root so the Vocab repository and persistent project state were not modified.

| Query | Canonical tokens | Status | Seeds | Selected files | Selected symbols | Relationships | Tests |
|---|---|---:|---:|---|---|---:|---:|
| `get_sheet` | `get`, `sheet` | matched | 5 | `app.py` | `get_sheet`, `get_audio_bytes`, `get_nltk_root`, `get_synonyms_nltk`, `get_mw_data`, `update_score` | 4 | 0 |
| `update_score` | `update`, `score` | matched | 1 | `app.py` | `update_score`, `get_sheet` | 1 | 0 |
| `get_synonyms_nltk` | `get`, `synonyms`, `nltk` | matched | 5 | `app.py` | `get_synonyms_nltk`, `get_nltk_root`, `get_sheet`, `get_audio_bytes`, `get_mw_data`, `update_score` | 4 | 0 |
| `gspread` | `gspread` | no_matches | 0 | none | none | 0 | 0 |
| `worksheet` | `worksheet` | no_matches | 0 | none | none | 0 | 0 |
| `session_state` | `session`, `state` | no_matches | 0 | none | none | 0 | 0 |
| `streamlit` | `streamlit` | no_matches | 0 | none | none | 0 | 0 |
| `google sheets` | `google`, `sheets` | no_matches | 0 | none | none | 0 | 0 |
| `practice` | `practice` | no_matches | 0 | none | none | 0 | 0 |
| `quiz` | `quiz` | no_matches | 0 | none | none | 0 | 0 |
| `container` | `container` | no_matches | 0 | none | none | 0 | 0 |
| `database` | `database` | no_matches | 0 | none | none | 0 | 0 |

The `get_sheet` row demonstrates that one structural seed can expand to related functions in the same file, not that the engine searches all source occurrences.

## 7. Vocab source-presence classification

Read-only inspection of tracked `app.py` and `requirements.txt` established:

| Term | Actual presence | Classification |
|---|---|---|
| `gspread` | `import gspread`, `gspread.authorize`, and requirements declaration | import, identifier, and dependency |
| `worksheet` | no literal occurrence in inspected source/dependency files | absent as a literal |
| `session_state` | repeated `st.session_state` attribute access | attribute/member reference |
| `streamlit` | imports in `app.py` and requirements declaration | import and dependency |
| `practice` | UI string `"Ready to review? We'll pick 10 words you need to practice."` and Practice UI region | string/UI product term |
| `quiz` | no literal occurrence in inspected `app.py`/requirements files; behavior is presented as Practice/flashcards | absent as a literal, despite related behavior |
| `google sheets` | exact phrase absent; Google-related URLs and sheet operations exist separately | multiword phrase absent, component evidence exists |
| `container` | no container implementation; `use_container_width` contains the token as an unrelated API parameter | incidental substring only, not container infrastructure |
| `database` | no direct database implementation or dependency | absent as an implementation |

Additional direct source evidence includes `get_sheet`, `sheet1`, `get_all_records`, `col_values`, `find`, `append_row`, and `update_cell`, which establishes spreadsheet persistence without the exact phrase `google sheets`.

## 8. Discovery-layer diagnosis

### Layer 1 — Symbol discovery

Works for top-level structural names. The three exact-symbol controls matched and retained relationship context.

### Layer 2 — Source/import/attribute/string discovery

Currently missing from Context seed generation despite partial scanner support:

- import/module metadata is already persisted but unused by `_build_seeds`;
- attribute occurrences such as `st.session_state` are not indexed as searchable source evidence;
- strings such as the Practice UI text are not searched;
- dependency declarations are not queried by Context;
- raw source line/range evidence is not represented in Context artifacts.

### Layer 3 — Deterministic product-language bridging

Partially feasible and not equivalent to semantic inference. A query such as `google sheets` can be normalized into `google` and `sheets`, then deterministically matched against source/import/dependency evidence where those tokens occur. It may lead to `gspread`, Google Sheets URL scopes, `get_sheet`, and sheet operations only through explicit lexical and structural evidence.

The phrase itself is absent, so a deterministic bridge must distinguish “token evidence supports this area” from “the repository contains the exact product phrase.” No synonym dictionary or semantic claim is justified by this benchmark alone.

### Layer 4 — Broader semantic inference

A question such as “where does the application remember whether I knew a word?” requires interpretation across session state, score updates, flashcards, and persistence behavior. Literal source evidence can support candidate locations, but it cannot by itself establish the intended question semantics. This is a separate future advisory/query-planning concern.

M011 therefore does not assume that Layers 3 and 4 are the same problem.

## 9. Original intended scope

The original Repo Control architecture explicitly describes targeted context generation to help coding agents start from a topic while still verifying authoritative source. M003 explicitly defined Context as deterministic lexical navigation, not semantic search.

M002.1 later made ordinary product-language usability a primary integration question, explicitly asking whether a coder can begin from “Google Sheets,” “Practice quiz,” or “Streamlit” without already knowing `gspread`, `get_sheet`, `update_score`, or `get_synonyms_nltk`.

Therefore:

- Symbol discovery: explicitly intended.
- General source-text/import discovery: implicitly required by the broader navigation objective, but not implemented in M003.
- Deterministic product-language bridging: explicitly raised as a product usability requirement in M002.1, but its achievable boundary was not defined.
- Broader semantic inference: not part of the deterministic M003 authority and should be evaluated separately.

## 10. Source-text search options

### Query-time bounded source scan

Pros: smallest change, no new persistent schema, straightforward freshness, language-portable lexical fallback. Cons: repeated query cost and need for careful file filtering and source-line evidence.

### Precomputed source-text index

Pros: efficient repeated queries and richer indexed evidence. Cons: schema/version changes, larger artifacts, cache invalidation, secret-handling risk, and more implementation surface.

### Existing latent capability

The scanner already persists import/module/imported-symbol metadata. Querying that metadata is the cheapest first improvement and should precede raw scanning. It can explain `gspread` and `streamlit` without adding a second scanner.

Conclusion: use existing metadata first, then add a bounded source-text fallback only for evidence categories not already available.

## 11. Searchable source categories

Recommended initial categories:

- imports and imported module names;
- dependency declarations already parsed by the scanner;
- bounded identifier/attribute evidence where parser metadata can provide it;
- selected string literals or source-text hits with line numbers;
- tracked file paths and module names, which already work.

Defer or treat cautiously:

- comments, because they are useful but noisy;
- arbitrary configuration values, because they may contain secrets;
- unrestricted raw files, because source/config files can expose credentials;
- common terms such as `app`, `get`, `data`, `word`, and `state`.

Evidence should identify provenance and location without emitting secret values. Existing tracked-file and ignore/exclusion policies must remain authoritative.

## 12. Text-hit to symbol-expansion feasibility

A feasible future flow is:

```text
query
  -> import/dependency/source hit
  -> file + line/range + evidence kind
  -> nearest enclosing function/class when available
  -> explicit module-scope marker when not available
  -> one-hop relationship expansion
  -> related tests
  -> bounded Context pack
```

For `gspread`, an import hit in `app.py` can lead to the file and then to nearby structural functions such as `get_sheet` and `update_score`. For `session_state`, AST attribute or source hits can identify `app.py`, but many occurrences are module-level or spread across the UI body; an enclosing-symbol claim must not be fabricated. `Practice` is similarly likely to produce a string/UI hit with no single enclosing business function.

## 13. Multiword query behavior

The current tokenizer produces `google` and `sheets` for `google sheets`, but current seed matching only evaluates metadata fields and does not search the source evidence where those tokens occur.

Recommended future deterministic behavior:

- preserve exact phrase matching when present;
- tokenize and require token-AND evidence for high-confidence multiword matches;
- allow token-OR only as lower-ranked evidence when explicitly represented as separate hits;
- retain token provenance and locations;
- do not add arbitrary synonym expansion or semantic equivalence;
- preserve `no_matches` when no supported evidence exists.

This can bridge `google sheets` toward Google URLs, sheet operations, `gspread`, and `get_sheet` only as an evidence chain, not as an invented semantic label.

## 14. Product-language/query-planning boundary

M011 evidence supports a layered boundary rather than a forced choice:

- Repo Control should deterministically bridge product terminology as far as normalized tokens and repository evidence support.
- Repo Control should expose provenance: import, dependency, attribute, string, path, symbol, or relationship.
- A coder, Architect, or AI may propose additional candidate terms or interpret a broader requirement.
- Repo Control remains authoritative for whether the proposed terms and resulting code locations actually exist.
- Semantic inference should remain separate and advisory until a later milestone establishes an authority and evaluation model.

This is an evidence-based boundary: Layer 3 has a useful deterministic subset; Layer 4 exceeds lexical evidence in some questions.

## 15. Coder burden analysis

Should be automated by Repo Control:

- finding literal imports and dependencies;
- finding source occurrences and line ranges;
- locating files and module paths;
- mapping hits to nearest structural symbols where unambiguous;
- expanding callers/callees/import relationships;
- locating statically related tests;
- preserving deterministic evidence and bounds.

Shared between Repo Control and coder/AI:

- proposing candidate terms for a broad requirement;
- choosing among multiple evidence regions;
- interpreting ambiguous module-scope UI code;
- deciding whether a lexical hit answers the product question.

Should remain coder/Architect reasoning:

- architectural conclusions;
- future design or migration decisions;
- semantic claims unsupported by repository evidence;
- deciding whether an absence is acceptable for the requested feature.

## 16. Proposed deterministic fallback pipeline

Recommended future order:

1. exact and normalized structural symbol lookup;
2. existing file/path/module lookup;
3. existing import/module/imported-symbol metadata lookup;
4. dependency declaration lookup where already available;
5. bounded source-text, attribute, and string-literal lookup;
6. map each hit to file, line/range, and optional enclosing symbol;
7. mark module-scope hits explicitly;
8. expand one hop using existing relationships;
9. add related tests;
10. apply deterministic ranking, deduplication, and existing result caps;
11. preserve no-match when no supported evidence exists.

The pipeline should retain current exact-symbol behavior and avoid rescanning through a separate scanner implementation.

## 17. Ranking and noise controls

Recommended precedence:

1. exact structural symbol;
2. exact import/dependency item;
3. exact source phrase;
4. exact source token in identifier/attribute;
5. multi-token source evidence with all tokens present;
6. file/module path evidence;
7. string-literal evidence;
8. comment evidence;
9. lower-confidence single-token evidence.

Every match should retain an inspectable evidence kind rather than only an opaque relevance score. Existing caps should remain the default bounds, with per-evidence-kind counts if needed.

## 18. False-positive findings

The `container` benchmark demonstrates why substring-only source search is unsafe: `use_container_width` is not a container implementation. Common words such as `app`, `get`, `data`, `word`, and `state` could flood results.

Recommended controls:

- exact-token boundaries for source identifiers;
- separate substring matching from identifier matching;
- minimum token length or lower ranking for common terms;
- per-file and global result caps;
- exact phrase and import evidence above comments/general strings;
- deterministic deduplication by file, evidence kind, and line/range;
- explicit negative-control tests.

## 19. Legitimate absence handling

`container` must not become evidence of containerization merely because `use_container_width` contains the substring. `database` must remain no implementation evidence when no database dependency, connection, schema, or persistence code is present.

The future artifact should distinguish:

- no lexical evidence;
- lexical evidence without structural confirmation;
- structural implementation evidence;
- advisory interpretation.

No result should claim an implementation that the repository does not establish.

## 20. Security findings

Source discovery must not expose secret contents merely because a query matches them.

Future implementation requirements:

- preserve tracked-file and ignore/exclusion policy;
- avoid indexing or printing `.env`, private keys, service-account JSON, credential stores, and equivalent secret-bearing files;
- emit safe path/evidence metadata rather than matched secret values;
- keep source snippets out of the initial artifact unless a separately reviewed redaction policy exists;
- cap line/range evidence and never return full credential-bearing lines;
- keep the target repository read-only.

The M011 reconnaissance did not open known secret files.

## 21. Parser/language implications

The first improvement should not become Vocab-specific. A reasonable generalized boundary is:

- language-agnostic lexical search over safe tracked source categories;
- language-specific structural expansion where a supported parser can identify enclosing symbols;
- explicit `module_scope` or `unmapped_source_hit` when no structural mapping exists.

Python can receive richer AST-based import/attribute/string metadata first because it is the current supported parser surface, but the artifact vocabulary should not hard-code `gspread`, Streamlit, or Google Sheets.

## 22. Existing test architecture

`tests/test_context.py` currently covers:

- command routing and repository selection;
- query normalization/tokenization;
- empty-query errors;
- exact/partial structural lexical behavior;
- deterministic output;
- no-match success;
- one-hop relationship boundaries;
- test-reference inclusion;
- selection limits and truncation;
- diagnostic filtering;
- target-repository immutability.

Missing future coverage includes:

- import-only match;
- dependency-only match;
- attribute-only match;
- string-literal match;
- multiword token evidence;
- source hit mapped to an enclosing function;
- source hit at module scope;
- ignored/secret-bearing file exclusion;
- noisy common-term bounds;
- exact symbol priority over source-text matches;
- evidence provenance and line/range determinism.

No tests were added during M011.

## 23. Frozen Vocab acceptance benchmark

Future implementation acceptance should require:

### Exact-symbol controls

- `get_sheet`: matched, `app.py` surfaced, structural relationships preserved.
- `update_score`: matched.
- `get_synonyms_nltk`: matched.

### Source/import/attribute controls

- `gspread`: `app.py` surfaced with import evidence and useful structural context where feasible.
- `streamlit`: `app.py` surfaced with import/dependency evidence.
- `session_state`: `app.py` surfaced with attribute/source evidence; no symbol named `session_state` required.

### Product-language controls

- `practice`: relevant UI/source evidence surfaced when the literal term exists.
- `google sheets`: materially better than current `no_matches` when deterministic token/source evidence supports it; no invented semantic facts.

### Legitimate absence controls

- `container`: no false container implementation claim.
- `database`: no false database implementation claim.

## 24. Native Repo Control fixture recommendations

M012 should add small synthetic repositories covering:

- import-only match;
- attribute-only match;
- string-literal match;
- multiword query;
- source hit with unambiguous enclosing function;
- source hit at module scope;
- ignored secret file;
- noisy common term;
- exact symbol priority over text match;
- parse failure and unsupported-language behavior.

These fixtures should be independent of Vocab and should assert artifact provenance, ordering, caps, and no leakage.

## 25. Performance implications

A query-time bounded scan is the smallest first step:

- avoids persistent schema changes;
- naturally reflects fresh scan state;
- is acceptable for small repositories such as Vocab;
- can become expensive for large repositories or repeated queries.

Use tracked-file filtering, size/line caps, deterministic ordering, and result caps. Do not prematurely build a full text index. Repeated-query performance can be measured in M012 after the evidence contract is stable.

## 26. Artifact/schema implications

Existing `context.json` schema version 1 can likely remain compatible if source evidence is additive, for example through additive seed/evidence fields and selection metadata.

Potential future fields:

- evidence kind;
- matched token(s);
- source line/range;
- enclosing symbol or explicit module-scope marker;
- source evidence provenance.

No schema was changed in M011. Any M012 schema extension must preserve existing fields and deterministic artifact identity behavior, or explicitly version the contract.

## 27. CLI/UI implications

The first implementation can remain largely in Context core logic. CLI and browser output should expose evidence provenance clearly enough to distinguish:

- symbol match;
- import/dependency match;
- attribute match;
- source-text/string match;
- structural expansion;
- advisory AI interpretation, if introduced later.

No CLI or UI change was made in M011.

## 28. Utilization implications

The minimum future workflow rule should be:

- coder invokes Repo Control Context before substantive implementation;
- Repo Control provides deterministic evidence where possible;
- direct source inspection remains allowed and authoritative;
- Context failure or no-match remains visible rather than being silently bypassed;
- guarded Git mutation remains separate from discovery.

No utilization tracking or milestone-session tracking should be added in M012 unless separately authorized.

## 29. Recommended implementation classification

**B — Small deterministic source-text fallback required.**

The first implementation should begin with the existing scanner metadata gap: make persisted import/module/imported-symbol and dependency facts available as Context seed candidates. Then add only the smallest bounded source-text/attribute/string evidence needed for cases not covered by existing metadata.

This is not classification A alone because `session_state` and `practice` require evidence categories not currently exposed as seed metadata. It is not C because the scanner and artifact model already provide a usable foundation. It is not D because useful product-language bridging is possible through deterministic token evidence without semantic inference.

## 30. Exact M012 recommendation

**M012 — Deterministic Source-Text Context Fallback and Structural Expansion**

Initial scope:

1. query existing scanner import/module/imported-symbol/dependency metadata;
2. add bounded safe source evidence for attributes, identifiers, and selected string literals;
3. map evidence to file, line/range, and optional enclosing symbol;
4. preserve module-scope hits explicitly;
5. integrate one-hop relationship and test expansion;
6. preserve exact-symbol priority and existing bounds;
7. add native fixtures and the frozen Vocab benchmark;
8. preserve no-match and legitimate-absence behavior;
9. expose evidence provenance without source-secret leakage.

## 31. Explicit non-goals

M011 and the recommended M012 should not:

- modify the Vocab application or Git state;
- implement semantic embeddings or LLM retrieval;
- add arbitrary synonym dictionaries;
- claim architectural meaning from lexical matches;
- execute target code;
- add automatic Git mutation;
- add selective staging or commit behavior;
- access Photo Organizer;
- expose secret contents;
- redesign unrelated scanner, snapshot, comparison, or workflow authorities.

## 32. Limitations / unresolved questions

- The benchmark confirms source presence but does not establish the best universal treatment of comments, configuration keys, or all languages.
- The canonical Vocab repository was not globally clean because M002.1 documentation work was still open. Direct `git status --short` evidence showed:

  ```text
   M milestones/002.1_repo_control_integration_baseline_and_m002_evidence_comparison_prompt.md
  ?? milestones/002.1_repo_control_integration_baseline_and_m002_evidence_comparison_closeout.md
  ```

  No Vocab application source files were listed as modified or untracked. The benchmark was run against the canonical committed/source implementation without mutating Vocab.
- A source hit near module-level Streamlit UI code may not have a meaningful enclosing symbol.
- The precise safe-file policy for future source-text indexing requires implementation-level review.
- The performance crossover between query-time scanning and a persistent text index was not measured in M011.
- Semantic interpretation of broad product questions remains unresolved by deterministic lexical evidence alone.

## 33. Final Repo Control state

The final M011 Repo Control state was captured after reconnaissance. No source implementation changes were made.

- branch: `main`
- HEAD: `859f9a651aee429fe20d55b8e5d236673480e7ff`
- upstream: `859f9a651aee429fe20d55b8e5d236673480e7ff` (`origin/main`)
- ahead/behind for `HEAD...@{upstream}`: `0 0`

Literal final `git status --short`:

```text
 M docs/008_guarded_staging_preparation_prompt.md
 M docs/009_browser_ui_foundation_and_read_only_console_prompt.md
?? .venv/
?? docs/011_context_source_text_and_product_language_discovery_reconnaissance_closeout.md
?? docs/011_context_source_text_and_product_language_discovery_reconnaissance_prompt.md
```

The known documentation changes, `.venv/`, the M011 prompt, and this required closeout are uncommitted. No staging, cleanup, restore, reset, commit, push, or target-repository mutation was performed.
