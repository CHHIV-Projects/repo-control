# Milestone 009 Browser UI Foundation and Read-Only Console Closeout

## 1. status

PASS

## 2. initial branch / HEAD / clean preflight

Preflight before coding:

- branch: `main`
- HEAD: `de40b6843061eb6ff6efe4fede2d4207a1c5d599`
- working tree: clean
- addendum confirmations consumed from prompt section starting near line 1450

## 3. files changed

Modified:

- `README.md`
- `pyproject.toml`
- `src/repoctl/cli.py`

Added:

- `src/repoctl/web/__init__.py`
- `src/repoctl/web/app.py`
- `src/repoctl/web/views.py`
- `src/repoctl/web/templates/base.html`
- `src/repoctl/web/templates/dashboard.html`
- `src/repoctl/web/templates/context.html`
- `src/repoctl/web/templates/snapshots.html`
- `src/repoctl/web/templates/comparisons.html`
- `src/repoctl/web/templates/analysis.html`
- `src/repoctl/web/templates/workflow.html`
- `src/repoctl/web/templates/error.html`
- `src/repoctl/web/static/app.css`
- `tests/test_web.py`
- `docs/009_browser_ui_foundation_and_read_only_console_closeout.md`

## 4. web framework/dependencies selected and rationale

Selected:

- Flask
- Jinja2 (Flask template engine)

Rationale:

- small Python-native server-rendered architecture;
- direct adapter over existing core services;
- no Node/npm toolchain;
- built-in test client enables deterministic web-route testing;
- local static assets and no external CDN.

Dependency declaration:

- `pyproject.toml` now includes `flask>=3.0,<4`.

## 5. web/core architecture

Implemented thin web adapter:

- `repoctl web` command starts local web server;
- routes parse bounded input;
- routes call existing core services (`status`, `context`, `snapshot`, `compare`, `analyze`);
- route output maps into explicit view models (`DashboardView`, `ContextView`, `SnapshotSummary`, `ComparisonSummary`, `AnalysisSummary`, `WorkflowArtifactSummary`);
- Jinja templates render human-readable pages;
- no route reimplements Git porcelain parsing.

## 6. CLI `repoctl web` command

Added command:

```bash
repoctl web --repository <path> [--host 127.0.0.1] [--port 8765]
```

Behavior:

- `--repository` required for explicit single-repository binding;
- default host `127.0.0.1`;
- default port `8765`.

## 7. repository startup-binding contract

At startup:

- repository path is canonicalized and validated as a Git worktree (`validate_git_worktree`);
- repository id derived once (`make_repository_id`);
- all routes operate strictly on that bound repository;
- browser never accepts arbitrary repository filesystem paths.

## 8. loopback/non-loopback behavior

Implemented fail-closed host policy:

- allowed hosts: `127.0.0.1`, `localhost`;
- non-loopback host (including `0.0.0.0`) is blocked with clear error message.

## 9. dashboard implementation

Implemented Dashboard page with:

- repository identity;
- branch, HEAD, workflow state;
- staged/unstaged/untracked/conflict counts;
- active Git operation names;
- upstream configured/ref/relation/ahead/behind;
- explicit remote caveat: no remote refresh performed;
- current snapshot candidate ID and matching snapshot ID.

Includes POST `Refresh Status` action using existing M006 status service.

## 10. context UI implementation

Implemented Context page with:

- bounded query form (`MAX_CONTEXT_QUERY_CHARS = 400`);
- deterministic context generation via existing M003 service;
- human-readable grouped rendering:
  - relevant files,
  - relevant symbols,
  - direct relationships,
  - related tests,
  - diagnostics/limitations;
- reason annotations (lexical/direct/test relationship classes);
- selection of existing context IDs.

## 11. snapshot UI implementation

Implemented Snapshots page with:

- list of immutable snapshots for bound repo;
- branch/head/clean/match information;
- POST `Create Snapshot` action using existing M004 service;
- repeated identical state reuses existing snapshot identity.

## 12. comparison UI implementation

Implemented Comparisons page with:

- selectable known before/after snapshot IDs;
- POST `Compare` action using existing M004 comparison service;
- list of known comparisons for bound repo;
- aggregate structural count rendering for selected comparison.

## 13. GPT-OSS analysis UI implementation

Implemented AI Review page with:

- selectable known comparison IDs only (no free-text ID input);
- POST `Analyze with Local GPT-OSS` action using existing M005/M005.1 service;
- rendering of analysis summary/signals/questions/evidence IDs;
- explicit advisory warning text.

## 14. workflow visibility implementation

Implemented Workflow page with read-only summary visibility:

- current workflow state;
- existing stage/commit plans and linked executions (if present);
- plan metadata summaries (id/type/branch/head/count);
- compatibility indicator from existing artifact facts (`head`/`branch` match only);
- no new plan-validity algorithm added.

## 15. explicit browser Git-mutation prohibition

Browser routes do not execute:

- stage/commit execution services;
- Git add/commit/push/fetch/pull;
- any M007/M008 mutation execution path.

M009 web layer is read-only toward target Git and artifact-producing only for deterministic external evidence routes.

## 16. CSRF implementation

Implemented per-process/per-session protection:

- per-process random Flask secret key;
- per-session random CSRF token in session cookie state;
- all POST routes require `csrf_token`;
- missing/invalid token returns error and aborts action.

## 17. HTML/output escaping evidence

- Jinja auto-escaping is used for all templates;
- focused test validates `<script>alert(1)</script>` is rendered escaped text and not executable markup.

## 18. external-state boundary

Artifact-producing routes continue writing only under:

- `~/.local/share/repoctl/<repository_id>/...`

