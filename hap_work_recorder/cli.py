#!/usr/bin/env python3
"""Local append-only work-event recorder with a SHA-256 hash chain.

This records only events explicitly submitted to the CLI. It cannot observe
ChatGPT's private reasoning or automatically discover actions performed outside
the instrumented workflow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GENESIS_HASH = "0" * 64
STATUSES = {"COMPLETE", "PARTIAL", "BLOCKED", "FAILED", "UNVERIFIED"}
PREFLIGHT = {"PASS", "BLOCKED", "UNVERIFIED"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def calculate_hash(record_without_hash: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(record_without_hash).encode("utf-8")).hexdigest()


def read_records(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    if not path.exists():
        return records, errors
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, 1):
                if not line.strip():
                    errors.append(f"line {line_no}: blank lines are not allowed")
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append(f"line {line_no}: invalid JSON: {exc}")
                    continue
                if not isinstance(record, dict):
                    errors.append(f"line {line_no}: record must be a JSON object")
                    continue
                records.append(record)
    except OSError as exc:
        errors.append(f"cannot read {path}: {exc}")
    return records, errors


def verify_records(records: list[dict[str, Any]], parse_errors: list[str] | None = None) -> list[str]:
    errors = list(parse_errors or [])
    previous = GENESIS_HASH
    for index, record in enumerate(records, 1):
        stored_hash = record.get("event_hash")
        if not isinstance(stored_hash, str):
            errors.append(f"record {index}: event_hash missing")
            continue
        if record.get("previous_hash") != previous:
            errors.append(f"record {index}: previous_hash mismatch")
        unhashed = {key: value for key, value in record.items() if key != "event_hash"}
        expected = calculate_hash(unhashed)
        if stored_hash != expected:
            errors.append(f"record {index}: event_hash mismatch")
        previous = stored_hash
    return errors


def append_event(path: Path, event_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing, parse_errors = read_records(path)
    verification_errors = verify_records(existing, parse_errors)
    if verification_errors:
        raise ValueError("ledger verification failed; refusing to append: " + "; ".join(verification_errors))
    previous_hash = existing[-1]["event_hash"] if existing else GENESIS_HASH
    record: dict[str, Any] = {
        "schema_version": "1.0",
        "event_id": str(uuid.uuid4()),
        "timestamp_utc": utc_now(),
        "project_id": "HAP-2026-OFFLINE-FIRST",
        "event_type": event_type,
        "previous_hash": previous_hash,
        "payload": payload,
    }
    record["event_hash"] = calculate_hash(record)
    # Append only; never truncate or rewrite an existing ledger.
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(canonical_json(record) + "\n")
        handle.flush()
    return record


def command_start(args: argparse.Namespace) -> int:
    if args.preflight != "PASS":
        print("BLOCKED: only --preflight PASS may start substantive work.", file=sys.stderr)
        return 2
    if not args.task.strip() or not args.scope.strip():
        print("BLOCKED: --task and --scope are required.", file=sys.stderr)
        return 2
    record = append_event(args.log, "WORK_STARTED", {
        "run_id": str(uuid.uuid4()),
        "task": args.task.strip(),
        "scope": args.scope.strip(),
        "preflight_decision": args.preflight,
        "acceptance_criteria": args.acceptance or "",
        "baseline": args.baseline or "UNRECORDED",
    })
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def command_event(args: argparse.Namespace) -> int:
    if not args.event_type.strip() or not args.summary.strip():
        print("BLOCKED: --type and --summary are required.", file=sys.stderr)
        return 2
    record = append_event(args.log, "OBSERVED_EVENT", {
        "event_type": args.event_type.strip(),
        "summary": args.summary.strip(),
        "source": args.source or "USER_OR_OPERATOR_REPORTED",
        "evidence_ref": args.evidence_ref or "NONE",
        "result": args.result or "UNVERIFIED",
    })
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def command_end(args: argparse.Namespace) -> int:
    if args.status not in STATUSES:
        print("BLOCKED: unsupported closeout status.", file=sys.stderr)
        return 2
    if args.status in {"PARTIAL", "BLOCKED", "FAILED", "UNVERIFIED"} and not args.reason.strip():
        print("BLOCKED: --reason is required for incomplete/unverified work.", file=sys.stderr)
        return 2
    record = append_event(args.log, "WORK_CLOSED", {
        "status": args.status,
        "summary": args.summary.strip(),
        "reason_unfinished_or_blocked": args.reason.strip() if args.reason else "",
        "evidence_refs": args.evidence_ref or [],
        "next_steps": args.next_step or [],
        "independent_review": args.independent_review or "NOT_PERFORMED",
    })
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def command_verify(args: argparse.Namespace) -> int:
    records, parse_errors = read_records(args.log)
    errors = verify_records(records, parse_errors)
    result = {
        "ledger": str(args.log),
        "records_checked": len(records),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "note": "Hash-chain integrity only; not proof of source authenticity or completeness.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=Path("evidence/work-log/events.jsonl"),
                        help="JSONL ledger path (default: evidence/work-log/events.jsonl)")
    sub = parser.add_subparsers(dest="command", required=True)

    start = sub.add_parser("start", help="Record a preflight decision and start a task")
    start.add_argument("--task", required=True)
    start.add_argument("--scope", required=True)
    start.add_argument("--preflight", choices=sorted(PREFLIGHT), required=True)
    start.add_argument("--acceptance")
    start.add_argument("--baseline")
    start.set_defaults(func=command_start)

    event = sub.add_parser("event", help="Append an explicitly observed/reported event")
    event.add_argument("--type", dest="event_type", required=True)
    event.add_argument("--summary", required=True)
    event.add_argument("--source", help="e.g. github_readback, test_runner, operator")
    event.add_argument("--evidence-ref")
    event.add_argument("--result", choices=["PASS", "FAIL", "PARTIAL", "BLOCKED", "UNVERIFIED", "NOT_RUN"],
                       default="UNVERIFIED")
    event.set_defaults(func=command_event)

    end = sub.add_parser("end", help="Record postflight closeout")
    end.add_argument("--status", choices=sorted(STATUSES), required=True)
    end.add_argument("--summary", required=True)
    end.add_argument("--reason", default="")
    end.add_argument("--evidence-ref", action="append")
    end.add_argument("--next-step", action="append")
    end.add_argument("--independent-review", default="NOT_PERFORMED")
    end.set_defaults(func=command_end)

    verify = sub.add_parser("verify", help="Verify JSONL parseability and hash chain")
    verify.set_defaults(func=command_verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
