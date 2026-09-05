# Repo Control Milestone 011

# Context Source-Text and Product-Language Discovery Reconnaissance

**Prompt file:** `docs/011_context_source_text_and_product_language_discovery_reconnaissance_prompt.md`  
**Required closeout:** `docs/011_context_source_text_and_product_language_discovery_reconnaissance_closeout.md`  
**Mode:** Reconnaissance only  
**Reasoning:** High  
**Repo Control implementation authority:** None  
**Vocab implementation authority:** None  
**Git mutation authority:** None except creation of the required M011 closeout  
**Runtime mutation authority:** None

---

# 1. Objective

Perform a focused reconnaissance of Repo Control's current Context discovery pipeline and determine why it successfully discovers known implementation symbols but fails to discover relevant code through ordinary source terms and product-language concepts.

This milestone is driven by evidence from the real canonical Vocab App repository:

`/home/chuck/projects/vocab-app`

During Vocab M002.1, Repo Control Context produced the following representative behavior:

Successful implementation-symbol discovery:

- `get_sheet` -> matched and surfaced `app.py`;
- `update_score` -> matched and surfaced `app.py`;
- `get_synonyms_nltk` -> matched and surfaced `app.py`.

Unsuccessful broader discovery:

- `google sheets` -> no matches;
- `gspread` -> no matches;
- `worksheet` -> no matches;
- `practice` -> no matches;
- `quiz` -> no matches;
- `streamlit` -> no matches;
- `session_state` -> no matches.

Expected absence:

- `container` -> no matches where no current container implementation exists;
- `database` -> no direct database implementation exists in canonical Vocab.

The evidence suggests that current Context discovery is substantially symbol-oriented and does not yet provide the source-text/product-language-to-symbol bridge required by the intended workflow.

M011 must determine the exact reason, the actual current design, and the smallest generalized improvement.

Do not implement that improvement in M011.

---

# 2. Product Intent

Repo Control is intended to reduce mechanical repository reconnaissance while preserving deterministic evidence.

A coder should not need to fully discover implementation names independently before Repo Control becomes useful.

The desired conceptual workflow is:

`product requirement`

→ `Repo Control deterministic discovery`

→ `relevant source locations`

→ `enclosing symbols`

→ `structural relationships`

→ `bounded Context evidence`

→ `coder/Architect reasoning`.

Example:

`Google Sheets persistence`

should ideally help lead toward evidence such as:

- `import gspread`;
- `get_sheet`;
- sheet reads;
- sheet writes;
- `update_score`;
- related functions;
- tests if present.

Repo Control does not need to infer the entire persistence architecture.

It does need to provide useful deterministic evidence from which a coder can reason.

Do not reduce the goal to exact-symbol lookup merely because exact-symbol lookup currently works.

---

# 3. Authority Boundary

This is a Repo Control milestone.

Canonical Repo Control repository:

`/home/chuck/projects/repo-control`

The Vocab repository is a read-only external testbed for this milestone.

Do not modify:

`/home/chuck/projects/vocab-app`

Do not modify Vocab Git state.

Do not modify Vocab application files.

Do not use the Photo Organizer repository, runtime, database, containers, configuration, storage, or source code.

Do not implement any Repo Control change during M011.

The only authored Repo Control output is:

`docs/011_context_source_text_and_product_language_discovery_reconnaissance_closeout.md`

---

# 4. Starting-State Gate

Capture the Repo Control state first:

    cd /home/chuck/projects/repo-control
    
    pwd
    git branch --show-current
    git rev-parse HEAD
    git status --short
    git remote -v
    git rev-parse @{upstream} 2>/dev/null || true
    git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null || true
    git log -8 --oneline --decorate

Known prior evidence from Vocab M002.1 showed:

- modified `docs/008_guarded_staging_preparation_prompt.md`;
- modified `docs/009_browser_ui_foundation_and_read_only_console_prompt.md`;
- untracked `.venv/`.

Do not assume that state is still present.

Observe the current state.

If unexpected source-code changes exist, stop and report.

If only the known documentation changes and repo-local `.venv/` remain, classify them explicitly before continuing read-only reconnaissance.

Do not clean, restore, stage, commit, or delete them during M011.

A dirty Repo Control working tree must be clearly distinguished from upstream parity.

