# Milestone 005 Closeout — GPT-OSS Structural Delta Analysis

STATUS: IMPLEMENTATION COMPLETE

MILESTONE ACCEPTANCE: ESCALATION REQUIRED

This closeout reflects full deterministic implementation and test validation, with fail-closed live-model behavior. During bounded live validation attempts, the local model did not return valid structured JSON for either required scenario.

## 1. Implementation Summary

Implemented Milestone 005 with a focused analysis layer that:

- adds `repoctl analyze <comparison_id> [--repository <path>]`;
- validates immutable comparison evidence before any model call;
- constructs a bounded deterministic `analysis_input.json` packet;
- enforces canonical category ordering, category caps, global byte limit, and final evidence-ID assignment;
- calls local-only Ollama (`127.0.0.1:11434`) for one request per invocation;
- validates and normalizes model output mechanically;
- enforces strict zero-delta and non-zero grounding rules;
- publishes immutable analysis artifacts transactionally;
- fails closed on provider/validation errors with no partial publish.

## 2. Files Added/Modified

Added:

- `src/repoctl/analysis/__init__.py`
- `src/repoctl/analysis/contracts.py`
- `src/repoctl/analysis/packet.py`
- `src/repoctl/analysis/provider.py`
- `src/repoctl/analysis/schema.py`
- `src/repoctl/analysis/manager.py`
- `tests/test_analysis.py`

Modified:

- `src/repoctl/cli.py`
- `src/repoctl/scanner/core.py`
- `README.md`

## 3. Analyze CLI Behavior

Added command:

- `repoctl analyze <comparison_id> [--repository <path>]`

Behavior:

- resolves target repository root and `repository_id` from current directory or explicit `--repository`;
- loads named immutable comparison from external state namespace;
- builds deterministic packet;
- resolves exact model digest from `/api/tags`;
- performs one provider request (`PROVIDER_ATTEMPTS = 1`);
- validates/normalizes response;
- writes immutable artifacts under external state;
- prints provenance IDs and model identity fields;
- returns non-zero on any validation/provider/integrity failure.

## 4. Local-Only Provider Boundary

Production provider path is loopback-only:

- `http://127.0.0.1:11434`

No cloud fallback, no alternate provider fallback, and no model auto-pull behavior were implemented.

## 5. GPT-OSS Model Name and Validated Digest

Live preflight source:

- `GET http://127.0.0.1:11434/api/tags`

Validated:

- exact `name == "gpt-oss:20b"`
- exactly one match
- digest format: 64-char lowercase hex

Observed digest:

- `17052f91a42e97930aa6e28a6c6c06a983e6a58dbb00434885a0cf5313e376f7`

## 6. Provider Request Contract

Request behavior implemented:

- model: `gpt-oss:20b`
- stream: `false`
- schema-constrained structured output requested via provider `format`
- options: `temperature=0`
- thinking disabled (`think=false`)
- no tool definitions
- one request per invocation (no auto-retry)

## 7. Deterministic Analysis-Packet Schema

`analysis_input.json` includes:

- `schema_version=1`
- `packet_id`
- `repository_id`
- `comparison_id`
- snapshot IDs
- before/after branch/head/coverage evidence
- full aggregate counts
- bounded detailed evidence records
- deterministic truncation metadata
- explicit authority statement

No source-code bodies/snippets are included.

## 8. Evidence-ID Contract

Implemented evidence prefixes:

- `A`, `C`, `F`, `Q`, `S`, `R`, `T`, `P`, `D`

Rules enforced:

- IDs assigned only after final byte-trim outcome;
- numbering is deterministic within prefix (`F001`, `F002`, ...);
- omitted records have no IDs;
- response IDs must exist in final packet evidence set.

## 9. Packet Bounds/Truncation Behavior

Implemented constants:

- `MAX_AI_FILE_RECORDS=25`
- `MAX_AI_REQUIREMENTS_RECORDS=10`
- `MAX_AI_SYMBOL_RECORDS=30`
- `MAX_AI_RELATIONSHIP_RECORDS=50`
- `MAX_AI_TEST_RECORDS=20`
- `MAX_AI_PARSE_RECORDS=10`
- `MAX_AI_DIAGNOSTIC_RECORDS=10`
- `MAX_ANALYSIS_PACKET_BYTES=32768`

Order/trim contract:

- category caps applied first;
- global byte enforcement applied second;
- tail-trim from canonical detailed stream only;
- protected evidence (aggregate/coverage/core metadata) preserved;
- hard fail if protected packet alone exceeds byte bound.

## 10. Packet/Request/Analysis Identity Contracts

Implemented:

- `packet_id = aip--...` from canonical packet payload bytes
- `request_id = areq--...` from packet_id + provider + model_name + model_digest + prompt_contract_version
- `analysis_id = ana--...` from request_id + canonical validated normalized model output bytes

Changing model digest changes request identity; different valid model outputs produce different analysis IDs.

## 11. AI Response Schema

Top-level required exact fields:

- `summary`
- `summary_evidence_ids`
- `review_signals`
- `questions_for_human_review`

Includes enum/bounds checks for categories/priorities and item limits.

## 12. Evidence-Grounding Validation

Validator enforces:

- required fields only;
- string and list bounds;
- valid enum values;
- evidence-ID existence in packet;
- no duplicate evidence IDs within an item;
- no CR/LF in summary/observation/interpretation/question strings.

Invalid outputs are rejected; no partial analysis publish.

## 13. Zero-Delta Rule

Strictly enforced:

- for zero-delta aggregate: `review_signals=[]` and `questions_for_human_review=[]`.

Any violation is a hard validation failure.

## 14. Analysis Storage/Immutability

Storage path:

- `~/.local/share/repoctl/<repository_id>/analyses/<comparison_id>/<analysis_id>/`

Required artifacts:

- `analysis_input.json`
- `analysis.json`
- `analysis.md`

Publication behavior:

- transactional staging then publish;
- reuse if existing content identical;
- fail closed on identity/content mismatch;
- no partial directory on failure.

## 15. Automated Test Results

Final suite execution:

- command: `PYTHONPATH=src python3 -m unittest`
- result: `Ran 66 tests ... OK`

Milestone 005 specific:

- command: `PYTHONPATH=src python3 -m unittest tests.test_analysis`
- result: `Ran 13 tests ... OK`

Syntax validation:

- `py_compile` over new/modified Milestone 005 modules passed.

## 16. Controlled Non-Zero Live GPT-OSS Result

Scenario:

- disposable fixture repository
- non-zero comparison: `cmp--7f2c951512105433`
- aggregate evidence confirmed structural deltas (files/requirements/symbol/dependency/call/test-reference changes present)

Live attempts (max 3 explicit invocations):

- attempt 1: fail
- attempt 2: fail
- attempt 3: fail

Failure category:

- `provider request failed: ollama structured response is not valid JSON`

No analysis artifacts were published for this comparison.

## 17. Zero-Delta Live GPT-OSS Result

Scenario:

- self-comparison zero-delta: `cmp--99ec1039b8aef143`

Live attempts (max 3 explicit invocations):

- attempt 1: fail
- attempt 2: fail
- attempt 3: fail

Failure category:

- `provider request failed: ollama structured response is not valid JSON`

No analysis artifacts were published for this comparison.

## 18. Representative Review Signals with Evidence IDs

No valid live model response was accepted, so no live signals were published.

Representative contract-conformant signal shape (from fake-provider automated validation path):

- `review_priority: low`
- `category: cross_category`
- `observation: Structural changes are present in deterministic aggregate evidence.`
- `interpretation: Direct source and test inspection is appropriate before drawing conclusions.`
- `evidence_ids: ["A001"]`

## 19. Practical Product-Check Result

Question:

- Can local GPT-OSS convert bounded deterministic structural evidence into useful prioritized review guidance?

Result for this environment:

- deterministic implementation supports the workflow;
- live local model did not satisfy strict structured-output grounding contract within bounded attempts;
- therefore practical live demonstration is incomplete under current model behavior.

## 20. Unsupported/Hallucinated Factual Claims Observed

No validated live outputs were accepted, so no published hallucinated claims occurred.

## 21. Target Repository Before/After Git Status

Disposable fixture target was used (not Vocab App).

Observed after live analyze attempts:

- `git status --porcelain=v2 -z --untracked-files=all | wc -c` -> `0`

This indicates no target repository mutation by `repoctl analyze` during live validation.

## 22. Limitations

- Live model output did not satisfy structured JSON contract in this environment.
- Milestone 005 remains fail-closed by design; invalid live output is rejected and unpublished.
- No source-body augmentation is implemented by contract.

## 23. Milestone 006 Opportunities (Not Implemented)

- Robust provider output debugging traces (still without storing hidden reasoning).
- Additional strict parser diagnostics for malformed structured outputs.
- Optional operator tooling for faster bounded manual re-invocation workflows.
- Future prompt/contract versioning for model-specific structured-output quirks while preserving safeguards.

## 24. Final Repo Control Plane Git Status

Final `git status --short` at closeout time:

- `M README.md`
- `M src/repoctl/cli.py`
- `M src/repoctl/scanner/core.py`
- `?? src/repoctl/analysis/`
- `?? tests/test_analysis.py`

No commit or push was performed in this closeout step.
