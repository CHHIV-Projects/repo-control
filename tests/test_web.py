from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from repoctl.analysis.manager import AnalysisError, analyze_comparison
from repoctl.analysis.provider import ModelIdentity
from repoctl.compare.manager import compare_snapshots
from repoctl.scanner.core import run_scan_with_artifacts
from repoctl.snapshot.manager import create_snapshot
from repoctl.web.app import create_web_app


def _git(repo: Path, *args: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
    return proc.stdout


def _git_text(repo: Path, *args: str) -> str:
    return _git(repo, *args).decode("utf-8", errors="strict").strip()


def _git_status_porcelain(repo: Path) -> bytes:
    return _git(repo, "status", "--porcelain=v2", "-z", "--untracked-files=all")


def _init_repo(root: Path, name: str = "web-repo") -> Path:
    repo = root / name
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")

    (repo / "app.py").write_text("def run():\n    return 1\n", encoding="utf-8")
    (repo / "module_a.py").write_text("from module_b import helper\n\n\ndef run():\n    return helper()\n", encoding="utf-8")
    (repo / "module_b.py").write_text("def helper():\n    return 1\n", encoding="utf-8")
    (repo / "test_module_a.py").write_text("from module_b import helper\n\n\ndef test_run():\n    helper()\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "initial")
    return repo


def _extract_csrf_token(client) -> str:
    with client.session_transaction() as sess:
        return sess["csrf_token"]


class _FakeProvider:
    def __init__(self, response_payload: dict) -> None:
        self._response_payload = response_payload
        self._identity = ModelIdentity(provider="ollama", model_name="gpt-oss:20b", model_digest="a" * 64)

    def resolve_model_identity(self) -> ModelIdentity:
        return self._identity

    def generate_analysis(self, **kwargs):
        return self._response_payload


class WebTests(unittest.TestCase):
    def test_init_rejects_non_git_repository(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with self.assertRaises(Exception):
                create_web_app(repository_path=str(root), state_root=root / "state")

    def test_loopback_policy_and_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            app = create_web_app(repository_path=str(repo), state_root=root / "state")
            self.assertEqual(app.config["BOUND_HOST"], "127.0.0.1")
            self.assertEqual(app.config["BOUND_PORT"], 8765)

            with self.assertRaises(ValueError):
                create_web_app(repository_path=str(repo), host="0.0.0.0", state_root=root / "state")

    def test_dashboard_renders_clean_state_and_upstream_caveat(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            app = create_web_app(repository_path=str(repo), state_root=root / "state")
            client = app.test_client()

            resp = client.get("/")
            text = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Repository Dashboard", text)
            self.assertIn("clean", text)
            self.assertIn("No remote refresh was performed.", text)

    def test_dashboard_renders_unstaged_state(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            (repo / "app.py").write_text("def run():\n    return 2\n", encoding="utf-8")

            app = create_web_app(repository_path=str(repo), state_root=root / "state")
            client = app.test_client()
            resp = client.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("unstaged_only", resp.get_data(as_text=True))

    def test_context_post_requires_csrf(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            app = create_web_app(repository_path=str(repo), state_root=root / "state")
            client = app.test_client()

            before_head = _git_text(repo, "rev-parse", "HEAD")
            before_status = _git_status_porcelain(repo)

            resp = client.post("/context/generate", data={"query": "source readiness"})
            self.assertEqual(resp.status_code, 400)
            self.assertIn("Invalid request token.", resp.get_data(as_text=True))
            self.assertEqual(before_head, _git_text(repo, "rev-parse", "HEAD"))
            self.assertEqual(before_status, _git_status_porcelain(repo))

    def test_context_escapes_html_and_keeps_target_git_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            app = create_web_app(repository_path=str(repo), state_root=root / "state")
            client = app.test_client()

            before_head = _git_text(repo, "rev-parse", "HEAD")
            before_status = _git_status_porcelain(repo)

            client.get("/context")
            csrf = _extract_csrf_token(client)
            resp = client.post(
                "/context/generate",
                data={"csrf_token": csrf, "query": "<script>alert(1)</script>"},
                follow_redirects=True,
            )
            text = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", text)
            self.assertNotIn("<script>alert(1)</script>", text)
            self.assertEqual(before_head, _git_text(repo, "rev-parse", "HEAD"))
            self.assertEqual(before_status, _git_status_porcelain(repo))

    def test_snapshot_create_requires_csrf(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state_root = root / "state"
            app = create_web_app(repository_path=str(repo), state_root=state_root)
            client = app.test_client()

            snapshots_root = state_root / app.config["REPO_ID"] / "snapshots"
            resp = client.post("/snapshots/create", data={})
            self.assertEqual(resp.status_code, 400)
            self.assertFalse(snapshots_root.exists())

    def test_snapshot_reuse_identity_on_repeat(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state_root = root / "state"
            app = create_web_app(repository_path=str(repo), state_root=state_root)
            client = app.test_client()

            client.get("/snapshots")
            csrf = _extract_csrf_token(client)
            resp1 = client.post("/snapshots/create", data={"csrf_token": csrf}, follow_redirects=True)
            self.assertEqual(resp1.status_code, 200)
            resp2 = client.post("/snapshots/create", data={"csrf_token": csrf}, follow_redirects=True)
            self.assertEqual(resp2.status_code, 200)

            repo_id = app.config["REPO_ID"]
            snapshots_root = state_root / repo_id / "snapshots"
            snapshot_ids = sorted([child.name for child in snapshots_root.iterdir() if child.is_dir()])
            self.assertEqual(len(snapshot_ids), 1)

    def test_comparison_known_snapshot_and_unknown_snapshot_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state_root = root / "state"
            app = create_web_app(repository_path=str(repo), state_root=state_root)
            client = app.test_client()

            before = create_snapshot(run_scan_with_artifacts(str(repo), state_root=state_root), state_root=state_root)
            (repo / "module_b.py").write_text("def helper():\n    return 2\n", encoding="utf-8")
            _git(repo, "add", "module_b.py")
            _git(repo, "commit", "-m", "change")
            after = create_snapshot(run_scan_with_artifacts(str(repo), state_root=state_root), state_root=state_root)

            client.get("/comparisons")
            csrf = _extract_csrf_token(client)
            good = client.post(
                "/comparisons/create",
                data={
                    "csrf_token": csrf,
                    "before_snapshot_id": before["snapshot_id"],
                    "after_snapshot_id": after["snapshot_id"],
                },
                follow_redirects=True,
            )
            self.assertEqual(good.status_code, 200)
            self.assertIn("Aggregate Counts", good.get_data(as_text=True))

            bad = client.post(
                "/comparisons/create",
                data={
                    "csrf_token": csrf,
                    "before_snapshot_id": "snap--unknown",
                    "after_snapshot_id": after["snapshot_id"],
                },
            )
            self.assertEqual(bad.status_code, 400)
            self.assertIn("known snapshot IDs", bad.get_data(as_text=True))

    def test_analysis_render_and_provider_failure_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state_root = root / "state"
            app = create_web_app(repository_path=str(repo), state_root=state_root)
            client = app.test_client()

            before = create_snapshot(run_scan_with_artifacts(str(repo), state_root=state_root), state_root=state_root)
            (repo / "module_b.py").write_text("from module_c import new_func\n\ndef helper():\n    return new_func()\n", encoding="utf-8")
            (repo / "module_c.py").write_text("def new_func():\n    return 3\n", encoding="utf-8")
            _git(repo, "add", "module_b.py", "module_c.py")
            _git(repo, "commit", "-m", "delta")
            after = create_snapshot(run_scan_with_artifacts(str(repo), state_root=state_root), state_root=state_root)
            cmp_result = compare_snapshots(before["snapshot_id"], after["snapshot_id"], str(repo), state_root=state_root)

            provider = _FakeProvider(
                {
                    "summary": "Deterministic structural evidence reviewed.",
                    "summary_evidence_ids": ["A001"],
                    "review_signals": [
                        {
                            "category": "cross_category",
                            "review_priority": "low",
                            "observation": "Structural changes present.",
                            "interpretation": "Inspect source and tests.",
                            "evidence_ids": ["A001"],
                        }
                    ],
                    "questions_for_human_review": [
                        {
                            "review_priority": "low",
                            "question": "Was this change intentional?",
                            "evidence_ids": ["A001"],
                        }
                    ],
                }
            )
            analysis_result = analyze_comparison(cmp_result["comparison_id"], str(repo), state_root=state_root, provider=provider)

            rendered = client.get(
                f"/analysis?comparison_id={cmp_result['comparison_id']}&analysis_id={analysis_result['analysis_id']}"
            )
            text = rendered.get_data(as_text=True)
            self.assertEqual(rendered.status_code, 200)
            self.assertIn("A001", text)
            self.assertIn("advisory", text.casefold())
            self.assertNotIn("message.thinking", text)

            client.get("/analysis")
            csrf = _extract_csrf_token(client)
            with mock.patch("repoctl.web.app.analyze_comparison", side_effect=AnalysisError("provider error [invalid_structured_content_json]: invalid")):
                failed = client.post(
                    "/analysis/run",
                    data={"csrf_token": csrf, "comparison_id": cmp_result["comparison_id"]},
                )
            self.assertEqual(failed.status_code, 400)
            self.assertIn("No TARGET GIT MUTATION".lower(), failed.get_data(as_text=True).lower())

    def test_workflow_page_has_visibility_and_no_mutation_controls(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state_root = root / "state"
            app = create_web_app(repository_path=str(repo), state_root=state_root)
            client = app.test_client()

            resp = client.get("/workflow")
            text = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Workflow Visibility", text)
            self.assertNotIn("Approve Stage", text)
            self.assertNotIn("Approve Commit", text)

    def test_forbidden_git_mutation_services_not_invoked_by_web_actions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state_root = root / "state"
            app = create_web_app(repository_path=str(repo), state_root=state_root)
            client = app.test_client()

            with mock.patch("repoctl.web.app.compare_snapshots") as cmp_mock, mock.patch("repoctl.web.app.create_snapshot") as snap_mock:
                client.get("/")
                client.get("/context")
                client.get("/workflow")
                self.assertFalse(cmp_mock.called)
                self.assertFalse(snap_mock.called)
