"""Bounded read-only local file collector.

This module reads only a caller-allowlisted file under an explicit root. It does
not write files, access a network, access a database, execute source content,
or approve evidence. The returned bytes are held in memory for the caller.
"""
from __future__ import annotations

import hashlib
import mimetypes
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

PROJECT_ID = "HAP-2026-OFFLINE-FIRST"
ALLOWED_PHASE = "PHASE_0_DOCUMENTATION_AND_GOVERNANCE_REVIEW"


class CollectionBlocked(ValueError):
    """Collection precondition or source-scope check failed."""


@dataclass(frozen=True)
class CollectedArtifact:
    envelope: dict[str, Any]
    content: bytes


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_relative_path(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CollectionBlocked("source path is required")
    if "\x00" in value:
        raise CollectionBlocked("NUL byte in source path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise CollectionBlocked("source path must be a normalized relative path without traversal")
    # Require POSIX-style paths in the cross-platform contract.
    if "\\" in value:
        raise CollectionBlocked("backslashes are not accepted in the portable source path")
    return path.as_posix()


def collect_local_file(
    *,
    root: str | Path,
    relative_path: str,
    allowed_paths: set[str] | frozenset[str],
    authorization_ref: str,
    phase: str = ALLOWED_PHASE,
    project_id: str = PROJECT_ID,
    max_bytes: int = 10_000_000,
) -> CollectedArtifact:
    """Read one explicitly allowlisted local file and return bytes plus metadata.

    Authorization is represented by a required reference string; this prototype
    does not independently validate the referenced approval record. Callers must
    verify that reference before invoking this function.
    """
    if project_id != PROJECT_ID:
        raise CollectionBlocked("project_id does not match the configured HAP project")
    if phase != ALLOWED_PHASE:
        raise CollectionBlocked("this prototype permits Phase 0 collection only")
    if not isinstance(authorization_ref, str) or not authorization_ref.strip():
        raise CollectionBlocked("authorization_ref is required; no source read attempted")
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or max_bytes < 1:
        raise CollectionBlocked("max_bytes must be a positive integer")

    requested = _normalize_relative_path(relative_path)
    allowlist = {_normalize_relative_path(item) for item in allowed_paths}
    if requested not in allowlist:
        raise CollectionBlocked("source path is not in the caller-provided allowlist")

    root_path = Path(root).resolve(strict=True)
    candidate = root_path / requested

    # Reject symlinks in every component, even if the resolved target remains
    # inside root; this avoids ambiguous source identity through path aliases.
    current = root_path
    for part in PurePosixPath(requested).parts:
        current = current / part
        if current.is_symlink():
            raise CollectionBlocked("symlink paths are not accepted by this prototype")

    resolved = candidate.resolve(strict=True)
    try:
        resolved.relative_to(root_path)
    except ValueError as exc:
        raise CollectionBlocked("resolved source path escapes the approved root") from exc

    if not resolved.is_file():
        raise CollectionBlocked("source must be a regular file")
    size_before = resolved.stat().st_size
    if size_before > max_bytes:
        raise CollectionBlocked(f"source exceeds max_bytes ({size_before} > {max_bytes})")

    with resolved.open("rb") as handle:
        content = handle.read(max_bytes + 1)
    if len(content) > max_bytes:
        raise CollectionBlocked("source grew beyond max_bytes while being read")
    if len(content) != size_before:
        raise CollectionBlocked("source size changed during collection; retry after revalidation")

    digest = hashlib.sha256(content).hexdigest()
    media_type, _ = mimetypes.guess_type(resolved.name)
    envelope: dict[str, Any] = {
        "schema_version": "0.1.0",
        "artifact_id": f"RAW-{uuid.uuid4()}",
        "project_id": PROJECT_ID,
        "phase": phase,
        "source_locator": requested,
        "source_version": "UNKNOWN",
        "captured_at_utc": _utc_now(),
        "original_filename": resolved.name,
        "media_type": media_type or "application/octet-stream",
        "byte_size": len(content),
        "hash_algorithm": "SHA-256",
        "sha256": digest,
        "authorization_ref": authorization_ref.strip(),
        "collection_status": "COLLECTED_UNVERIFIED",
        "transformation_status": "NONE",
        "derived_from": [],
        "limitations": [
            "Local filesystem metadata and allowlist are caller supplied.",
            "authorization_ref is required but not resolved by this prototype.",
            "SHA-256 identifies these bytes but does not prove source authenticity.",
            "No staging copy, independent verification, parsing, cloud transfer, or database write was performed.",
        ],
    }
    return CollectedArtifact(envelope=envelope, content=content)