---

# 5. Establish Current Context Architecture

Map the current implementation of Repo Control Context.

Determine:

- entry points;
- commands/API/UI routes that invoke Context;
- query normalization;
- query parsing;
- repository scanning/indexing;
- language/parser support;
- symbol extraction;
- seed generation;
- file selection;
- symbol selection;
- relationship expansion;
- test discovery;
- result ranking;
- evidence caps/bounds;
- caching;
- persistence of Context artifacts;
- reason/status handling.

Produce a concise execution flow from:

`user query`

through:

`Context result`.

Do not infer behavior from naming alone.

Trace the actual runtime path.

---

# 6. Define "Symbol" in the Current Implementation

Determine exactly what Repo Control currently indexes or recognizes as a symbol.

Examples to investigate include:

- functions;
- classes;
- methods;
- module-level assignments;
- imported names;
- attributes;
- variables;
- constants;
- file/module names;
- test names.

Do not assume these are all supported.

Document what the implementation actually treats as searchable structural symbols.

Determine whether:

`get_sheet`

works because it is a parsed function definition.

Determine why:

`gspread`

does not work despite appearing in source as an import.

Determine why:

`session_state`

does not work despite appearing repeatedly as an attribute reference.

---

# 7. Current Query-Matching Semantics

Determine how a Context query becomes candidate seeds.

Inspect behavior involving:

- exact match;
- partial match;
- substring match;
- token match;
- case normalization;
- underscore normalization;
- whitespace normalization;
- multiword queries;
- symbol-name matching;
- file-name matching;
- test-name matching.

Determine whether the current engine searches:

- parsed symbol names only;
- symbol metadata;
- file paths;
- source text;
- imports;
- string literals;
- comments;
- dependency manifests;
- attribute names.

Document each as:

- supported;
- unsupported;
- partial;
- unknown.

---

# 8. Reproduce the Vocab Benchmark

Against the canonical read-only Vocab repository, reproduce the bounded benchmark from M002.1 using the current Repo Control implementation.

Queries:

- `get_sheet`
- `update_score`
- `get_synonyms_nltk`
- `gspread`
- `worksheet`
- `session_state`
- `streamlit`
- `google sheets`
- `practice`
- `quiz`
- `container`
- `database`

Record for each:

- query;
- normalized/canonical query if exposed;
- match status;
- seed count;
- selected files;
- selected symbols;
- relationships;
- diagnostics;
- Context ID if applicable.

Do not modify Vocab.

The purpose is to confirm the behavior from the actual Repo Control implementation before designing changes.

---

# 9. Inspect the Relevant Vocab Source Directly

Read only the minimum canonical Vocab source necessary to establish why expected queries should or should not match.

For each benchmark term, classify its actual source presence.

Examples:

## `gspread`

Determine whether it appears as:

- import;
- identifier;
- attribute;
- string;
- comment;
- other.

## `session_state`

Determine whether it appears as:

- attribute access;
- identifier;
- string;
- other.

## `streamlit`

Determine whether it appears as:

- import;
- dependency;
- source text;
- other.

## `practice`

Determine whether it appears as:

- UI string;
- identifier;
- function;
- comment;
- other.

## `google sheets`

Determine whether that exact phrase exists at all.

This classification is essential.

Do not claim Repo Control failed to search text that does not actually exist.

---

# 10. Distinguish Three Discovery Layers

Use the following terminology explicitly.

## Layer 1 — Symbol discovery

Examples:

- `get_sheet`
- `update_score`
- `get_synonyms_nltk`

Question:

Can Repo Control find named structural code objects and expand relationships?

## Layer 2 — General source-text discovery

Examples:

- `gspread`
- `streamlit`
- `session_state`
- `Practice`

Question:

Can Repo Control locate relevant literal source occurrences even when they are not indexed symbols?

## Layer 3 — Product-language discovery

Examples:

- `google sheets`
- `practice quiz`
- `persistence`
- `where vocabulary is saved`

Question:

Can a user begin with domain/product terminology and reach useful implementation evidence?

Do not conflate these layers.

---

# 11. Determine Original Intended Context Scope

Inspect existing Repo Control architecture documents, milestone prompts, closeouts, tests, and code comments relevant to Context.

Determine whether source-text and/or product-language discovery were part of the intended original scope.

