# Repo Control Milestone 012

# Deterministic Source-Text Context Fallback and Structural Expansion

**Prompt file:** `docs/012_deterministic_source_text_context_fallback_and_structural_expansion_prompt.md`  
**Required closeout:** `docs/012_deterministic_source_text_context_fallback_and_structural_expansion_closeout.md`  
**Mode:** Implementation  
**Reasoning:** High  
**Repo Control implementation authority:** Yes, within the locked scope below  
**Vocab implementation authority:** None  
**Runtime mutation authority:** None  
**Database mutation authority:** None  
**Semantic/AI retrieval authority:** None

---

# 1. Objective

Implement the smallest generalized deterministic enhancement to Repo Control Context that closes the discovery gap established by M011.

M011 established that current Context:

- successfully discovers known structural symbols such as:
  - `get_sheet`;
  - `update_score`;
  - `get_synonyms_nltk`;
- already receives scanner metadata containing imports/imported modules/imported symbols;
- does not currently use that import metadata as Context seed evidence;
- does not search general source evidence such as:
  - attributes;
  - selected identifiers;
  - string literals;
  - module-scope source occurrences;
- therefore performs poorly when a coder begins with terms such as:
  - `gspread`;
  - `streamlit`;
  - `session_state`;
  - `practice`;
  - `google sheets`.

M012 must improve deterministic discovery without converting Context into a semantic search engine.

The intended progression is:

`query`

→ `existing structural symbol/path discovery`

→ `existing import/dependency metadata discovery`

→ `bounded safe source evidence where required`

→ `file/location evidence`

→ `optional enclosing structural symbol or explicit module-scope evidence`

→ `existing one-hop relationships`

→ `related tests`

→ `bounded deterministic Context artifact`.

The primary product objective is:

> A coder should be able to begin with ordinary repository/product terminology and receive materially useful deterministic evidence before already knowing the exact implementation function names.

---

# 2. Controlling Evidence

Read before implementation:

1. existing Repo Control project-control/workflow documents applicable to M012;
2. `docs/011_context_source_text_and_product_language_discovery_reconnaissance_prompt.md`;
3. `docs/011_context_source_text_and_product_language_discovery_reconnaissance_closeout.md`;
4. this M012 prompt.

Treat M011 as the controlling reconnaissance for this implementation.

Do not broaden M012 beyond the smallest implementation justified there.

---

# 3. Canonical Repositories

## Repo Control

Canonical implementation repository:

`/home/chuck/projects/repo-control`

Canonical branch:

`main`

## Vocab acceptance testbed

Canonical read-only testbed:

`/home/chuck/projects/vocab-app`

The historical frozen Vocab testbed:

`/home/chuck/ai-agent-tests/vocab-app`

is not the M012 acceptance target.

Do not modify either Vocab repository.

Do not access Photo Organizer.

---

# 4. Prompt Lifecycle Gate

The M012 prompt must be committed before substantive implementation begins.

At milestone start, verify that this prompt is already present in Repo Control history.

If the prompt is untracked or merely present as a working-tree file:

STOP and report.

Do not repeat the M011 prompt-start process deviation.

---

# 5. Starting-State Gate

Before implementation, capture:

    cd /home/chuck/projects/repo-control
    
    pwd
    git branch --show-current
    git rev-parse HEAD
    git status --short
    git remote -v
    git rev-parse @{upstream} 2>/dev/null || true
    git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null || true
    git log -8 --oneline --decorate

Known historical local state may include:

- modified `docs/008_guarded_staging_preparation_prompt.md`;
- modified `docs/009_browser_ui_foundation_and_read_only_console_prompt.md`;
- untracked `.venv/`.

Observe current reality rather than assuming those items still exist.

If they remain:

- classify them as pre-existing;
- do not modify them;
- do not stage them;
- do not clean them.

STOP if:

- unexpected Repo Control source-code modifications exist;
- the M012 prompt is not committed;
- evidence attribution is ambiguous;
- Vocab application source is unexpectedly dirty in a way that compromises acceptance testing.

---

# 6. Locked Implementation Scope

M012 is authorized to change only the Context/scanner/test surfaces necessary to implement:

1. discovery from already-persisted import/module/imported-symbol metadata;
2. dependency evidence where current scanner architecture already supports or can safely expose it;
3. bounded safe source evidence for:
   - attributes;
   - identifiers where needed;
   - selected string literals;
