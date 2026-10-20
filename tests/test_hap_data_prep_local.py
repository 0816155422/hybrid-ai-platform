import hashlib
import tempfile
import unittest
from pathlib import Path

from hap_data_prep import CollectionBlocked, collect_local_file
from hap_data_prep.local_files import normalize_structured_artifact


class LocalCollectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "source.md").write_bytes(b"# original\n")

    def tearDown(self):
        self.temp.cleanup()

    def collect(self, **overrides):
        args = {
            "root": self.root,
            "relative_path": "source.md",
            "allowed_paths": {"source.md"},
            "authorization_ref": "AUTH-REF-REVIEWED-BY-CALLER",
        }
        args.update(overrides)
        return collect_local_file(**args)

    def test_exact_bytes_and_digest(self):
        result = self.collect()
        self.assertEqual(result.content, b"# original\n")
        self.assertEqual(result.envelope["sha256"], hashlib.sha256(result.content).hexdigest())
        self.assertEqual(result.envelope["collection_status"], "COLLECTED_UNVERIFIED")

    def test_missing_authorization_blocks(self):
        with self.assertRaises(CollectionBlocked):
            self.collect(authorization_ref="")

    def test_allowlist_blocks_other_path(self):
        with self.assertRaises(CollectionBlocked):
            self.collect(allowed_paths={"other.md"})

    def test_traversal_blocks(self):
        with self.assertRaises(CollectionBlocked):
            self.collect(relative_path="../outside.md", allowed_paths={"../outside.md"})

    def test_phase_one_blocks(self):
        with self.assertRaises(CollectionBlocked):
            self.collect(phase="PHASE_1")

    def test_size_limit_blocks(self):
        with self.assertRaises(CollectionBlocked):
            self.collect(max_bytes=2)

    def test_json_normalization_preserves_raw_artifact(self):
        (self.root / "records.json").write_text('{"b":2,"a":1}', encoding="utf-8")
        raw = self.collect(relative_path="records.json", allowed_paths={"records.json"})
        before = raw.content
        derivative, normalized = normalize_structured_artifact(raw)
        self.assertEqual(raw.content, before)
        self.assertEqual(normalized, b'{"a":1,"b":2}\\n')
        self.assertEqual(derivative["derived_from"], [raw.envelope["artifact_id"]])
        self.assertEqual(derivative["status"], "DERIVED_UNVERIFIED")

    def test_csv_normalization(self):
        (self.root / "records.csv").write_text("id,name\\n1,Ada\\n2,Lin\\n", encoding="utf-8")
        raw = self.collect(relative_path="records.csv", allowed_paths={"records.csv"})
        derivative, normalized = normalize_structured_artifact(raw)
        self.assertEqual(normalized, b'[{"id":"1","name":"Ada"},{"id":"2","name":"Lin"}]\\n')
        self.assertEqual(derivative["input_media_type"], "text/csv")

    def test_malformed_json_blocks_normalization(self):
        (self.root / "broken.json").write_text("{bad json", encoding="utf-8")
        raw = self.collect(relative_path="broken.json", allowed_paths={"broken.json"})
        with self.assertRaisesRegex(CollectionBlocked, "invalid JSON source"):
            normalize_structured_artifact(raw)

    def test_does_not_create_files(self):
        before = {p.name for p in self.root.iterdir()}
        self.collect()
        self.assertEqual(before, {p.name for p in self.root.iterdir()})


if __name__ == "__main__":
    unittest.main()