Do not silently redefine the product goal based on current implementation.

For each discovery layer state whether it was:

- explicitly intended;
- implicitly intended;
- explicitly excluded;
- not previously defined clearly.

Cite repository evidence in the closeout.

---

# 12. Source-Text Search Reconnaissance

Determine what deterministic mechanisms could support Layer 2 without replacing the existing structural Context engine.

Evaluate at minimum:

## A. Query-time bounded source scan

Search selected repository files for literal/token matches at query time.

## B. Precomputed source-text index

Index searchable text during repository analysis.

## C. Existing system/library capability

Determine whether current parser/index data already contains enough information but is simply not queried.

For each evaluate:

- implementation complexity;
- deterministic behavior;
- performance;
- cache implications;
- repository-size implications;
- language portability;
- ranking;
- false positives;
- maintainability.

Do not implement.

---

# 13. Searchable Source Categories

Evaluate whether a deterministic fallback should search some or all of:

- import statements;
- dependency manifests;
- identifiers;
- attribute names;
- string literals;
- comments;
- file paths;
- module names;
- function/class names;
- test names;
- configuration keys.

Do not automatically recommend all categories.

For each category assess:

- usefulness;
- noise;
- implementation cost;
- security implications;
- relevance to the Vocab evidence.

Pay special attention to credentials/secrets.

Search must not cause secret contents to be emitted merely because a term appears in a secret-bearing file.

Existing exclusion/ignore policies must remain authoritative.

---

# 14. Source Match to Structural Context

A primary design question is whether source-text matches can become seeds for the existing structural Context machinery.

Investigate a flow such as:

`query`

→ `source-text/import hit`

→ `file + line/range`

→ `nearest/enclosing symbol`

→ `related symbols`

→ `tests`

→ `bounded Context pack`.

Determine whether current parser metadata makes this practical.

Examples:

`gspread`

→ import hit in `app.py`

→ relevant file

→ nearby/enclosing `get_sheet`

→ callers/related persistence functions.

`session_state`

→ source occurrences in `app.py`

→ enclosing UI/runtime regions or symbols where possible.

Document where this works cleanly and where module-level Streamlit code makes "enclosing symbol" ambiguous.

---

# 15. Multiword Product Query Behavior

Investigate deterministic handling for multiword queries such as:

`google sheets`

Possible strategies to evaluate include:

- exact phrase;
- normalized phrase;
- token AND;
- token OR with ranking;
- singular/plural normalization;
- identifier splitting;
- punctuation/underscore normalization.

Do not add arbitrary synonym dictionaries during M011.

Determine whether useful source evidence exists for individual query terms even where the exact phrase does not.

Example:

`google sheets`

may not literally appear, while:

- Google-related credentials;
- `gspread`;
- sheet operations;

do.

Document how far deterministic token handling can bridge this without semantic inference.

---

# 16. Product-Language Query Planning

Assess the proper responsibility boundary for broader product-language discovery.

Evaluate three possibilities:

## A. Repo Control deterministic only

Repo Control performs normalization/token/source searches but no semantic expansion.

## B. Coder/AI query planner + deterministic Repo Control evidence

The coding agent derives candidate search terms from the milestone requirement and Repo Control deterministically searches them.

Example:

`Google Sheets persistence`

may lead the agent to suggest:

- Google;
- sheet;
- spreadsheet;
- gspread;
- persistence;
- save;
- load.

Repo Control then verifies what actually exists.

## C. Semantic/embedding/LLM retrieval inside Repo Control

Evaluate only as a future option.

Do not assume it is necessary.

For each approach discuss:

- deterministic authority;
- auditability;
- reproducibility;
- usefulness;
- implementation complexity;
- risk of hallucinated relevance;
- token/compute cost;
- role separation.

The preferred near-term direction should preserve:

`AI proposes possibilities`

while:

`Repo Control establishes repository facts`.

---

# 17. Coder Burden Analysis

Explicitly evaluate what mechanical work Repo Control should remove from the coder.

Current coder behavior may include:

- guessing search terms;
- grepping source;
- searching imports;
- opening files;
- locating functions;
- finding callers/callees;
- locating tests;
- assembling evidence manually.

Classify each task as:

- should remain coder reasoning;
- should be automated by Repo Control;
- can be shared.

