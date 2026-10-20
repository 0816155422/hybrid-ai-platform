"""Unit tests for the dependency-free HAP evidence metadata validator."""
from __future__ import annotations

import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_evidence import PROJECT_ID, validate_manifest, validate_register


class EvidenceValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_register(self, rows: list[dict[str, str]]) -> Path:
        path = self.root / "register.csv"
        fields = [
            "artifact_id", "project_id", "title", "artifact_type", "origin",
            "original_filename", "version", "observed_at_utc", "byte_size",
            "sha256", "git_blob_sha", "evidence_status", "notes",
        ]
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        return path

    def valid_row(self, artifact_id: str = "ART-0001") -> dict[str, str]:
        return {
            "artifact_id": artifact_id,
            "project_id": PROJECT_ID,
            "title": "Example",
            "artifact_type": "documentation",
            "origin": "docs/example.md",
            "original_filename": "example.md",
            "version": "UNKNOWN",
            "observed_at_utc": "",
            "byte_size": "",
            "sha256": "PENDING",
            "git_blob_sha": "",
            "evidence_status": "UNVERIFIED",
            "notes": "Not yet hashed",
        }

    def write_manifest(self, entries: list[dict] | None = None) -> Path:
        path = self.root / "manifest.json"
        path.write_text(json.dumps({
            "project_id": PROJECT_ID,
            "manifest_version": "0.1.0-draft",
            "status": "TEMPLATE_NOT_COMPLETE",
            "hash_algorithm": "SHA-256",
            "entries": entries or [],
        }), encoding="utf-8")
        return path

    def test_valid_register_allows_pending_hash(self) -> None:
        self.assertEqual(validate_register(self.write_register([self.valid_row()])), [])

    def test_duplicate_artifact_ids_are_rejected(self) -> None:
        errors = validate_register(self.write_register([
            self.valid_row(), self.valid_row(),
        ]))
        self.assertTrue(any("duplicate artifact_id" in error for error in errors))

    def test_invalid_status_is_rejected(self) -> None:
        row = self.valid_row()
        row["evidence_status"] = "DONE"
        errors = validate_register(self.write_register([row]))
        self.assertTrue(any("unsupported evidence_status" in error for error in errors))

    def test_manifest_rejects_invalid_hash(self) -> None:
        errors = validate_manifest(self.write_manifest([
            {"path": "docs/a.md", "sha256": "not-a-hash"},
        ]))
        self.assertTrue(any("64 hex characters" in error for error in errors))

    def test_manifest_accepts_empty_template(self) -> None:
        self.assertEqual(validate_manifest(self.write_manifest()), [])


if __name__ == "__main__":
    unittest.main()
