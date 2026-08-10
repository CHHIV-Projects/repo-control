from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .analysis.manager import AnalysisError, analyze_comparison
from .compare.manager import compare_snapshots
from .context.generator import build_and_publish_context
from .scanner.core import run_scan, run_scan_with_artifacts
from .scanner.git_ops import ScanError
from .snapshot.manager import create_snapshot
from .workflow.status import WorkflowError, generate_milestone_status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="repoctl", description="Repo Control Plane CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Run deterministic repository scan")
    scan_parser.add_argument("repository", help="Path to target Git repository")

    context_parser = subparsers.add_parser("context", help="Generate deterministic context pack")
    context_parser.add_argument("query", help="Navigation query text")
    context_parser.add_argument("--repository", help="Path inside target Git repository")

    snapshot_parser = subparsers.add_parser("snapshot", help="Capture immutable deterministic snapshot")
    snapshot_parser.add_argument("--repository", help="Path inside target Git repository")

    compare_parser = subparsers.add_parser("compare", help="Compare two immutable snapshots")
    compare_parser.add_argument("before_snapshot_id", help="Before snapshot identifier")
    compare_parser.add_argument("after_snapshot_id", help="After snapshot identifier")
    compare_parser.add_argument("--repository", help="Path inside target Git repository")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze one immutable comparison with local GPT-OSS")
    analyze_parser.add_argument("comparison_id", help="Comparison identifier")
    analyze_parser.add_argument("--repository", help="Path inside target Git repository")

    milestone_parser = subparsers.add_parser("milestone", help="Milestone workflow commands")
    milestone_subparsers = milestone_parser.add_subparsers(dest="milestone_command", required=True)
    milestone_status_parser = milestone_subparsers.add_parser("status", help="Report deterministic read-only Git workflow state")
    milestone_status_parser.add_argument("--repository", help="Path inside target Git repository")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        try:
            result = run_scan(args.repository)
        except ScanError as exc:
            print(f"scan failed: {exc}", file=sys.stderr)
            return 2
        except Exception as exc:
            print(f"scan failed: {exc}", file=sys.stderr)
            return 1

        branch_text = result["branch"]["name"] if result["branch"]["state"] == "attached" else "detached"
        print("scan complete")
        print(f"target: {result['repository_root']}")
        print(f"repository_id: {result['repository_id']}")
        print(f"branch: {branch_text}")
        print(f"head: {result['head_commit']}")
        print(f"output: {result['output_dir']}")
        print(f"parse_errors: {result['parse_error_count']}")
        return 0

    if args.command == "context":
        repository_path = args.repository if args.repository else str(Path.cwd())
        try:
            scan_result = run_scan_with_artifacts(repository_path)
            context_result = build_and_publish_context(scan_result=scan_result, query=args.query)
        except ValueError as exc:
            print(f"context failed: {exc}", file=sys.stderr)
            return 2
        except ScanError as exc:
            print(f"context failed: {exc}", file=sys.stderr)
            return 2
        except Exception as exc:
            print(f"context failed: {exc}", file=sys.stderr)
            return 1

        print("context complete")
        print(f"target: {context_result['repository_root']}")
        print(f"repository_id: {context_result['repository_id']}")
        print(f"context_id: {context_result['context_id']}")
        print(f"output: {context_result['context_dir']}")
        print(f"match_status: {context_result['match_status']}")
        print(f"seed_count: {context_result['seed_count']}")
        print(f"selected_file_count: {context_result['selected_file_count']}")
        print(f"selected_symbol_count: {context_result['selected_symbol_count']}")
        print(f"selected_relationship_count: {context_result['selected_relationship_count']}")
        print(f"selected_test_reference_count: {context_result['selected_test_reference_count']}")
        return 0

    if args.command == "snapshot":
        repository_path = args.repository if args.repository else str(Path.cwd())
        try:
            scan_result = run_scan_with_artifacts(repository_path)
            snapshot_result = create_snapshot(scan_result=scan_result)
        except ScanError as exc:
            print(f"snapshot failed: {exc}", file=sys.stderr)
            return 2
        except Exception as exc:
            print(f"snapshot failed: {exc}", file=sys.stderr)
            return 1

        print("snapshot complete")
        print(f"target: {snapshot_result['repository_root']}")
        print(f"repository_id: {snapshot_result['repository_id']}")
        print(f"snapshot_id: {snapshot_result['snapshot_id']}")
        print(f"output: {snapshot_result['snapshot_dir']}")
        print(f"reused_existing: {snapshot_result['reused_existing']}")
        return 0

    if args.command == "compare":
        repository_path = args.repository if args.repository else str(Path.cwd())
        try:
            compare_result = compare_snapshots(args.before_snapshot_id, args.after_snapshot_id, repository_path)
        except ScanError as exc:
            print(f"compare failed: {exc}", file=sys.stderr)
            return 2
        except Exception as exc:
            print(f"compare failed: {exc}", file=sys.stderr)
            return 1

        print("compare complete")
        print(f"target: {compare_result['repository_root']}")
        print(f"repository_id: {compare_result['repository_id']}")
        print(f"comparison_id: {compare_result['comparison_id']}")
        print(f"output: {compare_result['comparison_dir']}")
        print(f"reused_existing: {compare_result['reused_existing']}")
        return 0

    if args.command == "analyze":
        repository_path = args.repository if args.repository else str(Path.cwd())
        try:
            analysis_result = analyze_comparison(args.comparison_id, repository_path)
        except AnalysisError as exc:
            msg = str(exc)
            if msg.startswith("provider error ["):
                print(msg, file=sys.stderr)
            else:
                print(f"analyze failed: {msg}", file=sys.stderr)
            return 2
        except ScanError as exc:
            print(f"analyze failed: {exc}", file=sys.stderr)
            return 2
        except Exception as exc:
            print(f"analyze failed: {exc}", file=sys.stderr)
            return 1

        print("analyze complete")
        print(f"target: {analysis_result['repository_root']}")
        print(f"repository_id: {analysis_result['repository_id']}")
        print(f"comparison_id: {analysis_result['comparison_id']}")
        print(f"packet_id: {analysis_result['packet_id']}")
        print(f"request_id: {analysis_result['request_id']}")
        print(f"analysis_id: {analysis_result['analysis_id']}")
        print(f"provider: {analysis_result['provider']}")
        print(f"model_name: {analysis_result['model_name']}")
        print(f"model_digest: {analysis_result['model_digest']}")
        print(f"output: {analysis_result['analysis_dir']}")
        print(f"reused_existing: {analysis_result['reused_existing']}")
        return 0

    if args.command == "milestone" and args.milestone_command == "status":
        repository_path = args.repository if args.repository else str(Path.cwd())
        try:
            status_result = generate_milestone_status(repository_path)
        except WorkflowError as exc:
            print(f"milestone status failed: {exc}", file=sys.stderr)
            return 2
        except ScanError as exc:
            print(f"milestone status failed: {exc}", file=sys.stderr)
            return 2
        except Exception as exc:
            print(f"milestone status failed: {exc}", file=sys.stderr)
            return 1

        branch_text = (
            status_result["branch"]["name"]
            if status_result["branch"]["state"] == "attached"
            else "(detached)"
        )
        upstream_ref = status_result["upstream"]["ref"] if status_result["upstream"]["ref"] else "none"
        relation = status_result["upstream"]["relation"] if status_result["upstream"]["relation"] else "unavailable"
        ahead = status_result["upstream"]["ahead"] if status_result["upstream"]["ahead"] is not None else "unavailable"
        behind = status_result["upstream"]["behind"] if status_result["upstream"]["behind"] is not None else "unavailable"
        operations = ", ".join(status_result["git_operations"]) if status_result["git_operations"] else "none"
        matching_snapshot = status_result["matching_snapshot_id"] if status_result["matching_snapshot_id"] else "none"

        print("milestone status complete")
        print(f"Repository: {status_result['repository_root']}")
        print(f"Branch: {branch_text}")
        print(f"HEAD: {status_result['head']}")
        print(f"Workflow state: {status_result['workflow_state']}")
        print(f"Staged: {status_result['working_tree']['staged']['count']}")
        print(f"Unstaged: {status_result['working_tree']['unstaged']['count']}")
        print(f"Untracked: {status_result['working_tree']['untracked']['count']}")
        print(f"Unmerged: {status_result['working_tree']['unmerged']['count']}")
        print(f"Upstream: {upstream_ref}")
        print(f"Local upstream relation: {relation}")
        print(f"Ahead: {ahead}")
        print(f"Behind: {behind}")
        print("Remote refresh: not performed")
        print(f"Git operation: {operations}")
        print(f"Matching snapshot: {matching_snapshot}")
        print(f"status_json: {status_result['status_json']}")
        print(f"status_md: {status_result['status_md']}")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
