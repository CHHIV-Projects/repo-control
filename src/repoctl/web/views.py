from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..analysis.manager import _verify_existing_analysis
from ..compare.manager import _verify_existing_comparison
from ..context.policy import MATCH_STATUS_MATCHED
from ..scanner.util import encode_path_order
from ..snapshot.manager import _verify_existing_snapshot


@dataclass(frozen=True)
class DashboardView:
    repository_name: str
    repository_root: str
    branch: str
    head: str
    workflow_state: str
    staged_count: int
    unstaged_count: int
    untracked_count: int
    unmerged_count: int
    git_operation: str
    upstream_ref: str
    upstream_relation: str
    upstream_ahead: str
    upstream_behind: str
    current_snapshot_candidate_id: str
    matching_snapshot_id: str
    remote_refresh_note: str


@dataclass(frozen=True)
class ContextView:
    context_id: str
    query: str
    canonical_query: str
    match_status: str
    seed_count: int
    selected_files: list[dict[str, Any]]
    selected_symbols: list[dict[str, Any]]
    relationships: list[dict[str, Any]]
    tests: list[dict[str, Any]]
    limitations: list[dict[str, Any]]
    parse_limitations: list[dict[str, Any]]
    selection_metadata: dict[str, Any]


@dataclass(frozen=True)
class SnapshotSummary:
    snapshot_id: str
    head_commit: str
    branch: str
    working_tree_clean: bool
    current_state_match: bool


@dataclass(frozen=True)
class ComparisonSummary:
    comparison_id: str
    before_snapshot_id: str
    after_snapshot_id: str
    aggregate_counts: dict[str, Any]


@dataclass(frozen=True)
class AnalysisSummary:
    analysis_id: str
    comparison_id: str
    model_name: str
    provider: str
    summary: str
    summary_evidence_ids: list[str]
    review_signals: list[dict[str, Any]]
    questions_for_human_review: list[dict[str, Any]]


@dataclass(frozen=True)
class WorkflowArtifactSummary:
    artifact_id: str
    kind: str
    branch: str
    head: str
    count: int
    compatibility: str
    execution_id: str | None


def _sorted_ids(path: Path) -> list[str]:
    if not path.exists() or not path.is_dir():
        return []
    ids = [child.name for child in path.iterdir() if child.is_dir()]
    return sorted(ids, key=lambda item: item.encode("utf-8"))


def load_context_payload(contexts_root: Path, context_id: str) -> dict[str, Any]:
    context_path = contexts_root / context_id / "context.json"
    return json.loads(context_path.read_text(encoding="utf-8"))


def load_dashboard_view(status_payload: dict[str, Any], repository_root: Path) -> DashboardView:
    branch = status_payload["branch"]["name"] if status_payload["branch"]["state"] == "attached" else "(detached)"
    upstream = status_payload["upstream"]
    operations = status_payload["git_operations"]

    return DashboardView(
        repository_name=repository_root.name,
        repository_root=str(repository_root),
        branch=branch,
        head=status_payload["head"],
        workflow_state=status_payload["workflow_state"],
        staged_count=status_payload["working_tree"]["staged"]["count"],
        unstaged_count=status_payload["working_tree"]["unstaged"]["count"],
        untracked_count=status_payload["working_tree"]["untracked"]["count"],
        unmerged_count=status_payload["working_tree"]["unmerged"]["count"],
        git_operation=", ".join(operations) if operations else "None",
        upstream_ref=upstream["ref"] or "not configured",
        upstream_relation=upstream["relation"] or "unavailable",
        upstream_ahead=str(upstream["ahead"]) if upstream["ahead"] is not None else "unavailable",
        upstream_behind=str(upstream["behind"]) if upstream["behind"] is not None else "unavailable",
        current_snapshot_candidate_id=status_payload["current_snapshot_id_candidate"],
        matching_snapshot_id=status_payload["matching_snapshot_id"] or "none",
        remote_refresh_note="No remote refresh was performed.",
    )