Do not require the coder to perform additional query-planning ceremony simply to compensate for Repo Control deficiencies.

The goal is less mechanical repository spelunking, not more.

---

# 18. Query-Fallback Design

Recommend whether Context should use a deterministic fallback sequence when exact symbol discovery produces no useful seeds.

Evaluate a conceptual order such as:

1. exact/normalized symbol lookup;
2. file/path lookup;
3. import/dependency lookup;
4. bounded source-text lookup;
5. map hits to structural symbols;
6. relationship expansion;
7. bounded evidence ranking.

Determine:

- which steps belong;
- ordering;
- stopping conditions;
- result caps;
- when no-match should remain no-match.

Do not implement the sequence.

---

# 19. Ranking and Noise Control

A broader search can easily become noisy.

Define how usefulness should be measured.

Consider ranking signals such as:

- exact symbol match;
- exact source-text match;
- import match;
- dependency match;
- identifier match;
- string match;
- comment match;
- file-name match;
- relationship proximity;
- test relationship.

Recommend a deterministic precedence.

Avoid arbitrary "relevance scores" unless their meaning is inspectable.

Define maximum result bounds appropriate to current Context behavior.

---

# 20. False-Positive Benchmark

Create a small read-only benchmark designed to detect over-broad search.

Use Vocab terms where appropriate.

Examples may include common words such as:

- `app`;
- `get`;
- `data`;
- `word`;
- `state`.

Determine how a source-text fallback could avoid flooding Context with low-value matches.

Do not optimize only for successful benchmark queries.

A useful Context engine must also remain bounded.

---

# 21. Absent-Implementation Behavior

Preserve legitimate no-match behavior.

Examples:

`container`

should not pretend a Docker/container implementation exists when canonical Vocab contains none.

`database`

should not invent PostgreSQL code where current persistence is Google Sheets.

Determine how future Context should distinguish:

- no lexical evidence;
- related lexical evidence;
- actual structural implementation;
- inferred future architecture.

Repo Control must never convert absence into fabricated certainty.

---

# 22. Security / Secret Handling

Source-text discovery expands the risk surface.

Inspect existing ignore/exclusion rules and determine how a future implementation must avoid:

- indexing ignored secret files;
- printing credential values;
- returning `.env` contents;
- returning private keys;
- returning service-account JSON;
- leaking tokens from source/config.

Recommend safe evidence representations.

Filename/path references may be acceptable where content exposure is not.

Do not open known secret files merely for this reconnaissance.

---

# 23. Parser / Language Considerations

Determine whether the proposed improvement should initially be:

- Python-specific;
- language-agnostic source search with language-specific structural expansion;
- fully language-agnostic.

Repo Control should remain generalized rather than become Vocab-specific.

Use the current supported-language architecture as the deciding evidence.

Do not hard-code:

- `gspread`;
- Streamlit;
- Google Sheets;
- Vocab-specific concepts.

Vocab is the benchmark, not the implementation target.

---

# 24. Test Architecture Reconnaissance

Inspect existing Context tests.

Determine current coverage for:

- exact symbol queries;
- partial symbol queries;
- no matches;
- relationships;
- test discovery;
- duplicate suppression;
- repository bounds;
- ignored files;
- errors/reason codes.

Identify missing tests needed for the proposed enhancement.

Do not write tests in M011.

---

# 25. Frozen Vocab Acceptance Benchmark

Define an explicit benchmark for the future implementation milestone.

At minimum include:

## Exact-symbol controls

`get_sheet`

Expected:

- still succeeds;
- no regression in structural relationships.

`update_score`

Expected:

- still succeeds.

`get_synonyms_nltk`

Expected:

- still succeeds.

## Source-text/import controls

`gspread`

Expected:

- surfaces `app.py`;
- identifies an import/source match;
- leads to useful structural context where feasible.

`streamlit`

Expected:

- surfaces `app.py`;
- identifies source/import evidence.

`session_state`

Expected:

- surfaces relevant `app.py` occurrences;
- does not require a symbol literally named `session_state`.

## Product/domain controls

`practice`

Expected:

- surfaces relevant source evidence if the literal UI term exists;
- leads toward the implementation region where feasible.

`google sheets`

Expected:

- provide materially more useful evidence than current `no_matches` if deterministic token/source evidence supports it;
- do not invent semantic facts unsupported by source.

## Legitimate absence controls

`container`

Expected:

- no false claim of container implementation.

Define precise pass criteria from actual Vocab source evidence.

---

# 26. Additional Repo Control Native Test Fixtures

The implementation must not be validated only against Vocab.

Recommend small synthetic/native Repo Control test fixtures covering:

- import-only match;
- attribute-only match;
- string-literal match;
- multiword query;
- source match mapped to enclosing function;
- source match at module scope;
- ignored secret file;
- noisy common term;
- exact symbol priority over text match.

This prevents overfitting to Vocab.

Do not create the fixtures in M011.

---

# 27. Performance Boundary

Assess likely performance implications.

Consider:

- small repositories;
- larger repositories;
- repeated queries;
- cached repository scans;
- source indexing;
- query-time grep-like search;
- result caps.

Do not prematurely optimize.

Recommend the smallest implementation that remains reasonable for real repositories.

If empirical timing can be measured read-only without changing state, bounded timing evidence may be captured.

---

# 28. Context Artifact Compatibility

Determine whether a future change can preserve existing Context artifact contracts.

Inspect:

- IDs;
- schemas;
- reason/status fields;
- selected files;
- selected symbols;
- relationships;
- diagnostics;
- cached artifacts.

Determine whether source-text evidence would require new fields.

Prefer additive, backward-compatible changes where reasonable.

Do not change schemas in M011.

---

# 29. UI / CLI Implications

Determine whether the improvement can remain largely within Context core logic or requires:

- CLI changes;
- browser UI changes;
- new evidence sections;
- new labels distinguishing symbol vs source-text matches.

Recommend clear evidence provenance.

A user should be able to tell whether a result came from:

- symbol match;
- import match;
- source-text match;
- structural expansion;
- advisory AI.

Do not implement UI changes.

---

# 30. Deterministic Evidence Hierarchy

Preserve the existing authority hierarchy.

Recommended conceptual order:

`Git/source truth`

→ `deterministic parsed/indexed facts`

→ `deterministic source-text/import evidence`

→ `structural expansion`

→ `snapshots/comparisons`

→ `advisory local AI`.

Source-text discovery should strengthen deterministic evidence rather than blur it with AI inference.

---

# 31. Utilization / Workflow Implications

M002.1 exposed a second issue:

A coder can bypass Repo Control if Context is not useful.

Assess how an improved Context capability would fit the future Vocab workflow.

Do not implement utilization tracking yet.

Recommend the minimum future rule:

- coder invokes Repo Control Context before substantive implementation;
- Repo Control provides deterministic evidence where possible;
- direct source inspection remains allowed;
- Context failure must be preserved rather than silently bypassed;
- Git mutation remains guarded through Repo Control where required.

Do not add milestone-session tracking in M011.

That may become a later real-gap milestone.

---

# 32. Proposed Implementation Scope

Conclude with the smallest implementation scope that would materially improve Context.

Classify the recommendation as:

## A — Existing engine already contains the capability; query path needs correction

## B — Small deterministic source-text fallback required

## C — Broader indexing redesign required

## D — Semantic layer required before the intended goal can be met

Choose one based on evidence.

If recommending B, define precisely:

- search categories;
- seed conversion;
- ranking;
- result caps;
- evidence representation;
- tests;
- unchanged behavior.

Do not make "semantic AI search" the default merely because product-language discovery is imperfect.

---

# 33. Separate Future Semantic Layer

If deterministic improvements cannot fully answer broad conceptual queries, define the remaining gap separately.

Example:

`Where does the application remember whether I knew a word?`

may require semantic interpretation beyond literal source search.

Document that as a possible later advisory retrieval layer.

Do not mix that problem into the first deterministic improvement unless required.

---

# 34. Recommended M012

Recommend the exact next Repo Control milestone.

Expected candidate:

`M012 — Deterministic Source-Text Context Fallback and Structural Expansion`

but choose the final scope/name based on reconnaissance.

The next milestone should implement only the smallest validated improvement.

---

# 35. Required Closeout

Create exactly:

`docs/011_context_source_text_and_product_language_discovery_reconnaissance_closeout.md`

The closeout must include:

## 1. Executive conclusion