4. deterministic evidence provenance;
5. file and line/range association;
6. optional enclosing function/class mapping where unambiguous;
7. explicit module-scope/unmapped-source representation where no enclosing structural symbol exists;
8. integration with existing one-hop relationship expansion;
9. related test discovery;
10. deterministic ranking, deduplication, and bounds;
11. tests required to prove the above;
12. CLI/browser presentation changes only where necessary to expose the new deterministic evidence clearly.

Do not refactor unrelated Repo Control architecture.

---

# 7. Explicit Non-Goals

Do not implement:

- embeddings;
- vector databases;
- semantic search;
- LLM retrieval;
- AI-generated repository facts;
- arbitrary synonym dictionaries;
- hard-coded Vocab terminology;
- hard-coded `gspread`, Streamlit, Google Sheets, or Vocab-specific rules;
- automatic query generation by AI;
- milestone-session utilization tracking;
- new Git mutation behavior;
- deployment/runtime features;
- target-code execution;
- source snippets containing arbitrary raw source lines unless specifically required and proven safe;
- broad comment search unless implementation evidence proves it is necessary;
- unrestricted configuration-value search;
- new persistent full-text indexing unless the bounded implementation proves query-time/current metadata insufficient.

M012 is a deterministic discovery improvement.

---

# 8. Preserve Existing Exact-Symbol Behavior

Existing structural discovery must remain authoritative and highest priority.

The following must not regress:

- exact function/class symbol lookup;
- path/module lookup;
- current query normalization;
- one-hop relationship expansion;
- related-test expansion;
- deterministic artifact generation;
- target repository immutability;
- selection caps;
- no-match behavior;
- diagnostic filtering;
- existing reason/status semantics.

Exact structural symbol results must outrank broader source evidence.

---

# 9. Existing Metadata First

Before introducing new source scanning, use the data the scanner already has.

M011 established that Python scan artifacts already persist:

- import records;
- imported module names;
- imported symbols.

Integrate these into Context discovery as deterministic evidence.

Examples:

`gspread`

should be discoverable because the repository contains import evidence.

`streamlit`

should be discoverable through import/dependency evidence where present.

Do not implement a second independent import parser.

Reuse authoritative existing scanner output.

---

# 10. Dependency Evidence

Determine the smallest safe way to expose dependency declarations as Context evidence.

Examples include package declarations in supported dependency manifests.

Requirements:

- deterministic;
- bounded;
- safe;
- no target mutation;
- evidence provenance visible;
- no secret-bearing arbitrary configuration parsing.

Dependency evidence should be distinguishable from structural implementation evidence.

Example:

`streamlit`

may produce:

- import evidence;
- dependency evidence;

without claiming that every dependency occurrence represents a particular architecture.

---

# 11. Source Evidence Fallback

When structural/import/dependency discovery does not provide sufficient seeds, add the smallest bounded safe source fallback justified by M011.

Initial source evidence categories should support cases such as:

- `st.session_state`;
- relevant identifier/attribute names;
- selected UI/product string literals such as `Practice`.

Prefer parser-aware evidence where available.

A generalized lexical source scan may be used where parser metadata does not already provide the evidence.

Do not search unrestricted arbitrary repository contents.

---

# 12. Safe File Boundary

Source-text discovery must operate only over files that are safe and appropriate for Context.

Preserve existing authoritative:

- tracked-file boundaries;
- ignore/exclusion rules;
- target-repository read-only guarantees.

Do not emit contents from:

- `.env`;
- private keys;
- service-account JSON;
- credential stores;
- secret-bearing runtime configuration;
- ignored files;
- equivalent sensitive artifacts.

Where a sensitive file can safely be identified by path without reading its content, do not turn that into permission to index or display secret values.

Add regression coverage for secret exclusion.

---

# 13. Evidence Provenance

Every new discovery path must make its provenance inspectable.

Recommended evidence kinds include, as appropriate:

- `symbol`;
- `path`;
- `module`;
- `import`;
- `dependency`;
- `attribute`;
- `identifier`;
- `string_literal`;
- `source_text`;
- `relationship`;
- `test_reference`.

Use the smallest schema change necessary.

