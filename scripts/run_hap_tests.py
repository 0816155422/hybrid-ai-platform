#!/usr/bin/env python3
"""Run the fixed HAP Phase 0 verification commands with bounded execution.

This is a test orchestrator, NOT an operating-system security sandbox. It uses
an allowlist of repository-owned checks, never invokes a shell, and records
exit codes, output, duration, environment metadata, and timeouts. It does not
access a database, deploy software, or contact external services intentionally.
"""
from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TIMEOUT_SECONDS = 120
MAX_TIMEOUT_SECONDS = 600


def build_steps(python_executable: str = sys.executable) -> list[dict[str, Any]]:
    """Return the fixed, allowlisted checks; never accept arbitrary commands."""
    return [
        {
            "name": "evidence_metadata_validation",
            "command": [python_executable, "scripts/validate_evidence.py"],
        },
        {
            "name": "python_unit_tests",
            "command": [
                python_executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "tests",
                "-v",
            ],
        },
    ]


def run_step(step: dict[str, Any], timeout_seconds: int) -> dict[str, Any]:
    started = time.monotonic()
    started_at = datetime.now(timezone.utc).isoformat()
    try:
        completed = subprocess.run(
            step["command"],
            cwd=ROOT,
            shell=False,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return {
            "name": step["name"],
            "command": step["command"],
            "status": "PASS" if completed.returncode == 0 else "FAIL",
            "exit_code": completed.returncode,
            "started_at_utc": started_at,
            "duration_seconds": round(time.monotonic() - started, 3),
            "stdout": completed.stdout,
            "stderr": completed.stderr,
        }
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        return {
            "name": step["name"],
            "command": step["command"],
            "status": "TIMEOUT",
            "exit_code": None,
            "started_at_utc": started_at,
            "duration_seconds": round(time.monotonic() - started, 3),
            "stdout": stdout,
            "stderr": stderr,
            "timeout_seconds": timeout_seconds,
        }
    except OSError as exc:
        return {
            "name": step["name"],
            "command": step["command"],
            "status": "ERROR",
            "exit_code": None,
            "started_at_utc": started_at,
            "duration_seconds": round(time.monotonic() - started, 3),
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Per-check timeout (1-{MAX_TIMEOUT_SECONDS}; default {DEFAULT_TIMEOUT_SECONDS})",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Optional path for a JSON execution report; parent directories are not created",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List the fixed checks without running them",
    )
    args = parser.parse_args(argv)
    if not 1 <= args.timeout_seconds <= MAX_TIMEOUT_SECONDS:
        parser.error(f"--timeout-seconds must be between 1 and {MAX_TIMEOUT_SECONDS}")

    steps = build_steps()
    if args.list:
        for step in steps:
            print(f"{step['name']}: {' '.join(step['command'])}")
        return 0

    report: dict[str, Any] = {
        "project_id": "HAP-2026-OFFLINE-FIRST",
        "runner": "scripts/run_hap_tests.py",
        "runner_type": "fixed_command_test_orchestrator_not_security_sandbox",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "commit_sha": __import__("os").environ.get("GITHUB_SHA", "UNKNOWN"),
        "python_version": sys.version,
        "platform": platform.platform(),
        "timeout_seconds_per_check": args.timeout_seconds,
        "database_write_policy": "ZERO_DATABASE_WRITE",
        "results": [],
    }

    for step in steps:
        print(f"=== START {step['name']} ===", flush=True)
        result = run_step(step, args.timeout_seconds)
        report["results"].append(result)
        print(f"=== {result['status']} {result['name']} (exit={result['exit_code']}) ===")
        if result["stdout"]:
            print(result["stdout"], end="" if result["stdout"].endswith("\n") else "\n")
        if result["stderr"]:
            print(result["stderr"], file=sys.stderr, end="" if result["stderr"].endswith("\n") else "\n")

    failed = [item for item in report["results"] if item["status"] != "PASS"]
    report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    report["overall_status"] = "PASS" if not failed else "FAIL"
    report["passed_checks"] = len(report["results"]) - len(failed)
    report["failed_or_blocked_checks"] = len(failed)

    if args.report:
        try:
            args.report.write_text(
                json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(f"REPORT_WRITTEN {args.report}")
        except OSError as exc:
            print(f"REPORT_WRITE_FAILED {args.report}: {exc}", file=sys.stderr)
            return 2

    print(
        f"RUN_SUMMARY status={report['overall_status']} "
        f"passed={report['passed_checks']} failed_or_blocked={report['failed_or_blocked_checks']}"
    )
    print("NOTE: PASS applies only to these checks in this run; it does not certify installation, isolation, or Phase 0 gate completion.")
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
