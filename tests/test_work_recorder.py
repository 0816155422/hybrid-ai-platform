"""Tests for HAP Work Recorder JSONL ledger and fail-closed behavior."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from hap_work_recorder.cli import append_event, read_records, verify_records, main


class WorkRecorderTests(unittest.TestCase):
    def test_append_builds_valid_hash_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            append_event(path, "TEST_A", {"summary": "first"})
            append_event(path, "TEST_B", {"summary": "second"})
            records, parse_errors = read_records(path)
            self.assertEqual(len(records), 2)
            self.assertEqual(verify_records(records, parse_errors), [])
            self.assertEqual(records[1]["previous_hash"], records[0]["event_hash"])

    def test_tampering_is_detected_and_append_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            append_event(path, "TEST_A", {"summary": "original"})
            data = json.loads(path.read_text(encoding="utf-8"))
            data["payload"]["summary"] = "altered"
            path.write_text(json.dumps(data) + "\n", encoding="utf-8")
            records, errors = read_records(path)
            self.assertTrue(verify_records(records, errors))
            with self.assertRaises(ValueError):
                append_event(path, "TEST_B", {"summary": "should not append"})

    def test_start_blocks_without_pass_preflight(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            result = main(["--log", str(path), "start", "--task", "demo",
                           "--scope", "local test", "--preflight", "UNVERIFIED"])
            self.assertEqual(result, 2)
            self.assertFalse(path.exists())

    def test_incomplete_closeout_requires_reason(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            result = main(["--log", str(path), "end", "--status", "PARTIAL",
                           "--summary", "some work"])
            self.assertEqual(result, 2)
            self.assertFalse(path.exists())

    def test_cli_records_start_event_and_closeout(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            self.assertEqual(main(["--log", str(path), "start", "--task", "demo",
                                   "--scope", "local files only", "--preflight", "PASS"]), 0)
            self.assertEqual(main(["--log", str(path), "event", "--type", "test",
                                   "--summary", "unit test ran", "--result", "PASS"]), 0)
            self.assertEqual(main(["--log", str(path), "end", "--status", "COMPLETE",
                                   "--summary", "finished"]), 0)
            records, errors = read_records(path)
            self.assertEqual(len(records), 3)
            self.assertEqual(verify_records(records, errors), [])


if __name__ == "__main__":
    unittest.main()
