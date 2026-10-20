"""Independent, read-only integrity checks for HAP data preparation artifacts.

This module does not trust the collector's status field. It recomputes digests
from supplied bytes and validates a small set of envelope invariants. It is not
a full JSON Schema validator or source-authenticity verifier.
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_REQUIRED_RAW = {
    "schema_version", "artifact_id", "project_id", "phase", "source_locator",
    "captured_at_utc", "byte_size", "hash_algorithm", "sha256",
    "collection_status", "transformation_status", "derived_from",
}


def verify_raw_artifact(envelope: dict[str, Any], content: bytes) -> dict[str, Any]:
    errors: list[str] = []
    missing = sorted(_REQUIRED_RAW - set(envelope))
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
    actual_hash = hashlib.sha256(content).hexdigest()
    if envelope.get("project_id") != "HAP-2026-OFFLINE-FIRST":
        errors.append("project_id mismatch")
    if envelope.get("phase") != "PHASE_0_DOCUMENTATION_AND_GOVERNANCE_REVIEW":
        errors.append("phase is not the authorized Phase 0 label")
    if envelope.get("schema_version") != "0.1.0":
        errors.append("unsupported schema_version")
    if envelope.get("hash_algorithm") != "SHA-256":
        errors.append("hash_algorithm must be SHA-256")
    claimed_hash = envelope.get("sha256")
    if not isinstance(claimed_hash, str) or not _SHA256.fullmatch(claimed_hash):
        errors.append("sha256 must be 64 lowercase hexadecimal characters")
    elif claimed_hash != actual_hash:
        errors.append("raw content SHA-256 mismatch")
    if envelope.get("byte_size") != len(content):
        errors.append("raw content byte_size mismatch")
    if envelope.get("collection_status") != "COLLECTED_UNVERIFIED":
        errors.append("raw collection status must remain COLLECTED_UNVERIFIED")
    if envelope.get("transformation_status") != "NONE":
        errors.append("raw artifact must not be marked transformed")
    if not isinstance(envelope.get("derived_from"), list):
        errors.append("derived_from must be a list")
    return {
        "verification_type": "RAW_ARTIFACT_INTEGRITY",
        "status": "PASS" if not errors else "FAIL",
        "checks": ["required_fields", "project_phase", "schema_version", "exact_bytes_sha256", "byte_size", "raw_status"],
        "errors": errors,
        "source_authenticity": "NOT_ESTABLISHED",
        "approval": "NOT_GRANTED",
    }


def verify_derivative(
    raw_envelope: dict[str, Any],
    derivative_envelope: dict[str, Any],
    derivative_bytes: bytes,
) -> dict[str, Any]:
    errors: list[str] = []
    actual_hash = hashlib.sha256(derivative_bytes).hexdigest()
    claimed_hash = derivative_envelope.get("sha256")
    if derivative_envelope.get("source_artifact_id") != raw_envelope.get("artifact_id"):
        errors.append("source_artifact_id does not match raw artifact")
    if derivative_envelope.get("derived_from") != [raw_envelope.get("artifact_id")]:
        errors.append("derived_from must link directly to the raw artifact")
    if derivative_envelope.get("project_id") != raw_envelope.get("project_id"):
        errors.append("project_id mismatch between raw and derivative")
    if derivative_envelope.get("hash_algorithm") != "SHA-256":
        errors.append("derivative hash_algorithm must be SHA-256")
    if not isinstance(claimed_hash, str) or not _SHA256.fullmatch(claimed_hash):
        errors.append("derivative sha256 must be 64 lowercase hexadecimal characters")
    elif claimed_hash != actual_hash:
        errors.append("derivative content SHA-256 mismatch")
    if derivative_envelope.get("byte_size") != len(derivative_bytes):
        errors.append("derivative byte_size mismatch")
    if derivative_envelope.get("status") != "DERIVED_UNVERIFIED":
        errors.append("derivative status must remain DERIVED_UNVERIFIED")
    return {
        "verification_type": "DERIVATIVE_INTEGRITY_AND_LINEAGE",
        "status": "PASS" if not errors else "FAIL",
        "checks": ["parent_link", "project_id", "exact_bytes_sha256", "byte_size", "derived_status"],
        "errors": errors,
        "semantic_correctness": "NOT_ESTABLISHED",
        "approval": "NOT_GRANTED",
    }
