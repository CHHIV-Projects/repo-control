from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from repoctl.cli import main
from repoctl.scanner.core import run_scan_with_artifacts
from repoctl.snapshot.manager import create_snapshot
from repoctl.workflow.commit_execution import execute_prepared_commit
from repoctl.workflow.commit_plan import prepare_commit
from repoctl.workflow.errors import WorkflowReasonError


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


def _init_repo(root: Path, name: str = "wf-commit") -> Path:
    repo = root / name
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")

    (repo / "app.py").write_text("def run():\n    return 1\n", encoding="utf-8")
    _git(repo, "add", "app.py")
    _git(repo, "commit", "-m", "initial")
    return repo


def _prepare_staged_change(repo: Path, state: Path) -> None:
    (repo / "app.py").write_text("def run():\n    return 2\n", encoding="utf-8")
    _git(repo, "add", "app.py")
    scan = run_scan_with_artifacts(str(repo), state_root=state)
    create_snapshot(scan, state_root=state)


def _prepare_plan(repo: Path, state: Path, msg: str = "test commit") -> dict:
    _prepare_staged_change(repo, state)
    return prepare_commit(str(repo), msg, state_root=state)


class WorkflowCommitTests(unittest.TestCase):
    def test_prepare_success_is_target_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"
            _prepare_staged_change(repo, state)

            before_head = _git_text(repo, "rev-parse", "HEAD")
            before_status = _git(repo, "status", "--porcelain=v2", "-z", "--untracked-files=all")
            result = prepare_commit(str(repo), "m007 prepare", state_root=state)
            after_head = _git_text(repo, "rev-parse", "HEAD")
            after_status = _git(repo, "status", "--porcelain=v2", "-z", "--untracked-files=all")

            self.assertEqual(before_head, after_head)
            self.assertEqual(before_status, after_status)
            self.assertTrue((Path(result["plan_dir"]) / "plan.json").exists())

    def test_prepare_blocks_missing_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"
            (repo / "app.py").write_text("def run():\n    return 2\n", encoding="utf-8")
            _git(repo, "add", "app.py")

            with self.assertRaises(WorkflowReasonError) as cm:
                prepare_commit(str(repo), "m", state_root=state)
            self.assertEqual(cm.exception.code, "matching_snapshot_required")

    def test_prepare_blocks_invalid_commit_message(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"
            _prepare_staged_change(repo, state)

            with self.assertRaises(WorkflowReasonError) as cm:
                prepare_commit(str(repo), "", state_root=state)
            self.assertEqual(cm.exception.code, "invalid_commit_message")

            with self.assertRaises(WorkflowReasonError) as cm2:
                prepare_commit(str(repo), "bad\x00msg", state_root=state)
            self.assertEqual(cm2.exception.code, "invalid_commit_message")

    def test_prepare_blocks_unstaged_untracked_conflict_and_detached(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state = root / "state"

            repo = _init_repo(root, "r1")
            _prepare_staged_change(repo, state)
            (repo / "app.py").write_text("def run():\n    return 3\n", encoding="utf-8")
            with self.assertRaises(WorkflowReasonError) as cm1:
                prepare_commit(str(repo), "m", state_root=state)
            self.assertEqual(cm1.exception.code, "unstaged_changes_present")

            repo2 = _init_repo(root, "r2")
            _prepare_staged_change(repo2, state)
            (repo2 / "new.txt").write_text("x\n", encoding="utf-8")
            with self.assertRaises(WorkflowReasonError) as cm2:
                prepare_commit(str(repo2), "m", state_root=state)
            self.assertEqual(cm2.exception.code, "untracked_changes_present")

            repo3 = _init_repo(root, "r3")
            _git(repo3, "checkout", "--detach", "HEAD")
            (repo3 / "app.py").write_text("def run():\n    return 2\n", encoding="utf-8")
            _git(repo3, "add", "app.py")
            scan = run_scan_with_artifacts(str(repo3), state_root=state)
            create_snapshot(scan, state_root=state)
            with self.assertRaises(WorkflowReasonError) as cm3:
                prepare_commit(str(repo3), "m", state_root=state)
            self.assertEqual(cm3.exception.code, "detached_head")

            repo4 = _init_repo(root, "r4")
            branch = _git_text(repo4, "branch", "--show-current")
            _git(repo4, "checkout", "-b", "feature")
            (repo4 / "app.py").write_text("def run():\n    return 10\n", encoding="utf-8")
            _git(repo4, "add", "app.py")
            _git(repo4, "commit", "-m", "feature")
            _git(repo4, "checkout", branch)
            (repo4 / "app.py").write_text("def run():\n    return 20\n", encoding="utf-8")
            _git(repo4, "add", "app.py")
            _git(repo4, "commit", "-m", "main")
            proc = subprocess.run(["git", "-C", str(repo4), "merge", "feature"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            self.assertNotEqual(proc.returncode, 0)
            scan = run_scan_with_artifacts(str(repo4), state_root=state)
            create_snapshot(scan, state_root=state)
            with self.assertRaises(WorkflowReasonError) as cm4:
                prepare_commit(str(repo4), "m", state_root=state)
            self.assertEqual(cm4.exception.code, "conflicts_present")

    def test_prepare_blocks_active_git_operation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"
            _prepare_staged_change(repo, state)

            marker = _git_text(repo, "rev-parse", "--git-path", "MERGE_HEAD")
            marker_path = Path(marker)
            if not marker_path.is_absolute():
                marker_path = (repo / marker_path).resolve()
            marker_path.parent.mkdir(parents=True, exist_ok=True)
            marker_path.write_text("deadbeef\n", encoding="utf-8")

            with self.assertRaises(WorkflowReasonError) as cm:
                prepare_commit(str(repo), "m", state_root=state)
            self.assertEqual(cm.exception.code, "git_operation_in_progress")

    def test_plan_deterministic_and_integrity_checks(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"

            plan1 = _prepare_plan(repo, state, "msg")
            plan2 = prepare_commit(str(repo), "msg", state_root=state)
            self.assertEqual(plan1["plan_id"], plan2["plan_id"])
            self.assertTrue(plan2["reused_existing"])

            plan_dir = Path(plan1["plan_dir"])
            payload = json.loads((plan_dir / "plan.json").read_text(encoding="utf-8"))
            payload["commit_message"] = "tampered"
            (plan_dir / "plan.json").write_text(json.dumps(payload, sort_keys=True) + "\n", encoding="utf-8")

            with self.assertRaises(WorkflowReasonError) as cm:
                execute_prepared_commit(str(repo), plan1["plan_id"], True, state_root=state)
            self.assertEqual(cm.exception.code, "plan_integrity_failed")

    def test_commit_requires_approval(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"

            plan = _prepare_plan(repo, state, "approved message")
            before = _git_text(repo, "rev-parse", "HEAD")
            with self.assertRaises(WorkflowReasonError) as cm:
                execute_prepared_commit(str(repo), plan["plan_id"], False, state_root=state)
            self.assertEqual(cm.exception.code, "approval_required")
            self.assertEqual(before, _git_text(repo, "rev-parse", "HEAD"))

    def test_plan_not_found_and_repository_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state = root / "state"

            repo1 = _init_repo(root, "m1")
            plan = _prepare_plan(repo1, state, "mismatch")

            repo2 = _init_repo(root, "m2")
            with self.assertRaises(WorkflowReasonError) as cm1:
                execute_prepared_commit(str(repo2), plan["plan_id"], True, state_root=state)
            self.assertEqual(cm1.exception.code, "repository_mismatch")

            with self.assertRaises(WorkflowReasonError) as cm2:
                execute_prepared_commit(str(repo1), "commit-plan--missing000", True, state_root=state)
            self.assertEqual(cm2.exception.code, "plan_not_found")

    def test_stale_plan_blocks_on_head_branch_and_staged_changes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state = root / "state"

            repo1 = _init_repo(root, "s1")
            plan1 = _prepare_plan(repo1, state, "m")
            _git(repo1, "checkout", "-b", "other")
            with self.assertRaises(WorkflowReasonError) as cm1:
                execute_prepared_commit(str(repo1), plan1["plan_id"], True, state_root=state)
            self.assertEqual(cm1.exception.code, "branch_changed")

            repo2 = _init_repo(root, "s2")
            plan2 = _prepare_plan(repo2, state, "m")
            _git(repo2, "commit", "--allow-empty", "-m", "advance head")
            with self.assertRaises(WorkflowReasonError) as cm2:
                execute_prepared_commit(str(repo2), plan2["plan_id"], True, state_root=state)
            self.assertEqual(cm2.exception.code, "head_changed")

            repo3 = _init_repo(root, "s3")
            plan3 = _prepare_plan(repo3, state, "m")
            (repo3 / "app.py").write_text("def run():\n    return 9\n", encoding="utf-8")
            _git(repo3, "add", "app.py")
            with self.assertRaises(WorkflowReasonError) as cm3:
                execute_prepared_commit(str(repo3), plan3["plan_id"], True, state_root=state)
            self.assertEqual(cm3.exception.code, "staged_state_changed")

    def test_hook_boundary_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            state = root / "state"

            repo = _init_repo(root)
            plan = _prepare_plan(repo, state, "hook check")
            hooks_dir = Path(_git_text(repo, "rev-parse", "--git-path", "hooks"))
            if not hooks_dir.is_absolute():
                hooks_dir = (repo / hooks_dir).resolve()
            hooks_dir.mkdir(parents=True, exist_ok=True)
            hook = hooks_dir / "pre-commit"
            hook.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            hook.chmod(0o755)

            with self.assertRaises(WorkflowReasonError) as cm:
                execute_prepared_commit(str(repo), plan["plan_id"], True, state_root=state)
            self.assertEqual(cm.exception.code, "unsupported_git_hooks")

            repo2 = _init_repo(root, "hooks-path")
            plan2 = _prepare_plan(repo2, state, "hooksPath")
            _git(repo2, "config", "core.hooksPath", ".githooks")
            with self.assertRaises(WorkflowReasonError) as cm2:
                execute_prepared_commit(str(repo2), plan2["plan_id"], True, state_root=state)
            self.assertEqual(cm2.exception.code, "unsupported_git_hooks")

    def test_git_identity_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"
            plan = _prepare_plan(repo, state, "identity")

            real_run = subprocess.run

            def fake_run(cmd, *args, **kwargs):
                if isinstance(cmd, list) and len(cmd) >= 5 and cmd[0] == "git" and cmd[3] == "var":
                    cp = subprocess.CompletedProcess(cmd, 1, stdout=b"", stderr=b"identity missing")
                    return cp
                return real_run(cmd, *args, **kwargs)

            with mock.patch("repoctl.workflow.commit_execution.subprocess.run", side_effect=fake_run):
                with self.assertRaises(WorkflowReasonError) as cm:
                    execute_prepared_commit(str(repo), plan["plan_id"], True, state_root=state)
            self.assertEqual(cm.exception.code, "git_identity_unavailable")

    def test_successful_commit_and_execution_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"
            plan = _prepare_plan(repo, state, "complete m007")

            before = _git_text(repo, "rev-parse", "HEAD")
            result = execute_prepared_commit(str(repo), plan["plan_id"], True, state_root=state)
            after = _git_text(repo, "rev-parse", "HEAD")
            self.assertNotEqual(before, after)
            self.assertEqual(result["head_after"], after)
            self.assertEqual(_git_text(repo, "show", "-s", "--format=%s", "HEAD"), "complete m007")
            self.assertEqual(_git_text(repo, "status", "--short"), "")
            self.assertTrue((Path(result["execution_dir"]) / "execution.json").exists())

    def test_commit_failure_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"
            plan = _prepare_plan(repo, state, "fail commit")

            real_run = subprocess.run

            def fake_run(cmd, *args, **kwargs):
                if isinstance(cmd, list) and len(cmd) >= 5 and cmd[0] == "git" and cmd[3] == "commit":
                    return subprocess.CompletedProcess(cmd, 1, stdout=b"", stderr=b"commit blocked")
                return real_run(cmd, *args, **kwargs)

            before = _git_text(repo, "rev-parse", "HEAD")
            with mock.patch("repoctl.workflow.commit_execution.subprocess.run", side_effect=fake_run):
                with self.assertRaises(WorkflowReasonError) as cm:
                    execute_prepared_commit(str(repo), plan["plan_id"], True, state_root=state)
            self.assertEqual(cm.exception.code, "git_commit_failed")
            self.assertEqual(before, _git_text(repo, "rev-parse", "HEAD"))

    def test_post_verification_failure_after_successful_commit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"
            plan = _prepare_plan(repo, state, "verify failure")
            before = _git_text(repo, "rev-parse", "HEAD")

            with self.assertRaises(WorkflowReasonError) as cm:
                execute_prepared_commit(
                    str(repo),
                    plan["plan_id"],
                    True,
                    state_root=state,
                    _test_force_post_verify_failure=True,
                )
            self.assertEqual(cm.exception.code, "post_commit_verification_failed")
            self.assertNotEqual(before, _git_text(repo, "rev-parse", "HEAD"))
            self.assertIsNotNone(cm.exception.commit_id)

    def test_commit_succeeded_audit_failed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"
            plan = _prepare_plan(repo, state, "audit failure")
            before = _git_text(repo, "rev-parse", "HEAD")

            with self.assertRaises(WorkflowReasonError) as cm:
                execute_prepared_commit(
                    str(repo),
                    plan["plan_id"],
                    True,
                    state_root=state,
                    _test_force_audit_failure=True,
                )
            self.assertEqual(cm.exception.code, "commit_succeeded_audit_failed")
            self.assertNotEqual(before, _git_text(repo, "rev-parse", "HEAD"))
            self.assertIsNotNone(cm.exception.commit_id)

    def test_cli_prepare_and_commit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = _init_repo(root)
            state = root / "state"
            _prepare_staged_change(repo, state)

            with mock.patch("repoctl.workflow.commit_plan.DEFAULT_STATE_ROOT", state), mock.patch(
                "repoctl.workflow.commit_execution.DEFAULT_STATE_ROOT", state
            ), mock.patch("repoctl.workflow.status.DEFAULT_STATE_ROOT", state):
                code = main(["milestone", "prepare-commit", "--repository", str(repo), "--message", "cli message"])
                self.assertEqual(code, 0)

                repo_id_dirs = [p for p in state.iterdir() if p.is_dir()]
                self.assertTrue(repo_id_dirs)
                plans = list((repo_id_dirs[0] / "workflow" / "commit_plans").iterdir())
                self.assertEqual(len(plans), 1)
                plan_id = plans[0].name

                code2 = main(["milestone", "commit", plan_id, "--approve", "--repository", str(repo)])
                self.assertEqual(code2, 0)


if __name__ == "__main__":
    unittest.main()
