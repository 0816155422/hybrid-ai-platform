#!/usr/bin/env python3
"""Validate HAP evidence metadata without accessing networks or modifying data.

This validator checks structure only. It does not verify that a claimed hash
matches source bytes, that a source is authentic, or that a gate should pass.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

PROJECT_ID = "HAP-2026-OFFLINE-FIRST"
ALLOWED_STATUSES = {
    "PASS", "FAIL", "PARTIAL", "UNVERIFIED", "NOT_RUN", "BLOCKED",
    "PENDING_REVIEW", "NOT_APPLICABLE",
}
REQUIRED_REGISTER_COLUMNS = {
    "artifact_id", "project_id", "title", "artifact_type", "origin",
    "original_filename", "version", "observed_at_utc", "byte_size",
    "sha256", "git_blob_sha", "evidence_status", "notes",
}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def validate_register(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or [])
            missing = sorted(REQUIRED_REGISTER_COLUMNS - headers)
            if missing:
                return [f"{path}: missing required columns: {', '.join(missing)}"]
            seen_ids: set[str] = set()
            for line_number, row in enumerate(reader, start=2):
                artifact_id = (row.get("artifact_id") or "").strip()
                if not artifact_id:
                    errors.append(f"{path}:{line_number}: artifact_id is empty")
                elif artifact_id in seen_ids:
                    errors.append(f"{path}:{line_number}: duplicate artifact_id {artifact_id}")
                seen_ids.add(artifact_id)

                project_id = (row.get("project_id") or "").strip()
                if project_id != PROJECT_ID:
                    errors.append(
                        f"{path}:{line_number}: project_id must be {PROJECT_ID}, got {project_id!r}"
                    )

                status = (row.get("evidence_status") or "").strip()
                if status not in ALLOWED_STATUSES:
                    errors.append(
                        f"{path}:{line_number}: unsupported evidence_status {status!r}"
                    )

                digest = (row.get("sha256") or "").strip()
                if digest not in {"", "PENDING", "NOT_COMPUTED", "UNKNOWN"} and not SHA256_RE.fullmatch(digest):
                    errors.append(
                        f"{path}:{line_number}: sha256 must be 64 hex characters or an explicit pending marker"
                    )

                byte_size = (row.get("byte_size") or "").strip()
                if byte_size:
                    try:
                        if int(byte_size) < 0:
                            raise ValueError
                    except ValueError:
                        errors.append(f"{path}:{line_number}: byte_size must be a non-negative integer")
    except OSError as exc:
        errors.append(f"{path}: cannot read register: {exc}")
    except csv.Error as exc:
        errors.append(f"{path}: CSV parse error: {exc}")
    return errors


def validate_manifest(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: cannot read valid JSON manifest: {exc}"]

    if not isinstance(payload, dict):
        return [f"{path}: manifest root must be an object"]
    if payload.get("project_id") != PROJECT_ID:
        errors.append(f"{path}: project_id must be {PROJECT_ID}")
    if payload.get("hash_algorithm") != "SHA-256":
        errors.append(f"{path}: hash_algorithm must be 'SHA-256'")
    entries = payload.get("entries")
    if not isinstance(entries, list):
        errors.append(f"{path}: entries must be a list")
        return errors

    seen_paths: set[str] = set()
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"{path}: entries[{index}] must be an object")
            continue
        artifact_path = str(entry.get("path", "")).strip()
        if not artifact_path:
            errors.append(f"{path}: entries[{index}] has no path")
        elif artifact_path in seen_paths:
            errors.append(f"{path}: duplicate manifest path {artifact_path!r}")
        seen_paths.add(artifact_path)
        digest = str(entry.get("sha256", "")).strip()
        if not SHA256_RE.fullmatch(digest):
            errors.append(f"{path}: entries[{index}].sha256 must be 64 hex characters")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--register", type=Path,
        default=Path("evidence/register/ARTIFACT_REGISTER.csv"),
    )
    parser.add_argument(
        "--manifest", type=Path,
        default=Path("evidence/manifests/SHA256_MANIFEST.json"),
    )
    args = parser.parse_args(argv)

    errors = validate_register(args.register) + validate_manifest(args.manifest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"VALIDATION_FAILED errors={len(errors)}")
        return 1

    print("VALIDATION_OK structure_only=true")
    print("NOTE: This does not recompute hashes or establish source authenticity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