No web/session/context/snapshot/comparison/analysis artifacts are written into the target repository.

## 19. no-telemetry/offline asset behavior

- no telemetry/analytics/tracking calls added;
- no external CDN/fonts/scripts/icons;
- static CSS served locally from package static directory.

## 20. CLI preservation result

Existing CLI commands remain available and unchanged in behavior. New command addition is additive only.

## 21. focused web test result

Command:

```bash
.venv/bin/python -m unittest tests.test_web -q
```

Result:

- `Ran 12 tests`
- `OK`

## 22. full regression result

Command:

```bash
.venv/bin/python -m unittest -q
```

Result:

- `Ran 140 tests`
- `OK`

## 23. Python-cache hygiene result

- no `.pyc`/`__pycache__` Git noise introduced in tracked status;
- temporary environment artifacts created for validation (`.venv`, `src/repoctl.egg-info`) were removed before final status capture.

Post-regression Git-operation marker check (development repository):

- `MERGE_HEAD=absent:.git/MERGE_HEAD`
- `rebase-merge=absent:.git/rebase-merge`
- `rebase-apply=absent:.git/rebase-apply`
- `REBASE_HEAD=absent:.git/REBASE_HEAD`
- `CHERRY_PICK_HEAD=absent:.git/CHERRY_PICK_HEAD`
- `REVERT_HEAD=absent:.git/REVERT_HEAD`
- `BISECT_LOG=absent:.git/BISECT_LOG`
- `BISECT_START=absent:.git/BISECT_START`

Result: all M006-recognized operation markers absent; no active Git operation reported.

## 24. practical isolated-repository browser validation

Actual runtime command-path smoke validation was performed using installed entrypoint behavior in the documented Python environment against disposable repositories:

Runtime start command:

```bash
.venv/bin/repoctl web --repository /tmp/tmp.UI6hiNO83Q/web-smoke --host 127.0.0.1 --port 8876
```

Observed runtime evidence (actual HTTP requests):

- server started successfully on `http://127.0.0.1:8876`;
- `GET /` returned success (dashboard rendered);
- local Jinja template rendering succeeded (`/` and `/context`);
- local static CSS served successfully (`GET /static/app.css` -> success);
- active repository identity rendered as disposable bound repository (`web-smoke`);
- non-loopback policy enforced by runtime command path:
  - `repoctl web --host 0.0.0.0 ...`
  - result: `web failed: non-loopback host binding is blocked in milestone 009; use 127.0.0.1 or localhost`;
- server shutdown completed cleanly;
- post-shutdown port check showed no remaining listener on `:8876`.

Additional deterministic browser-flow validation also covered:

- dashboard status rendering;
- context generation;
- snapshot creation and deterministic reuse;
- controlled repo change outside UI;
- second snapshot + structural comparison;
- analysis rendering;
- confirmation no target Git mutation from web actions.

## 25. live GPT-OSS browser validation result or bounded provider-unavailable report

Live provider validation was executed through actual M009 web actions against a disposable repository:

- runtime server:

```bash
.venv/bin/repoctl web --repository /tmp/tmp.dFs7cLgXoe/web-live-ai --host 127.0.0.1 --port 8878
```

- web-path sequence performed with real HTTP session/CSRF POST actions:
  - create snapshot (POST);
  - controlled repository change outside UI;
  - create second snapshot (POST);
  - create comparison (POST);
  - run analysis from `/analysis/run` (POST).

Observed results:

- provider available: `provider_available=1`;
- known comparison analyzed through web action:
  - `comparison_id=cmp--a81ac555e8774c32`;
- analysis rendered successfully in browser path:
  - `analysis_render_success=1`;
- grounded evidence IDs visible:
  - `evidence_ids_count=1`;
- advisory labeling visible:
  - `advisory_visible=1`;
- hidden thinking not rendered:
  - `thinking_hidden=1`;
- target repository unchanged by web actions after controlled external change:
  - `target_git_unchanged=1`.

## 26. Windows SSH-tunnel access validation/documentation

README now documents loopback access pattern and SSH forward example:

```bash
ssh -N -L 8765:127.0.0.1:8765 chuck@192.168.1.173
```

then:

```text
http://127.0.0.1:8765
```

## 27. confirmation no browser Git mutation occurred

Confirmed by focused tests and route coverage: browser actions do not mutate target Git.

## 28. confirmation no network Git mutation occurred

Confirmed: no fetch/pull/push routes or route calls were introduced in M009 web adapter.

## 29. confirmation no Vocab App mutation occurred

Confirmed: no Vocab App path was modified or used during M009 implementation.

## 30. confirmation no Photo Organizer access occurred

Confirmed: no Photo Organizer access occurred.

## 31. dependency additions

Added dependency:

- `flask>=3.0,<4`

No unrelated dependency upgrades were introduced.

## 32. limitations/deferred items

Deferred to later milestones:

- browser mutation controls for stage/commit approvals;
- LAN authentication and non-loopback exposure;
- multi-user/auth accounts;
- background jobs/websocket orchestration;
- deployment mechanics (systemd/Docker/reverse proxy/TLS).

## 33. recommendation for M010

Expose existing M007/M008 workflows in browser through explicit review and approval flow only:

- review immutable stage plan;
- explicit approve-stage;
- verify staged state;
- snapshot;
- review immutable commit plan;
- explicit approve-commit;
- verify post-commit evidence.

Reuse existing trusted core services without introducing browser-side mutation logic.

## 34. literal final `git status --short`

```text
 M README.md
 M pyproject.toml
 M src/repoctl/cli.py
?? docs/009_browser_ui_foundation_and_read_only_console_closeout.md
?? src/repoctl/web/
?? tests/test_web.py
```