def load_context_view(context_payload: dict[str, Any]) -> ContextView:
    return ContextView(
        context_id=context_payload["context_id"],
        query=context_payload["original_query"],
        canonical_query=context_payload["canonical_query"],
        match_status=context_payload["match_status"],
        seed_count=len(context_payload.get("seed_matches", [])),
        selected_files=context_payload.get("selected_files", []),
        selected_symbols=context_payload.get("selected_symbols", []),
        relationships=context_payload.get("relevant_internal_relationships", []),
        tests=context_payload.get("relevant_tests", []),
        limitations=context_payload.get("relevant_limitations", []),
        parse_limitations=context_payload.get("parse_limitations", []),
        selection_metadata=context_payload.get("selection_metadata", {}),
    )


def list_snapshots(snapshots_root: Path, repository_id: str, current_snapshot_candidate_id: str) -> list[SnapshotSummary]:
    rows: list[SnapshotSummary] = []
    for snapshot_id in _sorted_ids(snapshots_root):
        snapshot_dir = snapshots_root / snapshot_id
        snapshot_payload = _verify_existing_snapshot(snapshot_dir, repository_id)
        branch = snapshot_payload["branch"]["name"] if snapshot_payload["branch"]["state"] == "attached" else "(detached)"
        rows.append(
            SnapshotSummary(
                snapshot_id=snapshot_id,
                head_commit=snapshot_payload["head_commit"],
                branch=branch,
                working_tree_clean=bool(snapshot_payload["working_tree_clean"]),
                current_state_match=snapshot_id == current_snapshot_candidate_id,
            )
        )
    return rows


def list_comparisons(comparisons_root: Path, repository_id: str) -> list[ComparisonSummary]:
    rows: list[ComparisonSummary] = []
    for comparison_id in _sorted_ids(comparisons_root):
        comparison_dir = comparisons_root / comparison_id
        comparison_payload, _md = _verify_existing_comparison(comparison_dir)
        if comparison_payload.get("repository_id") != repository_id:
            continue
        rows.append(
            ComparisonSummary(
                comparison_id=comparison_id,
                before_snapshot_id=comparison_payload["before_snapshot_id"],
                after_snapshot_id=comparison_payload["after_snapshot_id"],
                aggregate_counts=comparison_payload.get("aggregate_counts", {}),
            )
        )
    return rows


def load_comparison_payload(comparisons_root: Path, comparison_id: str) -> dict[str, Any]:
    comparison_dir = comparisons_root / comparison_id
    payload, _md = _verify_existing_comparison(comparison_dir)
    return payload


def list_analyses(analyses_root: Path, comparison_id: str) -> list[AnalysisSummary]:
    target_root = analyses_root / comparison_id
    rows: list[AnalysisSummary] = []
    for analysis_id in _sorted_ids(target_root):
        analysis_dir = target_root / analysis_id
        _analysis_input, analysis_json, _analysis_md = _verify_existing_analysis(analysis_dir)
        output = analysis_json["validated_model_output"]
        rows.append(
            AnalysisSummary(
                analysis_id=analysis_id,
                comparison_id=comparison_id,
                model_name=analysis_json["model_name"],
                provider=analysis_json["provider"],
                summary=output["summary"],
                summary_evidence_ids=output["summary_evidence_ids"],
                review_signals=output["review_signals"],
                questions_for_human_review=output["questions_for_human_review"],
            )
        )
    return rows


def load_analysis_summary(analyses_root: Path, comparison_id: str, analysis_id: str) -> AnalysisSummary:
    analysis_dir = analyses_root / comparison_id / analysis_id
    _analysis_input, analysis_json, _analysis_md = _verify_existing_analysis(analysis_dir)
    output = analysis_json["validated_model_output"]
    return AnalysisSummary(
        analysis_id=analysis_id,
        comparison_id=comparison_id,
        model_name=analysis_json["model_name"],
        provider=analysis_json["provider"],
        summary=output["summary"],
        summary_evidence_ids=output["summary_evidence_ids"],
        review_signals=output["review_signals"],
        questions_for_human_review=output["questions_for_human_review"],
    )