Do not collapse all evidence into an opaque relevance score.

The user/coder should be able to tell why a result appeared.

---

# 14. Source Location Evidence

Where a source-derived hit exists, preserve deterministic location information sufficient to identify it.

Prefer:

- file path;
- line number or bounded line range;
- evidence type;
- matched token(s).

Do not automatically emit unrestricted source snippets.

If source excerpts are unnecessary to satisfy Context usability, keep them out of M012.

---

# 15. Enclosing Structural Symbol

Where a source hit occurs inside a parsed function/class:

- map the hit to the enclosing structural symbol;
- make that mapping explicit;
- allow existing structural relationship expansion from that symbol.

Example:

source/import evidence in a function

→ enclosing function

→ callers/callees/related tests.

Do not fabricate an enclosing symbol when none exists.

---

# 16. Module-Scope Evidence

Module-level applications such as the current Vocab Streamlit UI contain meaningful source evidence outside functions/classes.

Represent that honestly.

Use a clear deterministic state such as:

- `module_scope`;
- `unmapped_source_hit`;

or another generalized equivalent consistent with current artifact design.

Do not invent a synthetic function merely to fit existing symbol structures.

Module-scope evidence should still be able to select the relevant file.

---

# 17. Deterministic Product-Language Bridging

M012 must preserve the M011 distinction between deterministic product-language bridging and semantic reasoning.

For a query such as:

`google sheets`

Repo Control may:

1. normalize/tokenize the query;
2. search supported deterministic evidence categories;
3. identify evidence for `google`, `sheets`, `sheet`, or exact repository tokens where supported by the current tokenizer/rules;
4. combine evidence deterministically;
5. surface related files/symbols only through explicit repository evidence.

Repo Control must not claim:

`this is the Google Sheets persistence layer`

unless that conclusion is directly encoded in repository evidence.

The coder/Architect performs architectural interpretation.

---

# 18. Multiword Query Rules

Implement deterministic multiword handling consistent with M011.

Preferred behavior:

1. exact phrase evidence where present;
2. exact structural/import/dependency evidence;
3. token-AND evidence ranked above token-OR;
4. token-OR only when represented explicitly as separate lower-confidence evidence;
5. provenance retained for every token/hit;
6. no arbitrary semantic synonym expansion.

Preserve meaningful `no_matches`.

Do not force a result merely because some query token occurs somewhere.

---

# 19. Ranking

Preserve exact structural evidence priority.

Use an inspectable deterministic precedence based on M011 findings, such as:

1. exact structural symbol;
2. exact import/dependency;
3. exact source phrase;
4. exact identifier/attribute token;
5. multi-token source evidence with all meaningful tokens;
6. path/module evidence where applicable;
7. selected string-literal evidence;
8. lower-confidence single-token evidence.

Adjust ordering only if existing contracts/tests require a different safe arrangement.

Document any deviation in the closeout.

Do not introduce opaque model-derived relevance.

---

# 20. Noise Controls

Broader discovery must remain bounded.

Protect against terms such as:

- `app`;
- `get`;
- `data`;
- `word`;
- `state`.

Implement deterministic controls such as:

- token boundaries;
- per-file caps;
- global result caps;
- evidence-kind ranking;
- deterministic deduplication;
- minimum token rules where appropriate;
- truncation diagnostics.

Do not optimize only for Vocab positive cases.

A query that matches hundreds of irrelevant locations is not a successful implementation.

---

# 21. Negative-Control Behavior

The Vocab benchmark includes important negative controls.

## `container`

The source contains incidental text such as `use_container_width`.

Repo Control must not report this as evidence that the repository implements container infrastructure.

Literal lexical evidence may be reported only with honest provenance if the query policy allows it, but it must not become false structural meaning.

## `database`

Current canonical Vocab contains no database implementation.

Do not fabricate database implementation evidence.

The resulting Context must distinguish where appropriate:

- no relevant lexical evidence;
- incidental lexical evidence;
- structural implementation evidence.

---

# 22. Native Test Fixtures First

Before relying on Vocab acceptance, add generalized Repo Control-native tests/fixtures for the new behavior.

At minimum cover:

1. import-only match;
2. dependency-only match where supported;
3. attribute-only match;
4. string-literal match;
5. multiword query;
6. source hit inside an enclosing function;
7. source hit at module scope;
8. ignored/secret-bearing file exclusion;
9. noisy common-term bounds;
10. exact symbol priority over broader source evidence;
11. deterministic ordering;
12. evidence provenance;
13. line/range determinism;
14. no target mutation;
15. legitimate no-match;
16. incidental-substring negative control.

Do not make Vocab the only test fixture.

---

# 23. Characterization of Existing Tests

Before changing behavior, run the existing relevant Context tests.

Record the baseline.

At minimum inspect/run the existing `tests/test_context.py` coverage and any directly related scanner/artifact tests.

If existing tests fail before implementation:

STOP and report.

Do not normalize pre-existing failures into M012.

---

# 24. Implementation Sequence

Use this order unless source evidence proves a different smaller safe sequence is required:

## Step 1 — Characterize

- run existing Context tests;
- verify current Vocab benchmark behavior read-only.

## Step 2 — Existing metadata integration

- import/module/imported-symbol evidence;
- dependency evidence where already available.

## Step 3 — Native tests

Add generalized fixture coverage for new evidence categories.

## Step 4 — Bounded source fallback

Add only the source evidence required for:

- attributes;
- identifiers as needed;
- selected string literals;
- module-scope cases.

## Step 5 — Structural expansion

Map hits to enclosing symbols where unambiguous and reuse existing one-hop relationships/tests.

## Step 6 — Noise/security hardening

Verify caps, exclusions, deterministic ordering, and negative controls.

## Step 7 — Full focused regression

Run all Context/scanner/artifact tests relevant to the implementation.

## Step 8 — Frozen Vocab acceptance benchmark

Run the canonical read-only Vocab benchmark.

Do not modify Vocab.

---

# 25. Frozen Vocab Benchmark

Acceptance repository:

`/home/chuck/projects/vocab-app`

Capture its HEAD before the benchmark.

Do not require Vocab to be globally clean if the only changes are known M002.1 documentation artifacts, but verify:

- no application source files are modified;
- benchmark code comes from the canonical committed application source;
- M012 does not mutate the Vocab repository.

---

# 26. Required Vocab Exact-Symbol Controls

The following must continue to work:

## `get_sheet`

Expected:

- matched;
- `app.py` surfaced;
- structural symbol evidence preserved;
- relationship context preserved.

## `update_score`

Expected:

- matched;
- `app.py` surfaced.

## `get_synonyms_nltk`

Expected:

- matched;
- `app.py` surfaced.

Any regression is a STOP condition.

---

# 27. Required Vocab Source/Import Controls

## `gspread`

Must materially improve from `no_matches`.

Expected minimum:

- `app.py` surfaced;
- deterministic import/source evidence shown;
- provenance identifies why it matched;
- useful structural context added where feasible.

## `streamlit`

Must materially improve from `no_matches`.

Expected minimum:

- `app.py` surfaced;
- import and/or dependency evidence;
- provenance visible.

## `session_state`

Must materially improve from `no_matches`.

Expected minimum:

- `app.py` surfaced;
- attribute/source evidence;
- no requirement for a structural symbol literally named `session_state`;
- module-scope evidence handled honestly where appropriate.

---

# 28. Required Vocab Product-Language Controls

## `practice`

Expected minimum:

- relevant Vocab source/UI evidence surfaced where the literal term exists;
- `app.py` selected;
- evidence provenance visible;
- no fabricated architectural interpretation.

## `google sheets`

Expected:

- materially more useful than the current `no_matches` if deterministic token/import/dependency/source evidence supports it;
- an inspectable evidence chain toward the relevant file/implementation surface;
- no claim of semantic understanding unsupported by repository facts.

This benchmark is intentionally important.

The objective is not merely that exact implementation symbols work.

---

# 29. Required Vocab Legitimate-Absence Controls

## `container`

Must not falsely claim container infrastructure based on incidental `use_container_width`.

## `database`

Must not invent database implementation.

Record the exact result and why it is acceptable.

---

# 30. `worksheet` and `quiz` Controls

M011 established that:

- `worksheet` is not a literal source/dependency term in the inspected canonical Vocab implementation;
- `quiz` is not a literal implementation term in the current `app.py`.

Therefore M012 is not required to magically resolve these through semantic inference.