Current failure diagnosis and recommended next step.

## 2. Starting Repo Control state

Branch, HEAD, upstream, working tree.

## 3. Existing Context architecture

Actual query-to-result flow.

## 4. Current symbol model

What Repo Control recognizes/indexes structurally.

## 5. Current query semantics

Exact matching behavior.

## 6. Reproduced Vocab benchmark

All benchmark queries and results.

## 7. Vocab source-presence classification

Where each query term actually exists.

## 8. Discovery-layer diagnosis

Symbol vs source-text vs product-language.

## 9. Original intended scope

Whether each layer was part of Repo Control's intended objectives.

## 10. Source-text search options

Query-time vs indexed vs existing latent capability.

## 11. Searchable source categories

Imports, identifiers, strings, attributes, etc.

## 12. Text-hit to symbol-expansion feasibility

How source hits can feed structural Context.

## 13. Multiword query behavior

Deterministic options.

## 14. Product-language/query-planning boundary

Repo Control vs coder/AI responsibility.

## 15. Coder burden analysis

Mechanical tasks Repo Control should remove.

## 16. Proposed deterministic fallback pipeline

Exact recommended order.

## 17. Ranking and noise controls

Deterministic precedence and bounds.

## 18. False-positive findings

How to avoid flooding results.

## 19. Legitimate absence handling

How `container`/`database` style cases remain truthful.

## 20. Security findings

Secret/indexing safeguards.

## 21. Parser/language implications

Generalized design boundary.

## 22. Existing test architecture

Current coverage and gaps.

## 23. Frozen Vocab acceptance benchmark

Exact expected future results.

## 24. Native Repo Control fixture recommendations

Non-Vocab regression cases.

## 25. Performance implications

Expected cost and bounding approach.

## 26. Artifact/schema implications

Backward compatibility.

## 27. CLI/UI implications

Evidence provenance and presentation.

## 28. Utilization implications

How improved Context fits coder workflow.

## 29. Recommended implementation classification

A / B / C / D.

## 30. Exact M012 recommendation

Smallest implementation milestone.

## 31. Explicit non-goals

What should not be built yet.

## 32. Limitations / unresolved questions

Anything not safely determined.

## 33. Final Repo Control state

Capture:

    cd /home/chuck/projects/repo-control
    
    git branch --show-current
    git rev-parse HEAD
    git status --short
    git rev-parse @{upstream} 2>/dev/null || true
    git rev-list --left-right --count HEAD...@{upstream} 2>/dev/null || true

---

# 36. Stop Conditions

Stop and report if:

- the current Context implementation materially contradicts prior controlling documentation;
- the Vocab benchmark cannot be reproduced;
- investigation would require modifying Vocab;
- credentials would need to be opened or exposed;
- Repo Control source changes unexpectedly;
- the current dirty Repo Control state makes evidence attribution unreliable;
- a proposed change would require redesigning unrelated Repo Control subsystems merely to solve Context discovery;
- semantic/AI behavior appears required but its authority boundary cannot be kept separate from deterministic evidence.

Do not repair during reconnaissance.

---

# 37. Expected Outcome

M011 should answer, with evidence:

1. Why does `get_sheet` work while `gspread` does not?
2. Why does `get_synonyms_nltk` work while `streamlit` or `session_state` do not?
3. What exactly does current Context index/search?
4. Were source-text and product-language discovery part of the intended Repo Control objective?
5. What deterministic source evidence is currently missing?
6. Can source-text/import hits feed the existing structural context engine?
7. How should multiword product terminology be handled without inventing meaning?
8. What reasoning should remain with the coder/AI?
9. What mechanical discovery should Repo Control remove from the coder?
10. What is the smallest generalized improvement?
11. What exact Vocab benchmark proves the improvement?
12. What additional native fixtures prevent overfitting?
13. What should M012 implement?

---

# 38. Working Principle

> The real Vocab testbed exposed a gap. Diagnose the gap against the original Repo Control objective rather than redefining the objective downward.

Repo Control should preserve deterministic authority while making repository evidence easier to discover from the terminology a real coder actually starts with.

Do not implement until the search/index architecture and acceptance benchmark are understood.

---

**End of `011_context_source_text_and_product_language_discovery_reconnaissance_prompt.md`**
