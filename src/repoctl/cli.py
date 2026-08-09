from __future__ import annotations

import argparse
import sys

from .scanner.core import run_scan
from .scanner.git_ops import ScanError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="repoctl", description="Repo Control Plane CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Run deterministic repository scan")
    scan_parser.add_argument("repository", help="Path to target Git repository")

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

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