Record their results as semantic/product-language boundary evidence.

Do not hard-code aliases to make them pass.

---

# 31. Artifact Compatibility

Preserve the current Context artifact contract where possible.

Prefer additive fields.

If schema version 1 can safely represent the added deterministic evidence:

- retain compatibility.

If a schema version change is actually required:

STOP before performing the schema change and explain:

- why additive compatibility is insufficient;
- affected consumers;
- migration implications;
- alternative designs considered.

Do not casually version the artifact.

---

# 32. Deterministic Artifact Identity

Any new evidence fields must preserve deterministic artifact generation.

Repeated identical query + repository state must produce the same logical Context result and stable deterministic identity under the existing contract.

Add tests if required.

---

# 33. CLI and Browser Consistency

The CLI and browser must continue to use the same underlying Context discovery service.

Do not create a separate browser-only search algorithm.

If evidence provenance needs presentation changes:

- make the smallest shared/core addition;
- expose it consistently enough that CLI/browser consumers can interpret the evidence.

Do not redesign the browser.

---

# 34. Performance

M011 recommended a bounded query-time approach before building a persistent text index.

Measure enough to ensure the implementation is reasonable.

At minimum:

- record focused test runtime;
- record Vocab benchmark practicality;
- note any obvious repeated full-repository scan concerns.

Do not prematurely build a persistent full-text index.

If bounded query-time search is unexpectedly impractical even on the current test surfaces:

STOP and report before redesigning.

---

# 35. Security Validation

Explicitly test that the new discovery mechanism does not return secret content.

Use synthetic native fixtures.

Do not create real credentials for tests.

Verify that:

- ignored secret files remain excluded;
- secret values are not emitted;
- source evidence is bounded;
- target repositories remain unchanged.

Security regression is a STOP condition.

---

# 36. Coder Workflow Objective

M012 should reduce mechanical discovery work.

After implementation, a coder should not need to independently discover exact function names before Context becomes useful for straightforward lexical/product terminology that actually has repository evidence.

The intended working boundary is:

`coder receives requirement`

→ `coder invokes Context using natural/repository terminology`

→ `Repo Control deterministically surfaces useful evidence`

→ `coder reads/reasons further as needed`.

Do not require additional query-planning ceremony merely to compensate for Context deficiencies.

Direct source reading remains allowed and authoritative.

---

# 37. Product-Language Boundary

M012 is successful even though some semantic questions remain outside deterministic Context.

Example:

`where does the application remember whether I knew a word?`

may still require coder/AI interpretation.

Do not solve that problem here.

M012 should establish a stronger deterministic foundation so an advisory query-planning/semantic layer can be considered later only if real Vocab work continues to expose that need.

---

# 38. Required Test Evidence

At closeout, report:

- pre-change relevant test baseline;
- new tests added;
- focused Context test result;
- scanner/artifact test result where relevant;
- full Repo Control test result if practical and appropriate;
- Vocab benchmark result;
- target repository immutability verification.

Do not claim success from Vocab examples alone.

---

# 39. Acceptance Criteria

M012 passes only if all of the following are true:

1. Existing exact-symbol behavior does not regress.
2. `gspread` produces useful deterministic evidence.
3. `streamlit` produces useful deterministic evidence.
4. `session_state` produces useful deterministic evidence.
5. `practice` produces useful deterministic evidence where literal evidence exists.
6. `google sheets` produces materially improved deterministic evidence where repository tokens support it.
7. `container` does not falsely imply container infrastructure.
8. `database` does not falsely imply database implementation.
9. Source evidence provenance is inspectable.
10. Module-scope evidence is represented honestly.
11. Existing relationship expansion remains bounded.
12. Result caps and deterministic ordering remain intact.
13. Secret-bearing files/values are not exposed.
14. Target repositories remain read-only.
15. Native generalized tests prevent Vocab-specific overfitting.
16. CLI/browser continue to use the shared Context core.
17. No semantic/AI retrieval is introduced.
18. No unrelated Repo Control subsystem is redesigned.

---

# 40. Stop Conditions

STOP and report before continuing if:

- existing focused tests fail before implementation;
- exact-symbol behavior regresses;
- the proposed solution requires a broad scanner rewrite;
- a persistent full-text index becomes necessary to satisfy the locked scope;
- artifact compatibility cannot be preserved additively;
- source search risks exposing real secrets;
- the implementation requires hard-coded Vocab terminology;
- target repository mutation occurs;
- Vocab application source becomes modified;
- unrelated Repo Control source changes appear;
- deterministic product-language bridging appears impossible without semantic inference;
- result noise cannot be bounded safely;
- CLI/browser would require divergent discovery implementations.

Do not silently broaden the milestone.

---

# 41. Required Closeout

Create exactly:

`docs/012_deterministic_source_text_context_fallback_and_structural_expansion_closeout.md`

The closeout must include:

## 1. Executive result

PASS / PASS WITH FOLLOW-UP / STOP.

## 2. Starting Repo Control state

Branch, HEAD, upstream, ahead/behind, exact working-tree state.

## 3. Prompt lifecycle verification

Confirm M012 prompt was committed before implementation.

## 4. Pre-change test baseline

Relevant tests and results.

## 5. Implementation summary

Exact files/components changed and purpose.

## 6. Existing metadata integration

Imports/modules/imported symbols/dependencies.

## 7. Source evidence implementation

Attributes/identifiers/strings and safe bounds.

## 8. Evidence provenance

Kinds and artifact representation.

## 9. Enclosing-symbol/module-scope behavior

How source hits map structurally.

## 10. Ranking and deduplication

Final deterministic precedence.

## 11. Noise controls

Caps, token boundaries, common terms.

## 12. Security protections

Ignored files, secrets, safe evidence.

## 13. Native fixture coverage

New generalized tests.

## 14. Existing regression evidence

Exact-symbol and existing Context behavior.

## 15. Vocab benchmark — exact symbols

`get_sheet`, `update_score`, `get_synonyms_nltk`.

## 16. Vocab benchmark — source/import

`gspread`, `streamlit`, `session_state`.

## 17. Vocab benchmark — product language

`practice`, `google sheets`.

## 18. Vocab benchmark — semantic boundary

`worksheet`, `quiz`.

## 19. Vocab benchmark — negative controls

`container`, `database`.

## 20. Before/after benchmark comparison

M011 vs M012.

## 21. CLI/browser compatibility

Shared discovery path.

## 22. Artifact compatibility

Schema and deterministic identity.

## 23. Performance findings

Bounded evidence.

## 24. Target repository immutability

Direct proof Vocab was not modified.

## 25. Coder burden/result assessment

Did Context now materially reduce the need to know exact symbols?

## 26. Remaining product-language gap

What remains deterministic vs semantic.

## 27. Scope deviations

Any authorized or unavoidable deviations.

## 28. Test summary

Focused and broader regression counts.

## 29. Recommended next Repo Control step

Do not invent another Repo Control milestone unless actual evidence requires it.

## 30. Vocab readiness recommendation

State whether the improved Context is ready to be exercised in the next real Vocab implementation milestone.

## 31. Final Repo Control state

Capture:

    cd /home/chuck/projects/repo-control
    
    git branch --show-current
    git rev-parse HEAD
    git status --short
    git rev-parse @{upstream} 2>/dev/null || true
    git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null || true
    git log -5 --oneline --decorate

Do not stage or commit the closeout unless separately authorized by the Product Owner.

---

# 42. Expected Outcome

A successful M012 should demonstrate a real improvement in the Vocab testbed:

Before:

`google sheets`
→ no useful Context result

After:

`google sheets`
→ deterministic repository evidence
→ relevant source/import/dependency evidence
→ relevant file
→ structural context where supported
→ coder can continue reasoning.

Likewise:

`gspread`
→ useful import evidence

`streamlit`
→ useful import/dependency evidence

`session_state`
→ useful attribute/source evidence

`practice`
→ useful UI/string/source evidence.

At the same time:

`container`
must not become a false container implementation result;

and:

`database`
must not become a fabricated database result.

The implementation should improve discovery without weakening deterministic authority.

---

# 43. Working Principle

> Expand what Repo Control can deterministically discover; do not expand what it claims to understand.

Use existing scanner facts first, add only bounded source evidence that is genuinely missing, preserve exact-symbol priority, and immediately validate the improvement against both generalized native fixtures and the real Vocab application.

---

**End of `012_deterministic_source_text_context_fallback_and_structural_expansion_prompt.md`**