def list_context_ids(contexts_root: Path) -> list[str]:
    return _sorted_ids(contexts_root)


def snapshot_id_choices(snapshots_root: Path) -> list[str]:
    return _sorted_ids(snapshots_root)


def comparison_id_choices(comparisons_root: Path) -> list[str]:
    return _sorted_ids(comparisons_root)


def summarize_workflow_artifacts(workflow_root: Path, git_state: dict[str, Any]) -> list[WorkflowArtifactSummary]:
    rows: list[WorkflowArtifactSummary] = []
    branch_name = git_state["branch"]["name"] if git_state["branch"]["state"] == "attached" else "(detached)"
    head = git_state["head"]

    stage_executions_by_plan: dict[str, str] = {}
    stage_exec_root = workflow_root / "stage_executions"
    for execution_id in _sorted_ids(stage_exec_root):
        payload = json.loads((stage_exec_root / execution_id / "execution.json").read_text(encoding="utf-8"))
        stage_executions_by_plan[payload.get("plan_id", "")] = execution_id

    commit_executions_by_plan: dict[str, str] = {}
    commit_exec_root = workflow_root / "commit_executions"
    for execution_id in _sorted_ids(commit_exec_root):
        payload = json.loads((commit_exec_root / execution_id / "execution.json").read_text(encoding="utf-8"))
        commit_executions_by_plan[payload.get("plan_id", "")] = execution_id

    stage_plan_root = workflow_root / "stage_plans"
    for plan_id in _sorted_ids(stage_plan_root):
        payload = json.loads((stage_plan_root / plan_id / "plan.json").read_text(encoding="utf-8"))
        compatible = "compatible" if payload.get("head") == head and payload.get("branch", {}).get("name") == branch_name else "incompatible"
        rows.append(
            WorkflowArtifactSummary(
                artifact_id=plan_id,
                kind="stage_plan",
                branch=payload.get("branch", {}).get("name") or "(detached)",
                head=payload.get("head") or "unknown",
                count=int(payload.get("candidate_record_count", 0)),
                compatibility=compatible,
                execution_id=stage_executions_by_plan.get(plan_id),
            )
        )

    commit_plan_root = workflow_root / "commit_plans"
    for plan_id in _sorted_ids(commit_plan_root):
        payload = json.loads((commit_plan_root / plan_id / "plan.json").read_text(encoding="utf-8"))
        compatible = "compatible" if payload.get("head_before") == head and payload.get("branch", {}).get("name") == branch_name else "incompatible"
        rows.append(
            WorkflowArtifactSummary(
                artifact_id=plan_id,
                kind="commit_plan",
                branch=payload.get("branch", {}).get("name") or "(detached)",
                head=payload.get("head_before") or "unknown",
                count=int(payload.get("staged_record_count", 0)),
                compatibility=compatible,
                execution_id=commit_executions_by_plan.get(plan_id),
            )
        )

    return sorted(rows, key=lambda row: (row.kind, row.artifact_id.encode("utf-8")))


def relation_reason(rel: dict[str, Any]) -> str:
    if rel["relationship_type"] == "test_reference":
        return "related test"
    if rel["relationship_type"] == "module_dependency":
        return "direct relationship"
    if rel["relationship_type"] == "imported_symbol":
        return "direct relationship"
    if rel["relationship_type"] == "call":
        return "direct relationship"
    return "relationship"


def file_reason(file_row: dict[str, Any]) -> str:
    reasons = file_row.get("reasons", [])
    if not reasons:
        return "selected by deterministic policy"
    reason_text = reasons[0]
    if "exact" in reason_text or "substring" in reason_text or "token" in reason_text:
        return "lexical match"
    return reason_text


def match_label(match_status: str) -> str:
    return "MATCHED" if match_status == MATCH_STATUS_MATCHED else "NO MATCHES"
